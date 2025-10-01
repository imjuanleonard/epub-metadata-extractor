import pytest
from unittest.mock import patch, MagicMock
from src.task.process_book import process_book
from src.agent.librarian_model import ContentInformation, ThemeSetting, CharacterAndRelationships

# Common test data
EPUB_FILE_PATH = "path/to/book.epub"
METADATA_FILE_PATH = "path/to/metadata.tsv"
EPUB_ID = "test_book_id"
EPUB_CONTENT = "This is the content of the book."

# Mock content information returned by the librarian agent
MOCK_CONTENT_INFO = ContentInformation(
    genre="Science Fiction",
    themes=["AI", "Humanity", "Existentialism"],
    setting=ThemeSetting(time="2242", place="Neo-Veridia"),
    cultural_context="Globalized society",
    narrative_tone="Philosophical",
    author_writing_style="Introspective",
    characters_and_relationships=[
        CharacterAndRelationships(name="Jaxon", relationship="Protagonist"),
        CharacterAndRelationships(name="Elara", relationship="Antagonist"),
        CharacterAndRelationships(name="Kael", relationship="Supporting Character"),
    ],
)


@pytest.fixture
def mock_librarian_agent():
    """Fixture for a mocked LibrarianAgent."""
    agent = MagicMock()
    agent.extract_information.return_value = MOCK_CONTENT_INFO
    return agent


@patch("src.task.process_book.extract_epub_data")
@patch("src.task.process_book.read_publisher_metadata")
def test_process_book_prioritizes_publisher_metadata(
    mock_read_publisher_metadata, mock_extract_epub_data, mock_librarian_agent
):
    """
    Tests that process_book uses publisher metadata when available,
    even if EPUB metadata also exists.
    """
    # Arrange
    mock_read_publisher_metadata.return_value = {
        EPUB_ID: {"title": "Publisher Title", "author": "Publisher Author", "publishing_year": 2025}
    }
    mock_extract_epub_data.return_value = (
        {"dc:title": "EPUB Title", "dc:creator": "EPUB Author", "dc:date": 2024},
        EPUB_CONTENT,
        EPUB_ID,
    )

    # Act
    result = process_book(mock_librarian_agent, EPUB_FILE_PATH, METADATA_FILE_PATH)

    # Assert
    assert result.title == "Publisher Title"
    assert result.author == "Publisher Author"
    assert result.publishing_year == 2025
    assert result.epub_id == EPUB_ID
    assert result.genre == MOCK_CONTENT_INFO.genre
    mock_read_publisher_metadata.assert_called_once_with(file_path=METADATA_FILE_PATH, separator="\t")
    mock_extract_epub_data.assert_called_once_with(file_path=EPUB_FILE_PATH)
    mock_librarian_agent.extract_information.assert_called_once_with(epub_content=EPUB_CONTENT)


@patch("src.task.process_book.extract_epub_data")
@patch("src.task.process_book.read_publisher_metadata")
def test_process_book_falls_back_to_epub_metadata(mock_read_publisher_metadata, mock_extract_epub_data, mock_librarian_agent):
    """
    Tests that process_book falls back to EPUB metadata when publisher metadata is missing for the book.
    """
    # Arrange
    mock_read_publisher_metadata.return_value = {}  # No matching publisher metadata
    mock_extract_epub_data.return_value = (
        {"dc:title": "EPUB Title", "dc:creator": "EPUB Author", "dc:date": 2024},
        EPUB_CONTENT,
        EPUB_ID,
    )

    # Act
    result = process_book(mock_librarian_agent, EPUB_FILE_PATH, METADATA_FILE_PATH)

    # Assert
    assert result.title == "EPUB Title"
    assert result.author == "EPUB Author"
    assert result.publishing_year == 2024
    assert result.epub_id == EPUB_ID


@patch("src.task.process_book.extract_epub_data")
@patch("src.task.process_book.read_publisher_metadata")
def test_process_book_falls_back_to_default_values(mock_read_publisher_metadata, mock_extract_epub_data, mock_librarian_agent):
    """
    Tests that process_book falls back to default values when no metadata is found.
    """
    # Arrange
    mock_read_publisher_metadata.return_value = {}
    mock_extract_epub_data.return_value = ({}, EPUB_CONTENT, EPUB_ID)  # Empty metadata dict

    # Act
    result = process_book(mock_librarian_agent, EPUB_FILE_PATH, METADATA_FILE_PATH)

    # Assert
    assert result.title == "Unknown Title"
    assert result.author == "Unknown Author"
    assert result.publishing_year == 0
    assert result.epub_id == EPUB_ID


@patch("src.task.process_book.extract_epub_data")
@patch("src.task.process_book.read_publisher_metadata")
def test_process_book_with_mixed_metadata_sources(mock_read_publisher_metadata, mock_extract_epub_data, mock_librarian_agent):
    """
    Tests that process_book correctly combines metadata from different sources on a per-field basis.
    """
    # Arrange
    # Publisher provides title and year, but not author
    mock_read_publisher_metadata.return_value = {EPUB_ID: {"title": "Publisher Title", "publishing_year": 2025}}
    # EPUB provides author and a different title/year
    mock_extract_epub_data.return_value = (
        {"dc:title": "EPUB Title", "dc:creator": "EPUB Author", "dc:date": 2024},
        EPUB_CONTENT,
        EPUB_ID,
    )

    # Act
    result = process_book(mock_librarian_agent, EPUB_FILE_PATH, METADATA_FILE_PATH)

    # Assert
    assert result.title == "Publisher Title"  # From publisher
    assert result.author == "EPUB Author"  # Fallback to EPUB
    assert result.publishing_year == 2025  # From publisher
    assert result.epub_id == EPUB_ID
