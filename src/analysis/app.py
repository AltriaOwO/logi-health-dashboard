#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 00:25:39 2025

@author: anthony
"""
import pandas as pd
import streamlit as st
from analysis import (
    load_dataset,
    add_safety_score, add_workload_score,
    add_training_compliance, add_on_time_rate,
    add_incident_rate, add_financial_gap,
    add_violation_rate, add_composite_score
)
from analysis.trend_detection import trend_flags
from analysis.visualizations import (
    plot_distribution, plot_top_bottom,
    plot_trend_lines, plot_slope_heatmap,
    plot_risk_scatter
)

st.set_page_config(page_title="Penske Location Health", layout="wide")

# --- Sidebar: upload CSV / pick KPI ---
uploaded = st.sidebar.file_uploader("Please upload dataset", type=["xlsx", "csv"])
window = st.sidebar.slider("Trend window (month) ", 3, 12, 6)
kpi_choice = st.sidebar.selectbox("Select KPI fold line", 
    ["CompositeScore", "SafetyScore", "WorkloadScore"])

if uploaded:
    import pandas as pd
    # Determine the file name suffix and use pandas to read it directly
    if uploaded.name.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded)
    else:
        df = pd.read_csv(uploaded)
    df = (df.pipe(add_safety_score).pipe(add_workload_score)
            .pipe(add_training_compliance).pipe(add_on_time_rate)
            .pipe(add_incident_rate).pipe(add_financial_gap)
            .pipe(add_violation_rate).pipe(add_composite_score))

    # ----- Main KPIs -----
    st.header("Comprehensive Score Distribution")
    st.plotly_chart(plot_distribution(df, "CompositeScore"), use_container_width=True)

    st.header("Top / Bottom 10 Locations")
    st.plotly_chart(plot_top_bottom(df, "CompositeScore"), use_container_width=True)

    # ----- Trend Detection -----
    flags = trend_flags(df, "CompositeScore", window=window)
    st.header(f"{window} Trend Line")
    loc_sel = st.selectbox("Choose Location", sorted(df["LocationID"].unique()))
    st.plotly_chart(
        plot_trend_lines(df[df["LocationID"] == loc_sel], loc_sel, [kpi_choice]),
        use_container_width=True
    )

    st.header("Risk Scatter Plot")
    df_bad = df.merge(flags, on="LocationID", how="left")
    df_bad["TrendBadCount"] = df_bad["CompositeScore_bad"]
    st.plotly_chart(plot_risk_scatter(df_bad), use_container_width=True)

    # ----- Download PDF report button -----
    if st.button("Generate PDF reports"):
        from report.export_pdf import create_pdf
        pdf_path = create_pdf(df, flags)
        with open(pdf_path, "rb") as f:
            st.download_button("Download report", f, file_name="location_health.pdf")
else:
    st.info("Please upload the data file on the left to start the analysis.")
