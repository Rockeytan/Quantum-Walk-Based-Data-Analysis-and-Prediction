import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import transbigdata as tbd
import matplotlib as mpl

# =========================
# 基本绘图设置
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

# =========================
# 文件路径
# =========================
path_station = r"data\stations_0.01_20161101.csv"
path_coef = r"data\coefficients.csv"

# =========================
# 1. 读取站点坐标
# =========================
df = pd.read_csv(path_station)
lon = df.iloc[:, 1].values  # 第2列为经度
lat = df.iloc[:, 2].values  # 第3列为纬度
names = [f"N{i}" for i in range(1, len(lon) + 1)]

# =========================
# 2. 构建 0.01° × 0.01° 网格多边形
# =========================
res = 0.01
half = res / 2
tiles = []
for x, y in zip(lon, lat):
    tiles.append(Polygon([
        (x - half, y - half),
        (x + half, y - half),
        (x + half, y + half),
        (x - half, y + half)
    ]))

gdf_tiles = gpd.GeoDataFrame(
    {"Name": names, "lon": lon, "lat": lat},
    geometry=tiles,
    crs="EPSG:4326"
)

# =========================
# 3. 读取系数数据
# =========================
coef_df = pd.read_csv(path_coef)
coef_values = coef_df.values

# 只取前4列系数用于绘图
for i in range(4):
    gdf_tiles[f"Coef{i+1}"] = coef_values[i, :]

# =========================
# 绘图参数
# =========================
bounds = [104.039, 30.65294, 104.1221, 30.72394]
titles = ["1st scale", "2nd scale", "3rd scale", "4th scale"]
cols = ["Coef1", "Coef2", "Coef3", "Coef4"]

# =========================
# 自定义色带
# =========================
colors = ['#fff5eb', '#fee6ce', '#fdc08c', '#f1694c', '#b30000']
custom_cmap = mpl.colors.LinearSegmentedColormap.from_list("influence", colors, N=256)
norm = mpl.colors.Normalize(vmin=0, vmax=1)  # 全局归一化范围

# =========================
# 创建 1 行 4 列子图 + 底部 colorbar 空间
# =========================
fig, axes = plt.subplots(
    1, 4, 
    figsize=(22, 6),
    gridspec_kw={'bottom': 0.18}  # 为底部 colorbar 留出空间
)

# 存储所有 norm_val 用于统一颜色映射（可选，这里已全局归一化）
for idx in range(4):
    ax = axes[idx]
    col = cols[idx]

    # 归一化到 [0, 1]（按各列实际 min/max）
    actual_min = gdf_tiles[col].min()
    actual_max = gdf_tiles[col].max()
    if actual_max == actual_min:
        data_norm = pd.Series([0.5] * len(gdf_tiles), index=gdf_tiles.index)
    else:
        data_norm = (gdf_tiles[col] - actual_min) / (actual_max - actual_min)
        data_norm = data_norm.clip(0, 1)

    # 底图
    tbd.plot_map(ax, bounds=bounds, zoom='auto', style=1)

    # 热力网格
    gdf_plot = gdf_tiles.copy()
    gdf_plot["norm_val"] = data_norm
    gdf_plot.plot(
        ax=ax,
        column="norm_val",
        cmap=custom_cmap,
        norm=norm,  # 使用统一 norm
        edgecolor="black",
        linewidth=0.65,
        linestyle="--",
        alpha=0.35,
        zorder=4
    )

    # 网格边界
    gdf_tiles.boundary.plot(
        ax=ax,
        color="black",
        linewidth=0.3,
        linestyle="--",
        alpha=0.45,
        zorder=5
    )

    # 标题与坐标轴
    ax.set_title(titles[idx], fontsize=24)
    ax.set_xlabel("Longitude", fontsize=20)
    if idx == 0:
        ax.set_ylabel("Latitude", fontsize=20)
    else:
        ax.set_ylabel("")

    ax.tick_params(labelsize=15)
    ax.set_aspect('equal')
    ax.grid(False)

    # 隐藏边框
    for spine in ax.spines.values():
        spine.set_visible(False)

# =========================
# 添加共享 colorbar（底部居中）
# =========================
sm = mpl.cm.ScalarMappable(norm=norm, cmap=custom_cmap)
sm._A = []  # 必须设置，否则警告

cbar_ax = fig.add_axes([0.35, 0.06, 0.3, 0.02])  # [left, bottom, width, height]
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')

cbar.set_label("Normalized Coefficient", fontsize=22, labelpad=10)
cbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
cbar.set_ticklabels(['Low', '', '', '', 'High'])
cbar.ax.tick_params(labelsize=18)

# =========================
# 显示与保存
# =========================
plt.show()

# 可选：保存图像
# fig.savefig(r"E:\...\coefficient_maps_1x4_shared_colorbar.png", dpi=500, bbox_inches='tight')