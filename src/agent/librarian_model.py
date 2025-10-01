from pydantic import BaseModel, Field


class CharacterAndRelationships(BaseModel):
    name: str
    relationship: str


class ThemeSetting(BaseModel):
    time: str
    place: str


class ContentInformation(BaseModel):
    genre: str
    themes: list[str] = Field(min_length=3, max_length=10)
    setting: ThemeSetting
    cultural_context: str
    narrative_tone: str
    author_writing_style: str
    characters_and_relationships: list[CharacterAndRelationships] = Field(min_length=3, max_length=10)


class BookMetadata(BaseModel):
    title: str
    author: str
    publishing_year: int
    epub_id: str
    genre: str
    themes: list[str] = Field(min_length=3, max_length=10)
    setting: ThemeSetting
    cultural_context: str
    narrative_tone: str
    author_writing_style: str
    characters_and_relationships: list[CharacterAndRelationships] = Field(min_length=3, max_length=10)
