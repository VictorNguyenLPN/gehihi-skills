---
name: defect-review
description: >-
  Perform a read-only, defect-first code review on uncommitted changes, branch diffs,
  commits, or research codebases. Use when reviewing code for correctness bugs, silent
  ML data/metric leaks, performance bottlenecks, or redundant defensive bloat.
---

# Defect-First Code Review

Inspect the requested diff or codebase directly and report concrete, actionable findings. Do not modify files, create commits, or invent speculative issues.

## 1. Inspection Scope

1. Inspect `GEMINI.md` or `AGENTS.md` in the workspace if present.
2. For uncommitted changes, inspect `git diff` and `git status`. For a branch review, resolve the merge base via `git merge-base HEAD <base-ref>` and inspect `git diff <merge-base-sha>`.
3. Trace call sites and data flow around every modified function or tensor operation.

## 2. Defect Taxonomy

Flag an issue only when it is real, introduced in the reviewed target (or directly requested in a full audit), and demonstrably affects behavior:

- **Correctness & Logic**: Off-by-one errors, broken invariants, concurrency/race conditions, resource leaks, or silent exception swallowing (`except Exception: pass` / hidden fallbacks).
- **Research / ML Pipeline Defects**:
  - Train/validation/test data leakage (fit scalers/tokenizers/BM25 stats on full data before split).
  - Unseeded or inconsistent RNG in evaluation, missing `model.eval()` / `torch.inference_mode()`.
  - Silent tensor broadcasting bugs (e.g., `(B, 1)` vs `(B,)`), wrong mask polarity, or unmasked padding tokens in loss/attention.
  - Metric bugs (averaging macro/micro incorrectly, evaluating on truncated batches without weighting).
- **Performance Regressions**: Accidental `O(N^2)` loops, unbatched I/O, or GPU-CPU sync points (`.item()`, `.cpu()`) inside inner loops.
- **Defensive Bloat**: Redundant internal `try/except` fallbacks or dead single-use abstractions that obscure real failures.

Do not report formatting nits or unverified hypothetical concerns.

## 3. Output Format

List findings first, ordered by severity:

`[P<0-3>] Imperative finding title (path/to/file.py:line)`
One concise paragraph stating the exact execution path, why it fails or degrades performance, and the minimal fix.

Severity levels:
- `P0`: Critical failure, security hole, or corrupted experimental results/metrics.
- `P1`: Urgent correctness or performance bug that blocks merge/run.
- `P2`: Ordinary defect or suboptimal behavior worth fixing.
- `P3`: Redundant defensive bloat, fallback masking errors, or dead abstraction.

If no issues qualify, output `No findings.` followed by a one-sentence verification summary (including any test or coverage gaps).

