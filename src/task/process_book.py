from src.agent.librarian import LibrarianAgent
from src.agent.librarian_model import BookMetadata
from src.tool.csv_parser import read_publisher_metadata
from src.tool.epub import extract_epub_data
from src.utils.logger import log_execution_time


@log_execution_time
def process_book(librarian_agent: LibrarianAgent, epub_file_path: str, metadata_file_path: str) -> BookMetadata:
    """
    Processes a book by extracting metadata, analyzing content, and combining the information.

    Args:
        epub_file_path: The path to the EPUB file.
        metadata_file_path: The path to the publisher metadata CSV file.

    Returns:
        A BookMetadata object containing the combined book information.
    """
    publisher_metadata = read_publisher_metadata(file_path=metadata_file_path, separator="\t")

    epub_metadata, epub_content, epub_id = extract_epub_data(file_path=epub_file_path)

    content_information = librarian_agent.extract_information(epub_content=epub_content)

    book_title = publisher_metadata.get(epub_id, {}).get("title") or epub_metadata.get("dc:title") or "Unknown Title"
    book_author = publisher_metadata.get(epub_id, {}).get("author") or epub_metadata.get("dc:creator") or "Unknown Author"
    publishing_year = publisher_metadata.get(epub_id, {}).get("publishing_year") or epub_metadata.get("dc:date") or 0

    response = BookMetadata(
        title=book_title,
        author=book_author,
        publishing_year=publishing_year,
        epub_id=epub_id,
        genre=content_information.genre,
        themes=content_information.themes,
        setting=content_information.setting,
        cultural_context=content_information.cultural_context,
        narrative_tone=content_information.narrative_tone,
        author_writing_style=content_information.author_writing_style,
        characters_and_relationships=content_information.characters_and_relationships,
    )
    return response
