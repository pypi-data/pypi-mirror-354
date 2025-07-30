import os
from ksrpdfparser.table_extractor import TableExtractor


def test_extract_tables():
    test_pdf = "tests/sample_with_tables.pdf"
    if not os.path.exists(test_pdf):
        print(f"Test skipped: {test_pdf} not found.")
        return

    extractor = TableExtractor(test_pdf)
    tables = extractor.extract_tables()

    assert isinstance(tables, list)
    assert all(isinstance(table, list) for table in tables)
    assert all(isinstance(row, list) for table in tables for row in table)

    # Optional: print for manual inspection
    for table in tables:
        for row in table:
            print(row)
