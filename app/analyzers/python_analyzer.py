import ast
from pathlib import Path
from rich.console import Console

console = Console()

class PythonAnalyzer:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.analysis_results = {}

    def analyze(self):
        console.log(f"[cyan]Starting Python code analysis in {self.repo_path}...[/cyan]")
        python_files = list(self.repo_path.glob('**/*.py'))

        for file_path in python_files:
            if '.venv' in str(file_path) or 'site-packages' in str(file_path):
                continue

            relative_path = file_path.relative_to(self.repo_path)
            self.analysis_results[str(relative_path)] = {
                "classes": [],
                "functions": [],
                "imports": [],
                "docstrings": ""
            }
            try:
                content = file_path.read_text(encoding="utf-8")
                tree = ast.parse(content)
                self._parse_ast(tree, str(relative_path))
            except SyntaxError as e:
                console.log(f"[red]Syntax error in {relative_path}: {e}[/red]")
            except Exception as e:
                console.log(f"[red]Error analyzing {relative_path}: {e}[/red]")
        console.log(f"[green]Python code analysis complete.[/green]")
        return self.analysis_results

    def _parse_ast(self, tree, relative_path: str):
        current_module = self.analysis_results[relative_path]

        # Extract module-level docstring
        current_module["docstrings"] = ast.get_docstring(tree) or ""

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "methods": [],
                    "docstring": ast.get_docstring(node) or ""
                }
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_info["methods"].append({
                            "name": item.name,
                            "args": [arg.arg for arg in item.args.args],
                            "docstring": ast.get_docstring(item) or ""
                        })
                current_module["classes"].append(class_info)
            elif isinstance(node, ast.FunctionDef):
                # Only add top-level functions, not methods within classes
                if not isinstance(getattr(node, 'parent', None), ast.ClassDef):
                    current_module["functions"].append({
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node) or ""
                    })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    if isinstance(node, ast.Import):
                        current_module["imports"].append(alias.name)
                    else:
                        module = node.module if node.module else '.'
                        current_module["imports"].append(f"{module}.{alias.name}")

    # Helper to set parent for easy navigation (AST nodes don't have parents by default)
    @staticmethod
    def _add_parent_info(node):
        for child in ast.iter_child_nodes(node):
            child.parent = node
            PythonAnalyzer._add_parent_info(child)

if __name__ == "__main__":
    # Example Usage
    test_repo_name = "uvicorn"
    test_repo_path = Path("output") / test_repo_name

    if test_repo_path.exists():
        analyzer = PythonAnalyzer(test_repo_path)
        analysis_results = analyzer.analyze()
        console.log("[bold]Python Analysis Results:[/bold]")
        import json
        console.log(json.dumps(analysis_results, indent=2))
    else:
        console.log(f"[red]Test repository not found at {test_repo_path}. Please clone a repository first.[/red]")
