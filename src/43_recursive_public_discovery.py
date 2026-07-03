"""
Script: 43_recursive_public_discovery.py

Discovery controllata delle pagine pubbliche configurate.

Lo script segue link interni allo stesso dominio fino a una profondita limitata e
salva tutti i link candidati a dataset, report o pagine di dati. Non accede ad
aree riservate e non usa credenziali.
"""

from collections import deque
from urllib.parse import urljoin, urlparse
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils_paths import get_configured_path, ensure_project_folders, load_project_config


HEADERS = {"User-Agent": "Agenas-data-analysis/0.1"}
FILE_EXTENSIONS = [".csv", ".json", ".xml", ".xlsx", ".xls", ".zip", ".pdf", ".ods"]
KEYWORDS = ["download", "scarica", "dataset", "dati", "csv", "json", "xlsx", "open-data", "open data"]
MAX_DEPTH = 1
MAX_PAGES_PER_SOURCE = 25


def same_domain(url, base_url):
    return urlparse(url).netloc == urlparse(base_url).netloc


def classify_link(url, text):
    clean = url.split("?")[0].split("#")[0].lower()
    text_l = str(text).lower()
    if any(clean.endswith(ext) for ext in FILE_EXTENSIONS):
        return "file_candidate"
    if any(keyword in clean or keyword in text_l for keyword in KEYWORDS):
        return "page_candidate"
    return "other"


def fetch_links(page_url):
    response = requests.get(page_url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue
        absolute = urljoin(page_url, href)
        links.append((absolute, link.get_text(" ", strip=True)))
    return links


def discover_source(source):
    start_url = source.get("source_page_url", "")
    queue = deque([(start_url, 0)])
    visited = set()
    rows = []
    checked_at = datetime.now().isoformat(timespec="seconds")
    while queue and len(visited) < MAX_PAGES_PER_SOURCE:
        page_url, depth = queue.popleft()
        if page_url in visited:
            continue
        visited.add(page_url)
        try:
            links = fetch_links(page_url)
        except Exception as error:
            rows.append({"source_id": source.get("source_id"), "provider": source.get("provider"), "page_url": page_url, "found_url": "", "link_text": "", "link_type": "error", "depth": depth, "checked_at": checked_at, "error": str(error)})
            continue
        for found_url, text in links:
            link_type = classify_link(found_url, text)
            if link_type != "other":
                rows.append({"source_id": source.get("source_id"), "provider": source.get("provider"), "page_url": page_url, "found_url": found_url, "link_text": text, "link_type": link_type, "depth": depth, "checked_at": checked_at, "error": ""})
            if depth < MAX_DEPTH and same_domain(found_url, start_url) and found_url not in visited:
                queue.append((found_url, depth + 1))
    return rows


def main():
    ensure_project_folders()
    config = load_project_config()
    rows = []
    for source in config.SOURCES:
        rows.extend(discover_source(source))
    output_path = get_configured_path("outputs_tables") / "recursive_public_discovery.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"Recursive discovery written to {output_path}")


if __name__ == "__main__":
    main()
