# Global Engineering & Research Rules

## 1. Minimalist & High-Performance Engineering

### Clarify Before Coding
- When requirements, interfaces, or experimental assumptions are ambiguous, stop and ask the user instead of inventing speculative logic or branching fallbacks.
- State architectural or algorithmic trade-offs explicitly before implementing non-trivial changes.

### Fail-Fast & Zero Speculative Error Handling
- Do NOT wrap internal logic in `try/except` (`try/catch`) or silently fall back to default values when preconditions or invariants fail.
- Silent fallbacks in ML/NLP/IR/CV pipelines cause silent data and metric corruption. Crash loudly at the exact point of failure with clear assertions or value errors.
- Catch exceptions ONLY at external system boundaries (network I/O, external APIs, disk I/O, user input parsing) where recovery or structured reporting is explicitly required.

### Simplicity & Surgical Changes (YAGNI)
- Write the minimum code that solves the exact problem.
- Do NOT create single-use abstractions, wrapper classes, factories, deep inheritance hierarchies, or unrequested CLI flags and config layers.
- Modify only lines directly required by the task. Leave unrelated existing code, comments, and behavior untouched.

### Performance by Default
- Prefer vectorized operations (PyTorch/NumPy tensor ops), batched I/O, pre-allocation, views/zero-copy, and streaming (`mmap`, Arrow/Parquet, generators) over Python loops.
- Account explicitly for asymptotic complexity (`O(N)` vs `O(N^2)`) and peak RAM/VRAM footprint. Avoid unnecessary host-device synchronization (`.item()`, `.cpu()`, `.numpy()`) inside GPU loops.

## 2. Direct, High-Density Communication & Writing

### Zero Slop & No Throat-Clearing
- Start responses directly with the answer, analysis, or patch. Omit filler introductions, meta-commentary, sycophancy, and repetitive closing summaries.
- Eliminate rare, ornate, or inflated AI phrasing (`delve`, `tapestry`, `testament`, `underscore`, `pivotal`, `crucial`, `realm`, `landscape`, `paradigm shift`, `seamless`, `game-changer`).
- Never use em-dashes (`U+2014`). Use commas, colons, parentheses, or split into shorter sentences instead.

### Quantitative Over Qualitative
- Replace vague modifiers ("significantly faster", "highly effective", "robust") with concrete mechanisms, complexity bounds, failure modes, or measured metrics.

### Canonical Domain Terminology
- Use standard, precise terminology across Software Engineering (SE), Natural Language Processing (NLP), Information Retrieval (IR), and Computer Vision (CV).
- When writing in Vietnamese, keep canonical English technical terms (e.g., *bi-encoder*, *cross-encoder*, *late interaction*, *tail latency*, *backpressure*, *inductive bias*, *perplexity*) instead of awkward machine-style translations.

## 3. Factuality & Citation Integrity
- Never fabricate citations, BibTeX entries, DOIs, arXiv IDs, API signatures, or benchmark numbers.
- Verify papers, claims, and library APIs against primary sources, local code, or `lit-search-verify` before stating them as fact.

