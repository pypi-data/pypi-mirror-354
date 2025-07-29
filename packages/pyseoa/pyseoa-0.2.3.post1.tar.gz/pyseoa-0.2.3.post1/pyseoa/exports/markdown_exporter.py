from .base_exporter import BaseExporter
import os
import json


class MarkdownExporter(BaseExporter):
    """
    Exports SEO results to Markdown files.
    """

    def __init__(self, output_dir: str = 'markdown_reports') -> None:
        super().__init__()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export(self, results: dict) -> None:
        for url, data in results.items():
            filename = self._safe_filename(url) + '.md'
            path = os.path.join(self.output_dir, filename)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(f'# SEO Report for {url} (powered by [pysqoa](https://pysty.dev/pyseoa.html))\n\n')
                for key, value in data.items():
                    f.write(f'## {key}\n')
                    f.write(f'```json\n')
                    f.write(json.dumps(value, indent=2))
                    f.write('```\n')
