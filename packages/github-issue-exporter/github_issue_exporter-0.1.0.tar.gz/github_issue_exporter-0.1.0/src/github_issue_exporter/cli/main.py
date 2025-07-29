import asyncio
from pathlib import Path
from typing import List, Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

from ..core.config import ConfigManager
from ..core.export_engine import ExportEngine


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        from .. import __version__
        console.print(f"GitHub Issue Exporter v{__version__}")
        raise typer.Exit()


app = typer.Typer(
    name="github-issue-exporter",
    help="Export GitHub issues to individual JSON files with incremental updates.",
    add_completion=False
)

console = Console()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, 
        "--version", 
        callback=version_callback, 
        is_eager=True,
        help="Show version and exit"
    )
):
    """GitHub Issue Exporter - Export GitHub issues to individual JSON files."""
    return


def parse_repo_list(repo_input: str) -> List[str]:
    """Parse repository input which can be comma-separated or from a file."""
    if Path(repo_input).exists():
        # Read from file
        with open(repo_input, 'r') as f:
            repos = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return repos
    else:
        # Parse comma-separated list
        return [repo.strip() for repo in repo_input.split(',') if repo.strip()]


@app.command()
def export(
    repositories: str = typer.Argument(
        ..., 
        help="Repository names (owner/repo) separated by commas, or path to file containing repo list"
    ),
    output: Optional[str] = typer.Option(
        None, 
        "--output", "-o",
        help="Output directory for exported files (default: ./exports)"
    ),
    force: bool = typer.Option(
        False, 
        "--force", "-f",
        help="Force re-export of all issues, ignoring timestamps"
    ),
    state: str = typer.Option(
        "all", 
        "--state", "-s",
        help="Issue state to export: open, closed, or all"
    ),
    no_comments: bool = typer.Option(
        False, 
        "--no-comments",
        help="Skip exporting issue comments"
    ),
    concurrent: int = typer.Option(
        3, 
        "--concurrent", "-c",
        help="Maximum number of repositories to process concurrently"
    )
):
    """Export GitHub issues to JSON files."""
    
    if state not in ["open", "closed", "all"]:
        console.print("[red]Error: --state must be one of: open, closed, all[/red]")
        raise typer.Exit(1)
    
    if concurrent < 1 or concurrent > 10:
        console.print("[red]Error: --concurrent must be between 1 and 10[/red]")
        raise typer.Exit(1)
    
    # Parse repository list
    try:
        repo_list = parse_repo_list(repositories)
    except Exception as e:
        console.print(f"[red]Error parsing repository list: {str(e)}[/red]")
        raise typer.Exit(1)
    
    if not repo_list:
        console.print("[red]Error: No repositories specified[/red]")
        raise typer.Exit(1)
    
    # Validate repository format
    invalid_repos = []
    for repo in repo_list:
        if '/' not in repo or repo.count('/') != 1:
            invalid_repos.append(repo)
    
    if invalid_repos:
        console.print("[red]Error: Invalid repository format. Use 'owner/repo' format.[/red]")
        for repo in invalid_repos:
            console.print(f"  Invalid: {repo}")
        raise typer.Exit(1)
    
    # Show what will be exported
    console.print(f"[blue]Repositories to export ({len(repo_list)}):[/blue]")
    for repo in repo_list:
        console.print(f"  • {repo}")
    
    console.print(f"\n[blue]Settings:[/blue]")
    console.print(f"  Output directory: {output or './exports'}")
    console.print(f"  Issue state: {state}")
    console.print(f"  Include comments: {not no_comments}")
    console.print(f"  Force re-export: {force}")
    console.print(f"  Concurrent repositories: {concurrent}")
    
    # Confirm if more than 5 repositories
    if len(repo_list) > 5:
        if not Confirm.ask(f"\nProceed with export of {len(repo_list)} repositories?"):
            console.print("[yellow]Export cancelled.[/yellow]")
            raise typer.Exit(0)
    
    # Run export
    async def run_export():
        config_manager = ConfigManager()
        export_engine = ExportEngine(config_manager, console)
        
        if len(repo_list) == 1:
            # Single repository - use direct export with progress
            result = await export_engine.export_repository(
                repo_list[0],
                force=force,
                state=state,
                include_comments=not no_comments,
                output_dir=output,
                show_progress=True
            )
            results = [result]
        else:
            # Multiple repositories - use batch export
            results = await export_engine.export_repositories(
                repo_list,
                force=force,
                state=state,
                include_comments=not no_comments,
                output_dir=output,
                max_concurrent=concurrent
            )
        
        export_engine.print_export_summary(results)
        
        # Return exit code based on results
        failed_count = sum(1 for r in results if not r.success)
        return 1 if failed_count > 0 else 0
    
    try:
        exit_code = asyncio.run(run_export())
        raise typer.Exit(exit_code)
    except KeyboardInterrupt:
        console.print("\n[yellow]Export cancelled by user.[/yellow]")
        raise typer.Exit(130)
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
        raise typer.Exit(1)


