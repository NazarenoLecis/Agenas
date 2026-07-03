"""
Script: 00_discover_sources.py

Obiettivo
Leggere le fonti indicate in config/project_config.py e creare una tabella di
controllo dei link pubblici da verificare.

Come usare
1. Aggiornare config/project_config.py.
2. Eseguire python src/00_discover_sources.py dalla radice del repository.
3. Controllare data_catalog/discovered_links.csv.
"""

from datetime import datetime
import pandas as pd

from utils_paths import get_project_root, get_configured_path, load_project_config


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
            "status": "manual_review_required",
        })
    return pd.DataFrame(rows)


def main():
    root = get_project_root()
    config = load_project_config()
    output_path = get_configured_path("discovered_links")
    df = build_empty_discovery_table(config.SOURCES)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Discovery table written to {output_path.relative_to(root)}")


if __name__ == "__main__":
    main()
