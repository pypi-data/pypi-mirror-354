from typing import List, Tuple, Optional, Union
import pdfplumber


class TextExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pdf = pdfplumber.open(file_path)

    def extract_all_text(self) -> str:
        return "\n".join(page.extract_text() or "" for page in self.pdf.pages)

    def extract_text_by_page(
        self, page_number: Optional[int] = None
    ) -> Union[str, List[str]]:
        if page_number is not None:
            if 0 <= page_number < len(self.pdf.pages):
                return self.pdf.pages[page_number].extract_text() or ""
            else:
                raise IndexError(f"Page number {page_number} is out of range.")
        else:
            return [page.extract_text() or "" for page in self.pdf.pages]

    def extract_text_in_bbox(
        self, page_number: int, bbox: Tuple[float, float, float, float]
    ) -> Optional[str]:
        if 0 <= page_number < len(self.pdf.pages):
            page = self.pdf.pages[page_number]
            cropped = page.within_bbox(bbox)
            return cropped.extract_text() or ""
        return None

    def close(self):
        self.pdf.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
