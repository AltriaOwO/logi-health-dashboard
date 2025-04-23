#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 23:35:07 2025

@author: anthony
"""

import plotly.express as px
import pandas as pd

def plot_distribution(df: pd.DataFrame, col: str):
    return px.histogram(df, x=col, nbins=30, title=f"{col} distribution")

def plot_top_bottom(df: pd.DataFrame, col: str, n=10):
    stat = df.groupby("LocationID")[col].mean()
    top = stat.nlargest(n).reset_index()
    bottom = stat.nsmallest(n).reset_index()
    top["Group"] = "Top"
    bottom["Group"] = "Bottom"
    combined = pd.concat([top, bottom])
    return px.bar(combined, x=col, y="LocationID", color="Group",
                  orientation="h", title=f"Top & Bottom {n} Locations by {col}")