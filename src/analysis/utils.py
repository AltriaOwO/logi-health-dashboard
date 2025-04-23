#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 23:22:08 2025

@author: anthony
"""

import pandas as pd

def minmax_scale(series: pd.Series, higher_is_better=True, q_low=0.05, q_high=0.95):
    lo, hi = series.quantile([q_low, q_high])
    if hi == lo:
        return pd.Series(0.5, index=series.index)  # avoid denominator = 0
    if higher_is_better:
        scaled = (series - lo) / (hi - lo)
    else:
        scaled = (hi - series) / (hi - lo)
    return scaled.clip(0, 1)