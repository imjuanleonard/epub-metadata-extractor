import csv
from tika import parser
import outlines
from google import genai
from pydantic import BaseModel

class CharacterAndRelationships(BaseModel):
    name: str
    relationship: str

class ThemeSetting(BaseModel):
    time: str
    place: str

class ContentInformation(BaseModel):
    genre: str
    themes: list[str]
    setting: ThemeSetting
    cultural_context: str
    narrative_tone: str
    author_writing_style: str
    characters_and_relationships: list[CharacterAndRelationships]

class BookMetadata(BaseModel):
    title: str
    author: str
    publishing_year: int
    epub_id: str
    genre: str
    themes: list[str]
    setting: ThemeSetting
    cultural_context: str
    narrative_tone: str
    author_writing_style: str
    characters_and_relationships: list[CharacterAndRelationships]


def read_publisher_metadata(file_path: str, separator: str = ',') -> dict:
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=separator)
        
        # Skip header
        next(reader, None)  

        metadata = {}
        
        for rows in reader:
            metadata[rows[0]] = {
                "title": rows[1],
                "author": rows[2],
                "publishing_year": rows[3],
            }
        return metadata


def extract_information(epub_content: str) -> ContentInformation:
    client = genai.Client()
    # Create the model
    model = outlines.from_gemini(
        client=client,
        model_name="gemini-2.5-flash"
    )

    prompt = """
    You're an expert in literature and literary analysis. Your task is to extract and summarize key information from the provided book content. Please provide the following details in a structured format:
        genre (str): The main genre of the book (e.g., science fiction, crime, fantasy, romance)
        themes (list[str]): A list of the main themes being featured in the book.
        setting (dict[str, str]): A dictionary of the time and place that the story takes place in.
        cultural_context (str): A brief description of the relevant cultural context invoked in the story.
        narrative_tone (str): A brief description of the attitude or mood conveyed by the storytelling.
        author_writing_style (str): A brief description of the writing style and techniques employed by the author.
        characters_and_relationships (list[dict[str, str]]): A list of dictionaries outlining the central characters and their most important relationships using the fields name and relationship.
    """

    # Call it to generate text
    result = model(prompt + epub_content, ContentInformation)

    client.close()
    
    return ContentInformation.model_validate_json(result)

if __name__ == "__main__":
    publisher_metadata = read_publisher_metadata(file_path="./dataset/metadata.csv", separator='\t')

    FILE_NAME = "./dataset/pg74.epub"
    epub = parser.from_file(filename=FILE_NAME)
    epub_metadata = epub["metadata"]
    epub_content = epub["content"]

    epub_id = FILE_NAME.split("/")[-1].replace(".epub", "")

    content_information=extract_information(epub_content=epub_content)

    
    
    book_title= publisher_metadata.get(epub_id,{}).get("title", None) or epub_metadata.get("dc:title", None) or "Unknown Title"
    book_author= publisher_metadata.get(epub_id,{}).get("author", None) or epub_metadata.get("dc:creator", None) or "Unknown Author"
    publishing_year= publisher_metadata.get(epub_id,{}).get("publishing_year", None) or epub_metadata.get("dc:date", None) or 0
    response = BookMetadata(
        title=book_title,
        author=book_author,
        publishing_year=publishing_year,
        epub_id=epub_id,
        genre=content_information.genre ,
        themes=content_information.themes,
        setting=content_information.setting,
        cultural_context=content_information.cultural_context,
        narrative_tone=content_information.narrative_tone,
        author_writing_style=content_information.author_writing_style ,
        characters_and_relationships=content_information.characters_and_relationships
    )
    print(response.model_dump_json(indent=4))