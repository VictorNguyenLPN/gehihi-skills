---
name: minimal-perf-code
description: >-
  Write, refactor, simplify, or optimize code for minimal complexity and high performance.
  Use when writing new modules, refactoring bloated or defensive AI-generated code,
  removing redundant try/catch and fallbacks, or optimizing CPU, GPU, and memory
  performance in Python, PyTorch, NumPy, and backend systems.
---

# Minimal & High-Performance Code

Strip speculative bloat and optimize execution paths without altering intended behavior.

## 1. De-Bloating & Simplification Checklist

1. **The Laziness Ladder (Before Writing New Code)**:
   - Check in strict order: (1) existing helper or pattern in the codebase, (2) standard library or native runtime feature, (3) already-installed dependency, (4) minimal new code.
   - Never add a new dependency for a few lines of logic. Prefer deleting dead paths over wrapping them.
2. **Blast-Radius & Shortcut Convention**:
   - Before modifying a function signature or fixing a bug, `grep` all callers, tests, and fixtures; fix the root cause once in shared code.
   - Mark deliberate scaling shortcuts with an inline comment: `shortcut: <limit>, <upgrade trigger>`.
3. **Remove Speculative Error Handling**:
   - Delete internal `try/except` (`try/catch`) blocks that mask bugs or return silent defaults (`return None`, `x or default`, `getattr(obj, k, fallback)`).
   - Keep exception handling strictly at external I/O boundaries (network calls, third-party APIs, disk/CLI parsing) where recovery is explicitly requested.
   - Replace silent fallbacks with explicit preconditions (`assert` or raising `ValueError`/`KeyError`) so pipeline bugs surface at their source.
4. **Collapse Unnecessary Abstractions**:
   - Inline single-use helper functions, single-implementation interfaces/ABCs, and trivial wrapper classes into direct functions or `@dataclass(slots=True)`.
   - Remove unrequested config schemas, feature flags, and `**kwargs` pass-through layers.
5. **Clarify Ambiguity**:
   - If the contract or edge-case behavior is underspecified, ask the user before writing defensive branches.

## 2. Performance Optimization Protocol

### Algorithmic & Data Structure Level
- Eliminate nested `O(N^2)` scans via hash maps, sets, sorted binary search, or batch matrix operations.
- Avoid repeated allocations inside hot loops; pre-allocate buffers or accumulate into pre-sized arrays.

### PyTorch, NumPy & Scientific Computing
- Replace Python loops over batch, sequence, or spatial dimensions with vectorized broadcasting, `torch.einsum`, or index scatter/gather.
- Use `torch.inference_mode()` instead of `torch.no_grad()` during evaluation.
- Remove host-device synchronization calls (`.item()`, `.cpu()`, `.numpy()`, `print(tensor)`) from inside training/inference step loops.
- Use `pin_memory=True` + `non_blocking=True` for H2D transfers and `contiguous()`/`view()` instead of `.clone()` where aliasing is safe.

### I/O & Data Pipelines
- Stream large datasets with generators, `mmap`, Arrow/Parquet, or DuckDB instead of materializing full lists/DataFrames in RAM.
- Batch disk/DB writes and HTTP requests instead of per-item round trips.

## 3. Verification Workflow

1. Establish correctness baseline before optimization (unit test or `torch.testing.assert_close`).
2. Measure before and after with `timeit`, `cProfile`, `torch.utils.benchmark`, or peak RSS/VRAM tracking (`torch.cuda.max_memory_allocated()`).
3. Keep only changes that preserve numerical/functional equivalence and produce measurable complexity or runtime gains.

