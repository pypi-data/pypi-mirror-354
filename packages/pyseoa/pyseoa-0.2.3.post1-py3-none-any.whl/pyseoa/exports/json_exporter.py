# json_exporter.py

import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from .base_exporter import BaseExporter
from tqdm import tqdm



class JSONExporter(BaseExporter):
    """
    Handles exporting SEO analysis to JSON.
    """

    def __init__(self, output_dir: str = 'reports') -> None:
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, results: dict, workers: int = 1) -> None:
        def write(url: str):
            for url, data in results.items():
                filename = self._safe_filename(url)
                path = os.path.join(self.output_dir, f"{filename}.json")

                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

        urls = results.keys()

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(write, url): url for url in urls}
            for future in tqdm(as_completed(futures), total=len(futures), desc='Exporting JSON'):
                try:
                    future.result()
                except Exception as e:
                    print(f"⚠️ Failed to export {futures[future]}: {e}")