from typing import Dict, Any, List, Optional
from datetime import datetime
from github_issue_exporter import __version__


class DataTransformer:
    """Transform GitHub API data to desired JSON format."""
    
    def __init__(self):
        self.tool_version = __version__

    def _parse_datetime(self, datetime_str: Optional[str]) -> Optional[str]:
        """Parse and validate datetime string."""
        if not datetime_str:
            return None
        
        try:
            # GitHub API returns ISO format strings
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            return dt.isoformat()
        except Exception:
            return datetime_str

    def _extract_user_login(self, user_data: Optional[Dict[str, Any]]) -> Optional[str]:
        """Extract username from user object."""
        if not user_data:
            return None
        return user_data.get("login")

    def _extract_labels(self, labels_data: List[Dict[str, Any]]) -> List[str]:
        """Extract label names from labels array."""
        return [label.get("name", "") for label in labels_data if label.get("name")]

    def _extract_assignees(self, assignees_data: List[Dict[str, Any]]) -> List[str]:
        """Extract assignee usernames from assignees array."""
        return [
            assignee.get("login", "") 
            for assignee in assignees_data 
            if assignee.get("login")
        ]

    def _extract_milestone(self, milestone_data: Optional[Dict[str, Any]]) -> Optional[str]:
        """Extract milestone title."""
        if not milestone_data:
            return None
        return milestone_data.get("title")

    def transform_issue(self, repo_data: Dict[str, Any], issue_data: Dict[str, Any], 
                       comments_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Transform issue data to the desired output format."""
        
        issue = issue_data["issue"]
        comments = issue_data["comments"]
        
        # Transform repository info
        repository_info = {
            "owner": repo_data.get("owner", {}).get("login", ""),
            "name": repo_data.get("name", ""),
            "full_name": repo_data.get("full_name", "")
        }
        
        # Transform issue info
        issue_info = {
            "id": issue.get("id"),
            "number": issue.get("number"),
            "author": self._extract_user_login(issue.get("user")),
            "state": issue.get("state"),
            "title": issue.get("title", ""),
            "body": issue.get("body", ""),
            "labels": self._extract_labels(issue.get("labels", [])),
            "assignee": self._extract_user_login(issue.get("assignee")),
            "assignees": self._extract_assignees(issue.get("assignees", [])),
            "milestone": self._extract_milestone(issue.get("milestone")),
            "created_date": self._parse_datetime(issue.get("created_at")),
            "updated_date": self._parse_datetime(issue.get("updated_at")),
            "closed_date": self._parse_datetime(issue.get("closed_at"))
        }
        
        # Transform comments
        transformed_comments = []
        for comment in comments:
            transformed_comment = {
                "id": comment.get("id"),
                "author": self._extract_user_login(comment.get("user")),
                "body": comment.get("body", ""),
                "created_date": self._parse_datetime(comment.get("created_at")),
                "updated_date": self._parse_datetime(comment.get("updated_at"))
            }
            transformed_comments.append(transformed_comment)
        
        # Export metadata
        export_metadata = {
            "exported_at": datetime.now().isoformat(),
            "tool_version": self.tool_version
        }
        
        return {
            "repository": repository_info,
            "issue": issue_info,
            "comments": transformed_comments,
            "export_metadata": export_metadata
        }

    def transform_batch(self, repo_data: Dict[str, Any], 
                       issues_with_comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform a batch of issues with comments."""
        transformed_issues = []
        
        for issue_data in issues_with_comments:
            transformed_issue = self.transform_issue(repo_data, issue_data, issue_data["comments"])
            transformed_issues.append(transformed_issue)
        
        return transformed_issues

    def get_issue_updated_datetime(self, issue_data: Dict[str, Any]) -> datetime:
        """Extract issue updated datetime for comparison purposes."""
        updated_str = issue_data.get("updated_at")
        if not updated_str:
            # Return timezone-aware minimum datetime
            from datetime import timezone
            return datetime.min.replace(tzinfo=timezone.utc)
        
        try:
            return datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
        except Exception:
            # Return timezone-aware minimum datetime on error
            from datetime import timezone
            return datetime.min.replace(tzinfo=timezone.utc)

    def create_export_summary(self, repo_data: Dict[str, Any], 
                            exported_count: int, skipped_count: int, 
                            error_count: int) -> Dict[str, Any]:
        """Create export summary data."""
        return {
            "repository": {
                "owner": repo_data.get("owner", {}).get("login", ""),
                "name": repo_data.get("name", ""),
                "full_name": repo_data.get("full_name", "")
            },
            "export_summary": {
                "exported_count": exported_count,
                "skipped_count": skipped_count,
                "error_count": error_count,
                "total_processed": exported_count + skipped_count + error_count,
                "exported_at": datetime.now().isoformat(),
                "tool_version": self.tool_version
            }
        }