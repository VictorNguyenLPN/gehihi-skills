<div align="center">

<h3>Antigravity &amp; Gemini Research / Software Engineering Skills</h3>

<img src="assets/gehihi-logo.svg" alt="gehihi-skills" width="600" />

<br/>

[![GitHub Stars](https://img.shields.io/github/stars/VictorNguyenLPN/gehihi-skills?style=flat-square&logo=github)](https://github.com/VictorNguyenLPN/gehihi-skills/stargazers) [![GitHub Forks](https://img.shields.io/github/forks/VictorNguyenLPN/gehihi-skills?style=flat-square&logo=github)](https://github.com/VictorNguyenLPN/gehihi-skills/network/members) [![GitHub Issues](https://img.shields.io/github/issues/VictorNguyenLPN/gehihi-skills?style=flat-square&logo=github)](https://github.com/VictorNguyenLPN/gehihi-skills/issues)

</div>

Minimalist rules and modular `SKILL.md` workflows for **Google Antigravity** and **Gemini**, focused on Software Engineering (SE) and Scientific Research (NLP, IR, CV).

## Architecture

- **`GEMINI.md` (Always-On)**: Global constraints applied to every prompt (minimal code, fail-fast without speculative `try/except`, zero-slop prose, canonical terminology, verified citations).
- **`skills/*/SKILL.md` (On-Demand)**: Loaded only when triggered by task context or explicit skill name.

## Quick Start

Requires `bash`, `git`, and `python3` (stdlib only).

```bash
git clone git@github.com:VictorNguyenLPN/gehihi-skills.git
cd gehihi-skills
./scripts/install.sh
```

`install.sh` symlinks `GEMINI.md` to `~/.gemini/config/GEMINI.md`, writes `~/.gemini/config/skills.json`, and symlinks `skills/*` into `~/.agents/skills/`.

## Skills & Example Prompts

| Skill                        | Scope                                                                 | Example Prompt                                                                      |
| :--------------------------- | :-------------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `minimal-perf-code`          | Remove `try/except` bloat, vectorize PyTorch/NumPy, reduce complexity | _"Use `minimal-perf-code` to strip fallbacks and vectorize `retriever.py`."_        |
| `lit-search-verify`          | Search papers, structured reading, verify `.bib`/DOI/arXiv            | _"Use `lit-search-verify` to check `refs.bib` and summarize ColBERT."_              |
| `technical-academic-writing` | Edit LaTeX/docs with zero AI slop and canonical SE/NLP/IR/CV terms    | _"Use `technical-academic-writing` to polish `method.tex`, keeping all `\cite{}`."_ |
| `defect-review`              | Read-only `P0`-`P3` diff review for bugs, ML leaks, and bloat         | _"Use `defect-review` on `git diff` for data leaks or sync bottlenecks."_           |

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
ln -s /path/to/gehihi-skills/GEMINI.md /path/to/project/GEMINI.md
```

To add a skill, create `skills/<skill-name>/SKILL.md` with `name` and `description` YAML frontmatter, then re-run `./scripts/install.sh`.

## References & Acknowledgments

Built upon and adapted from the following open-source skill repositories and engineering guidelines:

- [anthropics/skills](https://github.com/anthropics/skills): `SKILL.md` open specification and progressive disclosure pattern.
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills): `karpathy-guidelines` (clarify before coding, simplicity first, surgical changes).
- [obra/superpowers](https://github.com/obra/superpowers): Verification-before-completion and disciplined debugging workflows.
- [openai/skills](https://github.com/openai/skills): `review-agent` read-only, defect-first (`P0`-`P3`) review rubric adapted for `defect-review`.
- [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) & [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills): Academic literature lookup and research workflow patterns.
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) & [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer): Anti-slop phrase filtering while preserving mathematical notation and citations.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail): Laziness ladder, caller blast-radius checks, whole-repo lean auditing, and `shortcut:` technical debt ledger.
