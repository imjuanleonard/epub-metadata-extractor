from src.agent.librarian import LibrarianAgent
from src.task.process_book import process_book


def main():
    """Initializes the agent, processes the book, and prints the metadata."""
    # These paths can be configured or passed as arguments
    EPUB_FILE_PATH = "./dataset/pg74.epub"
    METADATA_FILE_PATH = "./dataset/metadata.csv"

    librarian_agent = LibrarianAgent(model_name="gemini-2.5-flash")
    try:
        book_metadata = process_book(
            librarian_agent=librarian_agent,
            epub_file_path=EPUB_FILE_PATH,
            metadata_file_path=METADATA_FILE_PATH,
        )
        print(book_metadata.model_dump_json(indent=4))
    finally:
        librarian_agent.client.close()


if __name__ == "__main__":
    main()
