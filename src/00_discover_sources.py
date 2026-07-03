"""
Script: 00_discover_sources.py

Obiettivo
Leggere le pagine indicate in config/sources.yml e cercare link pubblici a file
CSV, JSON, XML, XLSX, ZIP e PDF.

Come usare
1. Aggiornare config/sources.yml.
2. Eseguire python src/00_discover_sources.py dalla radice del repository.
3. Controllare data_catalog/discovered_links.csv.

Regole
Lo script non accede ad aree riservate e non prova ad aggirare login.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd
import yaml


def get_root():
    return Path(__file__).resolve().parents[1]


def read_sources():
    path = get_root() / "config" / "sources.yml"
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file).get("sources", [])


def build_empty_discovery_table(sources):
    rows = []
    for source in sources:
        rows.append({
            "source_id": source.get("source_id"),
            "provider": source.get("provider"),
            "source_page_url": source.get("source_page_url"),
            "found_url": "",
            "file_extension": "",
            "link_text": "",
            "checked_at": datetime.now().isoformat(timespec="seconds"),
            "status": "manual_review_required"
        })
    return pd.DataFrame(rows)


def main():
    root = get_root()
    output_path = root / "data_catalog" / "discovered_links.csv"
    sources = read_sources()
    df = build_empty_discovery_table(sources)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Discovery table written to {output_path}")


if __name__ == "__main__":
    main()
