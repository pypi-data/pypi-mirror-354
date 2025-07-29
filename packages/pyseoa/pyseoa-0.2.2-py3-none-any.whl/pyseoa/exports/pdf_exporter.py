import os
from typing import List
from fpdf import FPDF
from urllib.parse import urlparse
from .base_exporter import BaseExporter


class PDFExporter(BaseExporter):
    """
    Exports SEO results to PDF files.
    """

    def __init__(self, output_dir: str = 'pdf_exports') -> None:
        super().__init__()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export(self, results: dict) -> None:
        for url, data in results.items():
            filename = self._safe_filename(url) + '.pdf'
            path = os.path.join(self.output_dir, filename)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_author('pyseoa')
            pdf.set_font('Arial', size=12)
            pdf.cell(200, 10, txt=self._safe_txt(f'SEO Report for {url}'), ln=True, align='L')
            pdf.ln(10)

            for key, value in data.items():
                pdf.set_font('Arial', style='B', size=11)
                pdf.multi_cell(0, 10, self._safe_txt(key))
                pdf.set_font('Arial', size=10)
                pdf.multi_cell(0, 10, self._safe_txt(value))
                pdf.ln(2)

            pdf.output(path)

    def _safe_txt(self, txt: str) -> str:
        return str(txt).encode('latin-1', errors='ignore').decode('latin-1')