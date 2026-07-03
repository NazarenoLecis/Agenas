"""
Script: 35_regional_sources_seed.py

Crea una tabella seed per mappare fonti regionali sanitarie da completare manualmente.
"""

import pandas as pd

from utils_paths import get_configured_path, ensure_project_folders


REGIONS = [
    "Piemonte", "Valle d Aosta", "Lombardia", "Bolzano", "Trento", "Veneto",
    "Friuli Venezia Giulia", "Liguria", "Emilia Romagna", "Toscana", "Umbria",
    "Marche", "Lazio", "Abruzzo", "Molise", "Campania", "Puglia",
    "Basilicata", "Calabria", "Sicilia", "Sardegna",
]

MODULES = ["waiting_times", "services", "emergency", "structures", "workforce", "costs"]


def main():
    ensure_project_folders()
    rows = []
    for region in REGIONS:
        for module in MODULES:
            rows.append({
                "region": region,
                "module_id": module,
                "source_page_url": "",
                "download_url": "",
                "license": "da_verificare",
                "status": "to_map",
                "notes": "",
            })
    output_path = get_configured_path("data_catalog").parent / "regional_sources_seed.csv"
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"Regional source seed written to {output_path}")


if __name__ == "__main__":
    main()
