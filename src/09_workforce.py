"""
Script: 09_workforce.py

Modulo iniziale per analisi del personale sanitario.
"""

import pandas as pd


def aggregate_workforce(df, group_cols, staff_col):
    return df.groupby(group_cols, dropna=False)[staff_col].sum().reset_index()


def add_staff_rate(df, staff_col, population_col, output_col):
    df = df.copy()
    df[output_col] = df[staff_col] / df[population_col] * 100000
    return df
