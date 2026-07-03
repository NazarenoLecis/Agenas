"""
Script: 06_export_json.py

Obiettivo
Creare file JSON leggeri da usare in dashboard statiche.

Il file legge le tabelle in outputs/tables e le esporta in outputs/dashboard_data
con un blocco metadata e una lista data.
"""

from datetime import datetime
from pathlib import Path

from utils_paths import get_configured_path, ensure_project_folders
from utils_io import read_table, write_json_object


def table_to_dashboard_json(table_path):
    df = read_table(table_path)
    return {
        "metadata": {
            "dataset_name": table_path.stem,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "source": "generated_by_repository",
        },
        "data": df.to_dict(orient="records"),
    }


def main():
    ensure_project_folders()
    tables_root = get_configured_path("outputs_tables")
    dashboard_root = get_configured_path("outputs_dashboard")
    csv_files = list(Path(tables_root).glob("*.csv"))
    for table_path in csv_files:
        output_path = dashboard_root / f"{table_path.stem}.json"
        payload = table_to_dashboard_json(table_path)
        write_json_object(payload, output_path)
    print(f"Exported {len(csv_files)} JSON files")


if __name__ == "__main__":
    main()
