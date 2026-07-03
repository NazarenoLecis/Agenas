"""
Script: 10_waiting_times.py

Modulo iniziale per tempi di attesa.
"""

import pandas as pd


def aggregate_waiting_times(df, group_cols, wait_col, volume_col=None):
    if volume_col and volume_col in df.columns:
        work = df.copy()
        work["weighted_wait"] = work[wait_col] * work[volume_col]
        out = work.groupby(group_cols, dropna=False).agg({"weighted_wait": "sum", volume_col: "sum"}).reset_index()
        out["average_wait"] = out["weighted_wait"] / out[volume_col]
        return out
    return df.groupby(group_cols, dropna=False)[wait_col].mean().reset_index(name="average_wait")
