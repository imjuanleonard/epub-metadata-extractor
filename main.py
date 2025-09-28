import csv
from tika import parser
from nextory.model import BookMetadata

# Set the metadata and create the first few jsons
# Title
# Author
# Publishing Year
# Epub ID

# Use The Ollama Model To Generate 
#● genre (str): The main genre of the book (e.g., science fiction, crime, fantasy, romance)
#● themes (list[str]): A list of the main themes being featured in the book.
#● setting (dict[str, str]): A dictionary of the time and place that the story takes place in.
#● cultural_context (str): A brief description of the relevant cultural context invoked in the story.
#● narrative_tone (str): A brief description of the attitude or mood conveyed by the storytelling.
#● author_writing_style (str): A brief description of the writing style and techniques employed by the author.
#● characters_and_relationships (list[dict[str, str]]): A list of dictionaries outlining the central characters and their most important relationships using the fields name and relationship.



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
    




if __name__ == "__main__":
    publisher_metadata = read_publisher_metadata(file_path="./dataset/metadata.csv", separator='\t')

    FILE_NAME = "./dataset/pg74.epub"
    epub = parser.from_file(filename=FILE_NAME)
    epub_metadata = epub["metadata"]
    epub_content = epub["content"]

    epub_id = FILE_NAME.split("/")[-1].replace(".epub", "")
    
    
    book_title= publisher_metadata.get(epub_id,{})["title"] or epub_metadata.get("dc:title", None) or "Unknown Title"
    book_author= publisher_metadata.get(epub_id,{})["author"] or epub_metadata.get("dc:creator", None) or "Unknown Author"
    publishing_year= publisher_metadata.get(epub_id,{})["publishing_year"] or epub_metadata.get("dc:date", None) or 0
    response = BookMetadata(
        title=book_title,
        author=book_author,
        publishing_year=publishing_year,
        epub_id=epub_id,
        genre="Science Fiction",
        themes=["Technology", "Future", "Society"],
        setting={"time": "21st Century", "place": "Earth"},
        cultural_context="A futuristic society grappling with advanced technology and its implications.",
        narrative_tone="A mix of suspenseful and contemplative, exploring deep philosophical questions.",
        author_writing_style="Descriptive and immersive, with a focus on world-building and character development.",
        characters_and_relationships=[
            {"name": "John Doe", "relationship": "Protagonist"},
            {"name": "Jane Smith", "relationship": "Antagonist"}
        ]
    )
    print(response.model_dump_json(indent=4))