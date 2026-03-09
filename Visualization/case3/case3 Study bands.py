# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 14:39:06 2025

@author: tlj
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# =========================
# 1) 参数：纬度范围与条带数
# =========================
lat_min, lat_max = -52, 48   # 52°S–48°N
n_bands = 25                # 25 latitude bands

# 条带边界（26条边界，25个区间）
edges = np.linspace(lat_min, lat_max, n_bands + 1)
mids  = 0.5 * (edges[:-1] + edges[1:])  # 每条带中心纬度

# =========================
# 2) 画布与投影（球面视角）
# =========================
lon0, lat0 = 110, 20  # 视角中心（可调整）
proj = ccrs.Orthographic(central_longitude=lon0, central_latitude=lat0)

fig = plt.figure(figsize=(7.2, 7.2), dpi=450)
ax = plt.axes(projection=proj)
ax.set_global()

# =========================
# 3) 生成条带着色（上黄下紫，接近示例）
# =========================
cmap = plt.get_cmap("viridis", n_bands)
norm = mpl.colors.Normalize(vmin=0, vmax=n_bands - 1)

# 经度采样（越密越平滑）
lons = np.linspace(-180, 180, 721)

# 逐条带画一个“纬向矩形面片”（PlateCarree 坐标下）
for j in range(n_bands):
    lat_lo, lat_hi = edges[j], edges[j + 1]
    lon2d, lat2d = np.meshgrid(lons, [lat_lo, lat_hi])
    val = np.full((1, lon2d.shape[1] - 1), j)

    ax.pcolormesh(
        lon2d, lat2d, val,
        transform=ccrs.PlateCarree(),
        cmap=cmap, norm=norm,
        shading="flat"
    )

# （可选）把范围外（极区）涂成浅灰，突出“只选了 52S–48N”
mask_color = "#dddddd"
mask_cmap = mpl.colors.ListedColormap([mask_color])

# 北极帽：lat_max -> 90
lon2d, lat2d = np.meshgrid(lons, [lat_max, 90])
val = np.zeros((1, lon2d.shape[1] - 1))
ax.pcolormesh(
    lon2d, lat2d, val,
    transform=ccrs.PlateCarree(),
    cmap=mask_cmap, shading="flat"
)

# 南极帽：-90 -> lat_min
lon2d, lat2d = np.meshgrid(lons, [-90, lat_min])
ax.pcolormesh(
    lon2d, lat2d, val,
    transform=ccrs.PlateCarree(),
    cmap=mask_cmap, shading="flat"
)

# =========================
# 4) 地理要素：海岸线等
# =========================
ax.add_feature(
    cfeature.COASTLINE.with_scale("110m"),
    linewidth=0.6,
    alpha=0.8
)

# 兼容不同 cartopy 版本：尽量设置球面外框线宽（可用就用，不可用就跳过）
try:
    ax.spines["geo"].set_linewidth(1.0)
except Exception:
    pass

# =========================
# 5) （可选）标注每条带编号 N01...N25
# =========================
add_labels = True
if add_labels:
    label_lon = lon0  # 在中心经线附近标注
    for j, latm in enumerate(mids, start=1):
        ax.text(
            label_lon, latm, f"N{j:02d}",
            transform=ccrs.PlateCarree(),
            ha="center", va="center",
            fontsize=7, color="k", alpha=0.65
        )

plt.tight_layout(pad=0.2)
plt.show()

# 保存（可选）
# fig.savefig("Figure5a_25_latitude_bands.png", dpi=600, bbox_inches="tight", transparent=True)
# fig.savefig("Figure5a_25_latitude_bands.pdf", bbox_inches="tight")
