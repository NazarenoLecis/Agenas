"""
Script: 52_build_health_expenditure_framework.py

Obiettivo
Preparare il modulo per spesa sanitaria regionale, popolazione, deflatori e
indicatori pro capite o per popolazione demografica rilevante.

Lo script produce sempre CSV e JSON. Quando gli input locali sono disponibili,
costruisce output normalizzati. Quando gli input non sono ancora disponibili,
scrive schema, regole e template operativi.
"""

from pathlib import Path
import importlib.util
import re

import numpy as np
import pandas as pd

from utils_paths import get_project_root, get_configured_path, ensure_project_folders
from utils_io import read_table, write_table


DEMOGRAPHY_INPUT_CANDIDATES = [
    "data/external/istat/demografia/popolazione_eta_regione.csv",
    "data/raw/istat/demografia/popolazione_eta_regione.csv",
    "data/processed/demography/istat_population_by_region_age.csv",
]

BIRTHS_INPUT_CANDIDATES = [
    "data/external/istat/demografia/nascite_regione.csv",
    "data/raw/istat/demografia/nascite_regione.csv",
    "data/processed/demography/istat_births_by_region.csv",
]

DEFLATOR_INPUT_CANDIDATES = [
    "data/external/istat/prezzi/deflatori.csv",
    "data/raw/istat/prezzi/deflatori.csv",
    "data/processed/prices/price_deflators.csv",
]

EXPENDITURE_INPUT_CANDIDATES = [
    "data/processed/health_expenditure/regional_health_expenditure_input.csv",
    "data/interim/health_expenditure/regional_health_expenditure_input.csv",
    "data/external/openbdap/ssn/conto_economico_regionale.csv",
]

SOURCE_PLAN = [
    {
        "source_id": "openbdap_ssn_ce_regionale",
        "provider": "OpenBDAP / RGS",
        "dataset_name": "Conto Economico enti SSN livello regionale",
        "role_in_module": "spesa sanitaria di competenza",
        "accounting_basis": "competenza_ce",
        "source_page_url": "https://bdap-opendata.rgs.mef.gov.it/",
    },
    {
        "source_id": "openbdap_ssn_ce_enti",
        "provider": "OpenBDAP / RGS",
        "dataset_name": "Conto Economico enti del SSN",
        "role_in_module": "dettaglio per ente sanitario",
        "accounting_basis": "competenza_ce",
        "source_page_url": "https://bdap-opendata.rgs.mef.gov.it/",
    },
    {
        "source_id": "siope_ssn_movimenti_cassa",
        "provider": "SIOPE / RGS",
        "dataset_name": "Movimenti di cassa enti SSN",
        "role_in_module": "pagamenti e incassi di cassa",
        "accounting_basis": "cassa_siope",
        "source_page_url": "https://www.siope.it/",
    },
    {
        "source_id": "istat_demo_population_age_region",
        "provider": "ISTAT",
        "dataset_name": "Popolazione residente per eta sesso regione",
        "role_in_module": "denominatori demografici",
        "accounting_basis": "",
        "source_page_url": "https://demo.istat.it/",
    },
    {
        "source_id": "istat_demo_births_region",
        "provider": "ISTAT",
        "dataset_name": "Nati vivi per regione",
        "role_in_module": "denominatore per natalita e neonatologia",
        "accounting_basis": "",
        "source_page_url": "https://demo.istat.it/",
    },
    {
        "source_id": "istat_prices_deflators",
        "provider": "ISTAT",
        "dataset_name": "Indici dei prezzi per deflazione della spesa",
        "role_in_module": "spesa in termini reali",
        "accounting_basis": "",
        "source_page_url": "https://www.istat.it/it/archivio/prezzi+al+consumo",
    },
]

