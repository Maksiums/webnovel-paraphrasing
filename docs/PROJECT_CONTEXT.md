# Webnovel Paraphrasing Project — Context & Roadmap

Version: 0.2.0
Last Updated: 2026-02-07
Scope: Public project context (versioned)

## 1. Project Overview

### Goal
This project aims to paraphrase full-length webnovels from EPUB input into cleaner, more readable EPUB output while preserving meaning, continuity, and story coherence.

### High-Level Pipeline

→ Input EPUB
→ Inspect EPUB structure
→ Split large XHTML files into one chapter per file
→ Detect volumes (optional)
→ Maintain persistent story state (story bible, summaries, glossary)
→ Paraphrase chapters (chunked, resumable, local LLM)
→ Optional consistency / validation pass
→ Rebuild EPUB (single file or per-volume)

## 2. Core Constraints & Design Decisions

### LLM / Compute
- Primary target: local inference
- Initial runtime: Ollama
- Architecture must allow backend swapping later:
  - llama.cpp (GGUF)
  - MLX (Apple Silicon)
  - transformers (if needed later)
- No paid APIs
- No fine-tuning planned initially (prompt-only)

### Scale
- Initial corpus is large (thousands of chapters)
- Input EPUB can contain large XHTML files (hundreds of chapters per file)
- Chapter splitting is required
- Processing is batch-oriented
- Long-running jobs are acceptable
- Resume / checkpointing is mandatory

### Quality Goals
- Preserve meaning and narrative continuity
- Improve fluency and readability
- Slight stylistic deviation is acceptable
- Character voice consistency is a bonus
- Terminology consistency is important

## 3. Input / Output Format

### Input
- EPUB
- Chapters may not be stored one-per-file
- Chapter boundaries detected via headings or text markers

### Output
- EPUB
- Built entirely from paraphrased chapter XHTML files
- One combined EPUB or per-volume EPUBs (optional)

## 4. Workdir-Based Architecture

All processing happens inside a run-specific work directory.
The final EPUB is rebuilt from scratch from processed artifacts.

runs/<run_id>/work/
- extracted/
- chapters_raw/
- chapters_paraphrased/
- state/
- chapter_index.json
- volumes.json
- reports/
- logs/

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
  - last 1–2 rewritten paragraphs
- Output must remain valid XHTML

## 7. Development Roadmap

Each feature corresponds to a separate branch merged into dev.

### Feature 0: project-skeleton
Repository scaffolding, CLI skeleton, logging, config.

### Feature 1: epub-inspection
Inspect EPUB metadata, spine, and XHTML layout.

### Feature 2: chapter-splitter
Split large XHTML files into one file per chapter.

### Feature 3: volume-detection
Assign chapters to volumes if detectable.

### Feature 4: state-store
Persistent progress, story bible, summaries.

### Feature 5: paraphrase-mvp-single-chapter
Paraphrase one chapter end-to-end with Ollama.

### Feature 6: paraphrase-batch-runner
Batch processing with resume and retries.

### Feature 7: consistency-pass
Detect and fix terminology and continuity drift.

### Feature 8: epub-builder
Rebuild final EPUB(s) from paraphrased chapters.

### Feature 9: evaluation-and-regression
Golden chapters, diffs, and regression checks.

## 8. Non-Goals

- No fine-tuning
- No deployment
- No paid APIs
- No UI
- No distribution

## 9. Guiding Principles

- Deterministic structure before LLM calls
- Clear separation of concerns
- Everything resumable and inspectable
- Optimize for correctness and learning first

## 10. Current Status

- Input: EPUB with large XHTML files
- Output: EPUB
- LLM runtime: Ollama
- Workflow: feature branches → dev

This file is the authoritative public project context.
