"""
Script: 44_agenas_links.py

Estrae link dal Portale Statistico Agenas, inclusi report e pagine collegate.
"""

from urllib.parse import urljoin
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils_paths import get_configured_path, ensure_project_folders, load_project_config


HEADERS = {"User-Agent": "Agenas-data-analysis/0.1"}


def fetch_links(url):
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    rows = []
    for link in soup.find_all("a"):
        text = link.get_text(" ", strip=True)
        href = link.get("href")
        if not href:
            continue
        absolute = urljoin(url, href)
        if text or "agenas" in absolute.lower():
            rows.append({"link_text": text, "url": absolute})
    return pd.DataFrame(rows).drop_duplicates()


def main():
    ensure_project_folders()
    config = load_project_config()
    sources = [s for s in config.SOURCES if s.get("provider") == "Agenas"]
    frames = []
    for source in sources:
        try:
            df = fetch_links(source.get("source_page_url"))
            df["source_id"] = source.get("source_id")
            df["provider"] = source.get("provider")
            df["checked_at"] = datetime.now().isoformat(timespec="seconds")
            frames.append(df)
        except Exception as error:
            frames.append(pd.DataFrame([{"source_id": source.get("source_id"), "provider": source.get("provider"), "link_text": "", "url": "", "checked_at": datetime.now().isoformat(timespec="seconds"), "error": str(error)}]))
    output = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    output_path = get_configured_path("outputs_tables") / "agenas_links.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)
    print(f"Agenas links written to {output_path}")


if __name__ == "__main__":
    main()
