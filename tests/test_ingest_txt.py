import json
from pathlib import Path

from typer.testing import CliRunner

from webnovel_paraphraser.cli import app

runner = CliRunner()


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_inspect_txt_lists_chapters_in_numeric_prefix_order(tmp_path: Path) -> None:
    input_dir = tmp_path / "txt_chapters"
    input_dir.mkdir()
    _write_text(input_dir / "001_chapter_1.txt", "Chapter 1\nFirst chapter body.")
    _write_text(input_dir / "000_prologue.txt", "Prologue\nIntro body.")

    result = runner.invoke(app, ["inspect-txt", str(input_dir)])

    assert result.exit_code == 0
    assert "Found 2 chapter files" in result.stdout
    assert "000 | 000_prologue.txt | Prologue" in result.stdout
    assert "001 | 001_chapter_1.txt | Chapter 1" in result.stdout


def test_ingest_txt_writes_manifest_and_report(tmp_path: Path) -> None:
    input_dir = tmp_path / "txt_chapters"
    input_dir.mkdir()
    runs_dir = tmp_path / "runs"

    _write_text(input_dir / "000_prologue.txt", "Prologue\nIntro body.")
    _write_text(input_dir / "001_chapter_1.txt", "Chapter 1\nFirst chapter body.")

    result = runner.invoke(
        app,
        [
            "ingest-txt",
            str(input_dir),
            "--run-id",
            "test-run",
            "--runs-dir",
            str(runs_dir),
        ],
    )

    assert result.exit_code == 0
    assert "Ingested 2 chapters" in result.stdout

    work_dir = runs_dir / "test-run" / "work"
    manifest_path = work_dir / "chapter_manifest.json"
    report_path = work_dir / "reports" / "ingest_txt_report.json"

    assert manifest_path.exists()
    assert report_path.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.0"
    assert manifest["run_id"] == "test-run"
    assert manifest["chapter_count"] == 2

    chapters = manifest["chapters"]
    assert [chapter["order"] for chapter in chapters] == [0, 1]
    assert [chapter["title"] for chapter in chapters] == ["Prologue", "Chapter 1"]

    for chapter in chapters:
        assert Path(chapter["source_path"]).exists()
        normalized_path = Path(chapter["normalized_text_path"])
        assert normalized_path.exists()
        assert normalized_path.parent == work_dir / "chapters_raw"
