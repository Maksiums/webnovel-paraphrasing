"""Command-line interface for the project."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

import typer

from webnovel_paraphraser.utils.logging import configure_logging

app = typer.Typer(help="Webnovel paraphrasing pipeline CLI.")
logger = logging.getLogger(__name__)


@app.callback()
def main(
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Enable debug logs.",
        ),
    ] = False,
) -> None:
    """Initialize app-wide concerns."""

    configure_logging(debug=debug)


@app.command("inspect-epub")
def inspect_epub(
    epub_path: Annotated[
        Path,
        typer.Argument(help="Path to source EPUB."),
    ],
) -> None:
    """Inspect EPUB metadata and structure (placeholder)."""

    logger.info("inspect_epub placeholder: %s", epub_path)
    typer.echo(f"TODO: inspect EPUB at {epub_path}")


@app.command("split-epub")
def split_epub(
    epub_path: Annotated[
        Path,
        typer.Argument(help="Path to source EPUB."),
    ],
    out_dir: Annotated[
        Path,
        typer.Option("--out-dir", help="Output directory for chapter files."),
    ] = Path("runs/latest/work/chapters_raw"),
) -> None:
    """Split source EPUB into chapter files (placeholder)."""

    logger.info("split_epub placeholder: epub=%s out_dir=%s", epub_path, out_dir)
    typer.echo(f"TODO: split EPUB at {epub_path} into {out_dir}")


@app.command("paraphrase-chapter")
def paraphrase_chapter(
    chapter_path: Annotated[
        Path,
        typer.Argument(help="Path to chapter XHTML or text file."),
    ],
) -> None:
    """Paraphrase one chapter (placeholder)."""

    logger.info("paraphrase_chapter placeholder: %s", chapter_path)
    typer.echo(f"TODO: paraphrase chapter {chapter_path}")


@app.command("build-epub")
def build_epub(
    source_dir: Annotated[
        Path,
        typer.Argument(help="Directory with paraphrased chapters."),
    ],
    output_epub: Annotated[
        Path,
        typer.Option("--output-epub", help="Output EPUB path."),
    ] = Path("runs/latest/output/output.epub"),
) -> None:
    """Build final EPUB from paraphrased chapters (placeholder)."""

    logger.info("build_epub placeholder: source=%s output=%s", source_dir, output_epub)
    typer.echo(f"TODO: build EPUB from {source_dir} -> {output_epub}")
