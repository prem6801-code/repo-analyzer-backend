from pydantic import BaseModel

class Chunk(BaseModel):
    id: str
    repo_name: str
    file_path: str
    language: str
    content: str
    start_line: int
    end_line: int

class Repository(BaseModel):
    repo_name: str
    repo_path: str

class SourceFile(BaseModel):
    path: str
    language: str