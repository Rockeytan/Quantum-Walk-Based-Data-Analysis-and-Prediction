# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 13:00:23 2025

@author: tlj
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import matplotlib as mpl
import os

# ==========================================
# 0. 全局样式设置 (Nature 风格)
# ==========================================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    'axes.labelsize': 20,
    'axes.titlesize': 22,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.linewidth': 1.2,
    'figure.dpi': 500
})

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['axes.linewidth'] = 0.5
mpl.rcParams['xtick.major.width'] = 0.5
mpl.rcParams['ytick.major.width'] = 0.5
mpl.rcParams['font.size'] = 5

# ==========================================
# 1. 数据准备：站点信息
# ==========================================
data = {
    'Station': [
        'Honolulu', 'Chichijima', 'Midway Atoll', 'Naha', 'Wake Island',
        'Kauai Island', 'Christmas (Kiritimati)', 'Kanton Atoll', 'Malakal (Palau)',
        'Kwajalein', 'Saipan', 'Apra Harbor (Guam)', 'Vila', 'Nukuʻalofa',
        'Rarotonga', 'Papeete', 'Rikitea', 'Lautoka'
    ],
    'Latitude': [
        21.3156, 27.0667, 28.2075, 26.2123, 19.2800,
        22.0964, 1.9846, -2.8333, 7.3333,
        8.7150, 15.1833, 13.4700, -17.75, -21.13,
        -21.20, -17.53, -23.1200, -17.6167
    ],
    'Longitude': [
        -157.8581, 142.2083, -177.3508, 127.6792, 166.6320,
        -159.5261, -157.4236, -171.6667, 134.4833,
        167.7230, 145.7500, 144.7500, 168.30, -175.18,
        -159.80, -149.57, -134.9700, 177.4500
    ]
}
df = pd.DataFrame(data)

# ==========================================
# 1.1 站点分组
# ==========================================
group_1 = ['Honolulu', 'Chichijima', 'Midway Atoll', 'Naha', 'Wake Island', 'Kauai Island']
group_2 = ['Christmas (Kiritimati)', 'Kanton Atoll', 'Malakal (Palau)', 'Kwajalein', 'Saipan', 'Apra Harbor (Guam)']
group_3 = ['Vila', 'Nukuʻalofa', 'Rarotonga', 'Papeete', 'Rikitea', 'Lautoka']

group_styles = {
    'row1_1980_2019': {'stations': group_1, 'edgecolor': '#1F77B4'},  # blue
    'row2_1979_2018': {'stations': group_2, 'edgecolor': '#2CA02C'},  # green
    'row3_1993_2018': {'stations': group_3, 'edgecolor': '#FF7F0E'}   # orange
}

# ==========================================
# 2. 坐标系统转换：[-180, 180] -> [0, 360]
# ==========================================
df['Lon_Shifted'] = df['Longitude'].apply(lambda x: x + 360 if x < 0 else x)
geometry = [Point(xy) for xy in zip(df['Lon_Shifted'], df['Latitude'])]
gdf_stations = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# ==========================================
# 3. 加载本地 Natural Earth 地图数据（关键修改！）
# ==========================================
# ⚠️ 请将以下路径替换为你实际存放 .shp 文件的位置
local_shapefile_path = r"data\ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"

if not os.path.exists(local_shapefile_path):
    raise FileNotFoundError(
        f"未找到 Natural Earth 数据文件，请先下载并解压到:\n{local_shapefile_path}\n"
        "下载地址: https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/"
    )

print("正在加载本地地图数据...")
world = gpd.read_file(local_shapefile_path)

# 确保 CRS 为 WGS84
if world.crs is None:
    world = world.set_crs("EPSG:4326")
else:
    world = world.to_crs("EPSG:4326")

# 创建右移 360° 的副本以覆盖跨国际日期变更线区域
world_right = world.copy()
world_right.geometry = world.geometry.translate(xoff=360)

# ==========================================
# 4. 绘图
# ==========================================
fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

# 4.1 绘制地图背景
map_style = {'color': '#F2F2F2', 'edgecolor': '#808080', 'linewidth': 0.3}
world.plot(ax=ax, **map_style)
world_right.plot(ax=ax, **map_style)

# 4.2 按组绘制站点（统一灰色填充 + 分组边框色）
for gname, ginfo in group_styles.items():
    sub = df[df['Station'].isin(ginfo['stations'])]
    ax.scatter(
        sub['Lon_Shifted'],
        sub['Latitude'],
        s=30,
        facecolor='gray',
        edgecolor=ginfo['edgecolor'],
        linewidths=1.4,
        zorder=6
    )

# 4.3 添加站点标签
for _, row in df.iterrows():
    x_offset, y_offset = 2.5, 0.5
    ha = 'left'

    # 特殊调整部分标签位置避免重叠
    if row['Station'] in ['Honolulu', 'Christmas (Kiritimati)']:
        y_offset = -2.0
    if row['Station'] == 'Nukuʻalofa':
        y_offset = -2.5

    ax.text(
        row['Lon_Shifted'] + x_offset,
        row['Latitude'] + y_offset,
        row['Station'],
        fontsize=10,
        color='#222222',
        ha=ha,
        va='center',
        zorder=7
    )

# ==========================================
# 5. 坐标轴设置
# ==========================================
ax.set_xlim(140, 220)
ax.set_ylim(-60, 60)
ax.set_aspect('equal')

# X 轴：140°E 到 140°W（显示为 140°E → 180° → 140°W）
xticks = range(120, 241, 20)
xticklabels = []
for x in xticks:
    if x <= 180:
        xticklabels.append(f"{x}°E")
    else:
        xticklabels.append(f"{360 - x}°W")
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)

# Y 轴：纬度标签
yticks = range(-60, 61, 10)
yticklabels = [f"{abs(y)}°{'N' if y > 0 else 'S'}" if y != 0 else "0°" for y in yticks]
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)

ax.set_xlabel('')
ax.set_ylabel('')

plt.tight_layout()
plt.show()

# 如需保存，取消注释以下行：
# plt.savefig('Pacific_Stations_Grouped.png', bbox_inches='tight', dpi=500)
# plt.savefig('Pacific_Stations_Grouped.pdf', bbox_inches='tight')