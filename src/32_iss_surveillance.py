"""
Script: 32_iss_surveillance.py

Modulo iniziale per sorveglianze ISS, fattori di rischio e prevenzione.
"""

import pandas as pd


def aggregate_surveillance(df, group_cols, indicator_col, value_col):
    return df.groupby(group_cols + [indicator_col], dropna=False)[value_col].mean().reset_index()


def aggregate_counts(df, group_cols, count_col):
    return df.groupby(group_cols, dropna=False)[count_col].sum().reset_index()
