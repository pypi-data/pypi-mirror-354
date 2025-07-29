import os
import json
from .base_exporter import BaseExporter


class HTMLExporter(BaseExporter):
    """
    Handles exporting SEO analysis results to a simple HTML report.
    """

    def __init__(self, output_dir: str = 'html_reports') -> None:
        super().__init__()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, results: dict) -> None:
        for url, data in results.items():
            filename = self._safe_filename(url) + '.html'
            path = os.path.join(self.output_dir, filename)

            with open(path, 'w', encoding='utf-8') as f:
                f.write('<html><head><title>SEP Reports</title></head><body>')
                f.write(f'<h1>SEO Report for {url}</h1>')
                f.write('<table border="1" cellpadding="5">')
                for key, value in data.items():
                    f.write(f'<tr><td><strong>{key}</strong></td><td><pre>{json.dumps(value, indent=2)}</pre></td></tr>')
                f.write('</table></body></html>')

            print(f"✅ HTML saved: {path}")