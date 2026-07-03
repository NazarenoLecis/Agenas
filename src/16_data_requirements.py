"""
Script: 16_data_requirements.py

Obiettivo
Creare una tabella con i requisiti minimi dei dati per ogni ambito di analisi.
"""

import pandas as pd

from utils_paths import get_configured_path, ensure_project_folders


REQUIREMENTS = [
    {"module_id": "mobility_flows", "required_fields": "origin;destination;service_or_drg;year;volume;economic_value"},
    {"module_id": "mobility_complexity", "required_fields": "drg;mdc;discipline;service;admission_type;volume;economic_value"},
    {"module_id": "workforce", "required_fields": "region;asl;structure;profession;category;year;staff_count"},
    {"module_id": "waiting_times", "required_fields": "region;service;priority_class;period;waiting_time;volume"},
    {"module_id": "costs", "required_fields": "region;provider;cost_item;year;amount"},
    {"module_id": "services", "required_fields": "region;asl;structure;service;year;volume"},
    {"module_id": "emergency", "required_fields": "region;structure;triage;outcome;period;accesses;time"},
    {"module_id": "hospital_activity", "required_fields": "region;structure;drg;discipline;admission_type;year;volume;days"},
]


def main():
    ensure_project_folders()
    output_path = get_configured_path("outputs_tables") / "data_requirements.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(REQUIREMENTS).to_csv(output_path, index=False)
    print(f"Data requirements written to {output_path}")


if __name__ == "__main__":
    main()
