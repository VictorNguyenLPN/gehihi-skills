---
name: lit-search-verify
description: >-
  Search, read, analyze, and verify academic papers, citations, BibTeX entries, and
  technical documentation across NLP, IR, CV, ML, and Software Engineering. Use when
  performing literature reviews, looking up papers on arXiv/Semantic Scholar/OpenAlex/DBLP/Crossref,
  reading papers structurally, or verifying citations and claims to prevent hallucination.
---

# Literature Search, Structured Reading & Verification

Ground every literature claim and BibTeX entry against primary academic APIs before citing.

## 1. Multi-Source Academic Search

Run [search_papers.py](./scripts/search_papers.py) to query arXiv, Semantic Scholar, OpenAlex, DBLP, or Crossref directly (Python 3 stdlib only, no external dependencies):

```bash
python3 scripts/search_papers.py --query "ColBERT late interaction" --source all --limit 5
python3 scripts/search_papers.py --query "flash attention" --source arxiv --year 2022-2024 --format bibtex
```

Options:
- `--source`: `arxiv`, `s2`, `openalex`, `dblp`, `crossref`, or `all` (default: `all`).
- `--limit`: results per source (default: `5`).
- `--year`: single year (`2024`) or inclusive range (`2022-2025`).
- `--format`: `markdown` (default), `json`, or `bibtex`.

If the `hf` CLI is installed and you need full-text markdown of a Hugging Face paper page, run:
```bash
hf papers search "<query>" --limit 5
hf papers read <arxiv_id>
```

## 2. Citation & BibTeX Verification

Never emit unverified BibTeX or trust memorized publication metadata. Verify every entry with [verify_bibtex.py](./scripts/verify_bibtex.py):

```bash
python3 scripts/verify_bibtex.py --bib path/to/references.bib
python3 scripts/verify_bibtex.py --doi "10.1145/3397271.3401075" --emit-canonical
python3 scripts/verify_bibtex.py --arxiv "2004.12832" --emit-canonical
python3 scripts/verify_bibtex.py --title "Attention Is All You Need"
```

Status codes:
- `[VERIFIED]`: Title, year, and first author match the authoritative source (Crossref, arXiv, or DBLP).
- `[MISMATCH]`: Entry resolved to a real work, but metadata (year, authors, or venue) differs. Inspect the diff and replace with the canonical record, and check whether an arXiv preprint has since been published at a peer-reviewed venue (ACL, EMNLP, SIGIR, NeurIPS, ICML, ICLR, CVPR, ICSE).
- `[NOT_FOUND]`: No authoritative match found. Treat as potentially hallucinated and do not cite until resolved.

## 3. Structured Paper Reading Protocol

When summarizing or analyzing a paper, extract these 6 fields directly from the text:
1. **Problem & Formalization**: Input/output spaces, objective function, and core assumptions.
2. **Delta over Prior Work**: Exact architectural, algorithmic, or theoretical change relative to closest baselines.
3. **Experimental Setup**: Datasets, split hygiene, baselines, hardware/compute budget, and evaluation metrics (`nDCG@k`, `MRR`, `mAP`, `Pass@k`, etc.).
4. **Key Empirical & Ablation Findings**: Quantitative deltas (`+X.X` points, latency/VRAM savings) and which components drive the gain.
5. **Threats to Validity & Limitations**: Hyperparameter sensitivity, unverified scaling claims, data contamination, or narrow domain assumptions.
6. **Claim-to-Source Grounding**: Map each cited statement to its exact paper ID and section/table/equation number.

