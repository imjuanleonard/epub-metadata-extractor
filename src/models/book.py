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