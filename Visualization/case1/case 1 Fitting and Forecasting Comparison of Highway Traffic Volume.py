import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =====================
# 全局样式设置
# =====================
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


# =====================
# 读取数据
# =====================
path_obs   = r"data\Observed volume.csv"
path_qw    = r"data\SGETV-QW.csv"
path_lstm  = r"data\LSTM.csv"
path_arima = r"data\ARIMA.csv"

obs   = pd.read_csv(path_obs)
qw    = pd.read_csv(path_qw)
lstm  = pd.read_csv(path_lstm)
arima = pd.read_csv(path_arima)

# =====================
# 选择节点
# =====================
node = "N1"

y_obs   = obs[node].values
y_qw    = qw[node].values
y_lstm  = lstm[node].values
y_arima = arima[node].values

# =====================
# 划分 Fitting (80%) / Forecasting (20%)
# =====================
sim_len  = int(len(y_obs) * 0.80)
pred_len = len(y_obs) - sim_len
cut = sim_len

x = np.arange(len(y_obs))   # ← 这里使用 Time Index，不再转换为天

# =====================
# 颜色方案（保持一致）
# =====================
COLOR_ORI   = "black"
COLOR_QW    = "blue"
COLOR_ARIMA = "red"
COLOR_LSTM  = "green"

# =====================
# 绘制整合图
# =====================
plt.figure(figsize=(14, 7))

# 训练区间（实线）
plt.plot(x[:cut], y_obs[:cut],   color=COLOR_ORI,   linewidth=1.8)
plt.plot(x[:cut], y_qw[:cut],    color=COLOR_QW,    linewidth=1.5)
plt.plot(x[:cut], y_arima[:cut], color=COLOR_ARIMA, linestyle="--", linewidth=1.5)
plt.plot(x[:cut], y_lstm[:cut],  color=COLOR_LSTM,  linestyle=":",  linewidth=1.5)

# 预测区间（虚线）
plt.plot(x[cut:], y_obs[cut:],   color=COLOR_ORI,   linestyle="--", linewidth=1.8)
plt.plot(x[cut:], y_qw[cut:],    color=COLOR_QW,    linestyle="--", linewidth=1.5)
plt.plot(x[cut:], y_arima[cut:], color=COLOR_ARIMA, linestyle="--", linewidth=1.5)
plt.plot(x[cut:], y_lstm[cut:],  color=COLOR_LSTM,  linestyle="--", linewidth=1.5)

# 竖线分割 Fitting 与 Forecasting
plt.axvline(x=cut, color="black", linestyle="--", linewidth=2)



# 轴名称
plt.ylabel("Volume", )
plt.xlabel("Time Index")

# 标题
plt.title(f"{node}",fontsize=30)

# 图例
plt.legend(["Original", "QWDAP", "ARIMA", "LSTM"], loc="best")

plt.tight_layout()
plt.show()
