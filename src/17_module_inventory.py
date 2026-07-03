"""
Script: 17_module_inventory.py

Obiettivo
Elencare i moduli tematici disponibili nel repository.
"""

from pathlib import Path
import pandas as pd

from utils_paths import get_project_root, get_configured_path, ensure_project_folders


def main():
    ensure_project_folders()
    root = get_project_root()
    src = root / "src"
    module_files = sorted(src.glob("0*_*.py")) + sorted(src.glob("1*_*.py"))
    rows = [{"file": path.name, "path": str(path.relative_to(root))} for path in module_files]
    output_path = get_configured_path("outputs_tables") / "module_inventory.csv"
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(f"Module inventory written to {output_path}")


if __name__ == "__main__":
    main()
