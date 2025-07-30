import pdfplumber
from typing import List, Optional


class TableExtractor:

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_tables(
        self, pages: Optional[List[int]] = None
    ) -> List[List[List[str]]]:
        tables = []

        with pdfplumber.open(self.pdf_path) as pdf:
            target_pages = range(len(pdf.pages)) if pages is None else pages

            for page_num in target_pages:
                page = pdf.pages[page_num]
                extracted = page.extract_tables()
                for table in extracted:
                    tables.append(table)

        return tables