@app.command()
def cleanup(
    repository: str = typer.Argument(
        ..., 
        help="Repository name (owner/repo) to clean up"
    ),
    output: Optional[str] = typer.Option(
        None, 
        "--output", "-o",
        help="Output directory where files are stored (default: ./exports)"
    ),
    dry_run: bool = typer.Option(
        False, 
        "--dry-run",
        help="Show what would be deleted without actually deleting"
    )
):
    """Remove files for issues that no longer exist in the repository."""
    
    if '/' not in repository or repository.count('/') != 1:
        console.print("[red]Error: Invalid repository format. Use 'owner/repo' format.[/red]")
        raise typer.Exit(1)
    
    async def run_cleanup():
        config_manager = ConfigManager()
        export_engine = ExportEngine(config_manager, console)
        
        if output:
            export_engine.filesystem = export_engine.filesystem.__class__(output)
        
        if dry_run:
            console.print(f"[yellow]DRY RUN: Would clean up deleted issues from {repository}[/yellow]")
            # TODO: Implement dry run logic
            return 0
        
        try:
            deleted_count = await export_engine.cleanup_deleted_issues(repository)
            if deleted_count > 0:
                console.print(f"[green]Cleaned up {deleted_count} deleted issues from {repository}[/green]")
            else:
                console.print(f"[blue]No deleted issues found in {repository}[/blue]")
            return 0
        except Exception as e:
            console.print(f"[red]Error during cleanup: {str(e)}[/red]")
            return 1
    
    try:
        exit_code = asyncio.run(run_cleanup())
        raise typer.Exit(exit_code)
    except KeyboardInterrupt:
        console.print("\n[yellow]Cleanup cancelled by user.[/yellow]")
        raise typer.Exit(130)


@app.command()
def config(
    show: bool = typer.Option(
        False, 
        "--show",
        help="Show current configuration"
    ),
    clear_auth: Optional[str] = typer.Option(
        None, 
        "--clear-auth",
        help="Clear stored authentication for repository (or 'global' for global token)"
    ),
    set_output: Optional[str] = typer.Option(
        None, 
        "--set-output",
        help="Set default output directory"
    )
):
    """Manage configuration and stored credentials."""
    
    config_manager = ConfigManager()
    
    if show:
        config_data = config_manager.load_config()
        
        table = Table(title="GitHub Issue Exporter Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")
        
        # Global settings
        table.add_row("Default Output Directory", config_data.global_settings.default_output_dir)
        table.add_row("Concurrent Repositories", str(config_data.global_settings.concurrent_repos))
        table.add_row("API Rate Limit Buffer", str(config_data.global_settings.api_rate_limit_buffer))
        
        # Authentication info (without showing tokens)
        has_global_token = bool(config_data.authentication.global_token)
        table.add_row("Global Token Set", "Yes" if has_global_token else "No")
        
        repo_count = len(config_data.authentication.repo_specific)
        table.add_row("Repository-specific Tokens", str(repo_count))
        
        console.print(table)
        
        if config_data.repositories:
            console.print("\n[blue]Repository Settings:[/blue]")
            for repo_name, settings in config_data.repositories.items():
                console.print(f"  • {repo_name}")
                if settings.output_dir:
                    console.print(f"    Output: {settings.output_dir}")
                if settings.last_export:
                    console.print(f"    Last export: {settings.last_export}")
    
    elif clear_auth:
        from ..core.auth import AuthenticationHandler
        
        auth_handler = AuthenticationHandler(config_manager, console)
        
        if clear_auth == "global":
            auth_handler.clear_stored_credentials()
        else:
            auth_handler.clear_stored_credentials(clear_auth)
    
    elif set_output:
        config_data = config_manager.load_config()
        config_data.global_settings.default_output_dir = set_output
        config_manager.save_config(config_data)
        console.print(f"[green]Default output directory set to: {set_output}[/green]")
    
    else:
        console.print("[yellow]Use --show to view configuration, or other options to modify it.[/yellow]")
        console.print("Run 'github-issue-exporter config --help' for available options.")


if __name__ == "__main__":
    app()