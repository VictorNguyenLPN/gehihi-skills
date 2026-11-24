#!/usr/bin/env python3
"""Query arXiv, Semantic Scholar, OpenAlex, DBLP, and Crossref using Python stdlib only."""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

USER_AGENT = "lit-search-verify/1.0 (mailto:research@local)"
TIMEOUT = 15


def http_get(url: str, extra_headers: dict[str, str] | None = None) -> bytes:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json, application/atom+xml, text/xml"}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        ctype = resp.headers.get("Content-Type", "")
        if "text/html" in ctype:
            raise urllib.error.URLError(f"Received HTML instead of API payload (Content-Type: {ctype})")
        return resp.read()


def clean_ws(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def parse_year_filter(year_arg: str | None) -> tuple[int | None, int | None]:
    if not year_arg:
        return None, None
    if "-" in year_arg:
        start_s, end_s = year_arg.split("-", 1)
        return (int(start_s) if start_s else None, int(end_s) if end_s else None)
    y = int(year_arg)
    return y, y


def year_in_range(year: int | None, y_min: int | None, y_max: int | None) -> bool:
    if y_min is None and y_max is None:
        return True
    if year is None:
        return False
    if y_min is not None and year < y_min:
        return False
    if y_max is not None and year > y_max:
        return False
    return True


def search_arxiv(query: str, limit: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {"search_query": f"all:{query}", "start": 0, "max_results": limit}
    )
    raw = http_get(f"http://export.arxiv.org/api/query?{params}")
    root = ET.fromstring(raw)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    results = []
    for entry in root.findall("atom:entry", ns):
        id_url = clean_ws(entry.findtext("atom:id", "", ns))
        arxiv_id = id_url.rsplit("/abs/", 1)[-1].split("v")[0] if "/abs/" in id_url else id_url
        published = clean_ws(entry.findtext("atom:published", "", ns))
        year = int(published[:4]) if len(published) >= 4 and published[:4].isdigit() else None
        authors = [
            clean_ws(a.findtext("atom:name", "", ns))
            for a in entry.findall("atom:author", ns)
        ]
        doi = clean_ws(entry.findtext("arxiv:doi", "", ns)) or None
        venue = clean_ws(entry.findtext("arxiv:journal_ref", "", ns)) or "arXiv"
        results.append(
            {
                "source": "arxiv",
                "title": clean_ws(entry.findtext("atom:title", "", ns)),
                "authors": [a for a in authors if a],
                "year": year,
                "venue": venue,
                "doi": doi,
                "arxiv_id": arxiv_id,
                "url": id_url,
                "citation_count": None,
                "abstract": clean_ws(entry.findtext("atom:summary", "", ns)),
            }
        )
    return results


def search_s2(query: str, limit: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,venue,externalIds,url,abstract,citationCount",
        }
    )
    data = json.loads(
        http_get(f"https://api.semanticscholar.org/graph/v1/paper/search?{params}")
    )
    results = []
    for item in data.get("data", []):
        ext = item.get("externalIds") or {}
        results.append(
            {
                "source": "s2",
                "title": clean_ws(item.get("title")),
                "authors": [a.get("name", "") for a in item.get("authors") or [] if a.get("name")],
                "year": item.get("year"),
                "venue": clean_ws(item.get("venue")) or "Unknown",
                "doi": ext.get("DOI"),
                "arxiv_id": ext.get("ArXiv"),
                "url": item.get("url") or "",
                "citation_count": item.get("citationCount"),
                "abstract": clean_ws(item.get("abstract")),
            }
        )
    return results


def reconstruct_openalex_abstract(inv_idx: dict[str, list[int]] | None) -> str:
    if not inv_idx:
        return ""
    pos_words: dict[int, str] = {}
    for word, positions in inv_idx.items():
        for p in positions:
            pos_words[p] = word
    return " ".join(pos_words[i] for i in sorted(pos_words))


def search_openalex(query: str, limit: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"search": query, "per-page": limit})
    data = json.loads(http_get(f"https://api.openalex.org/works?{params}"))
    results = []
    for w in data.get("results", []):
        doi_url = w.get("doi") or ""
        doi = doi_url.replace("https://doi.org/", "") if doi_url else None
        loc = w.get("primary_location") or {}
        src = loc.get("source") or {}
        authors = [
            (a.get("author") or {}).get("display_name", "")
            for a in w.get("authorships") or []
        ]
        results.append(
            {
                "source": "openalex",
                "title": clean_ws(w.get("title")),
                "authors": [a for a in authors if a],
                "year": w.get("publication_year"),
                "venue": clean_ws(src.get("display_name")) or "Unknown",
                "doi": doi,
                "arxiv_id": None,
                "url": doi_url or w.get("id") or "",
                "citation_count": w.get("cited_by_count"),
                "abstract": clean_ws(
                    reconstruct_openalex_abstract(w.get("abstract_inverted_index"))
                ),
            }
        )
    return results


def search_dblp(query: str, limit: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"q": query, "h": limit, "format": "json"})
    data = json.loads(http_get(f"https://dblp.org/search/publ/api?{params}"))
    hits = ((data.get("result") or {}).get("hits") or {}).get("hit") or []
    results = []
    for h in hits:
        info = h.get("info") or {}
        raw_authors = (info.get("authors") or {}).get("author") or []
        if isinstance(raw_authors, dict):
            raw_authors = [raw_authors]
        authors = [
            a.get("text", "") if isinstance(a, dict) else str(a) for a in raw_authors
        ]
        year_s = str(info.get("year") or "")
        year = int(year_s) if year_s.isdigit() else None
        results.append(
            {
                "source": "dblp",
                "title": clean_ws(info.get("title")).rstrip("."),
                "authors": [a for a in authors if a],
                "year": year,
                "venue": clean_ws(info.get("venue")) or "DBLP",
                "doi": info.get("doi"),
                "arxiv_id": None,
                "url": info.get("ee") or info.get("url") or "",
                "citation_count": None,
                "abstract": "",
            }
        )
    return results


