from github_tracker import GitHubTrending

if __name__ == "__main__":
    checker = GitHubTrending(interval=1800)
    data = checker.fetch_json()
    print(data)
