import json
import os
import re
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime


class FileSystemManager:
    def __init__(self, base_output_dir: str = "./exports"):
        self.base_output_dir = Path(base_output_dir)

    def slugify(self, text: str) -> str:
        """Convert text to a filesystem-safe slug."""
        # Convert to lowercase
        slug = text.lower()
        
        # Replace spaces and special characters with hyphens
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        # Limit length to avoid filesystem issues
        slug = slug[:100]
        
        return slug

    def get_repo_directory(self, repo_owner: str, repo_name: str) -> Path:
        """Get the directory path for a specific repository."""
        return self.base_output_dir / repo_owner / repo_name

    def get_state_directory(self, repo_owner: str, repo_name: str, state: str) -> Path:
        """Get the directory path for a specific issue state."""
        return self.get_repo_directory(repo_owner, repo_name) / state

    def ensure_repo_directory(self, repo_owner: str, repo_name: str) -> Path:
        """Ensure the repository directory and state subdirectories exist."""
        repo_dir = self.get_repo_directory(repo_owner, repo_name)
        repo_dir.mkdir(parents=True, exist_ok=True)
        
        # Create open and closed subdirectories
        open_dir = self.get_state_directory(repo_owner, repo_name, "open")
        closed_dir = self.get_state_directory(repo_owner, repo_name, "closed")
        open_dir.mkdir(parents=True, exist_ok=True)
        closed_dir.mkdir(parents=True, exist_ok=True)
        
        return repo_dir

    def generate_issue_filename(self, issue_number: int, issue_title: str) -> str:
        """Generate filename for an issue using issue number."""
        slugified_title = self.slugify(issue_title)
        return f"{issue_number}-{slugified_title}.json"

    def find_existing_issue_file(self, repo_owner: str, repo_name: str, issue_number: int) -> Optional[Path]:
        """Find existing issue file by number in both open and closed directories."""
        pattern = f"{issue_number}-*.json"
        
        # Check both open and closed directories
        for state in ["open", "closed"]:
            state_dir = self.get_state_directory(repo_owner, repo_name, state)
            if state_dir.exists():
                matching_files = list(state_dir.glob(pattern))
                if matching_files:
                    return matching_files[0]  # Return the first match
        
        return None

    def get_file_modification_time(self, file_path: Path) -> Optional[datetime]:
        """Get the modification time of a file."""
        try:
            if file_path.exists():
                timestamp = file_path.stat().st_mtime
                # Return timezone-aware datetime in UTC
                from datetime import timezone
                return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        except Exception:
            pass
        return None

    def needs_update(self, file_path: Path, issue_updated_at: datetime) -> bool:
        """Check if a file needs to be updated based on modification times."""
        if not file_path.exists():
            return True
        
        file_mod_time = self.get_file_modification_time(file_path)
        if file_mod_time is None:
            return True
        
        # Need update if issue was modified after file
        return issue_updated_at > file_mod_time

    def safe_write_json(self, file_path: Path, data: Dict[str, Any]) -> bool:
        """Safely write JSON data to file using temp file and rename pattern."""
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write to temporary file first
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.json.tmp',
                dir=file_path.parent,
                delete=False
            ) as temp_file:
                json.dump(data, temp_file, indent=2, default=str, ensure_ascii=False)
                temp_path = Path(temp_file.name)
            
            # Atomically rename temp file to final location
            temp_path.rename(file_path)
            return True
            
        except Exception as e:
            # Clean up temp file if it exists
            try:
                if 'temp_path' in locals():
                    temp_path.unlink(missing_ok=True)
            except Exception:
                pass
            raise e

    def read_existing_issue(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Read existing issue data from file."""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    def list_existing_issues(self, repo_owner: str, repo_name: str) -> List[Dict[str, Any]]:
        """List all existing issue files and their metadata from both open and closed directories."""
        issues = []
        
        # Check both open and closed directories
        for state in ["open", "closed"]:
            state_dir = self.get_state_directory(repo_owner, repo_name, state)
            
            if not state_dir.exists():
                continue
            
            for file_path in state_dir.glob("*.json"):
                try:
                    # Extract issue number from filename
                    filename = file_path.stem
                    issue_number_match = re.match(r'^(\d+)-', filename)
                    
                    if not issue_number_match:
                        continue
                    
                    issue_number = int(issue_number_match.group(1))
                    mod_time = self.get_file_modification_time(file_path)
                    
                    issue_data = self.read_existing_issue(file_path)
                    
                    issues.append({
                        'number': issue_number,
                        'state': state,
                        'file_path': file_path,
                        'modified_time': mod_time,
                        'data': issue_data
                    })
                    
                except Exception:
                    # Skip files that can't be processed
                    continue
        
        return sorted(issues, key=lambda x: x['number'])

    def cleanup_old_files(self, repo_owner: str, repo_name: str, current_issue_numbers: List[int]):
        """Remove files for issues that no longer exist."""
        existing_issues = self.list_existing_issues(repo_owner, repo_name)
        
        for issue_info in existing_issues:
            if issue_info['number'] not in current_issue_numbers:
                try:
                    issue_info['file_path'].unlink()
                except Exception:
                    # Ignore errors when deleting files
                    pass

    def get_export_summary(self, repo_owner: str, repo_name: str) -> Dict[str, Any]:
        """Get summary of exported issues for a repository."""
        existing_issues = self.list_existing_issues(repo_owner, repo_name)
        
        total_issues = len(existing_issues)
        if total_issues == 0:
            return {
                'total_issues': 0,
                'latest_export': None,
                'oldest_export': None
            }
        
        mod_times = [issue['modified_time'] for issue in existing_issues if issue['modified_time']]
        
        return {
            'total_issues': total_issues,
            'latest_export': max(mod_times) if mod_times else None,
            'oldest_export': min(mod_times) if mod_times else None
        }

    def write_issue_file(self, repo_owner: str, repo_name: str, issue_data: Dict[str, Any]) -> Path:
        """Write issue data to file in the appropriate state directory and return the file path."""
        # Ensure repository directory and state subdirectories exist
        self.ensure_repo_directory(repo_owner, repo_name)
        
        issue_number = issue_data['issue']['number']
        issue_title = issue_data['issue']['title']
        issue_state = issue_data['issue']['state']
        
        # Check if file already exists in either open or closed directory
        existing_file = self.find_existing_issue_file(repo_owner, repo_name, issue_number)
        
        # Generate new filename using issue number
        filename = self.generate_issue_filename(issue_number, issue_title)
        
        # Determine the correct state directory
        target_state_dir = self.get_state_directory(repo_owner, repo_name, issue_state)
        target_file_path = target_state_dir / filename
        
        # If file exists in a different state directory, remove it (state changed)
        if existing_file and existing_file.parent != target_state_dir:
            try:
                existing_file.unlink()
            except Exception:
                pass
        
        # If file exists in same state directory but with different title, remove old file
        elif existing_file and existing_file != target_file_path:
            try:
                existing_file.unlink()
            except Exception:
                pass
        
        # Write the new file in the correct state directory
        self.safe_write_json(target_file_path, issue_data)
        
        return target_file_path