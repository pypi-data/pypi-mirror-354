import asyncio
from typing import Optional, Tuple
import httpx
from rich.console import Console
from rich.prompt import Prompt
from .config import ConfigManager


class AuthenticationHandler:
    def __init__(self, config_manager: ConfigManager, console: Console):
        self.config_manager = config_manager
        self.console = console

    async def is_repo_private(self, repo_full_name: str) -> bool:
        """Check if a repository is private by making an unauthenticated API call."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"https://api.github.com/repos/{repo_full_name}",
                    headers={"Accept": "application/vnd.github.v3+json"}
                )
                
                if response.status_code == 200:
                    # Public repo - we can access it without auth
                    return False
                elif response.status_code == 404:
                    # Could be private or doesn't exist
                    # We'll need auth to determine which
                    return True
                else:
                    # Other error - assume we need auth
                    return True
            except Exception:
                # Network error - assume we need auth to be safe
                return True

    async def validate_credentials(self, token: str, repo_full_name: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Validate GitHub credentials and optionally check repo access."""
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            try:
                # First, validate the token by checking user info
                response = await client.get("https://api.github.com/user", headers=headers)
                
                if response.status_code != 200:
                    return False, f"Invalid token: {response.status_code}"
                
                user_data = response.json()
                username = user_data.get("login", "unknown")
                
                # If repo is specified, check access to it
                if repo_full_name:
                    repo_response = await client.get(
                        f"https://api.github.com/repos/{repo_full_name}",
                        headers=headers
                    )
                    
                    if repo_response.status_code == 404:
                        return False, f"Repository '{repo_full_name}' not found or no access"
                    elif repo_response.status_code != 200:
                        return False, f"Cannot access repository: {repo_response.status_code}"
                
                return True, username
                
            except Exception as e:
                return False, f"Network error: {str(e)}"

    def prompt_for_token(self, repo_full_name: Optional[str] = None) -> Optional[str]:
        """Prompt user for GitHub token."""
        if repo_full_name:
            self.console.print(f"\n[yellow]Authentication required for repository: {repo_full_name}[/yellow]")
        else:
            self.console.print("\n[yellow]GitHub authentication required[/yellow]")
        
        self.console.print("Please provide a GitHub Personal Access Token.")
        self.console.print("You can create one at: https://github.com/settings/tokens")
        self.console.print("Required scopes: 'repo' (for private repos) or 'public_repo' (for public repos)")
        
        token = Prompt.ask("\nGitHub Token", password=True)
        
        if not token or not token.strip():
            return None
        
        return token.strip()

    async def get_or_prompt_credentials(self, repo_full_name: str) -> Optional[str]:
        """Get existing credentials or prompt for new ones."""
        # Check if we have stored credentials for this repo
        stored_token = self.config_manager.get_repo_token(repo_full_name)
        
        if stored_token:
            # Validate stored credentials
            is_valid, result = await self.validate_credentials(stored_token, repo_full_name)
            if is_valid:
                self.console.print(f"[green]Using stored credentials for {repo_full_name} (user: {result})[/green]")
                return stored_token
            else:
                self.console.print(f"[red]Stored credentials for {repo_full_name} are invalid: {result}[/red]")
        
        # Check if repo is public and we don't need auth
        is_private = await self.is_repo_private(repo_full_name)
        if not is_private:
            self.console.print(f"[green]Repository {repo_full_name} is public - no authentication required[/green]")
            return None
        
        # Need to prompt for credentials
        self.console.print(f"[yellow]Repository {repo_full_name} is private or authentication is required[/yellow]")
        
        # Give user up to 3 attempts
        for attempt in range(3):
            token = self.prompt_for_token(repo_full_name)
            if not token:
                self.console.print("[red]Authentication cancelled by user[/red]")
                return False  # Explicitly cancelled
            
            # Validate the new token
            is_valid, result = await self.validate_credentials(token, repo_full_name)
            if is_valid:
                self.console.print(f"[green]Successfully authenticated as {result}[/green]")
                
                # Ask if user wants to store the token
                store_token = Prompt.ask(
                    f"Store token for {repo_full_name}? (y/n)",
                    choices=["y", "n"],
                    default="y"
                )
                
                if store_token.lower() == "y":
                    self.config_manager.set_repo_token(repo_full_name, token)
                    self.console.print("[green]Token stored securely[/green]")
                
                return token
            else:
                self.console.print(f"[red]Invalid credentials: {result}[/red]")
                if attempt < 2:  # Don't show this on the last attempt
                    self.console.print(f"[yellow]Please try again. ({attempt + 1}/3 attempts)[/yellow]")
        
        self.console.print("[red]Authentication failed after 3 attempts[/red]")
        return False  # Failed after attempts

    async def ensure_authentication(self, repo_full_name: str):
        """Ensure we have valid authentication for a repository."""
        try:
            return await self.get_or_prompt_credentials(repo_full_name)
        except KeyboardInterrupt:
            self.console.print("\n[red]Authentication cancelled by user[/red]")
            return False
        except Exception as e:
            if str(e).strip():
                self.console.print(f"[red]Authentication error: {str(e)}[/red]")
            else:
                self.console.print("[red]Authentication failed[/red]")
            return False

    def clear_stored_credentials(self, repo_full_name: Optional[str] = None):
        """Clear stored credentials for a repo or globally."""
        config = self.config_manager.load_config()
        
        if repo_full_name:
            if repo_full_name in config.authentication.repo_specific:
                del config.authentication.repo_specific[repo_full_name]
                self.config_manager.save_config(config)
                self.console.print(f"[green]Cleared stored credentials for {repo_full_name}[/green]")
            else:
                self.console.print(f"[yellow]No stored credentials found for {repo_full_name}[/yellow]")
        else:
            # Clear global token
            config.authentication.global_token = None
            self.config_manager.save_config(config)
            self.console.print("[green]Cleared global authentication token[/green]")

    def get_auth_headers(self, token: Optional[str]) -> dict:
        """Get authentication headers for API requests."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "github-issue-exporter/1.0.0"
        }
        
        if token:
            headers["Authorization"] = f"token {token}"
        
        return headers