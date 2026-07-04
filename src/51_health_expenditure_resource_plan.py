"""
Script: 51_health_expenditure_resource_plan.py

Crea un piano operativo delle risorse candidate del modulo spesa sanitaria.
Lo script produce CSV e JSON da revisionare prima di acquisire dati locali.
"""

import re
import pandas as pd

from utils_paths import get_configured_path, ensure_project_folders
from utils_io import write_csv_json_pair
from utils_download import infer_extension_from_url


ALLOWED_FORMATS = {"csv", "json", "xml", "xlsx", "xls", "zip", "ods"}


def safe_name(value):
    name = re.sub(r"[^a-zA-Z0-9]+", "_", str(value or "").strip()).strip("_").lower()
    return name or "resource"


def read_registry():
    path = get_configured_path("outputs_tables") / "health_expenditure_registry.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def normalize_format(row):
    fmt = str(row.get("format", "") or "").lower().replace(".", "")
    url = str(row.get("candidate_url", "") or "")
    if fmt not in ALLOWED_FORMATS and url:
        fmt = infer_extension_from_url(url)
    return fmt


def build_plan(registry):
    if registry.empty:
        return pd.DataFrame()
    output = registry.copy()
    output["candidate_url"] = output["candidate_url"].fillna("").astype(str).str.strip()
    output = output[output["candidate_url"] != ""]
    if output.empty:
        return pd.DataFrame()
    output["file_format"] = output.apply(normalize_format, axis=1)
    output = output[output["file_format"].isin(ALLOWED_FORMATS)]
    output = output.drop_duplicates(subset=["candidate_url"])
    output["recommended_local_folder"] = output.apply(lambda row: f"data/external/health_expenditure/{safe_name(row.get('provider', 'source'))}", axis=1)
    output["recommended_file_stem"] = output.apply(lambda row: safe_name("_".join([str(row.get("source_id", "")), str(row.get("dataset_name", ""))]))[:120], axis=1)
    output["resource_status"] = "planned_manual_review"
    return output


def main():
    ensure_project_folders()
    registry = read_registry()
    plan = build_plan(registry)
    output_path = get_configured_path("outputs_tables") / "health_expenditure_resource_plan.csv"
    write_csv_json_pair(plan, output_path.parent, output_path.stem)
    print(f"Health expenditure resource plan written to {output_path}")


if __name__ == "__main__":
    main()
