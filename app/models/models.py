from pydantic import BaseModel

class Chunk(BaseModel):
    id: str
    repo_name: str
    file_path: str
    language: str
    chunk_index: int
    content: str

class Repository(BaseModel):
    repo_name: str
    repo_path: str

class SourceFile(BaseModel):
    path: str
    language: str