# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 19:02:01 2025

@author: tlj
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    'axes.labelsize': 30,     # ← X/Y 轴名称字体大小
    'axes.titlesize': 22,     # ← 标题字体大小
    'xtick.labelsize': 30,    # ← X 轴刻度字体大小
    'ytick.labelsize': 30,    # ← Y 轴刻度字体大小
    'legend.fontsize': 20,    # ← 图例字体大小
    'axes.linewidth': 1.2,
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'figure.dpi': 500
})
# ==========================
# 1. 读取数据
# ==========================
df = pd.read_csv("data\Ori_10min_new.csv")  # ← 已上传数据路径
y = df["N1"].values

# ==========================
# 2. 绘图样式
# ==========================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    'axes.linewidth': 2.0,       # 边框加粗
    'xtick.major.width': 1.5,
    'ytick.major.width': 1.5,
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'figure.dpi': 500
})

# ==========================
# 3. 绘制折线图
# ==========================
plt.figure(figsize=(10, 8))

plt.plot(y, color='black', linewidth=2)

plt.title("Sample Traffic Volume (N1)",fontsize=30)
plt.ylabel("Volume")
plt.xlabel("Time Index")

# 去掉网格
plt.grid(False)

# 四边加粗
ax = plt.gca()
for spine in ax.spines.values():
    spine.set_linewidth(2)

plt.tight_layout()
plt.show()
