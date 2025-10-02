from unittest.mock import patch, MagicMock
from src.agent.librarian import LibrarianAgent
from src.agent.librarian_model import ContentInformation


@patch("src.agent.librarian.outlines.from_gemini")
@patch("src.agent.librarian.genai.Client")
def test_extract_information(mock_genai_client, mock_from_gemini):
    """
    Tests the extract_information method of the LibrarianAgent.
    """
    # Arrange
    mock_model = MagicMock()
    mock_from_gemini.return_value = mock_model

    mock_response_json = """
    {
        "genre": "Science Fiction",
        "themes": ["AI", "Humanity", "Existentialism"],
        "setting": {"time": "2242", "place": "Neo-Veridia"},
        "cultural_context": "A world grappling with the implications of advanced AI.",
        "narrative_tone": "Pensive and cautionary.",
        "author_writing_style": "Crisp and evocative.",
        "characters_and_relationships": [
            {"name": "Jaxon", "relationship": "Protagonist"},
            {"name": "Unit 734", "relationship": "Antagonist"},
            {"name": "Dr. Aris", "relationship": "Creator"}
        ]
    }
    """
    mock_model.return_value = mock_response_json

    agent = LibrarianAgent()
    epub_content = "Some sample epub content."

    # Act
    result = agent.extract_information(epub_content)

    # Assert
    assert isinstance(result, ContentInformation)
    assert result.genre == "Science Fiction"
    assert result.themes == ["AI", "Humanity", "Existentialism"]
    assert result.setting.time == "2242"
    assert result.setting.place == "Neo-Veridia"
    assert result.narrative_tone == "Pensive and cautionary."
    assert len(result.characters_and_relationships) == 3
    assert result.characters_and_relationships[0].name == "Jaxon"

    # Verify that the model was called with the correct prompt
    mock_model.assert_called_once()
    _, kwargs = mock_model.call_args
    assert "You're an expert in literature" in kwargs["model_input"]
    assert epub_content in kwargs["model_input"]
    assert kwargs["output_type"] == ContentInformation
    assert kwargs["temperature"] == 0.2
    assert kwargs["max_output_tokens"] == 200
    assert kwargs["top_p"] == 0.95

    agent.close()
    mock_genai_client.return_value.close.assert_called_once()
