<div align="center">

<h3>Antigravity &amp; Gemini Research / Software Engineering Skills</h3>

[![GitHub Stars](https://img.shields.io/github/stars/VictorNguyenLPN/skills?style=flat-square&logo=github)](https://github.com/VictorNguyenLPN/skills/stargazers) [![GitHub Forks](https://img.shields.io/github/forks/VictorNguyenLPN/skills?style=flat-square&logo=github)](https://github.com/VictorNguyenLPN/skills/network/members) [![GitHub Issues](https://img.shields.io/github/issues/VictorNguyenLPN/skills?style=flat-square&logo=github)](https://github.com/VictorNguyenLPN/skills/issues) [![Last Commit](https://img.shields.io/github/last-commit/VictorNguyenLPN/skills?style=flat-square&logo=git)](https://github.com/VictorNguyenLPN/skills/commits/main) [![Python 3.10+](https://img.shields.io/badge/python-3.10%2B%20(stdlib)-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) [![Agent](https://img.shields.io/badge/agent-Antigravity%20%7C%20Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)](https://github.com/VictorNguyenLPN/skills)

<img src="assets/gehihi-logo.svg" alt="Gehihi" width="400" />

</div>

Minimalist rules and modular `SKILL.md` workflows for **Google Antigravity** and **Gemini**, focused on Software Engineering (SE) and Scientific Research (NLP, IR, CV).

## Architecture

- **`GEMINI.md` (Always-On)**: Global constraints applied to every prompt (minimal code, fail-fast without speculative `try/except`, zero-slop prose, canonical terminology, verified citations).
- **`skills/*/SKILL.md` (On-Demand)**: Loaded only when triggered by task context or explicit skill name.

## Quick Start

Requires `bash`, `git`, and `python3` (stdlib only).

```bash
git clone git@github.com:VictorNguyenLPN/skills.git
cd skills
./scripts/install.sh
```

`install.sh` symlinks `GEMINI.md` to `~/.gemini/config/GEMINI.md`, writes `~/.gemini/config/skills.json`, and symlinks `skills/*` into `~/.agents/skills/`.

## Skills & Example Prompts

| Skill | Scope | Example Prompt |
| :--- | :--- | :--- |
| `minimal-perf-code` | Remove `try/except` bloat, vectorize PyTorch/NumPy, reduce complexity | *"Use `minimal-perf-code` to strip fallbacks and vectorize `retriever.py`."* |
| `lit-search-verify` | Search papers, structured reading, verify `.bib`/DOI/arXiv | *"Use `lit-search-verify` to check `refs.bib` and summarize ColBERT."* |
| `technical-academic-writing` | Edit LaTeX/docs with zero AI slop and canonical SE/NLP/IR/CV terms | *"Use `technical-academic-writing` to polish `method.tex`, keeping all `\cite{}`."* |
| `defect-review` | Read-only `P0`-`P3` diff review for bugs, ML leaks, and bloat | *"Use `defect-review` on `git diff` for data leaks or sync bottlenecks."* |

## CLI Tools (`lit-search-verify`)

```bash
# Search OpenAlex, Crossref, arXiv, or Semantic Scholar
python3 skills/lit-search-verify/scripts/search_papers.py --query "ColBERT" --source openalex --limit 5

# Verify BibTeX file, DOI, arXiv ID, or title
python3 skills/lit-search-verify/scripts/verify_bibtex.py --bib references.bib
python3 skills/lit-search-verify/scripts/verify_bibtex.py --doi "10.1145/3397271.3401075" --emit-canonical
python3 skills/lit-search-verify/scripts/verify_bibtex.py --title "Attention Is All You Need"
```

## Per-Project Rules & Extending

Link `GEMINI.md` inside any project repository:

```bash
ln -s /path/to/skills/GEMINI.md /path/to/project/GEMINI.md
```

To add a skill, create `skills/<skill-name>/SKILL.md` with `name` and `description` YAML frontmatter, then re-run `./scripts/install.sh`.
