import os
import fitz
import pdfplumber
from typing import List, Dict, Tuple
from ksrpdfparser.text_extractor import TextExtractor
from ksrpdfparser.image_extractor import ImageExtractor


def extract_metadata(pdf_path: str) -> dict:
    with pdfplumber.open(pdf_path) as pdf:
        return pdf.metadata


def get_number_of_pages(pdf_path: str) -> int:
    with pdfplumber.open(pdf_path) as pdf:
        return len(pdf.pages)


def save_text_to_file(text: str, output_file_path: str):
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(text)


def process_multiple_pdfs(pdf_folder: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(pdf_folder, filename)
            output_path = os.path.join(
                output_folder, f"{os.path.splitext(filename)[0]}.txt"
            )
            with TextExtractor(input_path) as extractor:
                text = extractor.extract_all_text()
            save_text_to_file(text, output_path)


def save_images_to_folder(
    images: List[Dict], output_folder: str, prefix: str = "img"
) -> List[str]:
    """
    Save extracted images to a folder.

    Args:
        images (List[Dict]): List of image dicts (ext, bytes, page, etc.)
        output_folder (str): Directory to save images.
        prefix (str): Optional prefix for file names.

    Returns:
        List[str]: File paths of saved images.
    """
    os.makedirs(output_folder, exist_ok=True)
    saved_files = []

    for idx, img in enumerate(images):
        ext = img["ext"]
        image_data = img["bytes"]
        page = img.get("page", "unknown")
        filename = f"{prefix}_page{page + 1}_{idx + 1}.{ext}"
        file_path = os.path.join(output_folder, filename)

        with open(file_path, "wb") as f:
            f.write(image_data)

        saved_files.append(file_path)

    return saved_files


def get_image_summary(pdf_path: str) -> List[Tuple[int, int]]:
    """
    Returns a list of tuples showing number of images per page.

    Args:
        pdf_path (str): Path to PDF.

    Returns:
        List[Tuple[int, int]]: (page_number, image_count)
    """
    summary = []
    with ImageExtractor(pdf_path) as extractor:
        for i in range(len(extractor.doc)):
            images = extractor.extract_images_from_page(i)
            summary.append((i, len(images)))
    return summary
