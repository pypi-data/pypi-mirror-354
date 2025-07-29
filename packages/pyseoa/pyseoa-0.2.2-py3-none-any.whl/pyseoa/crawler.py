import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import Set, List

class SiteCrawler:
    """
    Crawls a website and collects internal URLs up to maximum depth or page limit.
    """

    def __init__(self, base_url:str, max_pages:int = 100) -> None:
        """
        Initializes the crawler.

        Args:
            base_url (str): The starting URL to crawl.
            max_pages (int): Maximum number of pages to crawl.
        """
        self.base_url = base_url
        self.visited: Set[str] = set()
        self.to_visit: List[str] = [base_url]
        self.max_pages = max_pages
        self.domain = urlparse(base_url).netloc

    def is_internal_link(self, link: str) -> bool:
        """
        Checks if a link s internal to the domain.
        """
        parsed = urlparse(link)
        return not parsed.netloc or parsed.netloc == self.domain
    
    def extract_links(self, html: str, current_url: str) -> List[str]:
        """
        Extracts internal links from HTML content.
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            absolute_url = urljoin(current_url, href)
            if self.is_internal_link(absolute_url):
                links.add(absolute_url.split('#')[0])
        return list(links)
    
    def crawl(self) -> List[str]:
        """
        Crawls the website starting from the base URL and returns a list of discovered URLs.
        """
        discovered = []

        while self.to_visit and len(self.visited)< self.max_pages:
            current_url = self.to_visit.pop(0)
            if current_url in self.visited:
                continue
            
            try:
                response = requests.get(current_url, timeout=10)
                response.raise_for_status()
                self.visited.add(current_url)
                discovered.append(current_url)
                new_links = self.extract_links(response.text, current_url)
                for link in new_links:
                    if link not in self.visited and link not in self.to_visit:
                        self.to_visit.append(link)
            except requests.RequestException:
                continue

        return discovered