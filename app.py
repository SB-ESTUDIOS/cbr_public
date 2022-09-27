# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 16:38:46 2022

@author: gbournigal
"""

import streamlit as st
from index_generator import get_cbr_data
from plot import (
    cbr_index_fig,
    initial_plot,
    initial_plot_m,
    cbr_index_comp_fig,
)


st.set_page_config(
    page_title="Presión Monetaria Internacional",
    page_icon="🌎",
    layout="wide",
)

st.title("🌎Presión Monetaria Internacional")

dias = st.number_input("Días:", value=180, min_value=1, max_value=600)
series_index, cbr_historic = get_cbr_data(days=dias)

fig = cbr_index_fig(series_index)
fig_initial = initial_plot(cbr_historic)
fig_initial_m = initial_plot_m(cbr_historic)

st.subheader(
    f"""Índice Simple y Ponderado vs Tasa de Política Monetaria, ventana de {dias} días"""
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Incrementos y reducciones diarias por autoridades monetarias")
st.plotly_chart(fig_initial, use_container_width=True)

st.subheader("Incrementos y reducciones acumuladas mensuales")
st.plotly_chart(fig_initial_m, use_container_width=True)


series_index_30, cbr_historic = get_cbr_data(days=30)
series_index_60, cbr_historic = get_cbr_data(days=60)
series_index_90, cbr_historic = get_cbr_data(days=90)
series_index_180, cbr_historic = get_cbr_data(days=180)
series_index_360, cbr_historic = get_cbr_data(days=360)


simple = st.radio("Simple o Ponderado", ["simple", "ponderado"])

simple_parameter = True if simple == "simple" else False
tipo_ind = "simple" if simple == "simple" else "ponderado"

st.subheader(f"Comparación de múltiples rangos para el índice {tipo_ind}")
st.plotly_chart(
    cbr_index_comp_fig(
        series_index_60,
        series_index_90,
        series_index_180,
        series_index_360,
        simple,
    ),
    use_container_width=True,
)
