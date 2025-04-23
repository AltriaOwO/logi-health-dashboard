#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 23:35:07 2025

@author: anthony
"""

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

"""
analysis.visualizations
-----------------------
Encapsulates Plotly visualization functions and directly returns Figure objects,
making it convenient for unified calls in Jupyter/Streamlit/CLI.
"""



# ------------------------------------------------------------------
# 1. 综合分布直方图
# ------------------------------------------------------------------
def plot_distribution(df: pd.DataFrame, col: str, nbins: int = 30) -> go.Figure:
    fig = px.histogram(
        df,
        x=col,
        nbins=nbins,
        marginal="box",
        title=f"{col} Distribution(Box chart)",
        template="plotly_white",
    )
    fig.update_layout(yaxis_title="Count", bargap=0.05)
    return fig


# ------------------------------------------------------------------
# 2. Top / Bottom N Bar chart
# ------------------------------------------------------------------
def plot_top_bottom(df: pd.DataFrame, col: str, n: int = 10) -> go.Figure:
    stat = df.groupby("LocationID")[col].mean()
    top = stat.nlargest(n).reset_index().assign(Group="Top")
    bottom = stat.nsmallest(n).reset_index().assign(Group="Bottom")
    combined = pd.concat([top, bottom])

    fig = px.bar(
        combined,
        x=col,
        y="LocationID",
        color="Group",
        orientation="h",
        title=f"Top & Bottom {n} Locations by {col}",
        template="plotly_white",
        height=600,
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    return fig


# ------------------------------------------------------------------
# 3. KPI trend line
# ------------------------------------------------------------------
def plot_trend_lines(
    df_single_loc: pd.DataFrame,
    location_id: str | int,
    kpi_list: list[str],
) -> go.Figure:
    df_plot = df_single_loc.sort_values("YEAR_MONTH")
    fig = go.Figure()
    for kpi in kpi_list:
        fig.add_trace(
            go.Scatter(
                x=df_plot["YEAR_MONTH"],
                y=df_plot[kpi],
                mode="lines+markers",
                name=kpi,
            )
        )
    fig.update_layout(
        title=f"Trend Lines — Location {location_id}",
        xaxis_title="Year-Month",
        template="plotly_white",
        legend_title="KPI",
    )
    return fig


# ------------------------------------------------------------------
# 4. Slope Heatmap
#    import：get dataframe from trend_detection.slope_by_location
# ------------------------------------------------------------------
def plot_slope_heatmap(slopes_df: pd.DataFrame, kpi_list: list[str]) -> go.Figure:
    pivot = slopes_df.pivot(index="LocationID", columns="kpi", values="slope")
    # Only the required KPI order is preserved
    pivot = pivot[kpi_list]

    fig = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Slope Heatmap (positive = uptrend, negative = downtrend)",
    )
    fig.update_xaxes(side="top")
    return fig


# ------------------------------------------------------------------
# 5. CompositeScore vs TrendBadCount
# ------------------------------------------------------------------
def plot_risk_scatter(df: pd.DataFrame) -> go.Figure:
    """
    df needs to include columns：
        - CompositeScore
        - TrendBadCount （Total number of trend deterioration indicators）
    """
    fig = px.scatter(
        df,
        x="CompositeScore",
        y="TrendBadCount",
        hover_data=["LocationID"],
        title="Risk Scatter: CompositeScore vs TrendBadCount",
        template="plotly_white",
    )
    # layered lines for reference 
    fig.add_hline(y=df["TrendBadCount"].median(), line_dash="dot")
    fig.add_vline(x=df["CompositeScore"].median(), line_dash="dot")
    fig.update_layout(yaxis_title="Trend Bad Count", xaxis_title="Composite Score")
    return fig


# ------------------------------------------------------------------
# 6. KPI comparison scatter plot (any two columns)
# ------------------------------------------------------------------
def plot_pair_scatter(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str | None = None,
) -> go.Figure:
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        hover_data=["LocationID"],
        trendline="ols",
        title=f"{x_col} vs {y_col}",
        template="plotly_white",
    )
    return fig