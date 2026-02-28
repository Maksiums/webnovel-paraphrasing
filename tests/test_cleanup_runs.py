import os
from pathlib import Path

from typer.testing import CliRunner

from webnovel_paraphraser.cli import app

runner = CliRunner()


def _make_run_dir(base: Path, name: str) -> Path:
    run_dir = base / name
    (run_dir / "work").mkdir(parents=True)
    return run_dir


def test_cleanup_runs_dry_run_keeps_all_folders(tmp_path: Path) -> None:
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    _make_run_dir(runs_dir, "run-a")
    _make_run_dir(runs_dir, "run-b")
    _make_run_dir(runs_dir, "run-c")
    _make_run_dir(runs_dir, "run-d")

    result = runner.invoke(
        app,
        ["cleanup-runs", "--runs-dir", str(runs_dir), "--keep", "2"],
    )

    assert result.exit_code == 0
    assert "[DRY-RUN]" in result.stdout
    assert "No files were deleted" in result.stdout
    assert (runs_dir / "run-a").exists()
    assert (runs_dir / "run-b").exists()
    assert (runs_dir / "run-c").exists()
    assert (runs_dir / "run-d").exists()


def test_cleanup_runs_apply_removes_old_folders(tmp_path: Path) -> None:
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    first = _make_run_dir(runs_dir, "run-a")
    second = _make_run_dir(runs_dir, "run-b")
    third = _make_run_dir(runs_dir, "run-c")

    # Ensure deterministic mtime ordering for the test.
    os.utime(first, (1000, 1000))
    os.utime(second, (2000, 2000))
    os.utime(third, (3000, 3000))

    result = runner.invoke(
        app,
        ["cleanup-runs", "--runs-dir", str(runs_dir), "--keep", "1", "--apply"],
    )

    assert result.exit_code == 0
    assert "[APPLY]" in result.stdout
    assert "Removed 2 run folder(s)." in result.stdout

    run_dirs = [p for p in runs_dir.iterdir() if p.is_dir()]
    assert len(run_dirs) == 1