def search_crossref(query: str, limit: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"query": query, "rows": limit})
    data = json.loads(http_get(f"https://api.crossref.org/works?{params}"))
    items = (data.get("message") or {}).get("items") or []
    results = []
    for item in items:
        titles = item.get("title") or []
        title = clean_ws(titles[0]) if titles else ""
        authors = []
        for a in item.get("author") or []:
            full = f"{a.get('given', '')} {a.get('family', '')}".strip()
            if full:
                authors.append(full)
        issued = ((item.get("issued") or {}).get("date-parts") or [[None]])[0]
        year = issued[0] if issued and isinstance(issued[0], int) else None
        containers = item.get("container-title") or []
        venue = clean_ws(containers[0]) if containers else "Crossref"
        results.append(
            {
                "source": "crossref",
                "title": title,
                "authors": authors,
                "year": year,
                "venue": venue,
                "doi": item.get("DOI"),
                "arxiv_id": None,
                "url": item.get("URL") or "",
                "citation_count": item.get("is-referenced-by-count"),
                "abstract": clean_ws(re.sub(r"<[^>]+>", " ", item.get("abstract") or "")),
            }
        )
    return results


SOURCES = {
    "arxiv": search_arxiv,
    "s2": search_s2,
    "openalex": search_openalex,
    "dblp": search_dblp,
    "crossref": search_crossref,
}


def make_citekey(p: dict[str, Any]) -> str:
    first_author = (p["authors"][0].split()[-1] if p["authors"] else "unknown").lower()
    first_author = re.sub(r"[^a-z0-9]", "", first_author) or "unknown"
    year = p["year"] or "nd"
    first_word = re.sub(r"[^a-z0-9]", "", (p["title"].split()[0] if p["title"] else "paper").lower())
    return f"{first_author}{year}{first_word}"


def to_bibtex(p: dict[str, Any]) -> str:
    key = make_citekey(p)
    authors = " and ".join(p["authors"]) if p["authors"] else "Unknown"
    lines = [
        f"@misc{{{key},",
        f"  title = {{{p['title']}}},",
        f"  author = {{{authors}}},",
        f"  year = {{{p['year'] or ''}}},",
    ]
    if p["venue"]:
        lines.append(f"  howpublished = {{{p['venue']}}},")
    if p["doi"]:
        lines.append(f"  doi = {{{p['doi']}}},")
    if p["arxiv_id"]:
        lines.append(f"  eprint = {{{p['arxiv_id']}}},")
        lines.append("  archivePrefix = {arXiv},")
    if p["url"]:
        lines.append(f"  url = {{{p['url']}}},")
    lines.append("}")
    return "\n".join(lines)


def format_markdown(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No results found."
    out = []
    for i, p in enumerate(results, 1):
        authors = ", ".join(p["authors"][:5]) + (" et al." if len(p["authors"]) > 5 else "")
        ids = []
        if p["doi"]:
            ids.append(f"DOI: `{p['doi']}`")
        if p["arxiv_id"]:
            ids.append(f"arXiv: `{p['arxiv_id']}`")
        if p["citation_count"] is not None:
            ids.append(f"Citations: {p['citation_count']}")
        meta = " | ".join([str(p["year"] or "n.d."), p["venue"], *ids])
        out.append(f"### {i}. [{p['source']}] {p['title']}\n- **Authors**: {authors or 'Unknown'}\n- **Metadata**: {meta}\n- **URL**: {p['url']}")
        if p["abstract"]:
            snippet = p["abstract"][:350] + ("..." if len(p["abstract"]) > 350 else "")
            out.append(f"- **Abstract**: {snippet}")
    return "\n\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Search academic literature across primary APIs.")
    parser.add_argument("--query", required=True, help="Search query string")
    parser.add_argument(
        "--source",
        default="all",
        choices=["all", *SOURCES.keys()],
        help="Target academic API",
    )
    parser.add_argument("--limit", type=int, default=5, help="Max results per source")
    parser.add_argument("--year", help="Year or range, e.g. 2024 or 2022-2025")
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "json", "bibtex"],
        help="Output format",
    )
    args = parser.parse_args()

    y_min, y_max = parse_year_filter(args.year)
    selected = list(SOURCES.keys()) if args.source == "all" else [args.source]

    all_results: list[dict[str, Any]] = []
    errors: list[str] = []
    for src in selected:
        try:
            items = SOURCES[src](args.query, args.limit)
            all_results.extend(
                p for p in items if year_in_range(p.get("year"), y_min, y_max)
            )
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, ET.ParseError) as exc:
            errors.append(f"[{src}] {exc}")

    if errors:
        print("\n".join(errors), file=sys.stderr)

    if args.format == "json":
        print(json.dumps(all_results, indent=2, ensure_ascii=False))
    elif args.format == "bibtex":
        print("\n\n".join(to_bibtex(p) for p in all_results))
    else:
        print(format_markdown(all_results))

    return 0 if all_results or not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
