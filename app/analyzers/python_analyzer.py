import ast
from pathlib import Path
from rich.console import Console

console = Console()

class CallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = set()

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            # e.g., obj.method() or module.function()
            if isinstance(node.func.attr, str):
                self.calls.add(node.func.attr)
            elif isinstance(node.func.value, ast.Name):
                self.calls.add(f"{node.func.value.id}.{node.func.attr}")
        self.generic_visit(node)

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
                "docstrings": "",
                "api_endpoints": []
            }
            try:
                content = file_path.read_text(encoding="utf-8")
                tree = ast.parse(content)
                # Pre-process AST to add parent references
                for node in ast.walk(tree):
                    for child in ast.iter_child_nodes(node):
                        child.parent = node
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
                    "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
                    "docstring": ast.get_docstring(node) or ""
                }
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        call_visitor = CallVisitor()
                        call_visitor.visit(item)
                        class_info["methods"].append({
                            "name": item.name,
                            "args": [arg.arg for arg in item.args.args],
                            "docstring": ast.get_docstring(item) or "",
                            "calls": list(call_visitor.calls),
                            "is_api_endpoint": self._is_api_endpoint(item)
                        })
                current_module["classes"].append(class_info)
            elif isinstance(node, ast.FunctionDef):
                # Only add top-level functions, not methods within classes
                if not isinstance(getattr(node, 'parent', None), ast.ClassDef):
                    call_visitor = CallVisitor()
                    call_visitor.visit(node)
                    current_module["functions"].append({
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node) or "",
                        "calls": list(call_visitor.calls),
                        "is_api_endpoint": self._is_api_endpoint(node)
                    })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    if isinstance(node, ast.Import):
                        current_module["imports"].append(alias.name)
                    else:
                        module = node.module if node.module else '.'
                        current_module["imports"].append(f"{module}.{alias.name}")

            # Detect API Endpoints
            if self._is_api_endpoint(node):
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    # Extract HTTP method and path from decorators if possible
                    api_info = {"name": node.name, "method": "", "path": ""}
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                            if decorator.func.value.id in ["app", "router", "bp"] and decorator.func.attr in ["get", "post", "put", "delete", "patch"]:
                                api_info["method"] = decorator.func.attr.upper()
                                if decorator.args and isinstance(decorator.args[0], ast.Constant):
                                    api_info["path"] = decorator.args[0].value
                                break
                        elif isinstance(decorator, ast.Name) and decorator.id in ["api_view", "route"]:
                            api_info["method"] = "ANY" # Generic for Django/Flask
                            # Path extraction for Flask/Django would be more complex, often requires parsing decorator args
                            
                    current_module["api_endpoints"].append(api_info)

    def _is_api_endpoint(self, node) -> bool:
        # Detect FastAPI/Flask/Django API endpoints based on decorators
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return False
        
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                # FastAPI/Flask routes: @app.get('/'), @router.post('/'), @bp.route('/')
                if isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr in ["get", "post", "put", "delete", "patch", "route"]:
                        if isinstance(decorator.func.value, ast.Name):
                            # Simple check for common FastAPI/Flask app/router/blueprint names
                            if decorator.func.value.id in ["app", "router", "bp"]:
                                return True
                # Django REST framework: @api_view(['GET'])
                elif isinstance(decorator.func, ast.Name) and decorator.func.id == "api_view":
                    return True
            elif isinstance(decorator, ast.Name) and decorator.id == "app": # Simple case for @app decorators
                return True
        return False

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
