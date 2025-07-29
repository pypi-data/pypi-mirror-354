import csv
import json
from .base_exporter import BaseExporter


class CSVExporter(BaseExporter):
    """
    Handles exporting SEO analysis results to a combined CSV.
    """

    def __init__(self, output_file: str = 'seo_summary.csv') -> None:
        super().__init__()
        self.output_file = output_file

    def export(self, results: dict) -> None:
        all_keys = set()
        for result in results.values():
            all_keys.update(result.keys())
        all_keys = sorted(all_keys)

        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["URL"] + all_keys)
            for url, result in results.items():
                row = [url] + [json.dumps(result.get(k, '')) for k in all_keys]
                writer.writerow(row)
            print(f"✅ CSV saved: {self.output_file}")