"""
Script: 21_update_config_from_discovery.py

Obiettivo
Preparare una tabella di suggerimenti per aggiornare config/project_config.py
sulla base dei link trovati da 00_discover_sources.py.

Lo script non modifica automaticamente la configurazione. Produce CSV e JSON da
revisionare manualmente.
"""

import pandas as pd

from utils_paths import get_configured_path, ensure_project_folders
from utils_io import write_csv_json_pair


def main():
    ensure_project_folders()
    discovery_path = get_configured_path("discovered_links")
    output_path = get_configured_path("outputs_tables") / "config_update_candidates.csv"
    if not discovery_path.exists():
        print("Run src/00_discover_sources.py first.")
        return
    links = pd.read_csv(discovery_path)
    if "status" not in links.columns:
        candidates = pd.DataFrame()
    else:
        candidates = links[links["status"] == "candidate_download"].copy()
    write_csv_json_pair(candidates, output_path.parent, output_path.stem)
    print(f"Config update candidates written to {output_path}")


if __name__ == "__main__":
    main()
