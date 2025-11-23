import os
from pathlib import Path
from rich.console import Console

console = Console()

class GeneralScanner:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.file_list = []
        self.structure = {}
        self.languages = set()
        self.package_managers = []
        self.api_frameworks = []
        self.config_files = []

    def scan_repository(self):
        console.log(f"[cyan]Scanning repository at {self.repo_path}...[/cyan]")
        for root, dirs, files in os.walk(self.repo_path):
            # Exclude common ignored directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv', '.vscode', '.idea']]

            relative_root = Path(root).relative_to(self.repo_path)
            self.structure.setdefault(str(relative_root), {"files": [], "dirs": []})

            for d in dirs:
                self.structure[str(relative_root)]["dirs"].append(d)

            for f in files:
                file_path = Path(root) / f
                self.file_list.append(file_path)
                self.structure[str(relative_root)]["files"].append(f)
                self._detect_language(f)
                self._detect_package_manager_and_api(f, file_path)

        console.log(f"[green]Repository scan complete.[/green]")
        return {
            "file_list": [str(p.relative_to(self.repo_path)) for p in self.file_list],
            "structure": self.structure,
            "languages": list(self.languages),
            "package_managers": list(set(self.package_managers)),
            "api_frameworks": list(set(self.api_frameworks)),
            "config_files": list(set(self.config_files))
        }

    def _detect_language(self, filename: str):
        extension = filename.split('.')[-1]
        if extension in ['py', 'pyw']:
            self.languages.add('python')
        elif extension in ['js', 'jsx']:
            self.languages.add('javascript')
        elif extension in ['ts', 'tsx']:
            self.languages.add('typescript')
        elif extension in ['md', 'markdown']:
            self.languages.add('markdown')
        elif extension in ['json']:
            self.languages.add('json')
        elif extension in ['yml', 'yaml']:
            self.languages.add('yaml')
        elif extension in ['html', 'htm']:
            self.languages.add('html')
        elif extension in ['css', 'scss', 'less']:
            self.languages.add('css')
        elif extension in ['java']:
            self.languages.add('java')
        elif extension in ['c', 'cpp', 'h']:
            self.languages.add('c/c++')
        elif extension in ['go']:
            self.languages.add('go')
        elif extension in ['rs']:
            self.languages.add('rust')
        # Add more language detections as needed

    def _detect_package_manager_and_api(self, filename: str, file_path: Path):
        # Package Managers
        if filename == "requirements.txt":
            self.package_managers.append("pip")
        elif filename == "package.json":
            self.package_managers.append("npm/yarn")
        elif filename == "pyproject.toml":
            self.package_managers.append("poetry/pip")
            self.config_files.append(filename)
        elif filename == "setup.py":
            self.package_managers.append("setuptools")
        elif filename == "Cargo.toml":
            self.package_managers.append("cargo")

        # API Frameworks (basic detection for Python files)
        if file_path.suffix == '.py':
            try:
                content = file_path.read_text(encoding="utf-8")
                if "FastAPI" in content:
                    self.api_frameworks.append("FastAPI")
                if "Flask" in content:
                    self.api_frameworks.append("Flask")
                if "Django" in content:
                    self.api_frameworks.append("Django")
            except Exception as e:
                console.log(f"[yellow]Could not read {file_path} for API detection: {e}[/yellow]")

        # Config files
        if filename in ["Dockerfile", "docker-compose.yml", ".env", "config.py", "appsettings.json"]:
            self.config_files.append(filename)

if __name__ == "__main__":
    # Example Usage
    # Assuming a cloned repo exists in the 'output' directory
    test_repo_name = "uvicorn"
    test_repo_path = Path("output") / test_repo_name

    if test_repo_path.exists():
        scanner = GeneralScanner(test_repo_path)
        analysis_results = scanner.scan_repository()
        console.log("[bold]Analysis Results:[/bold]")
        import json
        console.log(json.dumps(analysis_results, indent=2))
    else:
        console.log(f"[red]Test repository not found at {test_repo_path}. Please clone a repository first.[/red]")
