import unittest
from ksrpdfparser.text_extractor import TextExtractor


class TestTextExtractor(unittest.TestCase):

    def setUp(self):
        self.pdf_path = "sample.pdf"  # Replace with your test PDF file path
        self.extractor = TextExtractor(self.pdf_path)

    def tearDown(self):
        self.extractor.close()

    def test_extract_all_text(self):
        text = self.extractor.extract_all_text()
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0)

    def test_extract_text_by_page(self):
        pages = self.extractor.extract_text_by_page()
        self.assertIsInstance(pages, list)
        self.assertTrue(len(pages) > 0)
        self.assertIsInstance(pages[0], str)

    def test_extract_text_in_bbox(self):
        bbox = (0, 0, 100, 100)
        text = self.extractor.extract_text_in_bbox(0, bbox)
        self.assertTrue(text is None or isinstance(text, str))


if __name__ == "__main__":
    unittest.main()
