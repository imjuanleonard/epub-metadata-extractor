import json
from unittest.mock import MagicMock, patch
from main import main


@patch("main.process_book")
@patch("main.LibrarianAgent")
def test_main_script_execution(mock_librarian_agent_class, mock_process_book, capsys):
    """
    Tests the main script execution flow.

    Verifies that:
    - LibrarianAgent is instantiated.
    - process_book is called with the correct arguments.
    - The agent's client is closed.
    - The result from process_book is printed to stdout.
    """
    # Arrange
    # Mock the instance of LibrarianAgent and its client
    mock_agent_instance = MagicMock()
    mock_librarian_agent_class.return_value = mock_agent_instance

    # Mock the return value of process_book
    mock_book_metadata = MagicMock()
    expected_dict = {"title": "Test Book", "author": "Test Author"}
    mock_book_metadata.model_dump_json.return_value = json.dumps(expected_dict, indent=4)
    mock_process_book.return_value = mock_book_metadata

    # Act
    # Execute the main function
    main()

    # Assert
    # Verify LibrarianAgent was instantiated correctly
    mock_librarian_agent_class.assert_called_once_with(model_name="gemini-2.5-flash")

    # Verify process_book was called with the correct arguments
    mock_process_book.assert_called_once_with(
        librarian_agent=mock_agent_instance,
        epub_file_path="./dataset/pg74.epub",
        metadata_file_path="./dataset/metadata.csv",
    )

    # Verify the agent's client was closed
    mock_agent_instance.client.close.assert_called_once()

    # Verify the output was printed correctly
    captured = capsys.readouterr()
    expected_json_output = json.dumps(expected_dict, indent=4)
    # Define ANSI color codes to match main.py
    GREEN = "\033[92m"
    ENDC = "\033[0m"
    expected_colored_output = f"{GREEN}{expected_json_output}{ENDC}"

    assert captured.out.strip() == expected_colored_output
