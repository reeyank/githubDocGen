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

        console.log(f"[green]Repository scan complete.[/green]")
        return {
            "file_list": [str(p.relative_to(self.repo_path)) for p in self.file_list],
            "structure": self.structure,
            "languages": list(self.languages)
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

if __name__ == "__main__":
    # Example Usage
    # Assuming a cloned repo exists in the 'output' directory
    test_repo_name = "uvicorn"
    test_repo_path = Path("output") / test_repo_name

    if test_repo_path.exists():
        scanner = GeneralScanner(test_repo_path)
        analysis_results = scanner.scan_repository()
        console.log("[bold]Analysis Results:[/bold]")
        console.log(analysis_results)
    else:
        console.log(f"[red]Test repository not found at {test_repo_path}. Please clone a repository first.[/red]")
