import os
import tempfile
import pytest
from ksrpdfparser.image_extractor import ImageExtractor
from ksrpdfparser.pdf_utils import save_images_to_folder, get_image_summary

# Sample test PDF with images (you must provide this file or mock it in CI)
TEST_PDF = "tests/resources/sample_with_images.pdf"


@pytest.fixture(scope="module")
def extractor():
    with ImageExtractor(TEST_PDF) as ex:
        yield ex


def test_extract_images_from_page(extractor):
    images = extractor.extract_images_from_page(0)
    assert isinstance(images, list)
    if images:
        assert "ext" in images[0]
        assert "bytes" in images[0]


def test_extract_all_images(extractor):
    images = extractor.extract_all_images()
    assert isinstance(images, list)
    for img in images:
        assert "ext" in img and "bytes" in img and "xref" in img


def test_save_images_to_folder(extractor):
    images = extractor.extract_all_images()
    with tempfile.TemporaryDirectory() as tmpdir:
        paths = save_images_to_folder(images, tmpdir)
        assert all(os.path.exists(path) for path in paths)
        assert len(paths) == len(images)


def test_get_image_summary():
    summary = get_image_summary(TEST_PDF)
    assert isinstance(summary, list)
    for item in summary:
        assert isinstance(item, tuple)
        assert isinstance(item[0], int)  # page number
        assert isinstance(item[1], int)  # image count
