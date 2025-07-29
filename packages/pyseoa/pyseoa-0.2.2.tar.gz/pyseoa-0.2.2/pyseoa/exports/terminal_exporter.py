from typing import List
from .base_exporter import BaseExporter
import json



class TerminalExporter(BaseExporter):
    """
    Exports SEO analysis results to the terminal.
    """

    def export(self, result: dict) -> None:
        print('🖥️ Terminal Output:')
        for url, data in result.items():
            print(f'\n🌐 URL: {url}')
            for key, value in data.items():
                print(f'  {key}: {json.dumps(value, indent=2) if isinstance(value, (dict,list)) else value}')
        print("\n✅ Done printing results.")