# Webnovel Paraphrasing Project — Context & Roadmap

Version: 0.3.0
Last Updated: 2026-02-28
Scope: Public project context (versioned)

## 1. Project Overview

### Goal
This project aims to paraphrase full-length webnovels into cleaner, more readable EPUB output while preserving meaning, continuity, and story coherence.

### Current Execution Strategy
Build a small end-to-end MVP first using a manually prepared dataset (6 chapter `.txt` files), then expand ingest support for larger EPUB workflows.

### High-Level Pipeline (Input-Agnostic Core)

→ Input adapter (txt/epub/etc.)
→ Chapter manifest (canonical contract)
→ Normalize chapter text into run workdir
→ Paraphrase chapters (chunked, resumable, local LLM)
→ Optional consistency / validation pass
→ Build EPUB output

## 2. Core Constraints & Design Decisions

### LLM / Compute
- Primary target: local inference
- Initial runtime: Ollama
- Architecture should allow backend swapping later:
  - llama.cpp (GGUF)
  - MLX (Apple Silicon)
  - transformers (if needed)
- No paid APIs
- No fine-tuning planned initially (prompt-only)

### Input-Agnostic Contract
All ingest methods must produce the same chapter manifest and normalized chapter files for downstream stages.

Planned supported sources:
- Folder of single-chapter `.txt` files (current MVP)
- Single `.txt` containing multiple chapters
- Single-chapter EPUB
- Multi-chapter EPUB requiring split

### Scale
- Initial production target is a large corpus (thousands of chapters)
- Input EPUB may contain very large XHTML files
- Batch processing and resume/checkpointing are mandatory

### Quality Goals
- Preserve meaning and narrative continuity
- Improve fluency and readability
- Slight stylistic deviation is acceptable
- Character voice consistency is a bonus
- Terminology consistency is important

## 3. Input / Output Staging in Repo

Local staging folders (contents gitignored):
- `input/txt_chapters/` for chapter `.txt` files
- `input/assets/` for optional cover PNG and related assets
- `output/` for generated EPUB and run exports

## 4. Workdir-Based Architecture

All processing happens inside a run-specific work directory.
Final EPUB is rebuilt from processed artifacts.

`runs/<run_id>/work/`
- `extracted/`
- `chapters_raw/`
- `chapters_paraphrased/`
- `state/`
- `chapter_manifest.json`
- `reports/`
- `logs/`

## 5. Persistent State Concepts

### Story Bible
Tracks characters, locations, terminology, and ongoing plot threads.

### Chapter Summaries
Short summaries generated after each chapter to preserve continuity.

### Glossary
Term → preferred rendering for terminology consistency.

## 6. Chunking & Paraphrasing Strategy

- Process chapters individually
- Split chapters into paragraph-based chunks
- Each chunk rewrite includes:
  - style guidance
  - compact story bible
  - chapter summary so far
  - recent rewritten context
- Output must remain valid XHTML-compatible text for EPUB assembly

## 7. Development Roadmap (Revised)

Each feature corresponds to a branch merged into `dev`.

### Feature 0: project-skeleton (done)
Repository scaffolding, CLI skeleton, logging, config, lint/test/CI baseline.

### Feature 1: txt-singles-ingest-manifest (current)
Ingest folder of single-chapter `.txt` files and emit canonical chapter manifest.

### Feature 2: state-store-mvp
Persistent run progress, checkpoint/resume primitives.

### Feature 3: paraphrase-mvp-single-chapter
Paraphrase one chapter end-to-end with Ollama.

### Feature 4: paraphrase-batch-runner
Batch processing over chapter manifest with retries and resume.

### Feature 5: epub-builder-mvp
Build EPUB from paraphrased chapters, optional cover PNG.

### Feature 6: txt-multichapter-ingest
Support one `.txt` file containing multiple chapters.

### Feature 7: epub-ingest-inspect-split
Ingest EPUB, inspect structure, and split chapters into canonical manifest form.

### Feature 8: volume-detection
Assign chapters to volumes when detectable.

### Feature 9: consistency-pass
Detect and fix terminology / continuity drift.

### Feature 10: evaluation-and-regression
Golden chapter checks, diff-based regression guardrails.

## 8. Non-Goals

- No fine-tuning
- No deployment
- No paid APIs
- No UI
- No distribution

## 9. Guiding Principles

- One internal pipeline contract, multiple ingest adapters
- Deterministic structure before LLM calls
- Clear separation of concerns
- Everything resumable and inspectable
- Optimize for correctness and learning first

## 10. Current Status

- Runtime: local Ollama
- Immediate target: 6 `.txt` chapter MVP run
- Output target: valid EPUB from paraphrased chapters
- Workflow: feature branches → `dev`

This file is the authoritative public project context.
