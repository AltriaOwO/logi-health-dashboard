#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 02:58:05 2025

@author: anthony
"""

"""
analysis.data_loader
--------------------
read data from Penske Location Health and 
Do the basic verification and type conversion
"""

from pathlib import Path
from typing import Union

import pandas as pd

# ======================== variable & config ======================== #
EXPECTED_COLS = {
    "LocationID", "YEAR_MONTH", "Driver Ct", "Shipment Ct", "Stop Ct",
    "Past due training Ct", "Ontime observation Ct",
    "Preventable incident Ct", "Non preventable incident Ct",
    "Duty Violation Ct", "Actual pretax", "Planned pretax",
    "Num voluntary terminations", "Avg Weekly Hours", "Avg Weekly Miles",
    "Days since last training", "Days since last coaching",
}

# ======================== main functions ============================ #
def load_dataset(path: Union[str, Path]) -> pd.DataFrame:
    """
    Read Excel/CSV file and return Data Frame. If the necessary column is missing,
    an error will be thrown.

    Parameters
    ----------
    path : str | pathlib.Path
        full file path，support .xlsx/.xls/.csv

    Returns
    -------
    pandas.DataFrame：
        * Column integrity check
        * YEAR_MONTH to datetime64
        * numeric columns float64 / int64
        * LocationID to category
    """
    path = Path(path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(path)

    # 1. read
    if path.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError("only support .xlsx/.xls/.csv files")

    # 2. Column integrity
    missing = EXPECTED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {missing}")

    # 3. Type transform
    df["YEAR_MONTH"] = pd.to_datetime(df["YEAR_MONTH"])
    df["LocationID"] = df["LocationID"].astype("category")

    num_cols = df.columns.difference(["LocationID", "YEAR_MONTH"])
    df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")

    return df