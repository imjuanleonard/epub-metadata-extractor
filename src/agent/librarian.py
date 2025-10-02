import outlines
from google import genai
from src.agent.librarian_model import ContentInformation
from src.utils.logger import log_execution_time


@log_execution_time
class LibrarianAgent:
    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.2,
        max_output_tokens: int = 200,
        top_p: float = 0.95,
    ):
        """
        Initializes the LibrarianAgent.

        Args:
            model_name: The name of the Gemini model to use.
            temperature: The sampling temperature to use control creativity, lower more consistent range 0 - 1.
            max_output_tokens: The maximum number of tokens to generate.
            top_p: The nucleus sampling probability control diversity, higher better range 0 - 1.
        """
        self.client = genai.Client()
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.top_p = top_p
        self.model = outlines.from_gemini(client=self.client, model_name=model_name)

    def close(self):
        self.client.close()

    def extract_information(self, epub_content: str) -> ContentInformation:
        prompt = """
        You're an expert in literature and literary analysis. Your task is to extract and summarize key information from the provided book content. Please provide the following details in a structured format:
            genre (str): Give only 1 main genre of the book (e.g., science fiction, crime, fantasy, romance)
            themes (list[str]): A list of the main themes being featured in the book.
            setting (dict[str, str]): A dictionary of the time and place that the story takes place in.
            cultural_context (str): A brief 1/2 sentence of the relevant cultural context invoked in the story.
            narrative_tone (str): A brief 1/2 sentence of the attitude or mood conveyed by the storytelling.
            author_writing_style (str): A brief 1/2 sentence of the writing style and techniques employed by the author.
            characters_and_relationships (list[dict[str, str]]): A list of dictionaries outlining the central characters and their most important relationships using the fields name and relationship.
        """

        result = self.model(
            model_input=prompt + "Lord of the Rings" + epub_content,
            output_type=ContentInformation,
        )

        return ContentInformation.model_validate_json(result)
