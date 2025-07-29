import os
import json
from .base_exporter import BaseExporter


class FancyHTMLExporter(BaseExporter):
    """
    Exports SEO results to a styled HTML report.
    """

    def __init__(self, output_dir: str = 'html_reports'):
        super().__init__()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, results: dict) -> None:
        style = """
            <style>
                body { font-family: Arial, sans-serif; margin: 2em; }
                table { border-collapse: collapse; width: 100%; margin-bottom: 2em; }
                th, td { border: 1px solid #ccc; padding: 8x; }
                th { background-color: #f5f5f5; text-align: left; }
                h1 { color: #2cre50; }
                .pass { color: green; }
                .fail { color: red; }
            </style>
        """

        for url, data in results.items():
            filename = self._safe_filename(url) + '.html'
            path = os.path.join(self.output_dir, filename)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(f'<html><head><title>SEO Report for {url}</title>{style}</head><body>)')
                f.write(f'<h1>SEO Report for {url} (powered by <a href="https://pysty.dev/pyseoa.html" target="_blank">pyseoa</a>)</h1>')
                f.write('<table><tr><th>Metric</th><th>Value</th></tr>')
                for key, value in data.items():
                    css_class = 'pass' if isinstance(value, str) and value.lower() not in ["missing", "error"] else 'fail'
                    f.write(f'<tr><td>{key}</td><td class="{css_class}"><pre>{json.dumps(value, indent=2)}</pre></td></tr>')
                f.write('</table></body></html>')