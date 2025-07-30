import unittest

from github_tracker import GitHubTrending


class TestGitHubTrending(unittest.TestCase):
    def setUp(self):
        self.trending = GitHubTrending()

    def test_init(self):
        self.assertEqual(self.trending.url, "https://github.com/trending")

    def test_fetch(self):
        text = self.trending.fetch_page()
        # print(text[:100])
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 1000)

    def test_fetch_json(self):
        data = self.trending.fetch_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn('repo_name', data[0])
        self.assertIn('description', data[0])
        self.assertIn('url', data[0])
        # print(data)
