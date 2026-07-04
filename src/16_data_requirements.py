"""
Script: 16_data_requirements.py

Obiettivo
Creare una tabella con i requisiti minimi dei dati per ogni ambito di analisi.
"""

import pandas as pd

from utils_paths import get_configured_path, ensure_project_folders
from utils_io import write_csv_json_pair


REQUIREMENTS = [
    {"module_id": "mobility_flows", "required_fields": "origin;destination;service_or_drg;year;volume;economic_value"},
    {"module_id": "mobility_complexity", "required_fields": "drg;mdc;discipline;service;admission_type;volume;economic_value"},
    {"module_id": "workforce", "required_fields": "region;asl;structure;profession;category;year;staff_count"},
    {"module_id": "waiting_times", "required_fields": "region;service;priority_class;period;waiting_time;volume"},
    {"module_id": "costs", "required_fields": "region;provider;cost_item;year;amount"},
    {"module_id": "health_expenditure", "required_fields": "year;region_name;accounting_basis;spending_area;amount_nominal_eur;population_total;relevant_population_type"},
    {"module_id": "services", "required_fields": "region;asl;structure;service;year;volume"},
    {"module_id": "emergency", "required_fields": "region;structure;triage;outcome;period;accesses;time"},
    {"module_id": "hospital_activity", "required_fields": "region;structure;drg;discipline;admission_type;year;volume;days"},
    {"module_id": "demography_denominators", "required_fields": "year;region_name;population_total;population_65_plus;population_75_plus;population_80_plus"},
    {"module_id": "price_deflators", "required_fields": "year;deflator_used;price_index;price_base_year"},
]


def main():
    ensure_project_folders()
    output_path = get_configured_path("outputs_tables") / "data_requirements.csv"
    write_csv_json_pair(pd.DataFrame(REQUIREMENTS), output_path.parent, output_path.stem)
    print(f"Data requirements written to {output_path}")


if __name__ == "__main__":
    main()
