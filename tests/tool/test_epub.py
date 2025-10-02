from unittest.mock import patch
from unittest.mock import MagicMock
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


@patch("src.tool.epub.get_logger")
@patch("src.tool.epub.parser.from_file")
def test_extract_epub_data_parsing_error(mock_from_file, mock_get_logger):
    """
    Tests the extract_epub_data function when parser.from_file raises an exception.
    """
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger
    mock_from_file.side_effect = Exception("Test parsing error")

    file_path = "a/b/c/error_book.epub"
    metadata, content, epub_id = extract_epub_data(file_path)

    assert epub_id == "error_book"
    assert metadata == {}
    assert content == ""
    mock_from_file.assert_called_once_with(file_path)
    mock_get_logger.assert_called_once_with("src.tool.epub")
    mock_logger.info.assert_called_once_with("Failed to parse EPUB file: Test parsing error")


@patch("src.tool.epub.parser.from_file")
def test_extract_epub_data_no_metadata(mock_from_file):
    """
    Tests the extract_epub_data function when the parsed data has no metadata.
    """
    mock_from_file.return_value = {
        "content": "This is the content of the mock book.",
    }

    file_path = "a/b/c/no_meta_book.epub"
    metadata, content, epub_id = extract_epub_data(file_path)

    assert epub_id == "no_meta_book"
    assert metadata == {}
    assert content == "This is the content of the mock book."
    mock_from_file.assert_called_once_with(file_path)


@patch("src.tool.epub.parser.from_file")
def test_extract_epub_data_no_content(mock_from_file):
    """
    Tests the extract_epub_data function when the parsed data has no content.
    """
    mock_from_file.return_value = {
        "metadata": {"title": "Mock Book"},
    }

    file_path = "a/b/c/no_content_book.epub"
    metadata, content, epub_id = extract_epub_data(file_path)

    assert epub_id == "no_content_book"
    assert metadata == {"title": "Mock Book"}
    assert content == ""
    mock_from_file.assert_called_once_with(file_path)


@patch("src.tool.epub.parser.from_file")
def test_extract_epub_data_empty_data(mock_from_file):
    """
    Tests the extract_epub_data function when the parsed data is empty.
    """
    mock_from_file.return_value = {}

    file_path = "a/b/c/empty_book.epub"
    metadata, content, epub_id = extract_epub_data(file_path)

    assert epub_id == "empty_book"
    assert metadata == {}
    assert content == ""
    mock_from_file.assert_called_once_with(file_path)
