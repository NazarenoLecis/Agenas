"""
Utility per pulizia e normalizzazione.

Le funzioni applicano regole minime e conservative: nomi colonna standardizzati,
spazi rimossi, valori mancanti preservati e conversioni numeriche solo quando
richieste esplicitamente.
"""

import re
import pandas as pd


def clean_column_name(column_name):
    """
    Converte un nome colonna in snake_case ASCII semplice.
    """
    name = str(column_name).strip().lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name or "column"


def clean_column_names(df):
    """
    Applica clean_column_name a tutte le colonne e risolve eventuali duplicati.
    """
    df = df.copy()
    seen = {}
    columns = []
    for column in df.columns:
        base_name = clean_column_name(column)
        count = seen.get(base_name, 0)
        seen[base_name] = count + 1
        if count == 0:
            columns.append(base_name)
        else:
            columns.append(f"{base_name}_{count + 1}")
    df.columns = columns
    return df


def strip_string_columns(df):
    """
    Rimuove spazi iniziali e finali dalle colonne testuali senza convertire i
    valori mancanti nella stringa 'nan'.
    """
    df = df.copy()
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].apply(lambda value: value.strip() if isinstance(value, str) else value)
    return df


def convert_numeric_columns(df, columns):
    """
    Converte in numerico le colonne indicate, se presenti.
    """
    df = df.copy()
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def normalize_table(df):
    """
    Applica le trasformazioni minime comuni a tutti i dataset.
    """
    df = clean_column_names(df)
    df = strip_string_columns(df)
    return df
