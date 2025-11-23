from pathlib import Path
from rich.console import Console
from tree_sitter import Language, Parser
import tree_sitter_languages

console = Console()

class JSAnalyzer:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.analysis_results = {}
        self.parser = Parser()

        try:
            JS_LANGUAGE = tree_sitter_languages.get_language('javascript')
            self.parser.set_language(JS_LANGUAGE)
            console.log("[green]Tree-sitter JavaScript language loaded.[/green]")
        except Exception as e:
            console.log(f"[red]Error loading tree-sitter JavaScript language: {e}. JS/TS analysis will be skipped.[/red]")
            self.parser = None

    def analyze(self):
        if not self.parser:
            console.log("[yellow]Skipping JS/TS analysis due to parser initialization error.[/yellow]")
            return {}

        console.log(f"[cyan]Starting JS/TS code analysis in {self.repo_path}...[/cyan]")
        js_ts_files = list(self.repo_path.glob('**/*.js')) + list(self.repo_path.glob('**/*.ts')) + \
                      list(self.repo_path.glob('**/*.jsx')) + list(self.repo_path.glob('**/*.tsx'))

        for file_path in js_ts_files:
            if 'node_modules' in str(file_path):
                continue

            relative_path = file_path.relative_to(self.repo_path)
            self.analysis_results[str(relative_path)] = {
                "functions": [],
                "classes": [],
                "imports": [],
                "exports": []
            }
            try:
                content = file_path.read_bytes()
                tree = self.parser.parse(content)
                self._parse_tree(tree.root_node, str(relative_path))
            except Exception as e:
                console.log(f"[red]Error analyzing {relative_path}: {e}[/red]")
        console.log(f"[green]JS/TS code analysis complete.[/green]")
        return self.analysis_results

    def _parse_tree(self, node, relative_path: str):
        current_module = self.analysis_results[relative_path]

        if node.type == 'function_declaration':
            function_name = None
            for child in node.children:
                if child.type == 'identifier':
                    function_name = child.text.decode('utf-8')
                    break
            if function_name:
                current_module["functions"].append({"name": function_name, "type": "function"})
        elif node.type == 'class_declaration':
            class_name = None
            for child in node.children:
                if child.type == 'identifier':
                    class_name = child.text.decode('utf-8')
                    break
            if class_name:
                current_module["classes"].append({"name": class_name, "type": "class"})
        elif node.type == 'import_statement':
            import_text = node.text.decode('utf-8')
            current_module["imports"].append(import_text)
        elif node.type == 'export_statement':
            export_text = node.text.decode('utf-8')
            current_module["exports"].append(export_text)

        for child in node.children:
            self._parse_tree(child, relative_path)

if __name__ == "__main__":
    # Example Usage
    test_repo_name = "example-js-repo" # Replace with a real JS/TS repo for testing
    test_repo_path = Path("output") / test_repo_name

    # Create a dummy JS file for testing if the repo doesn't exist
    if not test_repo_path.exists():
        test_repo_path.mkdir(parents=True, exist_ok=True)
        (test_repo_path / "test.js").write_text("function hello() { console.log('Hello'); } export default hello;")

    if test_repo_path.exists():
        analyzer = JSAnalyzer(test_repo_path)
        analysis_results = analyzer.analyze()
        console.log("[bold]JS/TS Analysis Results:[/bold]")
        import json
        console.log(json.dumps(analysis_results, indent=2))
    else:
        console.log(f"[red]Test repository not found at {test_repo_path}. Please clone a repository first.[/red]")
