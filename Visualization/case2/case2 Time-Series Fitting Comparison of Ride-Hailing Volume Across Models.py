# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:18:51 2025

@author: tlj
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ================= Global Style (Nature-like) =================
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

df_qwdap = pd.read_csv(path_qwdap)
df_arima = pd.read_csv(path_arima)
df_lstm  = pd.read_csv(path_lstm)

# Normalize column names (if needed)
df_qwdap.columns = df_qwdap.columns.str.strip()
df_arima.columns = df_arima.columns.str.strip()
df_lstm.columns  = df_lstm.columns.str.strip()

# ================= Nodes to Visualize =================
nodes = ["N1", "N25"]

# ================= Plotting: 3 rows, 1 column =================
fig, axs = plt.subplots(2, 1, figsize=(14, 7), sharex=True)  # 上下排列，共享 x 轴更紧凑
colors = {
    "Ori": "black",
    "QWDAP": "blue",
    "ARIMA": "#FF7F0E",  # orange
    "LSTM": "green"
}

for i, node in enumerate(nodes):
    ax = axs[i]

    # Column names
    col_ori   = f"{node}_Ori"
    col_qwdap = f"{node}_Fit"
    col_arima = f"{node}_Fit"  # assuming same naming in ARIMA/LSTM files
    col_lstm  = f"{node}_Fit"

    # Align length using minimum rows across all dataframes
    n = min(len(df_qwdap), len(df_arima), len(df_lstm))
    
    ax.plot(df_qwdap[col_ori][:n],   color=colors["Ori"],   label="Original", linewidth=1.6)
    ax.plot(df_qwdap[col_qwdap][:n], color=colors["QWDAP"], label="QWDAP", linewidth=1.4)
    ax.plot(df_arima[col_arima][:n], color=colors["ARIMA"], label="ARIMA", linewidth=1.4)
    ax.plot(df_lstm[col_lstm][:n],   color=colors["LSTM"],  label="LSTM", linewidth=1.4)

    ax.set_title(node, fontsize=30, pad=10)
    ax.set_ylabel("Volume")
    
    # Only show legend on the first subplot (top one)
    if i == 0:
        ax.legend(loc="upper right", frameon=True)

    ax.grid(False)

# Set common x-label
axs[-1].set_xlabel("Time index")
# axs[1].set_ylabel("Volume")

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()