# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 12:21:59 2025

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. 性能数据
# =========================
stations = ['Group 1', 'Group 2', 'Group 3']

mae = np.array([41.32214399, 41.55144031, 20.06181157])
rmse = np.array([51.97350730, 52.34628013, 25.19369050])
r2 = np.array([0.640678861, 0.702718815, 0.823390065])

# =========================
# 2. 全局风格（投稿级）
# =========================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    'axes.labelsize': 20,
    'axes.titlesize': 22,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'axes.linewidth': 1.2,
    'figure.dpi': 500
})

# Nature-safe 配色
color_mae  = '#9AC9A5'   # muted green
color_rmse = '#E6A15A'   # muted orange
color_r2   = '#4C6A92'   # muted blue

# =========================
# 3. 绘图
# =========================
fig, ax1 = plt.subplots(figsize=(6.8, 3.6), dpi=500)

x = np.arange(len(stations))
width = 0.15   # ✅ 最终确认的柱宽（细但稳定）

# --- 左轴：MAE / RMSE ---
bar_mae = ax1.bar(
    x - width, mae, width=width,
    color=color_mae, label='MAE'
)
bar_rmse = ax1.bar(
    x, rmse, width=width,
    color=color_rmse, label='RMSE'
)

ax1.set_ylabel('MAE / RMSE', fontsize=15)
ax1.set_xticks(x)
ax1.set_xticklabels(stations, fontsize=15)
ax1.set_ylim(0, max(rmse) * 1.15)

ax1.tick_params(axis='y', labelsize=15)
ax1.tick_params(axis='x', length=6)

# --- 右轴：R² ---
ax2 = ax1.twinx()
bar_r2 = ax2.bar(
    x + width, r2, width=width,
    color=color_r2, label=r'$R^2$'
)

ax2.set_ylabel(r'$R^2$', fontsize=15)
ax2.set_ylim(0, 1.0)
ax2.tick_params(axis='y', labelsize=15)

# =========================
# 4. 图例（最终版：清晰但不抢）
# =========================
handles = [bar_mae, bar_rmse, bar_r2]
labels = ['MAE', 'RMSE', r'$R^2$']

ax1.legend(
    handles, labels,
    loc='upper center',
    ncol=3,
    frameon=False,
    fontsize=14,
    handlelength=1.6,
    columnspacing=1.6,
    bbox_to_anchor=(0.5, 1.05)
)

# =========================
# 5. 标题与收尾
# =========================
# ax1.set_title('Performance Comparison', fontsize=22, pad=14)

ax1.grid(False)
ax2.grid(False)

plt.tight_layout()
plt.show()
