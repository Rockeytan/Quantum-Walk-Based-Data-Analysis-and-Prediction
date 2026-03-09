# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 22:18:41 2025

@author: tlj
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    'axes.labelsize': 20,     
    'axes.titlesize': 22,     
    'xtick.labelsize': 18,    
    'ytick.labelsize': 18,    
    'legend.fontsize': 18,
    'axes.linewidth': 1.5,
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'figure.dpi': 500
})


# -------------------------
# 1. 准备数据
# -------------------------

data = {
    "Subregion": [
        f"N{i}" for i in range(1, 57)
    ],
    "QWDAP": [
        0.9730,0.9763,0.9913,0.9830,0.9710,0.9641,0.9612,0.8833,0.8853,0.9712,
        0.9708,0.9371,0.9490,0.9647,0.7962,0.9264,0.9688,0.6926,0.9760,0.9735,
        0.9149,0.9624,0.9023,0.9415,0.9792,0.8562,0.9464,0.9503,0.9485,0.9758,
        0.9727,0.9382,0.9616,0.9577,0.8475,0.9767,0.9711,0.9576,0.9747,0.8876,
        0.9385,0.9359,0.9604,0.9568,0.9732,0.9760,0.9152,0.9715,0.9238,0.8015,
        0.9698,0.9474,0.9575,0.9666,0.8747,0.9593
    ],
    "ARIMA": [
        0.9237,0.9719,0.9748,0.9773,0.9621,0.9439,0.9265,0.9441,0.9501,0.9685,
        0.9632,0.9679,0.9566,0.9552,0.9542,0.9400,0.9507,0.9553,0.9458,0.9483,
        0.9473,0.9559,0.9495,0.8933,0.9550,0.9362,0.8895,0.9607,0.9626,0.9553,
        0.9465,0.7909,0.9442,0.9281,0.9472,0.9622,0.9461,0.8677,0.9373,0.6955,
        0.9298,0.8956,0.9286,0.9497,0.9103,0.9299,0.9363,0.8790,0.9397,0.9306,
        0.9135,0.9508,0.9292,0.8945,0.9357,0.8784
    ],
    "LSTM": [
        0.9209,0.9707,0.9729,0.9742,0.9620,0.9457,0.9290,0.9392,0.9498,0.9672,
        0.9615,0.9687,0.9524,0.9512,0.9547,0.9389,0.9522,0.9555,0.9422,0.9505,
        0.9470,0.9536,0.9491,0.8960,0.9551,0.9255,0.8785,0.9574,0.9641,0.9550,
        0.9480,0.7798,0.9448,0.9304,0.9465,0.9611,0.9468,0.8646,0.9378,0.6759,
        0.9343,0.8970,0.9293,0.9471,0.9043,0.9335,0.9290,0.8833,0.9392,0.9222,
        0.9048,0.9490,0.9102,0.8734,0.9456,0.8654
    ]
}




import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# 1. 数据
# -------------------------
df = pd.DataFrame(data)

models = ["QWDAP", "ARIMA", "LSTM"]
colors = ["#1f77b4", "#d62728", "#2ca02c"]

avg = df[models].mean()
std = df[models].std()

# -------------------------
# 2. Nature style
# -------------------------
plt.rcParams['font.family'] = 'Arial'
plt.rcParams.update({
    "axes.linewidth": 1.5,
    "xtick.major.width": 1.5,
    "ytick.major.width": 1.5,
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "figure.dpi": 500
})

fig, ax = plt.subplots(figsize=(5, 5))

# -------------------------
# 3. 设置柱子位置（拉大间距）
# -------------------------
x = np.array([0, 1.5, 3.0])   # ← 原本是 [0,1,2]，现在加大间隔
bar_width = 0.35              # ← 稍微变细

bars = ax.bar(
    x,
    avg,
    width=bar_width,
    yerr=std,
    capsize=5,
    color=colors,
    edgecolor='black',
    linewidth=1.2
)

# -------------------------
# 4. 在柱子上方添加数值
# -------------------------
# for xi, v in zip(x, avg):
#     ax.text(
#         xi,
#         v + 0.005,
#         f"{v:.4f}",
#         ha="center",
#         va="bottom",
#         fontsize=14,
#         fontweight="bold"
#     )

# -------------------------
# 5. 坐标轴
# -------------------------
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
ax.set_ylim(0.8, 1)
ax.set_ylabel("Average R² Value")
# ax.set_title("Highest & Most Consistent", pad=10)

# 设置 x 轴标签位置（与柱子对齐）
ax.set_xticks(x)
ax.set_xticklabels(models)

ax.tick_params(axis='both')

plt.tight_layout()
plt.show()
