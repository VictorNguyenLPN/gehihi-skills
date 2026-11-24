#!/usr/bin/env python3
"""Verify BibTeX entries, DOIs, arXiv IDs, or titles against Crossref, arXiv, and DBLP."""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

USER_AGENT = "lit-search-verify/1.0 (mailto:research@local)"
TIMEOUT = 15


def http_get(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json, application/atom+xml, text/xml"},
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        ctype = resp.headers.get("Content-Type", "")
        if "text/html" in ctype:
            raise urllib.error.URLError(f"Received HTML instead of API payload ({ctype})")
        return resp.read()


def clean_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", clean_ws(text).lower())


def token_jaccard(a: str, b: str) -> float:
    ta = set(normalize_text(a).split())
    tb = set(normalize_text(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def extract_author_surnames(author_str: str) -> list[str]:
    surnames = []
    for part in re.split(r"\s+and\s+", author_str, flags=re.IGNORECASE):
        part = clean_ws(part.replace("{", "").replace("}", ""))
        if not part:
            continue
        if "," in part:
            surnames.append(normalize_text(part.split(",", 1)[0]))
        else:
            surnames.append(normalize_text(part.split()[-1]))
    return [s for s in surnames if s]


def parse_bib_file(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    entries: list[dict[str, str]] = []
    raw_entries = re.split(r"(?=@\w+\s*\{)", text)
    for raw in raw_entries:
        raw = raw.strip()
        if not raw.startswith("@"):
            continue
        header_m = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", raw)
        if not header_m:
            continue
        entry: dict[str, str] = {
            "entry_type": header_m.group(1).lower(),
            "key": header_m.group(2),
        }
        for field_m in re.finditer(
            r"(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|\"([^\"]*)\"|(\d+))",
            raw,
            flags=re.DOTALL,
        ):
            name = field_m.group(1).lower()
            val = field_m.group(2) or field_m.group(3) or field_m.group(4) or ""
            entry[name] = clean_ws(val.replace("{", "").replace("}", ""))
        entries.append(entry)
    return entries


def fetch_crossref_doi(doi: str) -> dict[str, Any] | None:
    encoded = urllib.parse.quote(doi.strip(), safe="")
    try:
        data = json.loads(http_get(f"https://api.crossref.org/works/{encoded}"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    item = data.get("message") or {}
    titles = item.get("title") or []
    issued = ((item.get("issued") or {}).get("date-parts") or [[None]])[0]
    containers = item.get("container-title") or []
    authors = [
        f"{a.get('given', '')} {a.get('family', '')}".strip()
        for a in item.get("author") or []
    ]
    return {
        "provider": "crossref",
        "title": clean_ws(titles[0]) if titles else "",
        "authors": [a for a in authors if a],
        "year": issued[0] if issued and isinstance(issued[0], int) else None,
        "venue": clean_ws(containers[0]) if containers else "",
        "doi": item.get("DOI"),
        "arxiv_id": None,
        "url": item.get("URL") or "",
    }


def fetch_arxiv_id(arxiv_id: str) -> dict[str, Any] | None:
    clean_id = re.sub(r"^arXiv:", "", arxiv_id.strip(), flags=re.IGNORECASE)
    try:
        raw = http_get(f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(clean_id)}")
        root = ET.fromstring(raw)
    except (urllib.error.URLError, TimeoutError, ET.ParseError):
        return None
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    entry = root.find("atom:entry", ns)
    if entry is None:
        return None
    title = clean_ws(entry.findtext("atom:title", "", ns))
    if not title or title.lower() == "error":
        return None
    published = clean_ws(entry.findtext("atom:published", "", ns))
    year = int(published[:4]) if len(published) >= 4 and published[:4].isdigit() else None
    authors = [
        clean_ws(a.findtext("atom:name", "", ns))
        for a in entry.findall("atom:author", ns)
    ]
    doi = clean_ws(entry.findtext("arxiv:doi", "", ns)) or None
    venue = clean_ws(entry.findtext("arxiv:journal_ref", "", ns)) or "arXiv"
    return {
        "provider": "arxiv",
        "title": title,
        "authors": [a for a in authors if a],
        "year": year,
        "venue": venue,
        "doi": doi,
        "arxiv_id": clean_id,
        "url": clean_ws(entry.findtext("atom:id", "", ns)),
    }


def fetch_dblp_title(title: str) -> dict[str, Any] | None:
    params = urllib.parse.urlencode({"q": title, "h": 3, "format": "json"})
    try:
        data = json.loads(http_get(f"https://dblp.org/search/publ/api?{params}"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    hits = ((data.get("result") or {}).get("hits") or {}).get("hit") or []
    best: dict[str, Any] | None = None
    best_score = 0.0
    for h in hits:
        info = h.get("info") or {}
        cand_title = clean_ws(info.get("title", "")).rstrip(".")
        score = token_jaccard(title, cand_title)
        if score > best_score:
            best_score = score
            raw_authors = (info.get("authors") or {}).get("author") or []
            if isinstance(raw_authors, dict):
                raw_authors = [raw_authors]
            authors = [
                a.get("text", "") if isinstance(a, dict) else str(a) for a in raw_authors
            ]
            y_str = str(info.get("year") or "")
            best = {
                "provider": "dblp",
                "title": cand_title,
                "authors": [a for a in authors if a],
                "year": int(y_str) if y_str.isdigit() else None,
                "venue": clean_ws(info.get("venue", "")),
                "doi": info.get("doi"),
                "arxiv_id": None,
                "url": info.get("ee") or info.get("url") or "",
            }
    return best if best and best_score >= 0.6 else None


def fetch_openalex_query(query: str, title_match: str | None = None) -> dict[str, Any] | None:
    params = urllib.parse.urlencode({"search": query, "per-page": 3})
    try:
        data = json.loads(http_get(f"https://api.openalex.org/works?{params}"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    for w in data.get("results") or []:
        cand_title = clean_ws(w.get("title") or "")
        if title_match and token_jaccard(title_match, cand_title) < 0.6:
            continue
        doi_url = w.get("doi") or ""
        doi = doi_url.replace("https://doi.org/", "") if doi_url else None
        loc = w.get("primary_location") or {}
        src = loc.get("source") or {}
        authors = [
            (a.get("author") or {}).get("display_name", "")
            for a in w.get("authorships") or []
        ]
        return {
            "provider": "openalex",
            "title": cand_title,
            "authors": [a for a in authors if a],
            "year": w.get("publication_year"),
            "venue": clean_ws(src.get("display_name") or ""),
            "doi": doi,
            "arxiv_id": None,
            "url": doi_url or w.get("id") or "",
        }
    return None


def fetch_crossref_title(title: str) -> dict[str, Any] | None:
    params = urllib.parse.urlencode({"query.title": title, "rows": 3})
    try:
        data = json.loads(http_get(f"https://api.crossref.org/works?{params}"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    for item in (data.get("message") or {}).get("items") or []:
        titles = item.get("title") or []
        cand_title = clean_ws(titles[0]) if titles else ""
        if token_jaccard(title, cand_title) < 0.6:
            continue
        issued = ((item.get("issued") or {}).get("date-parts") or [[None]])[0]
        containers = item.get("container-title") or []
        authors = [
            f"{a.get('given', '')} {a.get('family', '')}".strip()
            for a in item.get("author") or []
        ]
        return {
            "provider": "crossref",
            "title": cand_title,
            "authors": [a for a in authors if a],
            "year": issued[0] if issued and isinstance(issued[0], int) else None,
            "venue": clean_ws(containers[0]) if containers else "",
            "doi": item.get("DOI"),
            "arxiv_id": None,
            "url": item.get("URL") or "",
        }
    return None


def verify_record(entry: dict[str, str]) -> tuple[str, dict[str, Any] | None, list[str]]:
    auth: dict[str, Any] | None = None
    if entry.get("doi"):
        auth = fetch_crossref_doi(entry["doi"])
    if not auth and entry.get("eprint"):
        auth = fetch_arxiv_id(entry["eprint"]) or fetch_openalex_query(entry["eprint"])
    if not auth and entry.get("arxiv"):
        auth = fetch_arxiv_id(entry["arxiv"]) or fetch_openalex_query(entry["arxiv"])
    if not auth and entry.get("title"):
        auth = (
            fetch_dblp_title(entry["title"])
            or fetch_openalex_query(entry["title"], title_match=entry["title"])
            or fetch_crossref_title(entry["title"])
        )

    if not auth:
        return "NOT_FOUND", None, ["No matching record found in Crossref, arXiv, OpenAlex, or DBLP."]

    issues: list[str] = []
    if entry.get("title") and token_jaccard(entry["title"], auth["title"]) < 0.75:
        issues.append(f"Title mismatch: local='{entry['title']}' vs auth='{auth['title']}'")
    if entry.get("year") and auth.get("year") and str(entry["year"]) != str(auth["year"]):
        issues.append(f"Year mismatch: local={entry['year']} vs auth={auth['year']}")
    if entry.get("author") and auth.get("authors"):
        local_first = extract_author_surnames(entry["author"])
        auth_first = extract_author_surnames(" and ".join(auth["authors"]))
        if local_first and auth_first and local_first[0] != auth_first[0]:
            issues.append(f"First author mismatch: local='{local_first[0]}' vs auth='{auth_first[0]}'")

    status = "MISMATCH" if issues else "VERIFIED"
    return status, auth, issues


def format_canonical_bibtex(key: str, auth: dict[str, Any]) -> str:
    authors = " and ".join(auth["authors"]) if auth["authors"] else "Unknown"
    lines = [
        f"@misc{{{key},",
        f"  title = {{{auth['title']}}},",
        f"  author = {{{authors}}},",
        f"  year = {{{auth['year'] or ''}}},",
    ]
    if auth.get("venue"):
        lines.append(f"  howpublished = {{{auth['venue']}}},")
    if auth.get("doi"):
        lines.append(f"  doi = {{{auth['doi']}}},")
    if auth.get("arxiv_id"):
        lines.append(f"  eprint = {{{auth['arxiv_id']}}},")
        lines.append("  archivePrefix = {arXiv},")
    if auth.get("url"):
        lines.append(f"  url = {{{auth['url']}}},")
    lines.append("}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify citations against Crossref, arXiv, and DBLP.")
    parser.add_argument("--bib", type=Path, help="Path to .bib file")
    parser.add_argument("--doi", help="Verify a single DOI")
    parser.add_argument("--arxiv", help="Verify a single arXiv ID (e.g. 2004.12832)")
    parser.add_argument("--title", help="Verify a single paper title via DBLP")
    parser.add_argument("--emit-canonical", action="store_true", help="Print canonical BibTeX for verified hits")
    args = parser.parse_args()

    entries: list[dict[str, str]] = []
    if args.bib:
        entries.extend(parse_bib_file(args.bib))
    if args.doi or args.arxiv or args.title:
        entries.append(
            {
                "key": args.arxiv or args.doi or "query",
                "doi": args.doi or "",
                "eprint": args.arxiv or "",
                "title": args.title or "",
            }
        )

    if not entries:
        parser.error("Provide --bib, --doi, --arxiv, or --title")

    has_failure = False
    for e in entries:
        status, auth, issues = verify_record(e)
        print(f"[{status}] {e['key']}")
        if auth:
            print(f"  Source : {auth['provider']} | {auth['year']} | {auth['venue']}")
            print(f"  Title  : {auth['title']}")
            print(f"  Authors: {', '.join(auth['authors'][:5])}")
            if auth.get("doi"):
                print(f"  DOI    : {auth['doi']}")
            if auth.get("arxiv_id"):
                print(f"  arXiv  : {auth['arxiv_id']}")
        for issue in issues:
            print(f"  Issue  : {issue}")
        if args.emit_canonical and auth:
            print(format_canonical_bibtex(e["key"], auth))
        if status == "NOT_FOUND":
            has_failure = True

    return 1 if has_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
