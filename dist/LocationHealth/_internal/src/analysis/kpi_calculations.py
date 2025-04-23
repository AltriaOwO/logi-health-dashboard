#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 02:50:44 2025

@author: anthony
"""

# ========================================================
# TrainingCompliance = 1 - Past due training Ct / Driver Ct (if Driver Ct = 0, set NaN) Driver training expiration rate; higher the better
# OnTimeRate = Ontime observation Ct / Shipment Ct, the higher the better
# IncidentRate = (Preventable + Non-preventable incident Ct) / Shipment Ct, the lower the better
# FinancialGap = Actual pretax - Planned pretax, the higher the better
# ViolationRate = Duty Violation Ct / Driver Ct, the lower the better

# src/analysis/kpi_calculations.py
import numpy as np
import pandas as pd

def add_training_compliance(df):
    out = df.copy()
    out["TrainingCompliance"] = 1 - (
        out["Past due training Ct"] / out["Driver Ct"].replace(0, np.nan)
    )
    return out

def add_on_time_rate(df):
    out = df.copy()
    out["OnTimeRate"] = (
        out["Ontime observation Ct"] / out["Shipment Ct"].replace(0, np.nan)
    )
    return out

def add_incident_rate(df):
    out = df.copy()
    numer = out["Preventable incident Ct"] + out["Non preventable incident Ct"]
    out["IncidentRate"] = numer / out["Shipment Ct"].replace(0, np.nan)
    return out

def add_financial_gap(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["FinancialGap"] = out["Actual pretax"] - out["Planned pretax"]
    return out

def add_violation_rate(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ViolationRate"] = (
        out["Duty Violation Ct"] / out["Driver Ct"].replace(0, np.nan)
    )
    return out

def add_safety_score(df: pd.DataFrame) -> pd.DataFrame:
    """SafetyScore = 1 - (Preventable + DutyViolation + PastDueTraining) / Driver Ct"""
    out = df.copy()
    numerator = (
        out["Preventable incident Ct"]
        + out["Duty Violation Ct"]
        + out["Past due training Ct"]
    )
    out["SafetyScore"] = 1 - numerator / out["Driver Ct"].replace(0, np.nan)
    return out

def add_workload_score(df: pd.DataFrame, target_hours: float = 50.0) -> pd.DataFrame:
    out = df.copy()
    out["WorkloadScore"] = 1 - (out["Avg Weekly Hours"] - target_hours).abs() / target_hours
    return out

from .utils import minmax_scale

_WEIGHTS = {
    "SafetyScore":      0.20,
    "WorkloadScore":    0.20,
    "TrainingCompliance": 0.15,
    "OnTimeRate":       0.15,
    "FinancialGap":     0.15,
    "IncidentRate":     0.10,
    "ViolationRate":    0.05,
}

_LOW_IS_BETTER = {"IncidentRate", "ViolationRate"}

def add_composite_score(df, weights=_WEIGHTS):
    out = df.copy()
    for col in weights:
        higher = col not in _LOW_IS_BETTER
        out[f"{col}_scaled"] = minmax_scale(out[col], higher_is_better=higher)
    out["CompositeScore"] = sum(out[f"{c}_scaled"] * w for c, w in weights.items())
    return out
