import outlines
from google import genai
from src.agent.model import ContentInformation


class LibrarianAgent():
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.client = genai.Client()
        self.model = outlines.from_gemini(
            client=self.client,
            model_name=model_name
        )
    
    def __enter__(self):
        return self.client
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        print("Client closed")
    
    def extract_information(self, epub_content: str) -> ContentInformation:

        prompt = """
        You're an expert in literature and literary analysis. Your task is to extract and summarize key information from the provided book content. Please provide the following details in a structured format:
            genre (str): Give only 1 main genre of the book (e.g., science fiction, crime, fantasy, romance)
            themes (list[str]): A list of the main themes being featured in the book.
            setting (dict[str, str]): A dictionary of the time and place that the story takes place in.
            cultural_context (str): A brief description of the relevant cultural context invoked in the story.
            narrative_tone (str): A brief description of the attitude or mood conveyed by the storytelling.
            author_writing_style (str): A brief description of the writing style and techniques employed by the author.
            characters_and_relationships (list[dict[str, str]]): A list of dictionaries outlining the central characters and their most important relationships using the fields name and relationship.
        """

        # Call it to generate text
        result = self.model(prompt + epub_content, ContentInformation)

        return ContentInformation.model_validate_json(result)
