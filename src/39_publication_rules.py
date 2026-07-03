"""
Script: 39_publication_rules.py

Definisce regole minime per pubblicare output aggregati.
"""

import pandas as pd

from utils_paths import get_configured_path, ensure_project_folders


RULES = [
    {"output_type": "cell_count", "minimum_value": 5, "rule": "do_not_publish_small_cells"},
    {"output_type": "regional_indicator", "minimum_value": 1, "rule": "ok_if_aggregated"},
    {"output_type": "structure_indicator", "minimum_value": 5, "rule": "review_if_low_volume"},
]


def main():
    ensure_project_folders()
    output_path = get_configured_path("outputs_tables") / "publication_rules.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(RULES).to_csv(output_path, index=False)
    print(f"Publication rules written to {output_path}")


if __name__ == "__main__":
    main()
