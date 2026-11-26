"""Refresh citation data for the academic site.

Free, key-less sources only:
- OpenAlex (https://api.openalex.org): works, cited-by count, h-index.
- Semantic Scholar (https://api.semanticscholar.org): per-paper citation counts.

Google Scholar has no public API and blocks automated access, and Scopus
metrics need an Elsevier API key, so those numbers in data/metrics.json are
updated on a manual re-check and the script leaves them untouched.
Run: python3 scripts/update_metrics.py  (then scripts/build_site.py)
"""
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

ORCID = "0000-0002-8136-8397"
AUTHOR_NAME = "Mahmoud M. Abdelatty"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "academic-site-updater (mailto:mma34@fayoum.edu.eg)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def update_openalex(metrics):
    q = urllib.parse.quote(AUTHOR_NAME)
    results = get(f"https://api.openalex.org/authors?search={q}").get("results", [])
    mine = next((a for a in results if any(
        (i or {}).get("display_name") == "Fayoum University" for i in a.get("last_known_institutions", []))), None)
    if not mine:
        print("OpenAlex: author not found, keeping existing values")
        return
    metrics["openalex"] = {
        "citations": mine.get("cited_by_count"),
        "works": mine.get("works_count"),
        "h_index": (mine.get("summary_stats") or {}).get("h_index"),
        "source": "https://openalex.org",
        "auto_update": True,
        "author_id": mine.get("id"),
        "author_search": AUTHOR_NAME,
        "as_of": time.strftime("%Y-%m-%d"),  # only set on a successful fetch
    }


def update_publication_counts(pubs):
    """Refresh ONLY the OpenAlex per-paper counts.
    scholar_citations are verified against the live Scholar profile and are
    never overwritten automatically: Scholar has no public API."""
    for pub in pubs["published"]:
        doi = pub.get("doi")
        if not doi:
            continue
        try:
            work = get(f"https://api.openalex.org/works/https://doi.org/{doi}")
            pub["openalex_citations"] = work.get("cited_by_count")
            time.sleep(0.2)
        except Exception as e:
            print(f"OpenAlex per-paper lookup failed for {doi}: {e}")


def detect_new_publications(pubs):
    """Add OpenAlex-indexed works by this author that are missing from the list."""
    metrics = json.loads((DATA / "metrics.json").read_text())
    author_id = (metrics.get("openalex") or {}).get("author_id")
    if not author_id:
        return
    works = get(f"https://api.openalex.org/works?filter=author.id:{author_id}&per-page=50").get("results", [])
    known = {p.get("doi", "").lower() for p in pubs["published"]}
    for w in works:
        doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
        if doi and doi not in known:
            pubs["published"].append({
                "title": w.get("title"),
                "authors": ", ".join(a["author"]["display_name"] for a in w.get("authorships", [])),
                "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
                "doi": doi,
                "openalex_citations": w.get("cited_by_count"),
                "auto_detected": True,
            })
            print(f"New publication auto-added: {w.get('title')}")


def main():
    metrics = json.loads((DATA / "metrics.json").read_text())
    pubs = json.loads((DATA / "publications.json").read_text())
    update_openalex(metrics)
    detect_new_publications(pubs)
    update_publication_counts(pubs)
    # Per-database as_of dates live inside each metrics block and in
    # publications.json (scholar_as_of); a date changes only after a
    # successful fetch for that database. Scholar/Scopus blocks are
    # untouched here (no free API), so their dates survive refreshes.
    (DATA / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n")
    (DATA / "publications.json").write_text(json.dumps(pubs, indent=2, ensure_ascii=False) + "\n")
    print("metrics.json and publications.json refreshed")


if __name__ == "__main__":
    main()
