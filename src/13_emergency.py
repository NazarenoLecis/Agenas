"""
Script: 13_emergency.py

Modulo iniziale per accessi, triage, tempi ed esiti di emergenza.
"""

import pandas as pd


def aggregate_emergency_accesses(df, group_cols, access_col):
    return df.groupby(group_cols, dropna=False)[access_col].sum().reset_index()


def aggregate_emergency_waits(df, group_cols, wait_col):
    return df.groupby(group_cols, dropna=False)[wait_col].mean().reset_index(name="average_time")
