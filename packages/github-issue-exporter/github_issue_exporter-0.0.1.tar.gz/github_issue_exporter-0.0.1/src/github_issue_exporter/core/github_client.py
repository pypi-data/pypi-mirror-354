import asyncio
import math
from typing import List, Dict, Any, Optional, AsyncGenerator
from datetime import datetime, timedelta
import httpx
from rich.console import Console
from rich.progress import Progress, TaskID


class RateLimitError(Exception):
    """Raised when API rate limit is exceeded."""
    pass


class GitHubAPIClient:
    def __init__(self, token: Optional[str] = None, console: Optional[Console] = None):
        self.token = token
        self.console = console or Console()
        self.base_url = "https://api.github.com"
        self.session: Optional[httpx.AsyncClient] = None
        
        # Rate limiting
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = datetime.now()
        self.rate_limit_buffer = 100

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.aclose()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "github-issue-exporter/1.0.0"
        }
        
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        return headers

    async def _handle_rate_limit(self, response: httpx.Response):
        """Handle rate limiting from response headers."""
        if "X-RateLimit-Remaining" in response.headers:
            self.rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
        
        if "X-RateLimit-Reset" in response.headers:
            reset_timestamp = int(response.headers["X-RateLimit-Reset"])
            self.rate_limit_reset = datetime.fromtimestamp(reset_timestamp)
        
        # If we're hitting rate limits, wait
        if response.status_code == 403 and "rate limit" in response.text.lower():
            wait_time = (self.rate_limit_reset - datetime.now()).total_seconds()
            if wait_time > 0:
                self.console.print(f"[yellow]Rate limit exceeded. Waiting {wait_time:.0f} seconds...[/yellow]")
                await asyncio.sleep(wait_time + 1)
                raise RateLimitError("Rate limit exceeded")

    async def _check_rate_limit_preemptive(self):
        """Check if we should wait before making a request."""
        if self.rate_limit_remaining < self.rate_limit_buffer:
            wait_time = (self.rate_limit_reset - datetime.now()).total_seconds()
            if wait_time > 0:
                self.console.print(f"[yellow]Approaching rate limit. Waiting {wait_time:.0f} seconds...[/yellow]")
                await asyncio.sleep(wait_time + 1)

    async def _make_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make HTTP request with retry logic and rate limiting."""
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
        
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        headers = self._get_headers()
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self._check_rate_limit_preemptive()
                
                response = await self.session.request(
                    method, full_url, headers=headers, **kwargs
                )
                
                await self._handle_rate_limit(response)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 403 and "rate limit" in response.text.lower():
                    # Rate limit handled in _handle_rate_limit
                    continue
                elif response.status_code >= 500:
                    # Server error - retry with exponential backoff
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        await asyncio.sleep(wait_time)
                        continue
                
                # Other errors - don't retry
                response.raise_for_status()
                return response
                
            except RateLimitError:
                # Rate limit handled, retry
                continue
            except httpx.RequestError as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                    continue
                raise e
        
        raise Exception(f"Failed to make request after {max_retries} attempts")

    async def get_repository_info(self, repo_full_name: str) -> Dict[str, Any]:
        """Get repository information."""
        response = await self._make_request("GET", f"/repos/{repo_full_name}")
        return response.json()

    async def get_issues_count_estimate(self, repo_full_name: str, state: str = "all") -> Dict[str, int]:
        """Get an estimate of issue counts by checking repository info and first page."""
        repo_info = await self.get_repository_info(repo_full_name)
        
        # Repository info gives us total open issues count
        open_issues_count = repo_info.get("open_issues_count", 0)
        
        # Get first page to see total from pagination
        first_page = await self.get_issues_page(repo_full_name, 1, state=state)
        total_pages = first_page["total_pages"]
        items_on_first_page = len(first_page["issues"])
        
        # Estimate total items (this includes pull requests)
        if total_pages > 1:
            estimated_total = (total_pages - 1) * 100 + items_on_first_page
        else:
            estimated_total = items_on_first_page
        
        return {
            "open_issues_from_repo": open_issues_count,
            "estimated_total_from_pagination": estimated_total,
            "total_pages": total_pages,
            "items_on_first_page": items_on_first_page
        }

    async def get_issues_page(self, repo_full_name: str, page: int = 1, per_page: int = 100, 
                            state: str = "all") -> Dict[str, Any]:
        """Get a single page of issues."""
        # GitHub API limits per_page to 100 max
        per_page = min(per_page, 100)
        
        params = {
            "page": page,
            "per_page": per_page,
            "state": state,
            "sort": "created",  # Changed from "updated" to "created" for more consistent pagination
            "direction": "asc"  # Ascending to get oldest first, more predictable
        }
        
        response = await self._make_request(
            "GET", f"/repos/{repo_full_name}/issues", params=params
        )
        
        return {
            "issues": response.json(),
            "total_pages": self._get_total_pages(response),
            "current_page": page
        }

    def _get_total_pages(self, response: httpx.Response) -> int:
        """Extract total pages from Link header."""
        link_header = response.headers.get("Link", "")
        if not link_header:
            return 1
        
        # Parse Link header to find last page
        import re
        for link in link_header.split(","):
            link = link.strip()
            if 'rel="last"' in link:
                # Extract page number from URL - more robust regex
                match = re.search(r'[?&]page=(\d+)', link)
                if match:
                    return int(match.group(1))
        
        # If no "last" link found, check if there's a "next" link
        # If there's no "next" link, we're on the last page
        for link in link_header.split(","):
            link = link.strip()
            if 'rel="next"' in link:
                # There are more pages, but we don't know how many
                # We'll use a different approach
                return -1  # Signal that we need to paginate manually
        
        return 1

    async def get_all_issues(self, repo_full_name: str, state: str = "all") -> List[Dict[str, Any]]:
        """Get all issues for a repository with pagination."""
        all_issues = []
        page = 1
        
        # Get first page to determine total pages
        first_page = await self.get_issues_page(repo_full_name, page, state=state)
        all_issues.extend(first_page["issues"])
        total_pages = first_page["total_pages"]
        
        if total_pages == -1:
            # Manual pagination - keep fetching until we get an empty page or less than per_page items
            page = 2
            while True:
                page_result = await self.get_issues_page(repo_full_name, page, state=state)
                issues = page_result["issues"]
                
                if not issues or len(issues) == 0:
                    break
                
                all_issues.extend(issues)
                
                # If we got less than per_page items, we're on the last page
                if len(issues) < 100:  # per_page default is 100
                    break
                
                page += 1
        elif total_pages > 1:
            # We know the total pages, fetch them concurrently
            tasks = []
            for page in range(2, total_pages + 1):
                tasks.append(self.get_issues_page(repo_full_name, page, state=state))
            
            # Process pages with limited concurrency
            semaphore = asyncio.Semaphore(5)  # Limit concurrent requests
            
            async def fetch_page(page_task):
                async with semaphore:
                    return await page_task
            
            page_results = await asyncio.gather(*[fetch_page(task) for task in tasks])
            
            for page_result in page_results:
                all_issues.extend(page_result["issues"])
        
        # Filter out pull requests (they appear in issues API)
        issues_only = [issue for issue in all_issues if "pull_request" not in issue]
        
        # Debug info - can be removed later
        if self.console:
            total_fetched = len(all_issues)
            total_after_filter = len(issues_only)
            pull_requests_filtered = total_fetched - total_after_filter
            
            if pull_requests_filtered > 0:
                self.console.print(f"[dim]Fetched {total_fetched} items, filtered out {pull_requests_filtered} pull requests, {total_after_filter} issues remaining[/dim]")
            else:
                self.console.print(f"[dim]Fetched {total_after_filter} issues total[/dim]")
        
        return issues_only

    async def get_issue_comments(self, repo_full_name: str, issue_number: int) -> List[Dict[str, Any]]:
        """Get all comments for a specific issue."""
        all_comments = []
        page = 1
        per_page = 100
        
        while True:
            params = {
                "page": page,
                "per_page": per_page
            }
            
            response = await self._make_request(
                "GET", f"/repos/{repo_full_name}/issues/{issue_number}/comments",
                params=params
            )
            
            comments = response.json()
            if not comments:
                break
            
            all_comments.extend(comments)
            
            if len(comments) < per_page:
                break
            
            page += 1
        
        return all_comments

    async def get_issue_with_comments(self, repo_full_name: str, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Get issue details with comments."""
        issue_number = issue["number"]
        
        # Get comments if the issue has any
        comments = []
        if issue.get("comments", 0) > 0:
            comments = await self.get_issue_comments(repo_full_name, issue_number)
        
        return {
            "issue": issue,
            "comments": comments
        }

    async def fetch_issues_with_comments(self, repo_full_name: str, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fetch all issues with their comments concurrently."""
        semaphore = asyncio.Semaphore(10)  # Limit concurrent requests
        
        async def fetch_issue_with_comments(issue):
            async with semaphore:
                return await self.get_issue_with_comments(repo_full_name, issue)
        
        tasks = [fetch_issue_with_comments(issue) for issue in issues]
        results = await asyncio.gather(*tasks)
        
        return results

    async def test_authentication(self) -> Dict[str, Any]:
        """Test if authentication is working."""
        response = await self._make_request("GET", "/user")
        return response.json()

    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limit status."""
        return {
            "remaining": self.rate_limit_remaining,
            "reset_time": self.rate_limit_reset,
            "seconds_until_reset": (self.rate_limit_reset - datetime.now()).total_seconds()
        }