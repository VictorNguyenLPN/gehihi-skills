---
name: defect-review
description: >-
  Perform a read-only, defect-first code review, whole-repo lean audit, or shortcut debt
  scan on uncommitted changes, branch diffs, commits, or research codebases. Use when
  reviewing code for correctness bugs, silent ML data/metric leaks, performance
  bottlenecks, dead/duplicate code, or listing `shortcut:` technical debt markers.
---

# Defect-First Review, Lean Audit & Debt Ledger

Inspect the requested target directly and report concrete, actionable findings using canonical SE/NLP/IR/CV terminology. Do not modify files, create commits, or invent speculative issues.

## 1. Modes & Inspection Scope

1. Inspect `GEMINI.md` or `AGENTS.md` in the workspace if present.
2. Select the mode matching the request:
   - **Diff & Commit Review**: For uncommitted changes, inspect `git diff` and `git status`. For a branch review, run `git merge-base HEAD <base-ref>` and inspect `git diff <merge-base-sha>`. Always `grep` callers of modified signatures to catch cross-file breakage.
   - **Whole-Repo Lean & Quality Audit**: Map entry points, configs, dependencies, and primary data flows. Trace high-risk paths end-to-end; before flagging dead code, `grep` the entire tree (including tests, fixtures, and dynamic string references).
   - **Shortcut Debt Ledger**: Scan tracked/unignored files via:
     ```bash
     git grep --no-index --exclude-standard -nE '(#|//|/[*]) ?(shortcut|ponytail):'
     ```

## 2. Defect & Lean Taxonomy

Flag an issue only when it is real and demonstrably affects correctness, safety, scale, or maintainability:

- **Correctness & Logic**: Off-by-one errors, broken invariants, concurrency/race conditions, resource leaks, broken callers, or silent exception swallowing (`except Exception: pass` / hidden fallbacks).
- **Research / ML Pipeline Defects**:
  - Train/validation/test data leakage (fitting scalers/tokenizers/BM25 stats before split).
  - Unseeded or inconsistent RNG in evaluation, missing `model.eval()` / `torch.inference_mode()`.
  - Silent tensor broadcasting bugs (e.g., `(B, 1)` vs `(B,)`), wrong mask polarity, or unmasked padding tokens in loss/attention.
  - Metric computation bugs (macro/micro mismatch, unweighted last-batch averaging).
- **Performance & Scale Regressions**: Accidental `O(N^2)` loops, N+1 queries, unbatched I/O, unbounded memory growth, or GPU-CPU sync points (`.item()`, `.cpu()`) inside inner loops.
- **Lean Reductions & Defensive Bloat**:
  - `delete`: Dead code, unused flags/configs, or speculative branches.
  - `reuse` / `merge`: Duplicate helpers or near-copies that must change together.
  - `stdlib`: Third-party dependencies replaceable by standard library or a few native lines.
  - `yagni`: Single-implementation abstractions, pass-through wrappers, or internal `try/except` fallbacks.
  - Note: A `shortcut: <limit>, <upgrade trigger>` comment is an intentional decision, not a defect, unless current load exceeds `<limit>`.

Do not report formatting nits or unverified hypothetical concerns.

## 3. Output Format

### Review / Audit Mode
List findings first, ordered by severity:

`[P<0-3>] Imperative finding title (path/to/file.py:line)`
One concise paragraph stating the execution path, concrete failure/bloat mechanism, and minimal fix.

Severity levels:
- `P0`: Critical failure, security hole, data loss, or corrupted experimental metrics.
- `P1`: Urgent correctness or scale bug blocking merge/run.
- `P2`: Ordinary defect, missing critical test, or measurable slowdown.
- `P3`: Lean reduction (`delete`/`reuse`/`stdlib`/`merge`), redundant defensive fallback, or dead abstraction.

End with `Lean: -<N> lines possible.` when lean reductions exist. If no issues qualify, output `No findings.` followed by a one-sentence verification summary.

### Debt Ledger Mode
Output one line per marker grouped by file:
`<file>:<line> | ceiling: <limit> | upgrade: <trigger>` (tag `no-trigger` if no upgrade path is specified).
End with `<N> markers, <M> with no trigger.` or `No shortcut debt. Clean ledger.`.
