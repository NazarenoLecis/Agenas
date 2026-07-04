"""
Script: 17_module_inventory.py

Obiettivo
Elencare i moduli tematici disponibili nel repository.
"""

from pathlib import Path
import pandas as pd

from utils_paths import get_project_root, get_configured_path, ensure_project_folders
from utils_io import write_csv_json_pair


EXCLUDED_PREFIXES = ["utils_"]


def is_script_module(path):
    if path.name.startswith("__"):
        return False
    if any(path.name.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    return path.suffix == ".py"


def main():
    ensure_project_folders()
    root = get_project_root()
    src = root / "src"
    module_files = sorted([path for path in src.glob("*.py") if is_script_module(path)])
    rows = [{"file": path.name, "path": str(path.relative_to(root))} for path in module_files]
    output_path = get_configured_path("outputs_tables") / "module_inventory.csv"
    write_csv_json_pair(pd.DataFrame(rows), output_path.parent, output_path.stem)
    print(f"Module inventory written to {output_path}")


if __name__ == "__main__":
    main()
