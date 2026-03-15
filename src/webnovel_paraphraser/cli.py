"""Command-line interface for the project."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Annotated

import typer

from webnovel_paraphraser.ingest import ingest_txt_chapters, inspect_txt_chapters
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


@app.command("inspect-txt")
def inspect_txt(
    input_dir: Annotated[
        Path,
        typer.Argument(help="Directory containing single-chapter .txt files."),
    ] = Path("input/txt_chapters"),
) -> None:
    """Inspect txt chapter input and print detected order/title metadata."""

    try:
        result = inspect_txt_chapters(input_dir=input_dir)
    except (FileNotFoundError, NotADirectoryError, UnicodeDecodeError, ValueError) as exc:
        raise typer.BadParameter(str(exc)) from exc

    chapter_count = int(result["chapter_count"])
    logger.info("inspect_txt found %s chapters in %s", chapter_count, input_dir)
    typer.echo(f"Found {chapter_count} chapter files in {result['input_dir']}")
    for chapter in result["chapters"]:
        typer.echo(
            f"{chapter['order']:03d} | {Path(chapter['source_path']).name} | {chapter['title']}"
        )


@app.command("ingest-txt")
def ingest_txt(
    input_dir: Annotated[
        Path,
        typer.Argument(help="Directory containing single-chapter .txt files."),
    ] = Path("input/txt_chapters"),
    run_id: Annotated[
        str,
        typer.Option("--run-id", help="Run identifier used under runs/<run_id>."),
    ] = "latest",
    runs_dir: Annotated[
        Path,
        typer.Option("--runs-dir", help="Base directory for run workdirs."),
    ] = Path("runs"),
) -> None:
    """Ingest txt chapters into a run workdir and emit chapter manifest/report."""

    try:
        result = ingest_txt_chapters(input_dir=input_dir, run_id=run_id, runs_dir=runs_dir)
    except (FileNotFoundError, NotADirectoryError, UnicodeDecodeError, ValueError) as exc:
        raise typer.BadParameter(str(exc)) from exc

    logger.info(
        "ingest_txt run=%s chapters=%s manifest=%s",
        run_id,
        result["chapter_count"],
        result["manifest_path"],
    )
    typer.echo(
        f"Ingested {result['chapter_count']} chapters into "
        f"{result['run_work_dir']}"
    )
    typer.echo(f"Manifest: {result['manifest_path']}")
    typer.echo(f"Report: {result['report_path']}")


@app.command("cleanup-runs")
def cleanup_runs(
    runs_dir: Annotated[
        Path,
        typer.Option("--runs-dir", help="Base directory that contains run folders."),
    ] = Path("runs"),
    keep: Annotated[
        int,
        typer.Option("--keep", min=0, help="How many most-recent run folders to keep."),
    ] = 3,
    apply: Annotated[
        bool,
        typer.Option(
            "--apply",
            help="Actually delete selected run folders. Without this flag, only preview.",
        ),
    ] = False,
) -> None:
    """Remove old run folders while keeping the most recent ones."""

    if not runs_dir.exists():
        raise typer.BadParameter(f"Runs directory does not exist: {runs_dir}")
    if not runs_dir.is_dir():
        raise typer.BadParameter(f"Runs path is not a directory: {runs_dir}")

    run_dirs = [p for p in runs_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
    run_dirs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    to_remove = run_dirs[keep:]

    if not to_remove:
        typer.echo(
            f"No run folders to remove in {runs_dir.resolve()} "
            f"(found {len(run_dirs)}, keep={keep})."
        )
        return

    mode = "APPLY" if apply else "DRY-RUN"
    typer.echo(f"[{mode}] Selected {len(to_remove)} run folder(s) for cleanup:")
    for run_path in to_remove:
        typer.echo(f"- {run_path.resolve()}")

    if not apply:
        typer.echo("No files were deleted. Re-run with --apply to remove selected folders.")
        return

    for run_path in to_remove:
        shutil.rmtree(run_path)
    logger.info("cleanup_runs removed %s folders from %s", len(to_remove), runs_dir)
    typer.echo(f"Removed {len(to_remove)} run folder(s).")
