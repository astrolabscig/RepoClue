"""Command-line entry point for RepoClue."""

import httpx

from repoclue.github.client import GitHubClient


def main() -> None:
    query = input("What kind of repository are you looking for? ")

    try:
        with GitHubClient() as client:
            result = client.search_repositories(query, limit=5)

        print(f"\nFound {result['total_count']} matching repositories.\n")

        for repo in result["items"]:
            print(f"{repo['full_name']}  ★ {repo['stargazers_count']}")
            print(repo["description"] or "No description provided.")
            print(repo["html_url"])
            print()

    except ValueError as error:
        print(f"Error: {error}")
    except httpx.HTTPStatusError as error:
        if error.response.status_code in (403, 429):
            print("GitHub API rate limit exceeded. Please try again later.")
        else:
            print(f"GitHub API returned an error: {error.response.status_code} {error.response.reason_phrase}")
    except httpx.RequestError as error:
        print(f"Could not reach GitHub. Check your internet connection: {error}")


if __name__ == "__main__":
    main()
