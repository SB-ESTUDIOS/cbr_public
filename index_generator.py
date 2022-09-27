# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:02:46 2022

@author: gbournigal
"""

import streamlit as st
import pandas as pd
import numpy as np
from data import get_all_data

contries_dict = {
    "Egypt, Arab Rep.": "Egypt",
    "Russian Federation": "Russia",
    "Korea, Rep.": "South Korea",
    "Macao SAR, China": "Macao",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Euro area": "Eurozone",
    "Gambia, The": "Gambia",
    "Hong Kong SAR, China": "Hong Kong",
    "United Arab Emirates": "U. Arab Emirates (UAE)",
    "United States": "USA",
}


def index_no_w(date, df, days=180):
    today = date
    cutoff_date = today - pd.Timedelta(days=days)
    rng = pd.date_range(cutoff_date, today)
    banks = len(df.pais.unique())
    df_cut = df[df["fecha"].isin(rng)]
    results = (
        df_cut["ult_cambio"][df_cut["ult_cambio"] == "raises"].count()
        - df_cut["ult_cambio"][df_cut["ult_cambio"] == "cuts"].count()
    ) / banks
    return results


def index_series_no_w(df, days=180):
    today = pd.to_datetime("today")
    start = min(df["fecha"]) + pd.Timedelta(days=days)
    rng = pd.date_range(start, today)
    series = pd.DataFrame({"fecha": rng})
    series["index_no_w"] = series.apply(
        lambda row: index_no_w(row["fecha"], df, days=days), axis=1
    )
    return series


def min_max_year(df, fecha_column):
    return min(df[fecha_column].dt.year), max(df[fecha_column].dt.year)


def weights(gdps, cbr_historic):
    countries = cbr_historic.sort_values(
        "fecha", ascending=False
    ).drop_duplicates(subset=["pais"], keep="last")
    weights = pd.DataFrame(columns=["ano", "pais"])

    min_year, max_year = min_max_year(cbr_historic, "fecha")

    for i in countries["pais"]:
        for j in range(min_year, max_year + 1):
            weights = weights.append({"ano": j, "pais": i}, ignore_index=True)
    gdps = gdps.replace({"pais": contries_dict})
    weights = weights.merge(gdps, how="left", on=["pais", "ano"])
    weights = (
        weights.set_index("pais")
        .groupby(level="pais")
        .ffill()
        .reset_index()
        .dropna()
    )
    weights_agg = weights.groupby(["ano", "pais"]).agg({"gdp": "sum"})
    percents_df = weights_agg.groupby(level=0).apply(
        lambda x: x / float(x.sum())
    )
    percents_df.reset_index(inplace=True)
    return percents_df


def index_w(date, df, w, days=180):
    df["value"] = np.where(
        df["ult_cambio"] == "raises",
        1,
        np.where(df["ult_cambio"] == "cuts", -1, 0),
    )
    df["ano"] = pd.DatetimeIndex(df["fecha"]).year
    df["ano"] = np.where(df["ano"] == 2022, 2021, df["ano"])
    df = df.merge(w, how="left", on=["pais", "ano"])
    df["value"] = df.gdp * df.value
    today = date
    cutoff_date = today - pd.Timedelta(days=days)
    rng = pd.date_range(cutoff_date, today).normalize()
    df_cut = df[df["fecha"].isin(rng)]
    results = df_cut["value"].sum()
    return results


def index_series_w(gdps, cbr_historic, days=180):
    w = weights(gdps, cbr_historic)
    today = pd.to_datetime("today")
    start = min(cbr_historic["fecha"]) + pd.Timedelta(days=days)
    rng = pd.date_range(start, today)
    series = pd.DataFrame({"fecha": rng})
    series["index_w"] = series.apply(
        lambda row: index_w(row["fecha"], cbr_historic, w, days), axis=1
    )
    return series


@st.cache(ttl=10000)
def get_cbr_data(days=180):
    gdps, cbr_historic, tpm = get_all_data()
    series_nw = index_series_no_w(cbr_historic, days=days)
    series_w = index_series_w(gdps, cbr_historic, days=days)
    series_index = series_nw.merge(series_w, how="left", on=["fecha"]).merge(
        tpm, how="left", on=["fecha"]
    )
    series_index["tpm"] = series_index["tpm"].ffill()
    return series_index, cbr_historic
