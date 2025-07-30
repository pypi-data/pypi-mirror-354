from typing import List, Dict, Tuple
import fitz  # PyMuPDF


class ImageExtractor:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc = fitz.open(file_path)

    def extract_images_from_page(self, page_number: int) -> List[Dict]:
        images = []
        if 0 <= page_number < len(self.doc):
            page = self.doc[page_number]
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                images.append(
                    {
                        "ext": base_image["ext"],
                        "bytes": base_image["image"],
                        "xref": xref,
                    }
                )
        return images

    def extract_all_images(self) -> List[Dict]:
        all_images = []
        for page_number in range(len(self.doc)):
            page = self.doc[page_number]
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                all_images.append(
                    {
                        "ext": base_image["ext"],
                        "bytes": base_image["image"],
                        "xref": xref,
                        "page": page_number,
                    }
                )
        return all_images

    def close(self):
        self.doc.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