DENOMINATOR_RULES = [
    {"priority": 10, "rule_id": "births", "keywords": ["natal", "nascit", "parto", "parti", "neonat", "punto nascita"], "relevant_population_type": "births"},
    {"priority": 20, "rule_id": "infancy", "keywords": ["infanzia", "infanti", "0-4", "prima infanzia"], "relevant_population_type": "population_0_4"},
    {"priority": 30, "rule_id": "pediatrics", "keywords": ["pediatr", "minori", "adolesc"], "relevant_population_type": "population_0_14"},
    {"priority": 40, "rule_id": "reproductive_health", "keywords": ["consultor", "gravid", "ostetric", "ginecolog", "salute riproduttiva"], "relevant_population_type": "women_15_49"},
    {"priority": 50, "rule_id": "old_age_80", "keywords": ["rsa", "adi anziani", "non autosufficienza", "residenziale anziani"], "relevant_population_type": "population_80_plus"},
    {"priority": 60, "rule_id": "old_age_75", "keywords": ["lungodegenza", "fragil", "residenzialita"], "relevant_population_type": "population_75_plus"},
    {"priority": 70, "rule_id": "old_age_65", "keywords": ["anzian", "cronic", "geriatr", "domiciliare"], "relevant_population_type": "population_65_plus"},
    {"priority": 999, "rule_id": "default_total", "keywords": [], "relevant_population_type": "population_total"},
]

SCHEMA_COLUMNS = [
    "year",
    "region_code",
    "region_name",
    "source",
    "accounting_basis",
    "spending_area",
    "spending_item_code",
    "spending_item_name",
    "amount_nominal_eur",
    "amount_real_eur",
    "price_base_year",
    "deflator_used",
    "population_total",
    "population_0",
    "population_0_4",
    "population_0_14",
    "population_0_17",
    "births",
    "women_15_49",
    "population_65_plus",
    "population_75_plus",
    "population_80_plus",
    "amount_per_capita",
    "amount_per_relevant_population",
    "relevant_population_type",
    "relevant_population_value",
]


