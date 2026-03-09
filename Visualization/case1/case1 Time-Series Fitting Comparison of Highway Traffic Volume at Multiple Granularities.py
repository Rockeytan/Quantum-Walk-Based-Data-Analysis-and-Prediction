# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 15:01:22 2025

@author: tlj
"""

import pandas as pd
import matplotlib.pyplot as plt

# ========================
# 全局字体与样式设置
# ========================
plt.rcParams['font.family'] = 'Times New Roman'   # 注意拼写：Roman
plt.rcParams.update({
    'axes.labelsize': 18,
    'axes.titlesize': 20,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'legend.fontsize': 16,
    'axes.linewidth': 1.2,
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'figure.dpi': 500
})

# ========================
# 选择节点，例如 N1、N2、N3...
# ========================
node = "N1"                         # ← 想换节点只改这里
col_ori = f"{node}_Ori"
col_fit = f"{node}_Fit"

# ========================
# 读取两个数据文件
# ========================
df_3min = pd.read_csv(
    r"data\FinalResult_3min.csv"
)
df_30min = pd.read_csv(
    r"data\FinalResult_60min.csv"
)

# ========================
# 绘图（上下子图）
# ========================
fig, axs = plt.subplots(2, 1, figsize=(12, 8))

# 上图（3min）
axs[0].plot(df_3min[col_ori], color='black', label='Original', linewidth=1.8)
axs[0].plot(df_3min[col_fit], color='blue', label='QWDAP', linewidth=1.5)
axs[0].set_title(f"{node} — 3-min granularity")
axs[0].legend(loc='upper right')
axs[0].set_ylabel("Volume")

# 下图（60min）
axs[1].plot(df_30min[col_ori], color='black', linewidth=1.8)
axs[1].plot(df_30min[col_fit], color='blue', linewidth=1.5)
axs[1].set_title(f"{node} — 60-min granularity")
axs[1].set_ylabel("Volume")
axs[1].set_xlabel("Time Index")

plt.tight_layout()
plt.show()

