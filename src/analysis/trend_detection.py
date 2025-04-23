#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 23:33:32 2025

@author: anthony
"""

import pandas as pd
from scipy.stats import linregress

_BAD_DIR = {        # lower is better
    "IncidentRate", "ViolationRate"
}

def slope_by_location(df: pd.DataFrame, kpi: str, window: int = 6):
    rows = []
    for loc, sub in df.groupby("LocationID"):
        sub = sub.sort_values("YEAR_MONTH").tail(window)
        if len(sub) < 3 or sub[kpi].isna().all():
            continue
        slope, *_ , pval, _ = linregress(range(len(sub)), sub[kpi])
        rows.append({"LocationID": loc, "kpi": kpi, "slope": slope, "pvalue": pval})
    return pd.DataFrame(rows)

def trend_flags(df: pd.DataFrame, kpi: str, window=6, alpha=0.05):
    higher_is_better = kpi not in _BAD_DIR
    slopes = slope_by_location(df, kpi, window)
    def is_bad(row):
        if higher_is_better:
            return int(row["slope"] < 0 and row["pvalue"] < alpha)
        else:
            return int(row["slope"] > 0 and row["pvalue"] < alpha)
    slopes[f"{kpi}_bad"] = slopes.apply(is_bad, axis=1)
    return slopes[["LocationID", f"{kpi}_bad"]]