# -*- coding: utf-8 -*-
"""
Created on Sat May  2 22:36:03 2026

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:18:51 2025

@author: tlj
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ================= Global Style =================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    'axes.labelsize': 30,
    'axes.titlesize': 30,
    'xtick.labelsize': 30,
    'ytick.labelsize': 30,
    'legend.fontsize': 20,
    'axes.linewidth': 1.2,
    'figure.dpi': 500
})

# ================= Load Data =================
path_qwdap = r"data\orifit.csv"
path_arima = r"data\orifit_ARIMA.csv"
path_lstm  = r"data\orifit_LSTM.csv"
path_nhits = r"data\HITS.csv"

df_qwdap = pd.read_csv(path_qwdap)
df_arima = pd.read_csv(path_arima)
df_lstm  = pd.read_csv(path_lstm)
df_nhits = pd.read_csv(path_nhits)

# Normalize column names
for df in [df_qwdap, df_arima, df_lstm, df_nhits]:
    df.columns = df.columns.str.strip()

# ================= Nodes to Visualize =================
nodes = ["N1", "N25"]

# ================= Plotting =================
fig, axs = plt.subplots(2, 1, figsize=(14, 7), sharex=True)

colors = {
    "Ori": "black",
    "QWDAP": "blue",
    "ARIMA": "#FF7F0E",
    "LSTM": "green",
    "N-HiTS": "#9467bd"
}

for i, node in enumerate(nodes):
    ax = axs[i]

    col_ori   = f"{node}_Ori"
    col_qwdap = f"{node}_Fit"
    col_arima = f"{node}_Fit"
    col_lstm  = f"{node}_Fit"
    col_nhits = f"{node}_Ori"   # HITS.csv 输出的是原列名，如 N1_Ori

    n = min(len(df_qwdap), len(df_arima), len(df_lstm), len(df_nhits))

    ax.plot(df_qwdap[col_ori][:n],
            color=colors["Ori"], label="Original", linewidth=1.8)

    ax.plot(df_qwdap[col_qwdap][:n],
            color=colors["QWDAP"], label="QWDAP", linewidth=1.5)

    ax.plot(df_arima[col_arima][:n],
            color=colors["ARIMA"], label="ARIMA", linewidth=1.5)

    ax.plot(df_lstm[col_lstm][:n],
            color=colors["LSTM"], label="LSTM", linewidth=1.5)

    ax.plot(df_nhits[col_nhits][:n],
            color=colors["N-HiTS"], label="N-HiTS", linewidth=1.5)

    ax.set_title(node, fontsize=30, pad=10)
    ax.set_ylabel("Volume")
    ax.grid(False)

    if i == 0:
        ax.legend(loc="best", frameon=True, ncol=2)

axs[-1].set_xlabel("Time index")

plt.tight_layout()
plt.show()
