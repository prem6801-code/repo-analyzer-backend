from git import Repo
from pathlib import Path
from app.models.models import Repository
from app.models.models import Chunk
from app.models.models import SourceFile
from tree_sitter import Parser
from tree_sitter_language_pack import get_language
# from app.utils import LANGUAGE_CONFIG

# from tree_sitter_language_pack import get_parser

LANGUAGE_CONFIG = {
    "js": {
        "chunk_types": {
            "class_declaration",
            "function_declaration",
            "method_definition",
            "lexical_declaration",
            "variable_declaration",
        }
    },
    "jsx": {
        "chunk_types": {
            "class_declaration",
            "function_declaration",
            "method_definition",
            "lexical_declaration",
            "variable_declaration",
        }
    },
    "ts": {
        "chunk_types": {
            "class_declaration",
            "function_declaration",
            "method_definition",
            "interface_declaration",
            "enum_declaration",
            "type_alias_declaration",
            "lexical_declaration",
            "variable_declaration",
        }
    },
    "tsx": {
        "chunk_types": {
            "class_declaration",
            "function_declaration",
            "method_definition",
            "interface_declaration",
            "enum_declaration",
            "type_alias_declaration",
            "lexical_declaration",
            "variable_declaration",
        }
    },
    "py": {
        "chunk_types": {
            "class_definition",
            "function_definition",
        }
    }
}


# service function to clone a repository from GitHub
def clone_repository(repo_url,name):
        repo = Repo.clone_from(repo_url, f"./repos/{name}")
        print(repo)
        print("Repository cloned successfully.", repo)
        return f"./repos/{name}"


# service function to get the list of files in a repository
IGNORE_DIRS = {"node_modules",".git","dist","build","coverage","__pycache__",".venv","venv",".idea",".vscode","target","out",}

# File extensions to index
SUPPORTED_EXTENSIONS = {".py": "python",".js": "javascript",".jsx": "javascript",".ts": "typescript",".tsx": "typescript",".java": "java",".go": "go",".cpp": "cpp",".cc": "cpp",".c": "c",".h": "c",".hpp": "cpp",".cs": "csharp",".rb": "ruby",".php": "php",".rs": "rust",".swift": "swift",".kt": "kotlin",".md": "markdown",".json": "json",".yaml": "yaml",".yml": "yaml",".toml": "toml",".ini": "ini",".cfg": "ini",".bat": "batch",".sh": "shell",".ps1": "powershell",".r": "r",".pl": "perl",".lua": "lua",".dart": "dart",".erl": "erlang",".ex": "elixir",".exs": "elixir",".clj": "clojure",".cljs": "clojure",".coffee": "coffeescript",".fs": "fsharp",".fsx": "fsharp",".vb": "vbnet"}

def scan_repository(repository_path: str) -> list[SourceFile]:
        repository = Path(repository_path)
        source_files = []
        
        for file in repository.rglob("*"):
            if not file.is_file():
                continue
            # Skip ignored directories
            if any(part in IGNORE_DIRS for part in file.parts):
                continue

            extension = file.suffix.lower()
            if extension not in SUPPORTED_EXTENSIONS:
                continue

            source_files.append(
                SourceFile(
                    path=str(file),
                    language=SUPPORTED_EXTENSIONS[extension],
                )
            )

        return source_files


# service function to get the list of chunks in a file
def print_tree(node, level=0):
    print(" " * level, node.type)
    for child in node.children:
        print_tree(child, level + 2)

def chunk_repository(source_files):
    for source_file in source_files:
        # print(source_file)
        # break
        tree, source_code = create_Ast(source_file)

        if tree is None:
            continue

        chunks = chunk_file_from_ast(
            tree,
            source_code,
            source_file,
            repo_name=source_file.path.split("/")[1]
        )

        print(chunks)
        # break

def create_Ast(source_file):
    print(source_file)
    parser = Parser()
    language = get_language(source_file.language)

    if language is None:
        return None, None

    parser.language = language

    with open(source_file.path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = parser.parse(source_code.encode())

    return tree, source_code

import uuid

def chunk_file_from_ast(tree, source_code, source_file, repo_name):
    config = LANGUAGE_CONFIG.get(source_file.language)

    # Fallback: unsupported language -> whole file is one chunk
    if config is None:
        return [
            Chunk(
                id=str(uuid.uuid4()),
                repo_name=repo_name,
                file_path=source_file.path,
                language=source_file.language,
                type="file",
                content=source_code,
                start_line=1,
                end_line=len(source_code.splitlines()),
            )
        ]

    chunk_types = config["chunk_types"]
    chunks = []

    def dfs(node):
        if node.type in chunk_types:
            chunks.append(
                Chunk(
                    id=str(uuid.uuid4()),
                    repo_name=repo_name,
                    file_path=source_file.path,
                    language=source_file.language,
                    type=node.type,
                    content=source_code[node.start_byte:node.end_byte],
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1,
                )
            )

        for child in node.children:
            dfs(child)

    dfs(tree.root_node)

    return chunks
     


