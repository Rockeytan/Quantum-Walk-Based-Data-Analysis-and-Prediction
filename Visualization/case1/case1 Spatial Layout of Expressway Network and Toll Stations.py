import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ============================
# 1. 读取 shapefile
# ============================
gdf_road = gpd.read_file(
    r"data\Station_location\高速公路_7个点.shp"
)
gdf_station = gpd.read_file(
    r"data\Station_location\收费站点_7个.shp"
)
gdf_city = gpd.read_file(
    r"data\Station_location\途径城市2.shp"
)

# ============================
# 2. 统一投影到经纬度（WGS84）
# ============================
target_crs = "EPSG:4326"  # WGS84，经纬度
if gdf_road.crs is not None:
    gdf_road = gdf_road.to_crs(target_crs)
if gdf_station.crs is not None:
    gdf_station = gdf_station.to_crs(target_crs)
if gdf_city.crs is not None:
    gdf_city = gdf_city.to_crs(target_crs)

# ============================
# 3. 基本图形设置
# ============================
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

fig, ax = plt.subplots(figsize=(5, 8),dpi=500)

# ============================
# 4. 绘制城市底图（浅灰）
# ============================
# gdf_city.plot(ax=ax, color="#E8E8E8", edgecolor="white", linewidth=0.3, zorder=0)

# ============================
# 5. 绘制高速公路（细灰线）
# ============================
gdf_road.plot(ax=ax, color="gray", linewidth=3, alpha=0.85, zorder=1)

# ============================
# 6. 绘制收费站点（白色空心圆）
# ============================
gdf_station.plot(
    ax=ax,
    color="white",
    edgecolor="black",
    markersize=40,
    linewidth=1,
    zorder=3
)

# ============================
# 7. 站点标签：直接 N1, N2, ...
# ============================
# for idx, row in gdf_station.iterrows():
#     x, y = row.geometry.x, row.geometry.y
#     label = f"N{idx + 1}"
#     # 经度 / 纬度尺度更小，偏移量也调小一点
#     ax.text(x + 0.02, y + 0.02, label, fontsize=8, weight="bold", zorder=4)

# ============================
# 8. 图例（灰条表示高速公路 / Toll Station）
# ============================
# legend_rect = Rectangle((0, 0), 1, 1, fc="gray", alpha=0.8)
# ax.legend([legend_rect], ["Toll Station"], loc="lower left", frameon=False, fontsize=9)

# ============================
# 9. 坐标轴设置：经纬度 & 细轴
# ============================
# 隐藏所有四条边框
for spine in ['top', 'right', 'bottom', 'left']:
    ax.spines[spine].set_visible(False)

# 完全移除坐标轴刻度（包括刻度线和刻度标签）
ax.set_xticks([])
ax.set_yticks([])

# 移除坐标轴标签
ax.set_xlabel('')
ax.set_ylabel('')

# 移除标题（如果之前设置了）
ax.set_title('')

# （可选）关闭科学计数法其实已无影响，因为没刻度了，但保留也无妨
ax.ticklabel_format(style='plain', axis='both')

# 保持经纬度比例
ax.set_aspect('equal', adjustable='box')

# 紧凑布局
plt.tight_layout()
plt.show()
