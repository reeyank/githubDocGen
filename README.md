# Documentation Website Generator

This application generates documentation websites from any public GitHub repository URL.

## Features

- **Input:** GitHub repository URL, optional documentation framework (mkdocs, pydoc, sphinx, mkdocs-material), output folder name, and MongoDB Atlas connection details.
- **Process:** Fetches/clones the repository, analyzes the codebase (languages, modules, APIs, etc.), stores/retrieves analysis results from MongoDB Atlas, generates Markdown documentation files, and builds a complete documentation website using the selected framework.
- **Output:** A complete folder containing the generated documentation website, fully buildable with `mkdocs serve` or `sphinx-build -b html source build`.

## Tech Stack

- Python 3.11+
- FastAPI (for API & web UI)
- Jinja2 (for template generation)
- GitPython (clone repos)
- PyGithub (read GitHub repos without cloning)
- MkDocs, MkDocs-Material (default doc framework)
- Sphinx (optional)
- Uvicorn (local dev server)
- Rich (for CLI feedback)
- Pydantic (for structured models)
- PyMongo (for MongoDB Atlas integration)
- Dnspython (for MongoDB Atlas SRV records)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd doc-generator
   ```

2. Install dependencies (make sure to use Python 3.12 or below if encountering issues with pydantic-core):
   ```bash
   python3 -m pip install -e .
   ```

## MongoDB Atlas Setup

This application uses MongoDB Atlas to cache analysis results. You need to provide your MongoDB Atlas connection URI and database name.

You can set these as environment variables:

```bash
export MONGO_URI="mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority"
export MONGO_DB_NAME="doc_generator_db"
```

Or pass them as command-line arguments to the CLI tool.

## Usage

### CLI Tool

```bash
python -m cli.generate <github_repo_url> \
    --framework mkdocs \
    --mongo-uri "mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority" \
    --mongo-db-name "doc_generator_db"
```

Example:

```bash
python -m cli.generate https://github.com/encode/uvicorn \
    --framework mkdocs-material \
    --output-folder-name uvicorn_docs \
    --mongo-uri "$MONGO_URI" \
    --mongo-db-name "$MONGO_DB_NAME"
```

### REST API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Then, send a POST request to `/generate` with a JSON body:

```json
{
  "repo_url": "https://github.com/user/repo",
  "framework": "mkdocs",
  "mongo_uri": "mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority",
  "mongo_db_name": "doc_generator_db"
}
```
