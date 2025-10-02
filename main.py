import logging
from src.agent.librarian import LibrarianAgent
from src.task.process_book import process_book
from src.utils.logger import log_execution_time

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler()]
)


@log_execution_time
def main():
    """Initializes the agent, processes the book, and prints the metadata."""
    # These paths can be configured or passed as arguments

    METADATA_FILE_PATH = "./dataset/metadata.csv"

    epub_file_paths: list[str] = [
        "./dataset/pg74.epub",
        "./dataset/pg76.epub",
    ]

    librarian_agent = LibrarianAgent(model_name="gemini-2.5-flash")
    try:
        book_metadatas = []

        for epub_file_path in epub_file_paths:
            book_metadata = process_book(
                librarian_agent=librarian_agent,
                epub_file_path=epub_file_path,
                metadata_file_path=METADATA_FILE_PATH,
            )
            book_metadatas.append(book_metadata)
        GREEN = "\033[92m"
        ENDC = "\033[0m"

        print(GREEN + book_metadata.model_dump_json(indent=4) + ENDC)

    finally:
        librarian_agent.client.close()


if __name__ == "__main__":
    main()
