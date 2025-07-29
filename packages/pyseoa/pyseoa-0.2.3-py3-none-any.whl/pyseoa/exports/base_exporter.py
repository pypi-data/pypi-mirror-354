import hashlib
from abc import ABC, abstractmethod
from typing import List
from urllib.parse import urlparse

class BaseExporter(ABC):
    """
    Abstract base class for all SEO exporters.
    """

    @abstractmethod
    def export(self, result: dict, original_urls: List[str] = [], workers: int = 1) -> None:
        """
        Export the results in the desired format.
        """
        pass

    @staticmethod
    def _safe_filename(url: str) -> str:
        parsed = urlparse(url)
        # use netloc + path, cleaned and truncated, or hash for uniquness
        base = f'{parsed.netloc}_{parsed.path.strip("/").replace("/", "_")}'
        if not base or base.endswith('_'):
            base += 'index'
        if len(base) > 100:
            # Prevent filename overflow - hash the full URL
            base = base[:50] + '_' + hashlib.md5(url.encode()).hexdigest()
        return base
