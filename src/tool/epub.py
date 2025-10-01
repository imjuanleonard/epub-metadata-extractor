from tika import parser
from src.utils.logger import log_execution_time


@log_execution_time
def extract_epub_data(file_path: str) -> tuple[dict, str, str]:
    """
    Extracts metadata and content from an EPUB file.

    Args:
        file_path: The path to the EPUB file.

    Returns:
        A tuple containing the EPUB metadata (dict) and content (str).
    """

    epub_id = file_path.split("/")[-1].replace(".epub", "")
    epub_data = parser.from_file(file_path)
    return epub_data.get("metadata", {}), epub_data.get("content", ""), epub_id
