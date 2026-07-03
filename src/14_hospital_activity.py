"""
Script: 14_hospital_activity.py

Modulo iniziale per ricoveri, DRG, discipline e degenza.
"""

import pandas as pd


def aggregate_hospital_activity(df, group_cols, volume_col):
    return df.groupby(group_cols, dropna=False)[volume_col].sum().reset_index()


def average_length_of_stay(df, group_cols, days_col, volume_col=None):
    if volume_col and volume_col in df.columns:
        work = df.copy()
        work["weighted_days"] = work[days_col] * work[volume_col]
        out = work.groupby(group_cols, dropna=False).agg({"weighted_days": "sum", volume_col: "sum"}).reset_index()
        out["average_length_of_stay"] = out["weighted_days"] / out[volume_col]
        return out
    return df.groupby(group_cols, dropna=False)[days_col].mean().reset_index(name="average_length_of_stay")
