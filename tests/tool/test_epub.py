from unittest.mock import patch
from src.tool.epub import extract_epub_data


@patch("src.tool.epub.parser.from_file")
def test_extract_epub_data(mock_from_file):
    """
    Tests the extract_epub_data function with a mocked EPUB file.
    """
    mock_from_file.return_value = {
        "metadata": {"title": "Mock Book"},
        "content": "This is the content of the mock book.",
    }

    file_path = "a/b/c/mock_book.epub"
    metadata, content, epub_id = extract_epub_data(file_path)

    assert epub_id == "mock_book"
    assert metadata == {"title": "Mock Book"}
    assert content == "This is the content of the mock book."
    mock_from_file.assert_called_once_with(file_path)
