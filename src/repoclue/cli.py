"""Command-line entry point for RepoClue."""

from repoclue.github.client import GitHubClient

VERSION = "0.1.0"


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
    except Exception as error:
        print(f"GitHub request failed: {error}")



if __name__ == "__main__":
    main()
