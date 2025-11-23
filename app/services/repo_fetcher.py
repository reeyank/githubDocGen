import os
import shutil
from pathlib import Path
import sys

import git
from rich.console import Console

console = Console()

class RepoFetcher:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def clone_repository(self, repo_url: str) -> Path:
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = self.output_dir / repo_name

        if repo_path.exists():
            console.log(f"[yellow]Repository '{repo_name}' already exists. Pulling latest changes.[/yellow]")
            try:
                repo = git.Repo(repo_path)
                repo.remotes.origin.pull()
                console.log(f"[green]Successfully pulled latest changes for '{repo_name}'.[/green]")
            except Exception as e:
                console.log(f"[red]Error pulling changes for '{repo_name}': {e}[/red]")
                raise
        else:
            console.log(f"[cyan]Cloning repository '{repo_url}' to '{repo_path}'...[/cyan]")
            try:
                git.Repo.clone_from(repo_url, repo_path)
                console.log(f"[green]Successfully cloned '{repo_name}'.[/green]")
            except Exception as e:
                console.log(f"[red]Error cloning '{repo_name}': {e}[/red]")
                raise
        return repo_path

    def clean_repository(self, repo_path: Path):
        if repo_path.exists():
            console.log(f"[yellow]Cleaning up repository at '{repo_path}'...[/yellow]")
            shutil.rmtree(repo_path)
            console.log(f"[green]Successfully cleaned up '{repo_path}'.[/green]")

if __name__ == "__main__":
    # Example usage
    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)
    fetcher = RepoFetcher(output_folder)
    
    # Replace with a real GitHub URL for testing
    test_repo_url = "https://github.com/encode/uvicorn.git" 
    
    try:
        cloned_repo_path = fetcher.clone_repository(test_repo_url)
        console.log(f"Cloned repository path: {cloned_repo_path}")
        # fetcher.clean_repository(cloned_repo_path)
    except Exception as e:
        console.log(f"[red]An error occurred: {e}[/red]")
