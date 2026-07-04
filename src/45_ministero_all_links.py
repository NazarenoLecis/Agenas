"""
Script: 45_ministero_all_links.py

Estrae link e candidati dataset dal portale Open Data del Ministero della Salute.
"""

from urllib.parse import urljoin, urlparse
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

from utils_paths import get_configured_path, ensure_project_folders
from utils_io import write_csv_json_pair


URL = "https://www.dati.salute.gov.it/"
HEADERS = {"User-Agent": "Agenas-data-analysis/0.1"}
KEYWORDS = ["dataset", "csv", "json", "xml", "download", "scarica", "dati", "open"]
SKIP_SCHEMES = {"mailto", "tel", "javascript", "data"}


def is_http_url(url):
    return urlparse(str(url)).scheme in {"http", "https"}


def main():
    ensure_project_folders()
    rows = []
    try:
        response = requests.get(URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        for link in soup.find_all("a"):
            href = link.get("href")
            text = link.get_text(" ", strip=True)
            if not href or urlparse(href).scheme in SKIP_SCHEMES:
                continue
            absolute = urljoin(URL, href)
            if not is_http_url(absolute):
                continue
            marker = f"{absolute} {text}".lower()
            if any(keyword in marker for keyword in KEYWORDS):
                rows.append({"url": absolute, "link_text": text, "checked_at": datetime.now().isoformat(timespec="seconds"), "error": ""})
    except Exception as error:
        rows.append({"url": URL, "link_text": "", "checked_at": datetime.now().isoformat(timespec="seconds"), "error": str(error)})
    output_path = get_configured_path("outputs_tables") / "ministero_all_links.csv"
    output = pd.DataFrame(rows).drop_duplicates()
    write_csv_json_pair(output, output_path.parent, output_path.stem)
    print(f"Ministero links written to {output_path}")


if __name__ == "__main__":
    main()
