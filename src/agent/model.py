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
