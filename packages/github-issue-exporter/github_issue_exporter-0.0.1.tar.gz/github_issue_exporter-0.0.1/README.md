# GitHub Issue Exporter

A command-line tool that exports GitHub issues to individual JSON files, with incremental updates and credential management. Supports multiple repositories with per-repo configuration.

Authored by Claude Code.

## Features

- **Incremental Updates**: Only exports issues that have been modified since last export
- **Multiple Repositories**: Process multiple repositories concurrently
- **Secure Credential Storage**: Encrypted storage of GitHub tokens
- **Rich Progress Display**: Beautiful progress bars and status updates
- **Flexible Configuration**: Per-repository settings and global configuration
- **Comprehensive Export**: Includes issue metadata, comments, labels, and assignees

## Installation

```bash
# Install with uv
uv tool install github-issue-exporter

# Or install in development mode
uv pip install -e .
```

## Quick Start

```bash
# Export issues from a single repository
github-issue-exporter owner/repo

# Export from multiple repositories
github-issue-exporter owner/repo1,owner/repo2,owner/repo3

# Custom output directory
github-issue-exporter owner/repo --output /path/to/exports

# Force re-export (ignore timestamps)
github-issue-exporter owner/repo --force

# Export only open issues
github-issue-exporter owner/repo --state open
```

## Authentication

The tool will automatically prompt for a GitHub Personal Access Token when needed. You can create one at: https://github.com/settings/tokens

Required scopes:
- `repo` (for private repositories)
- `public_repo` (for public repositories)

Tokens are stored securely using encryption and can be managed per-repository.

## Configuration

```bash
# View current configuration
github-issue-exporter config --show

# Clear stored authentication
github-issue-exporter config --clear-auth owner/repo

# Set default output directory
github-issue-exporter config --set-output /path/to/exports
```

## Output Format

Issues are exported as individual JSON files with the following structure:

```json
{
  "repository": {
    "owner": "string",
    "name": "string", 
    "full_name": "string"
  },
  "issue": {
    "id": "number",
    "number": "number",
    "author": "string",
    "state": "string",
    "title": "string",
    "body": "string",
    "labels": ["string"],
    "assignee": "string|null",
    "assignees": ["string"],
    "milestone": "string|null",
    "created_date": "iso_string",
    "updated_date": "iso_string",
    "closed_date": "iso_string|null"
  },
  "comments": [
    {
      "id": "number",
      "author": "string",
      "body": "string",
      "created_date": "iso_string",
      "updated_date": "iso_string"
    }
  ],
  "export_metadata": {
    "exported_at": "iso_string",
    "tool_version": "string"
  }
}
```

## File Organization

Files are organized by repository and issue state:

```
exports/
    owner1/
        repo1/
            open/
                1-first-issue-title.json
                3-another-open-issue.json
                ...
            closed/
                2-closed-issue-title.json
                4-resolved-issue.json
                ...
    owner2/
        repo2/
            open/
                1-some-open-issue.json
            closed/
                2-some-closed-issue.json
```

**Key Features:**
- Issues are organized into `open` and `closed` subdirectories based on their current state
- Filenames use the issue number (not internal ID) for easier identification  
- When an issue state changes, the file is automatically moved to the appropriate directory

## Commands

### export
Export GitHub issues to JSON files.

```bash
github-issue-exporter export [OPTIONS] REPOSITORIES
```

Options:
- `--output, -o`: Output directory (default: ./exports)
- `--force, -f`: Force re-export, ignoring timestamps
- `--state, -s`: Issue state (open, closed, all)
- `--no-comments`: Skip exporting comments
- `--concurrent, -c`: Max concurrent repositories (1-10)

### cleanup
Remove files for issues that no longer exist.

```bash
github-issue-exporter cleanup [OPTIONS] REPOSITORY
```

### config
Manage configuration and credentials.

```bash
github-issue-exporter config [OPTIONS]
```

### --version
Show version information.

```bash
github-issue-exporter --version
```

## Requirements

- Python 3.11+
- GitHub Personal Access Token (for private repos or higher rate limits)
