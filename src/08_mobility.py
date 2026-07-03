"""
Script: 08_mobility.py

Modulo iniziale per analisi della mobilita sanitaria.
"""

import pandas as pd


def build_origin_destination_matrix(df, origin_col, destination_col, value_col):
    return df.groupby([origin_col, destination_col], dropna=False)[value_col].sum().reset_index()
