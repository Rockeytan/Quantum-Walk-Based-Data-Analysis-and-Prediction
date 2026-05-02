# -*- coding: utf-8 -*-
"""
Created on Sat May  2 22:54:49 2026

@author: user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =====================
# 全局样式设置
# =====================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    'axes.labelsize': 30,
    'axes.titlesize': 22,
    'xtick.labelsize': 30,
    'ytick.labelsize': 30,
    'legend.fontsize': 20,
    'axes.linewidth': 1.2,
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'figure.dpi': 500
})

# =====================
# 读取数据
# =====================
path_obs   = r"data\Observed volume.csv"
path_qw    = r"data\SGETV-QW.csv"
path_lstm  = r"data\LSTM.csv"
path_arima = r"data\ARIMA.csv"
path_nhits = r"data\HITS.csv"

obs   = pd.read_csv(path_obs)
qw    = pd.read_csv(path_qw)
lstm  = pd.read_csv(path_lstm)
arima = pd.read_csv(path_arima)
nhits = pd.read_csv(path_nhits)

# 去除列名空格
for df in [obs, qw, lstm, arima, nhits]:
    df.columns = df.columns.str.strip()

# =====================
# 选择节点
# =====================
node = "N1"

y_obs   = obs[node].values
y_qw    = qw[node].values
y_lstm  = lstm[node].values
y_arima = arima[node].values

# HITS.csv 如果列名是 N1，就用 node；
# 如果列名是 N1_Ori，就自动切换
if node in nhits.columns:
    y_nhits = nhits[node].values
else:
    y_nhits = nhits[f"{node}_Ori"].values

# =====================
# 对齐长度
# =====================
n = min(len(y_obs), len(y_qw), len(y_lstm), len(y_arima), len(y_nhits))

y_obs   = y_obs[:n]
y_qw    = y_qw[:n]
y_lstm  = y_lstm[:n]
y_arima = y_arima[:n]
y_nhits = y_nhits[:n]

# =====================
# 划分 Fitting / Forecasting
# =====================
sim_len = int(n * 0.80)
cut = sim_len

x = np.arange(n)

# =====================
# 颜色方案
# =====================
COLOR_ORI   = "black"
COLOR_QW    = "blue"
COLOR_ARIMA = "red"
COLOR_LSTM  = "green"
COLOR_NHITS = "#9467bd"

# =====================
# 绘制整合图
# =====================
plt.figure(figsize=(14, 7))

# Fitting 区间
plt.plot(x[:cut], y_obs[:cut],   color=COLOR_ORI,   linewidth=1.8)
plt.plot(x[:cut], y_qw[:cut],    color=COLOR_QW,    linewidth=1.5)
plt.plot(x[:cut], y_arima[:cut], color=COLOR_ARIMA, linestyle="--", linewidth=1.5)
plt.plot(x[:cut], y_lstm[:cut],  color=COLOR_LSTM,  linestyle=":",  linewidth=1.5)
plt.plot(x[:cut], y_nhits[:cut], color=COLOR_NHITS, linestyle="-.", linewidth=1.5)

# Forecasting 区间
plt.plot(x[cut:], y_obs[cut:],   color=COLOR_ORI,   linestyle="--", linewidth=1.8)
plt.plot(x[cut:], y_qw[cut:],    color=COLOR_QW,    linestyle="--", linewidth=1.5)
plt.plot(x[cut:], y_arima[cut:], color=COLOR_ARIMA, linestyle="--", linewidth=1.5)
plt.plot(x[cut:], y_lstm[cut:],  color=COLOR_LSTM,  linestyle="--", linewidth=1.5)
plt.plot(x[cut:], y_nhits[cut:], color=COLOR_NHITS, linestyle="--", linewidth=1.5)

# 分割线
plt.axvline(x=cut, color="black", linestyle="--", linewidth=2)

# 轴名称
plt.ylabel("Volume")
plt.xlabel("Time Index")

# 标题
plt.title(f"{node}", fontsize=30)

# 图例
plt.legend(
    ["Original", "QWDAP", "ARIMA", "LSTM", "N-HiTS"],
    loc="upper left"
)

plt.tight_layout()
plt.show()
