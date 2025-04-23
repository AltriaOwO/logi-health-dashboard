#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 02:56:33 2025

@author: anthony
"""

"""
analysis package
Expose the core functions in a centralized manner to facilitate external calls:
    >>> from analysis import load_dataset, add_training_compliance
"""

from .data_loader import load_dataset
from .kpi_calculations import (
    add_safety_score,
    add_workload_score,
    add_training_compliance,
    add_on_time_rate,
    add_incident_rate,
    add_financial_gap,
    add_violation_rate,
    add_composite_score,
)

__all__ = [
    "load_dataset",
    "add_safety_score",
    "add_workload_score",
    "add_training_compliance",
    "add_on_time_rate",
    "add_incident_rate",
    "add_financial_gap",
    "add_violation_rate",
    "add_composite_score",
]