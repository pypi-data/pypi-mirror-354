import json
import os
from pathlib import Path
from typing import Dict, Optional, Any
from cryptography.fernet import Fernet
from pydantic import BaseModel, Field
from datetime import datetime


class RepoSpecificAuth(BaseModel):
    token: Optional[str] = None
    username: Optional[str] = None
    last_export: Optional[datetime] = None


class RepoSettings(BaseModel):
    output_dir: Optional[str] = None
    last_export: Optional[datetime] = None
    include_closed: bool = True
    export_comments: bool = True


class GlobalSettings(BaseModel):
    default_output_dir: str = "./exports"
    concurrent_repos: int = 3
    api_rate_limit_buffer: int = 100


class AuthSettings(BaseModel):
    global_token: Optional[str] = None
    repo_specific: Dict[str, RepoSpecificAuth] = Field(default_factory=dict)


class Config(BaseModel):
    global_settings: GlobalSettings = Field(default_factory=GlobalSettings)
    authentication: AuthSettings = Field(default_factory=AuthSettings)
    repositories: Dict[str, RepoSettings] = Field(default_factory=dict)


class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "github-issue-exporter-tool"
        self.config_file = self.config_dir / "config.json"
        self.key_file = self.config_dir / "key.key"
        self._ensure_config_dir()
        self._cipher = self._get_or_create_cipher()
        self._config: Optional[Config] = None

    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Set restrictive permissions on config directory
        os.chmod(self.config_dir, 0o700)

    def _get_or_create_cipher(self) -> Fernet:
        """Get or create encryption cipher for credential storage."""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Set restrictive permissions on key file
            os.chmod(self.key_file, 0o600)
        
        return Fernet(key)

    def _encrypt_value(self, value: str) -> str:
        """Encrypt a string value."""
        return self._cipher.encrypt(value.encode()).decode()

    def _decrypt_value(self, encrypted_value: str) -> str:
        """Decrypt a string value."""
        return self._cipher.decrypt(encrypted_value.encode()).decode()

    def _encrypt_config_data(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive data in config dictionary."""
        encrypted = config_dict.copy()
        
        # Encrypt global token
        if encrypted.get("authentication", {}).get("global_token"):
            encrypted["authentication"]["global_token"] = self._encrypt_value(
                encrypted["authentication"]["global_token"]
            )
        
        # Encrypt repo-specific credentials
        for repo_name, auth_data in encrypted.get("authentication", {}).get("repo_specific", {}).items():
            if auth_data.get("token"):
                encrypted["authentication"]["repo_specific"][repo_name]["token"] = self._encrypt_value(
                    auth_data["token"]
                )
            if auth_data.get("username"):
                encrypted["authentication"]["repo_specific"][repo_name]["username"] = self._encrypt_value(
                    auth_data["username"]
                )
        
        return encrypted

    def _decrypt_config_data(self, encrypted_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt sensitive data in config dictionary."""
        decrypted = encrypted_dict.copy()
        
        # Decrypt global token
        if decrypted.get("authentication", {}).get("global_token"):
            try:
                decrypted["authentication"]["global_token"] = self._decrypt_value(
                    decrypted["authentication"]["global_token"]
                )
            except Exception:
                # If decryption fails, clear the token
                decrypted["authentication"]["global_token"] = None
        
        # Decrypt repo-specific credentials
        for repo_name, auth_data in decrypted.get("authentication", {}).get("repo_specific", {}).items():
            if auth_data.get("token"):
                try:
                    decrypted["authentication"]["repo_specific"][repo_name]["token"] = self._decrypt_value(
                        auth_data["token"]
                    )
                except Exception:
                    decrypted["authentication"]["repo_specific"][repo_name]["token"] = None
            
            if auth_data.get("username"):
                try:
                    decrypted["authentication"]["repo_specific"][repo_name]["username"] = self._decrypt_value(
                        auth_data["username"]
                    )
                except Exception:
                    decrypted["authentication"]["repo_specific"][repo_name]["username"] = None
        
        return decrypted

    def load_config(self) -> Config:
        """Load configuration from file."""
        if self._config is not None:
            return self._config
        
        if not self.config_file.exists():
            self._config = Config()
            return self._config
        
        try:
            with open(self.config_file, 'r') as f:
                encrypted_data = json.load(f)
            
            decrypted_data = self._decrypt_config_data(encrypted_data)
            self._config = Config.model_validate(decrypted_data)
            return self._config
        except Exception as e:
            # If config is corrupted, start fresh
            self._config = Config()
            return self._config

    def save_config(self, config: Optional[Config] = None):
        """Save configuration to file."""
        if config is None:
            config = self._config
        
        if config is None:
            return
        
        config_dict = config.model_dump()
        encrypted_data = self._encrypt_config_data(config_dict)
        
        with open(self.config_file, 'w') as f:
            json.dump(encrypted_data, f, indent=2, default=str)
        
        # Set restrictive permissions on config file
        os.chmod(self.config_file, 0o600)
        self._config = config

    def get_repo_token(self, repo_full_name: str) -> Optional[str]:
        """Get authentication token for a specific repository."""
        config = self.load_config()
        
        # Check for repo-specific token first
        repo_auth = config.authentication.repo_specific.get(repo_full_name)
        if repo_auth and repo_auth.token:
            return repo_auth.token
        
        # Fall back to global token
        return config.authentication.global_token

    def set_repo_token(self, repo_full_name: str, token: str):
        """Set authentication token for a specific repository."""
        config = self.load_config()
        
        if repo_full_name not in config.authentication.repo_specific:
            config.authentication.repo_specific[repo_full_name] = RepoSpecificAuth()
        
        config.authentication.repo_specific[repo_full_name].token = token
        self.save_config(config)

    def set_global_token(self, token: str):
        """Set global authentication token."""
        config = self.load_config()
        config.authentication.global_token = token
        self.save_config(config)

    def get_repo_settings(self, repo_full_name: str) -> RepoSettings:
        """Get settings for a specific repository."""
        config = self.load_config()
        return config.repositories.get(repo_full_name, RepoSettings())

    def update_repo_settings(self, repo_full_name: str, settings: RepoSettings):
        """Update settings for a specific repository."""
        config = self.load_config()
        config.repositories[repo_full_name] = settings
        self.save_config(config)

    def update_last_export(self, repo_full_name: str, export_time: datetime):
        """Update last export time for a repository."""
        config = self.load_config()
        
        if repo_full_name not in config.repositories:
            config.repositories[repo_full_name] = RepoSettings()
        
        config.repositories[repo_full_name].last_export = export_time
        
        # Also update in auth section if exists
        if repo_full_name in config.authentication.repo_specific:
            config.authentication.repo_specific[repo_full_name].last_export = export_time
        
        self.save_config(config)

    def get_global_settings(self) -> GlobalSettings:
        """Get global settings."""
        config = self.load_config()
        return config.global_settings

    def update_global_settings(self, settings: GlobalSettings):
        """Update global settings."""
        config = self.load_config()
        config.global_settings = settings
        self.save_config(config)