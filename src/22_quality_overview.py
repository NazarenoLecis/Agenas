"""
Script: 22_quality_overview.py

Obiettivo
Creare una sintesi minima dello stato della pipeline e dei file prodotti.
"""

from pathlib import Path
import pandas as pd

from utils_paths import get_project_root, get_configured_path, ensure_project_folders
from utils_io import write_csv_json_pair


def count_files(folder):
    folder = Path(folder)
    if not folder.exists():
        return 0
    return sum(1 for path in folder.rglob("*") if path.is_file())


def main():
    ensure_project_folders()
    root = get_project_root()
    rows = []
    for key in ["data_raw", "data_processed", "outputs_tables", "outputs_figures", "outputs_dashboard"]:
        folder = get_configured_path(key)
        rows.append({"area": key, "path": str(folder.relative_to(root)), "files": count_files(folder)})
    output_path = get_configured_path("outputs_reports") / "pipeline_quality_overview.csv"
    write_csv_json_pair(pd.DataFrame(rows), output_path.parent, output_path.stem)
    print(f"Quality overview written to {output_path}")


if __name__ == "__main__":
    main()
