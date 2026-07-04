"""
Script: 50_health_expenditure_registry.py

Costruisce un registry unico delle fonti operative per il modulo spesa sanitaria.

Combina:
- risorse OpenBDAP da API CKAN
- link SIOPE
- link ISTAT demografia
- dataset registry generale

Produce CSV e JSON.
"""

import pandas as pd

from utils_paths import get_configured_path, ensure_project_folders
from utils_io import write_csv_json_pair


OUTPUT_COLUMNS = [
    "provider", "source_id", "source_role", "source_type", "dataset_name",
    "candidate_url", "format", "accounting_basis", "theme", "relevance_score",
    "license", "notes",
]


def read_csv_if_exists(path):
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def align_columns(df):
    output = df.copy() if not df.empty else pd.DataFrame()
    for column in OUTPUT_COLUMNS:
        if column not in output.columns:
            output[column] = ""
    return output[OUTPUT_COLUMNS]


def openbdap_rows(tables_root):
    path = tables_root / "openbdap_health_expenditure_resources.csv"
    df = read_csv_if_exists(path)
    if df.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    rows = pd.DataFrame({
        "provider": df.get("provider", "OpenBDAP / RGS"),
        "source_id": df.get("package_name", "openbdap_ckan"),
        "source_role": "health_expenditure_accrual_or_cash_candidate",
        "source_type": "ckan_resource",
        "dataset_name": df.get("package_title", ""),
        "candidate_url": df.get("resource_url", ""),
        "format": df.get("resource_format", ""),
        "accounting_basis": df.apply(lambda row: "cassa_siope" if "siope" in str(row.to_dict()).lower() or "movimenti di cassa" in str(row.to_dict()).lower() else "competenza_ce", axis=1),
        "theme": "health_expenditure",
        "relevance_score": df.get("relevance_score", ""),
        "license": df.get("license_title", ""),
        "notes": df.get("package_notes", ""),
    })
    return align_columns(rows)


def istat_rows(tables_root):
    path = tables_root / "istat_demography_links.csv"
    df = read_csv_if_exists(path)
    if df.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    rows = pd.DataFrame({
        "provider": df.get("provider", "ISTAT"),
        "source_id": df.get("source_id", "istat_demography"),
        "source_role": df.get("source_role", "demography_denominators"),
        "source_type": df.get("link_type", "page_candidate"),
        "dataset_name": "ISTAT demography denominator candidate",
        "candidate_url": df.get("url", ""),
        "format": df.get("link_type", ""),
        "accounting_basis": "",
        "theme": "demography_denominators",
        "relevance_score": "",
        "license": "da_verificare",
        "notes": df.get("link_text", ""),
    })
    return align_columns(rows)


def siope_rows(tables_root):
    path = tables_root / "siope_links.csv"
    df = read_csv_if_exists(path)
    if df.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    rows = pd.DataFrame({
        "provider": df.get("provider", "SIOPE"),
        "source_id": df.get("source_id", "siope"),
        "source_role": "cash_payments_and_revenues",
        "source_type": df.get("link_type", "page_candidate"),
        "dataset_name": "SIOPE cash flow candidate",
        "candidate_url": df.get("url", ""),
        "format": df.get("link_type", ""),
        "accounting_basis": "cassa_siope",
        "theme": "health_expenditure",
        "relevance_score": "",
        "license": "da_verificare",
        "notes": df.get("link_text", ""),
    })
    return align_columns(rows)


def configured_rows():
    path = get_configured_path("outputs_tables") / "dataset_registry.csv"
    df = read_csv_if_exists(path)
    if df.empty or "theme" not in df.columns:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    df = df[df["theme"].isin(["health_expenditure", "demography_denominators", "price_deflators", "costs"])] if "theme" in df.columns else pd.DataFrame()
    if df.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    rows = pd.DataFrame({
        "provider": df.get("provider", ""),
        "source_id": df.get("source_id", ""),
        "source_role": "configured_source",
        "source_type": df.get("access_type", ""),
        "dataset_name": df.get("dataset_name", ""),
        "candidate_url": df.get("candidate_url", df.get("source_page_url", "")),
        "format": "",
        "accounting_basis": df.apply(lambda row: "cassa_siope" if str(row.get("provider", "")).lower() == "siope" else "", axis=1),
        "theme": df.get("theme", ""),
        "relevance_score": "",
        "license": df.get("license", ""),
        "notes": df.get("notes", ""),
    })
    return align_columns(rows)


def main():
    ensure_project_folders()
    tables_root = get_configured_path("outputs_tables")
    frames = [configured_rows(), openbdap_rows(tables_root), istat_rows(tables_root), siope_rows(tables_root)]
    output = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=OUTPUT_COLUMNS)
    output = align_columns(output)
    output = output.drop_duplicates()
    if "relevance_score" in output.columns:
        output["relevance_score_numeric"] = pd.to_numeric(output["relevance_score"], errors="coerce").fillna(0)
        output = output.sort_values(["relevance_score_numeric", "provider", "dataset_name"], ascending=[False, True, True]).drop(columns=["relevance_score_numeric"])
    output_path = tables_root / "health_expenditure_registry.csv"
    write_csv_json_pair(output, output_path.parent, output_path.stem)
    print(f"Health expenditure registry written to {output_path}")


if __name__ == "__main__":
    main()
