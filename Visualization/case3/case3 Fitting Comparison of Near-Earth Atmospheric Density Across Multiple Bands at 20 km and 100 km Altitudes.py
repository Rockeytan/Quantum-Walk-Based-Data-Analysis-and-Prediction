# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:17:12 2025

@author: tlj
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

# ======================
# 设置 Nature 风格
# ======================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    'axes.labelsize': 20,
    'axes.titlesize': 20,
    'xtick.labelsize': 15,
    'ytick.labelsize': 15,
    'axes.linewidth': 1.2,
    'figure.dpi': 450,
})

# ======================
# 读数据
# ======================
df = pd.read_csv("data\orifit_dens_20km.csv")
cols = df.columns.tolist()

# 提取 N 列名
stations = sorted(set(re.findall(r"(N\d+)_", "_".join(cols))))

# 保存路径
save_dir = "J:\数据恢复\Quantum Walk-Based Data Analysis and Prediction\图\case3\Fig_Compare"
os.makedirs(save_dir, exist_ok=True)

# ======================
# 批量绘制
# ======================
for st in stations:

    suffixes = []
    for h in ["20", "100"]:
        if f"{st}_Ori_{h}" in df.columns:
            suffixes.append(h)

    if not suffixes:
        continue

    fig, axes = plt.subplots(1, len(suffixes), figsize=(12, 3), sharex=False)
    if len(suffixes) == 1:
        axes = [axes]

    plt.subplots_adjust(wspace=0)

    for i, h in enumerate(suffixes):
        ori = df[f"{st}_Ori_{h}"].values
        fit = df[f"{st}_Fit_{h}"].values
        x = np.arange(len(ori))

        ax = axes[i]
        ax.plot(x, ori, '-k', lw=2, label="Original")
        ax.plot(x, fit, '-b', lw=1, label="QWDAP")
        
        ax.set_title(f"{st} - {h} km")
        ax.set_xlabel("Time index")

        # ---- Y轴仅左侧展示
        if i == 0:
            ax.set_ylabel("Density")
        else:
            ax.set_ylabel("")

        # ---- 仅 N1-20km 显示 legend
        if st == "N1" and h == "20":
            ax.legend(frameon=True, fontsize=15)
        else:
            ax.legend([], [], frameon=False)

        ax.grid(False)

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f"{st}.png"), bbox_inches="tight")
    plt.show()
    plt.close()

print("🎯绘图完成（仅 N1-20km 显示图例）")
