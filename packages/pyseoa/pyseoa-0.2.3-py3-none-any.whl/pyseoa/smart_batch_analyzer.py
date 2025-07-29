from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from typing import List
from analyzer import BatchSEOAnalyzer
from crawler import SiteCrawler



class SmartBatchSEOAnalyzer(BatchSEOAnalyzer):
    """
    Extended BatchSEOAnalyzer that supports optional crawling to analyze internal links.

    Args:
        urls (List[str]): Starting URLs.
        follow_links: (bool): Whether to crawl and analyze internal links.
        max_pages (int): Maximum number of pages to crawl per domain.
        workers (int): Number of threads for crawling and analysing.
        **kwargs: Passed to parent BatchSEOAnalyzer.
    """

    def __init__(self, urls: List[str], follow_links: bool = False, max_pages: int = 10, workers: int = 5, **kwargs) -> None:
        self.original_urls = urls
        self.follow_links = follow_links
        self.max_pages = max_pages
        self.workers = workers
        
        if follow_links:
            print('🔍 Crawling enabled.')
            all_urls = set()
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(SiteCrawler(url, max_pages).crawl): url for url in urls}
                for future in tqdm(futures, desc='Crawling', total=len(futures)):
                    try:
                        crawled = future.result()
                        all_urls.update(crawled)
                    except Exception as e:
                        print(f"⚠️ Failed to crawl {futures[future]}: {e}")
            urls = list(all_urls)

        super().__init__(urls, **kwargs)


