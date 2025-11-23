from pathlib import Path
from pydantic import BaseModel, Field
from rich.console import Console
from fastapi import HTTPException
from sentence_transformers import SentenceTransformer

from app.services.repo_fetcher import RepoFetcher
from app.services.structure_builder import StructureBuilder
from app.analyzers.general_scanner import GeneralScanner
from app.analyzers.python_analyzer import PythonAnalyzer
# from app.analyzers.js_analyzer import JSAnalyzer # Temporarily disabled
from app.generators.mkdocs_generator import MkDocsGenerator
from app.generators.sphinx_generator import SphinxGenerator
from app.services.database_service import MongoDBService

console = Console()

class GenerateRequest(BaseModel):
    repo_url: str
    framework: str = "mkdocs"
    output_folder_name: str | None = None
    mongo_uri: str = Field(..., description="MongoDB Atlas connection URI")
    mongo_db_name: str = Field(..., description="MongoDB database name")

async def generate_documentation(request: GenerateRequest, output_base_dir: Path):
    repo_url = request.repo_url
    framework = request.framework
    output_folder_name = request.output_folder_name
    mongo_uri = request.mongo_uri
    mongo_db_name = request.mongo_db_name

    project_name = repo_url.split('/')[-1].replace('.git', '')
    if output_folder_name:
        project_name = output_folder_name

    output_project_dir = output_base_dir / project_name
    output_docs_site_dir = output_project_dir / "docs_site"

    # Initialize the embedding model globally
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    console.log(f"[bold magenta]Starting documentation generation for {repo_url} with {framework} framework.[/bold magenta]")

    db_service = MongoDBService(mongo_uri, mongo_db_name)
    if not db_service.connect():
        raise HTTPException(status_code=500, detail="Failed to connect to MongoDB Atlas.")

    analysis_collection = db_service.get_collection("analysis_results")
    cached_analysis = analysis_collection.find_one({"repo_url": repo_url})

    full_analysis_results = {}
    if cached_analysis:
        console.log("[yellow]Using cached analysis results from MongoDB Atlas.[/yellow]")
        full_analysis_results = cached_analysis["analysis_data"]
        # Ensure repo_url is present in the results even if loaded from cache
        full_analysis_results["repo_url"] = repo_url
        cloned_repo_path = output_project_dir / "cloned_repo"
        if not cloned_repo_path.exists(): # If repo was cleaned up, re-clone for generation
            fetcher = RepoFetcher(output_project_dir.parent)
            cloned_repo_path = fetcher.clone_repository(repo_url)
    else:
        # 1. Fetch / Clone the GitHub repository
        fetcher = RepoFetcher(output_project_dir.parent) # Output to parent of project dir, so project dir is created inside output
        cloned_repo_path = fetcher.clone_repository(repo_url)

        # 2. Analyze the codebase
        console.log("[bold]Analyzing codebase...[/bold]")
        general_scanner = GeneralScanner(cloned_repo_path)
        general_analysis = general_scanner.scan_repository()

        python_analyzer = PythonAnalyzer(cloned_repo_path)
        python_analysis = python_analyzer.analyze()

        # js_analyzer = JSAnalyzer(cloned_repo_path)
        # js_analysis = js_analyzer.analyze()
        js_analysis = {} # Temporarily empty

        full_analysis_results = {
            "repo_url": repo_url,
            "general": general_analysis,
            "python": python_analysis,
            "js": js_analysis,
        }

        # Generate embedding for the full analysis results
        analysis_text = str(full_analysis_results) # Convert dict to string for embedding
        embedding = embedding_model.encode(analysis_text).tolist()

        analysis_collection.insert_one({"repo_url": repo_url, "analysis_data": full_analysis_results, "embedding": embedding})
        console.log("[green]Analysis results and embeddings saved to MongoDB Atlas.[/green]")

    # 3. Generate documentation files and build website
    structure_builder = StructureBuilder(output_project_dir.parent)
    docs_output_path = structure_builder.create_docs_structure(project_name, framework)

    if framework == "mkdocs" or framework == "mkdocs-material":
        generator = MkDocsGenerator(output_docs_site_dir, project_name, full_analysis_results)
        generator.generate()
        # After generation, cleanup the cloned repo
        fetcher.clean_repository(cloned_repo_path)
        db_service.disconnect()
        return {"message": "Documentation generated successfully!", "output_path": str(output_docs_site_dir), "command_to_run": f"cd {output_docs_site_dir} && mkdocs serve"}
    elif framework == "sphinx":
        generator = SphinxGenerator(output_docs_site_dir, project_name, full_analysis_results)
        generator.generate()
        # After generation, cleanup the cloned repo
        fetcher.clean_repository(cloned_repo_path)
        db_service.disconnect()
        return {"message": "Sphinx documentation generated successfully! (Basic structure)", "output_path": str(output_docs_site_dir), "command_to_run": f"cd {output_docs_site_dir} && sphinx-build -b html source build"}
    else:
        # Simple static generator (for now, MkDocs is the default if not specified)
        generator = MkDocsGenerator(output_docs_site_dir, project_name, full_analysis_results)
        generator.generate()
        # After generation, cleanup the cloned repo
        fetcher.clean_repository(cloned_repo_path)
        db_service.disconnect()
        return {"message": "Documentation generated successfully using default MkDocs!", "output_path": str(output_docs_site_dir), "command_to_run": f"cd {output_docs_site_dir} && mkdocs serve"}
