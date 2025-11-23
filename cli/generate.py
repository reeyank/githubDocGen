import argparse
from pathlib import Path
import asyncio
from rich.console import Console
from rich.table import Table
import os

from app.api.generate import generate_documentation, GenerateRequest

console = Console()

async def main():
    parser = argparse.ArgumentParser(
        description="Generate documentation websites from a GitHub repository."
    )
    parser.add_argument(
        "repo_url",
        type=str,
        help="The URL of the GitHub repository (e.g., https://github.com/user/repo)"
    )
    parser.add_argument(
        "--framework",
        type=str,
        default="mkdocs",
        choices=["mkdocs", "mkdocs-material", "sphinx"],
        help="The documentation framework to use (default: mkdocs)"
    )
    parser.add_argument(
        "--output-folder-name",
        type=str,
        help="Optional: Name of the output folder for the generated documentation (defaults to repo name)"
    )
    parser.add_argument(
        "--mongo-uri",
        type=str,
        default=os.environ.get("MONGO_URI"),
        help="MongoDB Atlas connection URI (can be set via MONGO_URI environment variable)"
    )
    parser.add_argument(
        "--mongo-db-name",
        type=str,
        default=os.environ.get("MONGO_DB_NAME"),
        help="MongoDB database name (can be set via MONGO_DB_NAME environment variable)"
    )

    args = parser.parse_args()

    if not args.mongo_uri or not args.mongo_db_name:
        console.log("[bold red]Error: MongoDB URI and database name are required. Please provide them via arguments or environment variables.[/bold red]")
        exit(1)

    output_base_dir = Path("output")
    output_base_dir.mkdir(exist_ok=True)

    request = GenerateRequest(
        repo_url=args.repo_url,
        framework=args.framework,
        output_folder_name=args.output_folder_name,
        mongo_uri=args.mongo_uri,
        mongo_db_name=args.mongo_db_name
    )

    console.log("[bold green]Starting documentation generation via CLI...[/bold green]")
    try:
        result = await generate_documentation(request, output_base_dir)
        console.log("[bold green]Documentation generation complete![/bold green]")

        table = Table(title="Generation Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        for key, value in result.items():
            table.add_row(key, str(value))
        
        console.print(table)
        console.log(f"[bold]To view your documentation, run:[/bold] [yellow]{result.get("command_to_run")}[/yellow]")

    except Exception as e:
        console.log(f"[bold red]Error during documentation generation: {e}[/bold red]")
        import traceback
        console.print(traceback.format_exc(), style="red")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
