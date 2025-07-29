import asyncio
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, TaskID, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

from .config import ConfigManager
from .auth import AuthenticationHandler
from .filesystem import FileSystemManager
from .github_client import GitHubAPIClient
from .transformer import DataTransformer


class ExportResult:
    def __init__(self, repo_full_name: str):
        self.repo_full_name = repo_full_name
        self.success = False
        self.exported_count = 0
        self.skipped_count = 0
        self.error_count = 0
        self.errors: List[str] = []
        self.total_issues = 0
        self.export_time: Optional[datetime] = None

    def add_error(self, error: str):
        self.errors.append(error)
        self.error_count += 1

    def mark_success(self, exported: int, skipped: int, total: int):
        self.success = True
        self.exported_count = exported
        self.skipped_count = skipped
        self.total_issues = total
        self.export_time = datetime.now()


class ExportEngine:
    def __init__(self, config_manager: ConfigManager, console: Console):
        self.config_manager = config_manager
        self.console = console
        self.auth_handler = AuthenticationHandler(config_manager, console)
        self.filesystem = FileSystemManager()
        self.transformer = DataTransformer()

    async def export_repository(self, repo_full_name: str, force: bool = False, 
                               state: str = "all", include_comments: bool = True,
                               output_dir: Optional[str] = None, show_progress: bool = True) -> ExportResult:
        """Export issues from a single repository."""
        result = ExportResult(repo_full_name)
        
        try:
            # Get authentication token BEFORE starting any progress indicators
            token = await self.auth_handler.ensure_authentication(repo_full_name)
            
            # If authentication failed or was cancelled, return error
            if token is False:  # Explicitly cancelled or failed
                result.add_error("Authentication failed or was cancelled")
                return result
            
            # Set up filesystem with custom output directory if specified
            if output_dir:
                self.filesystem = FileSystemManager(output_dir)
            
            async with GitHubAPIClient(token, self.console) as github_client:
                # Get repository information
                try:
                    repo_data = await github_client.get_repository_info(repo_full_name)
                except Exception as e:
                    result.add_error(f"Failed to fetch repository info: {str(e)}")
                    return result
                
                repo_owner = repo_data["owner"]["login"]
                repo_name = repo_data["name"]
                
                # Ensure output directory exists
                self.filesystem.ensure_repo_directory(repo_owner, repo_name)
                
                # Now that authentication is complete, show progress for actual work
                if show_progress:
                    progress_mgr = Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                        TimeRemainingColumn(),
                        console=self.console
                    )
                else:
                    from contextlib import nullcontext
                    progress_mgr = nullcontext()
                
                with progress_mgr as progress:
                    
                    # Get issue count estimate for debugging
                    try:
                        count_info = await github_client.get_issues_count_estimate(repo_full_name, state)
                        self.console.print(f"[dim]Repository reports {count_info['open_issues_from_repo']} open issues[/dim]")
                        self.console.print(f"[dim]Pagination estimates {count_info['estimated_total_from_pagination']} total items across {count_info['total_pages']} pages[/dim]")
                    except Exception:
                        pass  # Don't fail the export if this fails
                    
                    # Fetch all issues
                    if show_progress:
                        issues_task = progress.add_task(
                            f"[cyan]Fetching issues from {repo_full_name}...", 
                            total=None
                        )
                    
                    try:
                        issues = await github_client.get_all_issues(
                            repo_full_name, state=state
                        )
                        if show_progress:
                            progress.update(issues_task, completed=1)
                    except Exception as e:
                        result.add_error(f"Failed to fetch issues: {str(e)}")
                        return result
                    
                    if not issues:
                        self.console.print(f"[yellow]No issues found in {repo_full_name}[/yellow]")
                        result.mark_success(0, 0, 0)
                        return result
                    
                    result.total_issues = len(issues)
                    
                    # Filter issues that need updating
                    issues_to_process = []
                    for issue in issues:
                        issue_number = issue["number"]
                        existing_file = self.filesystem.find_existing_issue_file(
                            repo_owner, repo_name, issue_number
                        )
                        
                        if force or not existing_file:
                            issues_to_process.append(issue)
                        else:
                            # Check if file needs update
                            issue_updated = self.transformer.get_issue_updated_datetime(issue)
                            if self.filesystem.needs_update(existing_file, issue_updated):
                                issues_to_process.append(issue)
                            else:
                                result.skipped_count += 1
                    
                    if not issues_to_process:
                        self.console.print(f"[green]All issues in {repo_full_name} are up to date[/green]")
                        result.mark_success(0, result.skipped_count, result.total_issues)
                        return result
                    
                    # Fetch issue details with comments
                    if show_progress:
                        details_task = progress.add_task(
                            f"[cyan]Fetching issue details and comments...", 
                            total=len(issues_to_process)
                        )
                    
                    try:
                        if include_comments:
                            issues_with_comments = await github_client.fetch_issues_with_comments(
                                repo_full_name, issues_to_process
                            )
                            if show_progress:
                                progress.update(details_task, completed=len(issues_to_process))
                        else:
                            # Create issue data without comments
                            issues_with_comments = [
                                {"issue": issue, "comments": []} 
                                for issue in issues_to_process
                            ]
                            if show_progress:
                                progress.update(details_task, completed=len(issues_to_process))
                    except Exception as e:
                        result.add_error(f"Failed to fetch issue details: {str(e)}")
                        return result
                    
                    # Process and save issues
                    if show_progress:
                        save_task = progress.add_task(
                            f"[cyan]Saving issues to files...", 
                            total=len(issues_with_comments)
                        )
                    
                    for issue_data in issues_with_comments:
                        try:
                            # Transform data
                            transformed_data = self.transformer.transform_issue(
                                repo_data, issue_data, issue_data["comments"]
                            )
                            
                            # Write to file
                            file_path = self.filesystem.write_issue_file(
                                repo_owner, repo_name, transformed_data
                            )
                            
                            result.exported_count += 1
                            if show_progress:
                                progress.update(save_task, advance=1)
                            
                        except Exception as e:
                            result.add_error(f"Failed to save issue {issue_data['issue'].get('number', 'unknown')}: {str(e)}")
                            if show_progress:
                                progress.update(save_task, advance=1)
                
                # Update last export time
                self.config_manager.update_last_export(repo_full_name, datetime.now())
                
                result.mark_success(result.exported_count, result.skipped_count, result.total_issues)
                
        except Exception as e:
            result.add_error(f"Unexpected error: {str(e)}")
        
        return result

    async def export_repositories(self, repo_names: List[str], force: bool = False,
                                 state: str = "all", include_comments: bool = True,
                                 output_dir: Optional[str] = None,
                                 max_concurrent: int = 3) -> List[ExportResult]:
        """Export issues from multiple repositories with limited concurrency."""
        
        if output_dir:
            self.filesystem = FileSystemManager(output_dir)
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def export_single_repo(repo_name: str) -> ExportResult:
            async with semaphore:
                return await self.export_repository(
                    repo_name, force=force, state=state, 
                    include_comments=include_comments, output_dir=output_dir,
                    show_progress=False  # Don't show individual progress when in batch mode
                )
        
        # Show overall progress
        self.console.print(f"[bold blue]Starting export of {len(repo_names)} repositories...[/bold blue]")
        
        # Create tasks for all repositories
        tasks = [export_single_repo(repo_name) for repo_name in repo_names]
        
        # Execute with progress tracking only when there are multiple repos
        results = []
        if len(repo_names) > 1:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console
            ) as progress:
                
                overall_task = progress.add_task(
                    "[green]Overall progress...", 
                    total=len(repo_names)
                )
                
                # Process repositories
                for task in asyncio.as_completed(tasks):
                    result = await task
                    results.append(result)
                    progress.update(overall_task, advance=1)
                    
                    # Show immediate feedback
                    if result.success:
                        self.console.print(
                            f"[green]✓[/green] {result.repo_full_name}: "
                            f"{result.exported_count} exported, {result.skipped_count} skipped"
                        )
                    else:
                        self.console.print(
                            f"[red]✗[/red] {result.repo_full_name}: "
                            f"{len(result.errors)} errors"
                        )
        else:
            # Single repository - just run it directly without overall progress
            for task in asyncio.as_completed(tasks):
                result = await task
                results.append(result)
        
        return results

    def print_export_summary(self, results: List[ExportResult]):
        """Print summary of export results."""
        if not results:
            return
        
        successful_repos = [r for r in results if r.success]
        failed_repos = [r for r in results if not r.success]
        
        total_exported = sum(r.exported_count for r in successful_repos)
        total_skipped = sum(r.skipped_count for r in successful_repos)
        total_issues = sum(r.total_issues for r in successful_repos)
        
        self.console.print("\n[bold blue]Export Summary[/bold blue]")
        self.console.print("=" * 50)
        
        if successful_repos:
            self.console.print(f"[green]Successful repositories: {len(successful_repos)}[/green]")
            self.console.print(f"[green]Total issues exported: {total_exported}[/green]")
            self.console.print(f"[yellow]Total issues skipped: {total_skipped}[/yellow]")
            self.console.print(f"[blue]Total issues processed: {total_issues}[/blue]")
        
        if failed_repos:
            self.console.print(f"\n[red]Failed repositories: {len(failed_repos)}[/red]")
            for result in failed_repos:
                self.console.print(f"[red]  • {result.repo_full_name}[/red]")
                for error in result.errors[:3]:  # Show first 3 errors
                    self.console.print(f"    - {error}")
                if len(result.errors) > 3:
                    self.console.print(f"    ... and {len(result.errors) - 3} more errors")
        
        # Show file locations
        if successful_repos:
            output_dir = self.filesystem.base_output_dir
            self.console.print(f"\n[blue]Files exported to: {output_dir.absolute()}[/blue]")

    async def cleanup_deleted_issues(self, repo_full_name: str) -> int:
        """Remove files for issues that no longer exist in the repository."""
        try:
            token = await self.auth_handler.ensure_authentication(repo_full_name)
            
            async with GitHubAPIClient(token, self.console) as github_client:
                # Get current issues
                current_issues = await github_client.get_all_issues(repo_full_name, state="all")
                current_issue_numbers = [issue["number"] for issue in current_issues]
                
                # Get repository info for directory structure
                repo_data = await github_client.get_repository_info(repo_full_name)
                repo_owner = repo_data["owner"]["login"]
                repo_name = repo_data["name"]
                
                # Get existing files
                existing_issues = self.filesystem.list_existing_issues(repo_owner, repo_name)
                existing_issue_numbers = [issue["number"] for issue in existing_issues]
                
                # Find deleted issues
                deleted_issue_numbers = set(existing_issue_numbers) - set(current_issue_numbers)
                
                # Remove files for deleted issues
                self.filesystem.cleanup_old_files(repo_owner, repo_name, current_issue_numbers)
                
                return len(deleted_issue_numbers)
                
        except Exception as e:
            self.console.print(f"[red]Error during cleanup: {str(e)}[/red]")
            return 0