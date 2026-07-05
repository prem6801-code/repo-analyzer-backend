from git import Repo
from pathlib import Path
from app.models.models import Repository
from app.models.models import Chunk
from app.models.models import SourceFile
from tree_sitter import Parser
from tree_sitter_language_pack import get_language
# from tree_sitter_language_pack import get_parser


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
            chunks = chunk_file(source_file)
            break

def chunk_file(source_file):
    parser = Parser()
    language = get_language(source_file.language)
    if language is None:
        print(f"Language {source_file.language} not supported.")
        return []

    parser.language = language  
    path = Path(source_file.path)
    with path.open("r", encoding="utf-8") as f:
        source_code = f.read()

    tree = parser.parse(source_code.encode("utf-8"))
    print(f"Parsed {source_file.path}")
    print_tree(tree.root_node)
    return tree

