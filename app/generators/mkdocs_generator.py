from pathlib import Path
from rich.console import Console
from jinja2 import Environment, FileSystemLoader

console = Console()

class MkDocsGenerator:
    def __init__(self, output_path: Path, project_name: str, analysis_results: dict):
        self.output_path = output_path
        self.project_name = project_name
        self.docs_dir = output_path / "docs"
        self.analysis_results = analysis_results
        self.env = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"))

    def generate(self):
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self._create_mkdocs_yml()
        self._create_index_md()
        self._create_getting_started_md()
        self._create_installation_md()
        self._create_architecture_md()
        self._create_api_md()
        self._create_modules_md()
        console.log(f"[green]MkDocs documentation generated in {self.output_path}[/green]")

    def _create_mkdocs_yml(self):
        template = self.env.get_template("mkdocs.yml.j2")
        mkdocs_config = {
            "site_name": f"{self.project_name} Documentation",
            "site_description": f"Documentation for the {self.project_name} project.",
            "repo_url": self.analysis_results.get("repo_url", ""),
            "theme": {
                "name": "material"
            },
            "nav": [
                {"Home": "index.md"},
                {"Getting Started": "getting-started.md"},
                {"Installation": "installation.md"},
                {"Architecture": "architecture.md"},
                {"API Reference": "api/index.md"},
                {"Modules": "modules/index.md"}
            ]
        }
        content = template.render(mkdocs_config)
        (self.output_path / "mkdocs.yml").write_text(content)
        console.log("[green]mkdocs.yml created.[/green]")

    def _create_index_md(self):
        template = self.env.get_template("index.md.j2")
        content = template.render({"project_name": self.project_name})
        (self.docs_dir / "index.md").write_text(content)
        console.log("[green]index.md created.[/green]")

    def _create_getting_started_md(self):
        template = self.env.get_template("getting-started.md.j2")
        content = template.render()
        (self.docs_dir / "getting-started.md").write_text(content)
        console.log("[green]getting-started.md created.[/green]")

    def _create_installation_md(self):
        template = self.env.get_template("installation.md.j2")
        content = template.render()
        (self.docs_dir / "installation.md").write_text(content)
        console.log("[green]installation.md created.[/green]")

    def _create_architecture_md(self):
        template = self.env.get_template("architecture.md.j2")
        # Placeholder for actual architecture content based on analysis_results
        content = template.render({
            "general_analysis": self.analysis_results.get("general", {}),
            "python_analysis": self.analysis_results.get("python", {})
        })
        (self.docs_dir / "architecture.md").write_text(content)
        console.log("[green]architecture.md created.[/green]")

    def _create_api_md(self):
        api_dir = self.docs_dir / "api"
        api_dir.mkdir(exist_ok=True)

        # Create an index for API documentation
        index_content = "# API Reference\n\n"
        python_analysis = self.analysis_results.get("python", {})
        for file, data in python_analysis.items():
            if data["functions"] or data["classes"]:
                file_name = Path(file).stem
                index_content += f"- [{file_name.replace('_', ' ').title()}](/{api_dir.name}/{file_name}.md)\n"
                self._create_python_api_page(api_dir, file, data)

        (api_dir / "index.md").write_text(index_content)
        console.log("[green]API index.md created and Python API pages generated.[/green]")

    def _create_python_api_page(self, api_dir: Path, file_path: str, data: dict):
        template = self.env.get_template("python_api_page.md.j2")
        file_name = Path(file_path).stem
        content = template.render({"file_path": file_path, "data": data})
        (api_dir / f"{file_name}.md").write_text(content)

    def _create_modules_md(self):
        modules_dir = self.docs_dir / "modules"
        modules_dir.mkdir(exist_ok=True)

        index_content = "# Modules\n\n"
        general_analysis = self.analysis_results.get("general", {})
        if "structure" in general_analysis:
            for folder, folder_data in general_analysis["structure"].items():
                if folder_data["files"] or folder_data["dirs"]:
                    folder_name = folder.replace("/", "_")
                    index_content += f"- [{folder.replace('/', ' ').title()}](/{modules_dir.name}/{folder_name}.md)\n"
                    self._create_module_page(modules_dir, folder, folder_data)

        (modules_dir / "index.md").write_text(index_content)
        console.log("[green]Modules index.md created and module pages generated.[/green]")

    def _create_module_page(self, modules_dir: Path, folder_path: str, data: dict):
        template = self.env.get_template("module_page.md.j2")
        folder_name = folder_path.replace("/", "_")
        content = template.render({"folder_path": folder_path, "data": data})
        (modules_dir / f"{folder_name}.md").write_text(content)


if __name__ == "__main__":
    # Example Usage
    output_folder = Path("output")
    project_name = "uvicorn"
    output_path = output_folder / project_name / "docs_site"
    
    # Dummy analysis results for testing
    dummy_analysis = {
        "repo_url": "https://github.com/encode/uvicorn.git",
        "general": {
            "languages": ["python", "markdown"],
            "structure": {
                ".": {"files": ["README.md", "main.py"], "dirs": ["app"]},
                "app": {"files": ["__init__.py"], "dirs": []}
            }
        },
        "python": {
            "app/main.py": {
                "classes": [{'name': 'App', 'methods': [{'name': '__init__', 'args': ['self']}]}],
                "functions": [{'name': 'run', 'args': ['config']}],
                "imports": ['fastapi'],
                "docstrings": "Main application file."
            }
        }
    }

    generator = MkDocsGenerator(output_path, project_name, dummy_analysis)
    generator.generate()
    console.log(f"To view the generated docs, run: cd {output_path} && mkdocs serve")
