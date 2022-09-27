# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 16:02:39 2022

@author: gbournigal
"""


import plotly.graph_objects as go
from plotly.subplots import make_subplots


def fig_beautifier(fig, x_title=False, y_title=False):
    fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(
            size=16,
        ),
    )

    if x_title is not False:
        fig.update_xaxes(title_text=x_title)

    if y_title is not False:
        fig.update_yaxes(title_text=y_title)

    return fig


def cbr_index_fig(df):
    df.sort_values("fecha", inplace=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=df.fecha,
            y=df.index_no_w,
            name="Índice Simple",
            marker_color="#B4C7E7",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df.fecha,
            y=df.index_w,
            name="Índice ponderado",
            marker=dict(color="#8497B0"),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df.fecha,
            y=df.tpm,
            name="TPM RD",
            marker_color="#33CCCC",
        ),
        secondary_y=True,
    )
    fig.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=0.94,
        y1=0,
        line=dict(color="Grey", dash="dot"),
        xref="paper",
        yref="y",
    )

    fig.update_layout(
        yaxis2=dict(
            tickfont=dict(
                color="#33CCCC",
            ),
            titlefont=dict(
                color="#33CCCC",
            ),
        ),
        font=dict(
            size=16,
        ),
    )

    fig.update_yaxes(
        title_text="Índice de Presión Internacional",
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Tasa de de Política Monetaria RD",
        tickformat=".2%",
        secondary_y=True,
    )
    fig.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    fig = fig_beautifier(fig, x_title="Fecha")
    return fig


def cbr_index_comp_fig(
    series_index_60,
    series_index_90,
    series_index_180,
    series_index_360,
    simple=True,
):
    if simple:
        variable = "index_no_w"
    else:
        variable = "index_w"

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=series_index_60.fecha,
            y=series_index_60[f"{variable}"],
            name="Índice 60 días",
            marker_color="black",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=series_index_90.fecha,
            y=series_index_90[f"{variable}"],
            name="Índice 90 días",
            marker_color="#B4C7E7",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=series_index_180.fecha,
            y=series_index_180[f"{variable}"],
            name="Índice 180 días",
            marker=dict(color="#8497B0"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=series_index_360.fecha,
            y=series_index_360[f"{variable}"],
            name="Índice 360 días",
            marker_color="#33CCCC",
        )
    )
    fig.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=0.94,
        y1=0,
        line=dict(color="Grey", dash="dot"),
        xref="paper",
        yref="y",
    )

    fig.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    fig = fig_beautifier(fig, x_title="Fecha")
    return fig


def initial_plot(df):
    df_positive = df[df["value"] == 1]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_positive.fecha,
            y=df_positive.value,
            name="Incrementos de tasa",
            marker=dict(color="blue"),
        )
    )
    df_negative = df[df["value"] == -1]
    fig.add_trace(
        go.Bar(
            x=df_negative.fecha,
            y=df_negative.value,
            name="Reducciones de tasa",
            marker=dict(color="red"),
        )
    )
    fig = fig_beautifier(fig, x_title="Fecha")
    return fig


def initial_plot_m(df):
    df_positive = df[df["value"] == 1]
    df_positive = df_positive.groupby(
        [df_positive.fecha.dt.year, df_positive.fecha.dt.month]
    )["value"].sum()
    df_positive.index.set_names(["ano", "mes"], inplace=True)
    df_positive = df_positive.reset_index()
    df_positive["fecha"] = (
        df_positive["ano"].astype("str")
        + "-"
        + df_positive["mes"].astype("str")
    )
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_positive.fecha,
            y=df_positive.value,
            name="Incrementos de tasa",
            marker=dict(color="blue"),
        )
    )
    df_negative = df[df["value"] == -1]
    df_negative = df_negative.groupby(
        [df_negative.fecha.dt.year, df_negative.fecha.dt.month]
    )["value"].sum()
    df_negative.index.set_names(["ano", "mes"], inplace=True)
    df_negative = df_negative.reset_index()
    df_negative["fecha"] = (
        df_negative["ano"].astype("str")
        + "-"
        + df_negative["mes"].astype("str")
    )
    fig.add_trace(
        go.Bar(
            x=df_negative.fecha,
            y=df_negative.value,
            name="Reducciones de tasa",
            marker=dict(color="red"),
        )
    )
    fig = fig_beautifier(fig, x_title="Fecha")
    return fig
