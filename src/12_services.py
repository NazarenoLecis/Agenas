"""
Script: 12_services.py

Modulo iniziale per numero e tipo di prestazioni.
"""

import pandas as pd


def aggregate_services(df, group_cols, volume_col):
    return df.groupby(group_cols, dropna=False)[volume_col].sum().reset_index()


def add_service_rate(df, volume_col, population_col, output_col):
    df = df.copy()
    df[output_col] = df[volume_col] / df[population_col] * 100000
    return df