def load_health_config():
    root = get_project_root()
    config_path = root / "config" / "health_expenditure_config.py"
    spec = importlib.util.spec_from_file_location("health_expenditure_config", config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_csv_json_pair(df, folder, stem):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    write_table(df, folder / f"{stem}.csv")
    write_table(df, folder / f"{stem}.json")


def find_first_existing_path(root, candidate_paths):
    for relative_path in candidate_paths:
        path = root / relative_path
        if path.exists():
            return path
    return None


def load_optional_table(root, candidate_paths):
    path = find_first_existing_path(root, candidate_paths)
    if path is None:
        return pd.DataFrame(), None
    return read_table(path), path


def clean_column_name(column_name):
    value = str(column_name).strip().lower()
    value = value.replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", "_")
    value = re.sub("_+", "_", value)
    return value.strip("_")


def clean_columns(df):
    if df.empty:
        return df
    output = df.copy()
    output.columns = [clean_column_name(column) for column in output.columns]
    return output


def coalesce_columns(df, candidates, output_column):
    output = df.copy()
    existing = [column for column in candidates if column in output.columns]
    if not existing:
        output[output_column] = np.nan
        return output
    output[output_column] = output[existing].bfill(axis=1).iloc[:, 0]
    return output


def parse_age(age_value):
    if pd.isna(age_value):
        return np.nan
    if isinstance(age_value, (int, float, np.integer, np.floating)):
        return int(age_value)
    value = str(age_value).strip().lower()
    if value in ["totale", "total", "tutte", "all"]:
        return np.nan
    match = re.search(r"\d+", value)
    if match is None:
        return np.nan
    return int(match.group(0))


def normalize_sex(value):
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    if text in ["f", "female", "femmina", "donne", "donna"]:
        return "female"
    if text in ["m", "male", "maschio", "uomini", "uomo"]:
        return "male"
    return text


def normalize_population_table(df):
    if df.empty:
        return pd.DataFrame()
    output = clean_columns(df)
    output = coalesce_columns(output, ["anno", "year", "time", "periodo"], "year")
    output = coalesce_columns(output, ["codice_regione", "region_code", "cod_reg", "codice"], "region_code")
    output = coalesce_columns(output, ["regione", "region_name", "territorio", "ripartizione"], "region_name")
    output = coalesce_columns(output, ["eta", "age", "classe_eta"], "age")
    output = coalesce_columns(output, ["sesso", "sex", "genere"], "sex")
    output = coalesce_columns(output, ["valore", "value", "popolazione", "population", "residenti"], "population")

    required_columns = ["year", "region_name", "age", "population"]
    if any(column not in output.columns for column in required_columns):
        return pd.DataFrame()

    output["year"] = pd.to_numeric(output["year"], errors="coerce")
    output["age_numeric"] = output["age"].apply(parse_age)
    output["sex_normalized"] = output["sex"].apply(normalize_sex)
    output["population"] = pd.to_numeric(output["population"], errors="coerce")
    output["region_name"] = output["region_name"].astype(str).str.strip()
    output["region_code"] = output["region_code"].fillna("").astype(str).str.strip()
    output = output.dropna(subset=["year", "region_name", "age_numeric", "population"])
    output["year"] = output["year"].astype(int)
    output["age_numeric"] = output["age_numeric"].astype(int)
    return output


def sum_population(group, min_age=None, max_age=None, sex=None):
    subset = group
    if min_age is not None:
        subset = subset[subset["age_numeric"] >= min_age]
    if max_age is not None:
        subset = subset[subset["age_numeric"] <= max_age]
    if sex is not None:
        subset = subset[subset["sex_normalized"] == sex]
    return subset["population"].sum()


def build_population_denominators(population_df):
    normalized = normalize_population_table(population_df)
    if normalized.empty:
        return pd.DataFrame()

    rows = []
    for keys, group in normalized.groupby(["year", "region_code", "region_name"], dropna=False):
        year, region_code, region_name = keys
        rows.append({
            "year": int(year),
            "region_code": region_code,
            "region_name": region_name,
            "population_total": sum_population(group),
            "population_0": sum_population(group, 0, 0),
            "population_0_4": sum_population(group, 0, 4),
            "population_0_14": sum_population(group, 0, 14),
            "population_0_17": sum_population(group, 0, 17),
            "women_15_49": sum_population(group, 15, 49, "female"),
            "population_65_plus": sum_population(group, 65, None),
            "population_75_plus": sum_population(group, 75, None),
            "population_80_plus": sum_population(group, 80, None),
        })
    return pd.DataFrame(rows)


def normalize_births_table(df):
    if df.empty:
        return pd.DataFrame()
    output = clean_columns(df)
    output = coalesce_columns(output, ["anno", "year", "time", "periodo"], "year")
    output = coalesce_columns(output, ["codice_regione", "region_code", "cod_reg", "codice"], "region_code")
    output = coalesce_columns(output, ["regione", "region_name", "territorio", "ripartizione"], "region_name")
    output = coalesce_columns(output, ["nati", "nati_vivi", "births", "valore", "value"], "births")
    if any(column not in output.columns for column in ["year", "region_name", "births"]):
        return pd.DataFrame()
    output["year"] = pd.to_numeric(output["year"], errors="coerce")
    output["births"] = pd.to_numeric(output["births"], errors="coerce")
    output["region_name"] = output["region_name"].astype(str).str.strip()
    output["region_code"] = output["region_code"].fillna("").astype(str).str.strip()
    output = output.dropna(subset=["year", "region_name", "births"])
    output["year"] = output["year"].astype(int)
    return output[["year", "region_code", "region_name", "births"]]


def merge_births(denominators, births):
    if denominators.empty:
        return denominators
    output = denominators.copy()
    if births.empty:
        output["births"] = np.nan
        return output

    by_code = output.merge(
        births[["year", "region_code", "births"]],
        on=["year", "region_code"],
        how="left",
    )
    by_name = output.merge(
        births[["year", "region_name", "births"]],
        on=["year", "region_name"],
        how="left",
    )
    output["births"] = by_code["births"].combine_first(by_name["births"])
    return output


def normalize_deflators_table(df, settings):
    columns = ["year", "deflator_used", "price_index", "price_base_year"]
    if df.empty:
        return pd.DataFrame(columns=columns)

    output = clean_columns(df)
    output = coalesce_columns(output, ["anno", "year", "time", "periodo"], "year")
    output = coalesce_columns(output, ["deflator_used", "indice", "index_name", "serie"], "deflator_used")
    output = coalesce_columns(output, ["price_index", "indice_prezzi", "index_value", "value", "valore"], "price_index")
    output = coalesce_columns(output, ["price_base_year", "base_year", "anno_base"], "price_base_year")
    if any(column not in output.columns for column in ["year", "price_index"]):
        return pd.DataFrame(columns=columns)

    output["year"] = pd.to_numeric(output["year"], errors="coerce")
    output["price_index"] = pd.to_numeric(output["price_index"], errors="coerce")
    output["deflator_used"] = output["deflator_used"].fillna(settings["default_deflator"])
    output["price_base_year"] = pd.to_numeric(output["price_base_year"], errors="coerce").fillna(settings["base_price_year"])
    output = output.dropna(subset=["year", "price_index"])
    output["year"] = output["year"].astype(int)
    output["price_base_year"] = output["price_base_year"].astype(int)
    return output[columns]


def normalize_expenditure_table(df, settings):
    if df.empty:
        return pd.DataFrame()

    output = clean_columns(df)
    output = coalesce_columns(output, ["anno", "year", "time", "periodo"], "year")
    output = coalesce_columns(output, ["codice_regione", "region_code", "cod_reg", "codice"], "region_code")
    output = coalesce_columns(output, ["regione", "region_name", "territorio"], "region_name")
    output = coalesce_columns(output, ["fonte", "source"], "source")
    output = coalesce_columns(output, ["basis", "accounting_basis", "criterio_contabile"], "accounting_basis")
    output = coalesce_columns(output, ["area_spesa", "spending_area", "categoria", "macrovoce"], "spending_area")
    output = coalesce_columns(output, ["codice_voce", "spending_item_code", "codice_gestionale", "voce_codice"], "spending_item_code")
    output = coalesce_columns(output, ["voce", "spending_item_name", "descrizione", "descrizione_voce"], "spending_item_name")
    output = coalesce_columns(output, ["importo", "amount_nominal_eur", "valore", "value"], "amount_nominal_eur")

    required_columns = ["year", "region_name", "spending_area", "amount_nominal_eur"]
    if any(column not in output.columns for column in required_columns):
        return pd.DataFrame()

    output["year"] = pd.to_numeric(output["year"], errors="coerce")
    output["amount_nominal_eur"] = pd.to_numeric(output["amount_nominal_eur"], errors="coerce")
    output["region_name"] = output["region_name"].astype(str).str.strip()
    output["spending_area"] = output["spending_area"].fillna("").astype(str).str.strip()

    for column in ["region_code", "source", "accounting_basis", "spending_item_code", "spending_item_name"]:
        output[column] = output[column].fillna("").astype(str).str.strip()

    output["source"] = output["source"].replace("", "not_specified")
    output["accounting_basis"] = output["accounting_basis"].replace("", settings["default_accounting_basis"])
    output = output.dropna(subset=["year", "region_name", "amount_nominal_eur"])
    output["year"] = output["year"].astype(int)

    return output[
        [
            "year",
            "region_code",
            "region_name",
            "source",
            "accounting_basis",
            "spending_area",
            "spending_item_code",
            "spending_item_name",
            "amount_nominal_eur",
        ]
    ]


def match_relevant_population_type(row):
    text = " ".join([str(row.get("spending_area", "")), str(row.get("spending_item_name", ""))]).lower()
    for rule in sorted(DENOMINATOR_RULES, key=lambda item: item["priority"]):
        keywords = rule["keywords"]
        if not keywords:
            return rule["relevant_population_type"]
        if any(keyword.lower() in text for keyword in keywords):
            return rule["relevant_population_type"]
    return "population_total"


def add_real_amounts(expenditure, deflators, settings):
    if expenditure.empty:
        return expenditure

    output = expenditure.copy()
    default_deflator = settings["default_deflator"]
    base_year = settings["base_price_year"]
    output["deflator_used"] = default_deflator
    output["price_base_year"] = base_year

    if deflators.empty:
        output["amount_real_eur"] = np.nan
        return output

    selected = deflators[deflators["deflator_used"] == default_deflator].copy()
    if selected.empty:
        selected = deflators.copy()

    base_values = selected[selected["year"] == base_year]["price_index"]
    if base_values.empty:
        output["amount_real_eur"] = np.nan
        return output

    base_value = base_values.iloc[0]
    selected = selected[["year", "price_index"]].rename(columns={"price_index": "deflator_year_value"})
    output = output.merge(selected, on="year", how="left")
    output["amount_real_eur"] = output["amount_nominal_eur"] * base_value / output["deflator_year_value"]
    output = output.drop(columns=["deflator_year_value"])
    return output


def add_demographic_adjustments(expenditure, denominators):
    if expenditure.empty:
        return expenditure

    output = expenditure.copy()
    output["relevant_population_type"] = output.apply(match_relevant_population_type, axis=1)

    if denominators.empty:
        output["amount_per_capita"] = np.nan
        output["relevant_population_value"] = np.nan
        output["amount_per_relevant_population"] = np.nan
        return output

    denominator_columns = [column for column in denominators.columns if column != "region_code"]
    output = output.merge(denominators[denominator_columns], on=["year", "region_name"], how="left")
    output["amount_per_capita"] = output["amount_nominal_eur"] / output["population_total"]
    output["relevant_population_value"] = output.apply(
        lambda row: row.get(row["relevant_population_type"], np.nan),
        axis=1,
    )
    output["amount_per_relevant_population"] = output["amount_nominal_eur"] / output["relevant_population_value"]
    return output


def build_schema_table():
    rows = [{"column_name": column, "required": column in ["year", "region_name", "accounting_basis", "spending_area", "amount_nominal_eur"]} for column in SCHEMA_COLUMNS]
    return pd.DataFrame(rows)


def build_rules_table():
    rows = []
    for rule in DENOMINATOR_RULES:
        row = rule.copy()
        row["keywords"] = ";".join(rule["keywords"])
        rows.append(row)
    return pd.DataFrame(rows)


def empty_denominators_dataset():
    return pd.DataFrame(columns=[
        "year",
        "region_code",
        "region_name",
        "population_total",
        "population_0",
        "population_0_4",
        "population_0_14",
        "population_0_17",
        "births",
        "women_15_49",
        "population_65_plus",
        "population_75_plus",
        "population_80_plus",
    ])


def empty_deflators_dataset():
    return pd.DataFrame(columns=["year", "deflator_used", "price_index", "price_base_year"])


def empty_health_expenditure_dataset():
    return pd.DataFrame(columns=SCHEMA_COLUMNS)


def align_health_expenditure_columns(df):
    if df.empty:
        return empty_health_expenditure_dataset()
    output = df.copy()
    for column in SCHEMA_COLUMNS:
        if column not in output.columns:
            output[column] = np.nan
    return output[SCHEMA_COLUMNS]


def write_outputs(health_config, denominators, deflators, expenditure_adjusted):
    processed_root = get_configured_path("data_processed")
    tables_root = get_configured_path("outputs_tables")

    processed_demography = processed_root / "demography"
    processed_health = processed_root / "health_expenditure"
    processed_prices = processed_root / "prices"

    if denominators.empty:
        denominators = empty_denominators_dataset()
    if deflators.empty:
        deflators = empty_deflators_dataset()
    expenditure_adjusted = align_health_expenditure_columns(expenditure_adjusted)

    write_csv_json_pair(pd.DataFrame(SOURCE_PLAN), tables_root, "health_expenditure_source_plan")
    write_csv_json_pair(build_schema_table(), tables_root, "health_expenditure_required_schema")
    write_csv_json_pair(pd.DataFrame(health_config.DEMOGRAPHIC_DENOMINATORS), tables_root, "health_expenditure_denominator_dictionary")
    write_csv_json_pair(build_rules_table(), tables_root, "health_expenditure_denominator_rules")

    write_csv_json_pair(denominators, processed_demography, "demographic_denominators_region_year")
    write_csv_json_pair(deflators, processed_prices, "price_deflators")
    write_csv_json_pair(expenditure_adjusted, processed_health, "regional_health_expenditure_demographic_adjusted")
    write_csv_json_pair(expenditure_adjusted, tables_root, "regional_health_expenditure_demographic_adjusted")


def main():
    ensure_project_folders()
    root = get_project_root()
    health_config = load_health_config()
    settings = health_config.HEALTH_EXPENDITURE_SETTINGS

    population_raw, population_path = load_optional_table(root, DEMOGRAPHY_INPUT_CANDIDATES)
    births_raw, births_path = load_optional_table(root, BIRTHS_INPUT_CANDIDATES)
    deflators_raw, deflators_path = load_optional_table(root, DEFLATOR_INPUT_CANDIDATES)
    expenditure_raw, expenditure_path = load_optional_table(root, EXPENDITURE_INPUT_CANDIDATES)

    denominators = build_population_denominators(population_raw)
    denominators = merge_births(denominators, normalize_births_table(births_raw))

    deflators = normalize_deflators_table(deflators_raw, settings)

    expenditure = normalize_expenditure_table(expenditure_raw, settings)
    expenditure = add_real_amounts(expenditure, deflators, settings)
    expenditure_adjusted = add_demographic_adjustments(expenditure, denominators)

    write_outputs(health_config, denominators, deflators, expenditure_adjusted)

    print("Health expenditure framework written")
    print(f"Population input: {population_path if population_path else 'missing'}")
    print(f"Births input: {births_path if births_path else 'missing'}")
    print(f"Deflator input: {deflators_path if deflators_path else 'missing'}")
    print(f"Expenditure input: {expenditure_path if expenditure_path else 'missing'}")


if __name__ == "__main__":
    main()
