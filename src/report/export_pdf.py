#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 00:45:48 2025

@author: anthony

PDF Export Module for Location Health Report
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from pathlib import Path
import pandas as pd
from datetime import date

TEMPLATE_DIR = Path(__file__).parent / "templates"
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"])
)

def create_pdf(df: pd.DataFrame, flags: pd.DataFrame) -> Path:
    tmpl = env.get_template("report.html")

    # Prepare summary table
    summary_html = df["CompositeScore"].describe().to_frame().to_html(classes="pandas")

    # Filter top 10 with deterioration (bad trend = 1)
    bad_flags = flags[flags["CompositeScore_bad"] == 1].copy()
    bad_flags = bad_flags.head(10)
    bad_flags_html = bad_flags.to_html(index=False, classes="pandas")

    # Inject into template
    html_out = tmpl.render(
        summary=summary_html,
        flags=bad_flags_html,
        logo_path=(Path(__file__).parent.parent / "assets" / "logo.png").resolve().as_uri(),
        date=date.today().isoformat()
    )

    # Output
    out_path = Path("report/location_health.pdf")
    out_path.parent.mkdir(exist_ok=True, parents=True)
    HTML(string=html_out, base_url=".").write_pdf(out_path)
    return out_path