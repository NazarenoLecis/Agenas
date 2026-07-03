"""
Utility per controlli qualita sui dati.

Ogni funzione restituisce un dizionario. Questo rende semplice salvare un report
CSV o JSON leggibile dopo ogni passaggio della pipeline.
"""


def check_not_empty(df, check_name="not_empty"):
    """
    Controlla che il DataFrame abbia almeno una riga.
    """
    return {
        "check_name": check_name,
        "passed": len(df) > 0,
        "value": len(df),
        "message": "rows_count",
    }


def check_required_columns(df, required_columns, check_name="required_columns"):
    """
    Controlla che tutte le colonne obbligatorie siano presenti.
    """
    missing = [column for column in required_columns if column not in df.columns]
    return {
        "check_name": check_name,
        "passed": len(missing) == 0,
        "value": ";".join(missing),
        "message": "missing_columns" if missing else "ok",
    }


def check_duplicates(df, key_columns, check_name="duplicates"):
    """
    Controlla duplicati sulle colonne chiave indicate.
    """
    available_keys = [column for column in key_columns if column in df.columns]
    if not available_keys:
        return {
            "check_name": check_name,
            "passed": False,
            "value": "",
            "message": "no_key_columns_available",
        }
    duplicates = df.duplicated(subset=available_keys).sum()
    return {
        "check_name": check_name,
        "passed": duplicates == 0,
        "value": int(duplicates),
        "message": "duplicate_rows",
    }


def run_basic_quality_checks(df, required_columns=None, key_columns=None):
    """
    Esegue un insieme minimo di controlli qualita.
    """
    required_columns = required_columns or []
    key_columns = key_columns or []
    checks = [check_not_empty(df)]
    if required_columns:
        checks.append(check_required_columns(df, required_columns))
    if key_columns:
        checks.append(check_duplicates(df, key_columns))
    return checks
