# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 11:58:43 2022

@author: gbournigal
"""

import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

TPM_URL = os.getenv('TPM_URL')
GDPS_URL = os.getenv('GDPS_URL')
CBR_URL = os.getenv('CBR_URL')

mes_dict = {
    'Ene': 1,
    'Feb': 2,
    'Mar': 3,
    'Abr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Ago': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dic': 12
    }

def get_tpm():
    df = get_plain_excel(TPM_URL, header=4, usecols='A:C')
    df = fix_tpm_df(df)
    return df


def get_cbr_historic():
    url = CBR_URL
    df_list = pd.read_html(url)
    df = df_list[3].copy()
    df.columns = ['ano','mes','info','basura']
    df['ano_fixed'] = df['ano'].str.extract(r'([0-9]{4})').ffill()
    df['mes'] = df['mes'].str.replace('Mai','May')
    df['fecha'] = df['mes'] + ', ' + df['ano_fixed']
    df['pais'] = df['info'].str.extract(r'((.+?(?= raises))|(.+?(?= cuts))|(.+?(?= sets)))')[0]
    df = df[pd.isnull(df.ano)]
    df['ult_cambio'] = df['info'].str.extract(r'(raises|cuts|sets)')[0]
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df[['pais','fecha','ult_cambio']]
    df['pais'] = df['pais'].str.strip()
    df = df[df['ult_cambio']!='sets']
    return df


def get_gdps():
    df = get_plain_excel(GDPS_URL, header=3, extension='xls')
    df.rename(
        columns={
            df.columns[0]: 'pais'
            },
        inplace=True
        )
    valid_columns = []
    for i in df.columns:
        try:
            if i in ['pais']:
                valid_columns.append(i)
            if int(i) >= 2015:
                valid_columns.append(i)
        except ValueError:
            pass
    df = df[valid_columns]
    df = pd.melt(df, id_vars='pais', value_vars=valid_columns.remove('pais')).rename(
        columns={
            'variable': 'ano',
            'value': 'gdp'
            }
        ).dropna()
    df['ano'] = df['ano'].astype('int')
    return df


def get_plain_excel(url, header=0, usecols=None, extension='xlsx'):
    r = requests.get(url)
    with open(f'temp.{extension}', 'wb') as document:
        document.write(r.content)
    return pd.read_excel(f'temp.{extension}', header=header, usecols=usecols)


def fix_tpm_df(df):
    df.rename(columns={
        df.columns[0]: 'ano',
        df.columns[1]: 'mes',
        df.columns[2]: 'tpm'
        },
        inplace=True)
    df = df.dropna(subset=['tpm'])
    df['ano'] = df['ano'].ffill()
    df['mes'] = df['mes'].str[:3]
    df = df.replace({"mes": mes_dict})
    df['fecha'] = df['mes'].astype('str') + ', ' + df['ano'].astype('str')
    df['fecha'] = pd.to_datetime(df['fecha'], errors = 'coerce')
    df = df[['fecha', 'tpm']]
    return df


def get_all_data():
    gdps = get_gdps()
    cbr_historic = get_cbr_historic()
    tpm = get_tpm()
    return gdps, cbr_historic, tpm