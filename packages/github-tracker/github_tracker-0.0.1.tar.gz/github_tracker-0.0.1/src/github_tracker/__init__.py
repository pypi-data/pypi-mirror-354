from github_tracker.github_trending import GitHubTrending

try:
    from importlib.metadata import version
except ImportError:  # For Python<3.8
    from importlib_metadata import version

__version__ = version("github-tracker")
__all__ = ["GitHubTrending"]
