"""
Command-line interface for project-to-epub.
"""

import logging
import os
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from project_to_epub import __version__
from project_to_epub.converter import convert_project_to_epub

# Default configuration
DEFAULT_CONFIG = {
    "output_directory": ".",
    "default_theme": "default_eink",
    "large_file_threshold_mb": 10,
    "skip_large_files": True,
    "log_level": "INFO",
    "epub_metadata": {
        "author": "Project-to-EPUB Tool",
        "language": "en",
        "publisher": "Project-to-EPUB v1.0",
    },
}

app = typer.Typer(
    help="Convert a software project directory into an EPUB file for offline code reading."
)


def version_callback(value: bool):
    """Print the version and exit."""
    if value:
        typer.echo(f"project-to-epub version: {__version__}")
        raise typer.Exit()


@app.command()
def main(
    input_directory: Annotated[
        Optional[Path], typer.Argument(help="Path to the project directory to convert")
    ] = None,
    output: Annotated[
        Optional[Path], typer.Option("-o", "--output", help="Output EPUB file path")
    ] = None,
    theme: Annotated[
        Optional[str],
        typer.Option(help="Syntax highlighting theme (e.g., default_eink, monokai)"),
    ] = None,
    log_level: Annotated[
        str, typer.Option(help="Log level (DEBUG, INFO, WARNING, ERROR)")
    ] = "INFO",
    title: Annotated[
        Optional[str],
        typer.Option(help="Set EPUB title (defaults to project directory name)"),
    ] = None,
    author: Annotated[Optional[str], typer.Option(help="Set EPUB author")] = None,
    limit_mb: Annotated[
        Optional[float], typer.Option(help="Set large file threshold in MB")
    ] = None,
    no_skip_large: Annotated[
        bool, typer.Option(help="Error out on large files instead of skipping")
    ] = False,
    hierarchical_toc: Annotated[
        bool, typer.Option(help="Use hierarchical TOC instead of flat TOC")
    ] = False,
    version: Annotated[
        bool,
        typer.Option(
            "--version", callback=version_callback, help="Show version and exit"
        ),
    ] = False,
):
    """
    Convert a software project directory into an EPUB file for offline code reading.

    This tool creates an EPUB that preserves your project structure in the table of contents,
    applies syntax highlighting to code files, and respects .gitignore rules.
    """
    # Setup logging
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        typer.echo(f"Invalid log level: {log_level}", err=True)
        raise typer.Exit(code=1)
    logging.basicConfig(level=numeric_level, format="%(levelname)s: %(message)s")

    # Handle input directory
    if input_directory is None:
        input_directory = Path.cwd()
        logging.info(
            f"No input directory specified, using current directory: {input_directory}"
        )

    # Resolve to absolute path to handle relative paths like "." or ".."
    input_directory = input_directory.resolve()

    # Validate input directory
    if not input_directory.exists() or not input_directory.is_dir():
        typer.echo(
            f"Error: Input directory '{input_directory}' does not exist or is not a directory",
            err=True,
        )
        raise typer.Exit(code=1)

    # Get the folder name from the resolved absolute path
    folder_name = input_directory.name

    # Handle output path
    if output is None:
        # Default: create in current directory with folder name
        output = Path.cwd() / f"{folder_name}.epub"
    elif output.is_dir():
        # If output is a directory, append the folder name
        output = output / f"{folder_name}.epub"

    # Prepare configuration with defaults and CLI overrides
    config = DEFAULT_CONFIG.copy()

    # Apply CLI overrides (only for non-None values)
    cli_overrides = {
        "theme": theme,
        "title": title,
        "author": author,
        "large_file_threshold_mb": limit_mb,
        "skip_large_files": not no_skip_large,
        "flat_toc": not hierarchical_toc,  # Invert the flag for user-friendliness
    }

    for key, value in cli_overrides.items():
        if value is not None:
            if key.startswith("epub_metadata_"):
                # Handle nested metadata fields
                meta_key = key.replace("epub_metadata_", "")
                if "epub_metadata" not in config:
                    config["epub_metadata"] = {}
                config["epub_metadata"][meta_key] = value
            else:
                config[key] = value

    # Convert the project
    try:
        result = convert_project_to_epub(input_directory, output, config)
        typer.echo(result)
    except Exception as e:
        typer.echo(f"Error during conversion: {e}", err=True)
        logging.error(f"Conversion failed: {e}", exc_info=True)
        raise typer.Exit(code=1)


# Entry point for the command-line script
def run_cli():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    app()
