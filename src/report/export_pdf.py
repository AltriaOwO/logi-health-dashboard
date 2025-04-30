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

    # Select locations whose trend is deteriorating (CompositeScore_bad == 1)
    bad_df = (
        df[["LocationID", "CompositeScore"]]
        .merge(flags, on="LocationID", how="inner")
        .query("CompositeScore_bad == 1")
        .nsmallest(10, "CompositeScore")           # lowest composite scores = worst performers
        .drop(columns="CompositeScore_bad") \
        .assign(Detected="Detected") \
        .rename(columns={
            "CompositeScore": "CompositeScore (0‑1 scale)",
            "Detected": ""
        })
    )
    bad_flags_html = bad_df.to_html(index=False, classes="pandas")

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