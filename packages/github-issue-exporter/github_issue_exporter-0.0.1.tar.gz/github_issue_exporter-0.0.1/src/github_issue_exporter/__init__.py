"""GitHub Issue Exporter Tool

A command-line tool that exports GitHub issues to individual JSON files, 
with incremental updates and credential management. Supports multiple 
repositories with per-repo configuration.
"""

try:
    from importlib.metadata import version
except ImportError:
    # Python < 3.8 fallback
    from importlib_metadata import version

try:
    __version__ = version("github-issue-exporter")
except Exception:
    # Fallback for development/editable installs where metadata might not be available
    __version__ = "dev"