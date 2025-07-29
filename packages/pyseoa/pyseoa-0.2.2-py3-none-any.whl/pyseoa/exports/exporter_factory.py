from .base_exporter import BaseExporter
from .json_exporter import JSONExporter
from .csv_exporter import CSVExporter
from .html_exporter import HTMLExporter
from .fancy_html_exporter import FancyHTMLExporter
from .markdown_exporter import MarkdownExporter
from .pdf_exporter import PDFExporter
from .terminal_exporter import TerminalExporter

class ExporterFactory:
    """
    Factory for creating exporter instances.
    """

    def get_exporter(self, export_type: str, **kwargs) -> BaseExporter:
        export_type = export_type.lower()
        if export_type == 'json':
            return JSONExporter(**kwargs)
        elif export_type == 'csv':
            return CSVExporter(**kwargs)
        elif export_type == 'html':
            return HTMLExporter(**kwargs)
        elif export_type == 'fancy_html':
            return FancyHTMLExporter(**kwargs)
        elif export_type == 'markdown':
            return MarkdownExporter(**kwargs)
        elif export_type == 'pdf':
            return PDFExporter(**kwargs)
        elif export_type == 'terminal':
            return TerminalExporter(**kwargs)
        else:
            raise ValueError(f'Unsupported export type: {export_type}')