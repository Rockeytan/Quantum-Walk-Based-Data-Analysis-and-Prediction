# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 11:22:01 2025

@author: user
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 1) 文件路径
# =========================
BASE_DIR = r"your_path"
FILES = [
    os.path.join(BASE_DIR, "1_FinalResult.csv"),
    os.path.join(BASE_DIR, "2_FinalResult.csv"),
    os.path.join(BASE_DIR, "3_FinalResult.csv"),
]

CHOSEN_NODE = {
    FILES[0]: "N1",
    FILES[1]: "N2",
    # FILES[2]: "N3",
}

# =========================
# 2) 风格
# =========================
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({
    "axes.linewidth": 1.0,
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "figure.dpi": 500
})

OBS_COLOR = "#4C78A8"   # 观测
FIT_COLOR = "#B23A3A"   # 拟合

# =========================
# 3) 读取（处理空表头）
# =========================
def read_finalresult(path):
    df = pd.read_csv(path)
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "Time"})
    return df

dfs = [read_finalresult(f) for f in FILES]

# =========================
# 4) 统一长度（关键）
# =========================
min_len = min(len(df) for df in dfs)
dfs = [df.iloc[:min_len].reset_index(drop=True) for df in dfs]

# =========================
# 5) 绘图函数
# =========================
def plot_node(ax, df, node, show_legend=False):
    ori = f"{node}_Ori"
    fit = f"{node}_Fit"

    x = range(len(df))
    y_ori = df[ori].values
    y_fit = df[fit].values

    if show_legend:
        ax.plot(x, y_ori, color=OBS_COLOR, linewidth=2,
                alpha=0.75, label="Observed")
        ax.plot(x, y_fit, color=FIT_COLOR, linewidth=3,
                alpha=0.95, label="QWDAP")
        ax.legend(
            loc="best",
            fontsize=18,
            frameon=True
        )
    else:
        ax.plot(x, y_ori, color=OBS_COLOR, linewidth=2, alpha=0.75)
        ax.plot(x, y_fit, color=FIT_COLOR, linewidth=3, alpha=0.95)
    ax.set_ylabel('SSH(mm)', fontsize=20)
    ax.grid(False)
    ax.tick_params(axis="both", labelsize=20, length=4)

# =========================
# 6) 主图
# =========================
fig, axes = plt.subplots(2, 1, figsize=(12, 5), sharex=True)

for i, path in enumerate(FILES):
    plot_node(
        axes[i],
        dfs[i],
        CHOSEN_NODE[path],
        show_legend=(i == 0)   # ✅ 只在第一张子图加图例
    )

axes[1].set_xlabel("Time index", fontsize=2)

plt.tight_layout()
plt.show()
