---
name: technical-academic-writing
description: >-
  Write, edit, and review academic papers (LaTeX/Markdown), technical documentation,
  research proposals, and engineering reports with high information density, zero AI slop,
  and canonical domain terminology in Software Engineering, NLP, IR, and CV. Use whenever
  drafting, polishing, translating, or reviewing prose, papers, READMEs, or technical explanations.
---

# Technical & Academic Writing

Produce concise, high-density prose grounded in quantitative claims and canonical domain terminology.

## 1. Core Editorial Rules

1. **Zero Throat-Clearing**: Start paragraphs directly with the claim, mechanism, or finding. Cut scene-setting openers and redundant closing summaries.
2. **Preserve Mathematical & Empirical Invariants**: Never alter equations, symbols, experimental metrics, standard deviations, p-values, or LaTeX macros (`\cite{}`, `\citet{}`, `\citep{}`, `\ref{}`, `\label{}`).
3. **Quantitative Over Qualitative**: Replace vague intensifiers (*very, significantly, remarkably, substantially, state-of-the-art*) with exact deltas (`+2.4 nDCG@10`), complexity bounds (`O(N log d)`), or failure conditions, or delete the modifier.
4. **Active, Direct Syntax**: Prefer active voice for design decisions and empirical actions (*"We train..."*, *"The retriever indexes..."*). Use passive voice only when the actor is immaterial.
5. **No Em-Dashes or Ornate Phrasing**: Never use em-dashes (`U+2014`); use commas, colons, parentheses, or periods. Avoid inflated metaphors, dramatic binary contrasts (*"It is not merely X; it is Y"*), and superficial participial tails (*"...highlighting the importance of..."*).

## 2. Reference Routing

- When editing or auditing prose for AI clichés, filler patterns, or Vietnamese translationese, read [references/banned-lexicon.md](./references/banned-lexicon.md).
- When writing, reviewing, or translating domain content in **NLP**, **IR**, **CV**, or **Software Engineering**, read [references/domain-terminology.md](./references/domain-terminology.md).

