# GitHub Issue Exporter Tool Architecture Plan

## High-Level Overview
A command-line tool that exports GitHub issues to individual JSON files, with incremental updates and credential management. Supports multiple repositories with per-repo configuration.

## Core Components

### 1. Configuration Manager
- **Purpose**: Handle credential storage and retrieval for multiple repositories
- **Location**: `~/.config/github-issue-exporter-tool/config.json`
- **Responsibilities**:
  - Create config directory if it doesn't exist
  - Store/retrieve GitHub tokens per repository or globally
  - Handle config file encryption/decryption for security
  - Validate stored credentials
  - Manage per-repository settings and preferences

### 2. Authentication Handler
- **Purpose**: Manage GitHub API authentication across repositories
- **Responsibilities**:
  - Detect if repository is private (via API call)
  - Prompt for credentials if needed and not stored for specific repo
  - Test credential validity before proceeding
  - Handle token-based and basic auth methods
  - Store new credentials via Configuration Manager
  - Support both repo-specific and global authentication tokens

### 3. File System Manager
- **Purpose**: Handle file operations and naming with repository organization
- **Responsibilities**:
  - Generate slugified filenames from issue titles
  - Check for existing files with matching ID prefix (ignore title part)
  - Create output directory structure (organized by repository)
  - Handle file reading/writing operations
  - Implement safe file updates (temp file → rename pattern)
  - Manage repository-specific export directories

### 4. GitHub API Client (HTTPX-based)
- **Purpose**: Interface with GitHub REST API using async HTTP client
- **Responsibilities**:
  - Fetch repository information with async httpx requests
  - Retrieve issues list with pagination using async operations
  - Fetch individual issue details concurrently
  - Retrieve comments for each issue with pagination
  - Handle rate limiting and retries with exponential backoff
  - Parse API responses into internal data structures
  - Support multiple concurrent repository operations
  - Manage connection pooling and timeout configurations

### 5. Data Transformer
- **Purpose**: Convert API data to desired JSON format
- **Responsibilities**:
  - Map GitHub API response fields to output schema
  - Extract and format issue metadata (ID, author, state, title, body, labels, assignee, dates)
  - Process comments array with ID, author, message body
  - Handle missing/null fields gracefully
  - Ensure consistent date formatting
  - Include repository context in exported data

### 6. Export Engine
- **Purpose**: Orchestrate the export process
- **Responsibilities**:
  - Coordinate between all other components
  - Implement incremental update logic per repository
  - Handle batch processing of issues
  - Provide progress feedback to user
  - Manage error handling and recovery
  - Support parallel processing of multiple repositories

### 7. CLI Interface (Typer-based)
- **Purpose**: Handle command-line interaction using Typer framework
- **Responsibilities**:
  - Define command structure with automatic help generation via Typer
  - Parse command-line arguments (repo URLs, output directory, batch mode, etc.)
  - Display rich progress indicators and status using Rich console
  - Handle user prompts for credentials with Rich prompts
  - Show summary statistics per repository and overall with Rich tables
  - Provide comprehensive help and usage information
  - Support batch mode for multiple repositories
  - Handle subcommands for different operations (export, config, auth)

## Data Flow

1. **Initialization**
   - Parse CLI arguments (single repo, multiple repos, or config file with repo list)
   - Load existing configuration
   - Validate output directory structure

2. **Authentication**
   - For each repository:
     - Check if repo is private
     - Load or prompt for credentials (repo-specific or global)
     - Validate API access

3. **Discovery**
   - For each repository:
     - Fetch repository metadata
     - Retrieve issues list (all pages)
     - Scan existing export files in repo-specific directory

4. **Processing**
   - For each repository and issue:
     - Check if existing file needs update (compare timestamps)
     - Fetch issue details and comments if needed
     - Transform data to target format
     - Write to appropriately named file in repo directory

5. **Completion**
   - Display summary statistics per repository and overall
   - Handle any errors or warnings

## File Naming Strategy
- Directory structure: `{output_dir}/{repo_owner}/{repo_name}/`
- File pattern: `{issue_id}-{slugified_title}.json`
- Slugification rules: lowercase, replace spaces/special chars with hyphens, remove consecutive hyphens
- Update detection: glob pattern `{issue_id}-*.json` to find existing files regardless of title changes

## Configuration Schema
```json
{
  "global_settings": {
    "default_output_dir": "path",
    "concurrent_repos": 3,
    "api_rate_limit_buffer": 100
  },
  "authentication": {
    "global_token": "encrypted_token",
    "repo_specific": {
      "owner/repo-name": {
        "token": "encrypted_token",
        "username": "encrypted_username",
        "last_export": "iso_date"
      }
    }
  },
  "repositories": {
    "owner/repo-name": {
      "output_dir": "custom_path",
      "last_export": "iso_date",
      "include_closed": true,
      "export_comments": true
    }
  }
}
```

## Output JSON Schema
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

## CLI Usage Examples
```bash
# Single repository
github-issue-exporter owner/repo

# Multiple repositories
github-issue-exporter owner/repo1 owner/repo2 owner/repo3

# From config file
github-issue-exporter --config repos.txt

# Custom output directory
github-issue-exporter owner/repo --output /path/to/exports

# Force re-export (ignore timestamps)
github-issue-exporter owner/repo --force

# Export only open issues
github-issue-exporter owner/repo --state open
```

## Error Handling Strategy
- Network errors: retry with exponential backoff
- Authentication errors: re-prompt for credentials per repository
- File system errors: clear error messages with suggested fixes  
- API rate limiting: respect headers and wait appropriately
- Partial failures: continue processing other repositories/issues, report at end
- Repository access errors: skip inaccessible repos, continue with others

## Technology Stack
- **Language**: Python 3.11+
- **Package Manager**: `uv` for fast dependency management and virtual environments
- **CLI Framework**: `typer` for command-line interface with automatic help generation
- **Output/Formatting**: `rich` for beautiful terminal output, progress bars, and error formatting
- **HTTP Client**: `httpx` for async-capable HTTP requests to GitHub API
- **Additional Dependencies**: 
  - JSON handling (built-in `json` module)
  - File system operations (built-in `pathlib`)
  - Async processing (`asyncio` for concurrent API calls)
  - Encryption for credentials (`cryptography` library)
  - Configuration management (built-in or `pydantic` for validation)

## Implementation Considerations
- Security: Encrypt stored credentials, clear sensitive data from memory
- Performance: Async HTTP calls with `httpx`, efficient file I/O, parallel repository processing
- Scalability: Handle large numbers of repositories and issues efficiently
- Rich UI: Progress bars, spinners, and colored output using `rich` console
- Type Safety: Use type hints throughout for better development experience

## Multi-Repository Features
- Batch processing with progress indicators
- Repository-specific configuration overrides
- Parallel processing with configurable concurrency limits
- Centralized credential management with per-repo overrides
- Aggregated reporting across all processed repositories
- Resume capability for interrupted batch operations