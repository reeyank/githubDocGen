from pathlib import Path
from rich.console import Console

console = Console()

class StructureBuilder:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def create_docs_structure(self, project_name: str, framework: str = "mkdocs") -> Path:
        project_output_path = self.output_dir / project_name
        docs_path = project_output_path / "docs"

        if framework == "mkdocs" or framework == "mkdocs-material":
            docs_path.mkdir(parents=True, exist_ok=True)
            console.log(f"[green]Created MkDocs documentation structure at {docs_path}[/green]")
            return docs_path
        elif framework == "sphinx":
            # Sphinx usually has a 'source' directory within the project folder
            sphinx_source_path = project_output_path / "source"
            sphinx_source_path.mkdir(parents=True, exist_ok=True)
            console.log(f"[green]Created Sphinx documentation structure at {sphinx_source_path}[/green]")
            return sphinx_source_path
        else:
            # For simple static generator, just create a docs folder
            docs_path.mkdir(parents=True, exist_ok=True)
            console.log(f"[green]Created generic documentation structure at {docs_path}[/green]")
            return docs_path

    def get_output_path(self, project_name: str) -> Path:
        return self.output_dir / project_name
