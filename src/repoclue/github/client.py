"""HTTP client for GitHub's public REST API."""

import httpx

GITHUB_API_URL = "https://api.github.com"

class GitHubClient:
    """Make requests to GitHub's public API."""
    def __init__(self, timeout: float = 10.0) -> None:
        self._client = httpx.Client(
            base_url=GITHUB_API_URL,
            timeout=timeout,
            headers={
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    def search_repositories(
            self,
            query: str,
            limit: int = 10,
    ) -> dict:
        """Search public repositories and return GitHub's JSON response."""
        if not query.strip():
            raise ValueError("Search query cannot be empty")

        if not 1 <= limit <= 100:
            raise ValueError("Limit must be between 1 and 100.")

        response = self._client.get(
            "/search/repositories",
            params={
                "q": query,
                "per_page": limit,
                "sort": "stars",
                "order": "desc",
            },
        )
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Release the HTTP connection resources."""
        self._client.close()

    def __enter__(self) -> "GitHubClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
