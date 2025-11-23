from pathlib import Path
from rich.console import Console

console = Console()

class DocWriter:
    def __init__(self, output_base_path: Path):
        self.output_base_path = output_base_path

    def write_markdown_file(self, file_path: Path, content: str):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            file_path.write_text(content, encoding="utf-8")
            console.log(f"[green]Successfully wrote documentation to {file_path}[/green]")
        except Exception as e:
            console.log(f"[red]Error writing file {file_path}: {e}[/red]")
            raise

    def write_config_file(self, file_path: Path, content: str):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            file_path.write_text(content, encoding="utf-8")
            console.log(f"[green]Successfully wrote configuration to {file_path}[/green]")
        except Exception as e:
            console.log(f"[red]Error writing config file {file_path}: {e}[/red]")
            raise

    def copy_template_file(self, source_path: Path, destination_path: Path):
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Ensure source_path exists and is a file
            if not source_path.is_file():
                raise FileNotFoundError(f"Template file not found: {source_path}")

            # If the destination exists and is a directory, copy into it
            if destination_path.exists() and destination_path.is_dir():
                final_destination = destination_path / source_path.name
            else:
                final_destination = destination_path

            # Copy the file, preserving metadata
            final_destination.write_bytes(source_path.read_bytes())
            console.log(f"[green]Successfully copied template from {source_path} to {final_destination}[/green]")
        except Exception as e:
            console.log(f"[red]Error copying template file from {source_path} to {destination_path}: {e}[/red]")
            raise
