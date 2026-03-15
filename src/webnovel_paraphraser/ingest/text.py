"""Text chapter ingest helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

NUMERIC_PREFIX_RE = re.compile(r"^(?P<prefix>\d+)[_\-\s]+(?P<rest>.*)$")


@dataclass(frozen=True)
class DiscoveredChapter:
    """Discovered chapter source file and its ingest metadata."""

    source_path: Path
    order: int
    title: str
    chapter_id: str


def _parse_sort_key(path: Path) -> tuple[int, int, str]:
    stem = path.stem
    match = NUMERIC_PREFIX_RE.match(stem)
    if match:
        return (0, int(match.group("prefix")), stem.lower())
    return (1, 0, stem.lower())


def _clean_title_from_stem(stem: str) -> str:
    match = NUMERIC_PREFIX_RE.match(stem)
    base = match.group("rest") if match else stem
    normalized = base.replace("_", " ").replace("-", " ").strip()
    if not normalized:
        return "Untitled"
    return normalized.title()


def _extract_title(content: str, fallback_stem: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return _clean_title_from_stem(fallback_stem)


def discover_txt_chapters(input_dir: Path) -> list[DiscoveredChapter]:
    """Discover and order chapter `.txt` files from an input directory."""

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")

    txt_files = sorted(
        (p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() == ".txt"),
        key=_parse_sort_key,
    )
    if not txt_files:
        raise ValueError(f"No .txt files found in: {input_dir}")

    discovered: list[DiscoveredChapter] = []
    for order, source_path in enumerate(txt_files):
        content = source_path.read_text(encoding="utf-8-sig")
        title = _extract_title(content, fallback_stem=source_path.stem)
        discovered.append(
            DiscoveredChapter(
                source_path=source_path,
                order=order,
                title=title,
                chapter_id=f"ch_{order:04d}",
            )
        )
    return discovered


def inspect_txt_chapters(input_dir: Path) -> dict[str, object]:
    """Inspect txt chapter inputs and return summary metadata."""

    discovered = discover_txt_chapters(input_dir)
    chapters = [
        {
            "chapter_id": item.chapter_id,
            "order": item.order,
            "title": item.title,
            "source_path": str(item.source_path.resolve()),
        }
        for item in discovered
    ]
    return {
        "input_dir": str(input_dir.resolve()),
        "chapter_count": len(discovered),
        "chapters": chapters,
    }


def ingest_txt_chapters(input_dir: Path, run_id: str, runs_dir: Path) -> dict[str, object]:
    """Ingest txt chapters into a run workdir and emit a chapter manifest."""

    discovered = discover_txt_chapters(input_dir)
    run_work_dir = runs_dir / run_id / "work"
    raw_dir = run_work_dir / "chapters_raw"
    reports_dir = run_work_dir / "reports"
    raw_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    manifest_chapters: list[dict[str, object]] = []
    for item in discovered:
        original_text = item.source_path.read_text(encoding="utf-8-sig")
        normalized_path = raw_dir / f"{item.order:04d}.txt"
        normalized_path.write_text(original_text, encoding="utf-8")

        manifest_chapters.append(
            {
                "chapter_id": item.chapter_id,
                "order": item.order,
                "title": item.title,
                "source_type": "txt_single_file",
                "source_path": str(item.source_path.resolve()),
                "normalized_text_path": str(normalized_path.resolve()),
            }
        )

    generated_at = datetime.now(UTC).isoformat()
    manifest = {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "run_id": run_id,
        "input_dir": str(input_dir.resolve()),
        "chapter_count": len(manifest_chapters),
        "chapters": manifest_chapters,
    }

    manifest_path = run_work_dir / "chapter_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=True, indent=2), encoding="utf-8")

    report = {
        "generated_at": generated_at,
        "run_id": run_id,
        "chapter_count": len(manifest_chapters),
        "manifest_path": str(manifest_path.resolve()),
        "raw_chapters_dir": str(raw_dir.resolve()),
    }
    report_path = reports_dir / "ingest_txt_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")

    return {
        "run_id": run_id,
        "chapter_count": len(manifest_chapters),
        "run_work_dir": str(run_work_dir.resolve()),
        "manifest_path": str(manifest_path.resolve()),
        "report_path": str(report_path.resolve()),
    }
