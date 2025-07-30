import requests
from bs4 import BeautifulSoup


class GitHubTrending:
    def __init__(self, url="https://github.com/trending", interval=3600):
        self.url = url
        self.interval = interval  # 单位：秒

    def fetch_page(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print("Error fetching page:", e)
            return None

    def parse_trending_repos(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        repo_elements = soup.find_all('article', class_='Box-row')
        trending_repos = []

        for repo in repo_elements:
            full_name_elem = repo.h2.a
            description = repo.find('p', class_='col-9 color-fg-muted my-1 pr-4')
            repo_name = full_name_elem.get_text(strip=True).replace('\n', '').replace(' ', '')
            result = {
                'repo_name': repo_name,
                'description': description.get_text(strip=True) if description else '',
                'url': f"https://github.com{full_name_elem['href']}",
            }
            trending_repos.append(result)

        return trending_repos

    def fetch_json(self):
        html = self.fetch_page()
        print("html length:", len(html))
        current_projects = self.parse_trending_repos(html)
        return current_projects
