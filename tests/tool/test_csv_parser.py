import pytest
from src.tool.csv_parser import read_publisher_metadata

def test_read_publisher_metadata():
    """
    Tests the read_publisher_metadata function with a sample CSV file.
    """
    expected_metadata = {
        "1": {
            "title": "Book One",
            "author": "Author A",
            "publishing_year": "2021",
        },
        "2": {
            "title": "Book Two",
            "author": "Author B",
            "publishing_year": "2022",
        },
        "3": {
            "title": "Book Three",
            "author": "Author C",
            "publishing_year": "2023",
        },
    }

    actual_metadata = read_publisher_metadata("tests/fixtures/sample_data.csv")
    assert actual_metadata == expected_metadata