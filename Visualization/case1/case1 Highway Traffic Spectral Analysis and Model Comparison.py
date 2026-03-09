# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 14:04:14 2025

@author: tlj
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import periodogram

# ======================
# Global style
# ======================
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams.update({
    'axes.labelsize': 30,
    'axes.titlesize': 30,
    'xtick.labelsize': 30,
    'ytick.labelsize': 30,
    'legend.fontsize': 20,
    'axes.linewidth': 1.2,
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'figure.dpi': 500
})

# ======================
# 1. Read data
# ======================
path_obs   = r"data\Observed volume.csv"
path_qw    = r"data\SGETV-QW.csv"
path_lstm  = r"data\LSTM.csv"
path_arima = r"data\ARIMA.csv"

obs   = pd.read_csv(path_obs)
qw    = pd.read_csv(path_qw)
lstm  = pd.read_csv(path_lstm)
arima = pd.read_csv(path_arima)

# ======================
# 2. Select node + preprocess
# ======================
node = "N1"

y_obs   = obs[node].to_numpy(dtype=float)
y_qw    = qw[node].to_numpy(dtype=float)
y_lstm  = lstm[node].to_numpy(dtype=float)
y_arima = arima[node].to_numpy(dtype=float)

fs = 144  # 10-min sampling -> 144 samples/day

# align length
n = min(len(y_obs), len(y_qw), len(y_lstm), len(y_arima))
y_obs, y_qw, y_lstm, y_arima = y_obs[:n], y_qw[:n], y_lstm[:n], y_arima[:n]

def assert_finite(x, name):
    if not np.all(np.isfinite(x)):
        bad = np.sum(~np.isfinite(x))
        raise ValueError(f"{name} contains {bad} NaN/Inf.")

assert_finite(y_obs, "Observed")
assert_finite(y_qw, "QWDAP")
assert_finite(y_lstm, "LSTM")
assert_finite(y_arima, "ARIMA")

df = fs / n  # frequency resolution (cycles/day), for 720 -> 0.2

# ======================
# 3. RAW PSD
# ======================
f,  P_obs   = periodogram(y_obs,   fs=fs, scaling="density")
_,  P_qw    = periodogram(y_qw,    fs=fs, scaling="density")
_,  P_lstm  = periodogram(y_lstm,  fs=fs, scaling="density")
_,  P_arima = periodogram(y_arima, fs=fs, scaling="density")

mask = f > 0
f = f[mask]
P_obs, P_qw, P_lstm, P_arima = P_obs[mask], P_qw[mask], P_lstm[mask], P_arima[mask]

xmin = float(f.min()) * 0.95

# ======================
# 4. Peak-aligned vertical lines (only for interpretable bands)
# ======================
def half_width_for_target(f0, df):
    if np.isclose(f0, 1.0):
        return max(0.30, 1.5 * df)
    if f0 <= 4.0:
        return max(0.40, 2.0 * df)
    return min(0.55, max(0.45, 2.5 * df))

def local_peak_near(f, P, f0, hw):
    band = (f >= f0 - hw) & (f <= f0 + hw)
    if not np.any(band):
        return None
    idx = np.argmax(P[band])
    fx = f[band][idx]
    px = P[band][idx]
    return fx, px, np.where(band)[0]

def prominent_gate(P, band_idx, peak_idx, ratio_thr=1.6):
    Pb = P[band_idx]
    med = float(np.median(Pb))
    pk  = float(P[peak_idx])
    if med <= 0:
        return True
    return (pk / med) >= ratio_thr

# label ONLY period (simple)
targets = [
    ("24h", 1.0, "#1f77b4"),
    ("12h", 2.0, "#ff7f0e"),
    ("8h",  3.0, "#2ca02c"),
    ("6h",  4.0, "#d62728"),
    # ("4h",  6.0, "#9467bd"),
]

marks = []
for lab, f0, c in targets:
    hw = half_width_for_target(f0, df)
    out = local_peak_near(f, P_obs, f0, hw)
    if out is None:
        continue
    fx, px, band_idx = out
    peak_idx = int(np.argmin(np.abs(f - fx)))

    # reject if drift too far (avoid forcing)
    if abs(fx - f0) > 0.95 * hw:
        continue
    if not prominent_gate(P_obs, band_idx, peak_idx, ratio_thr=1.6):
        continue

    marks.append((lab, fx, c))

# ======================
# 5. Plot
# ======================
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(f, P_obs,   color="black",   linewidth=2.2, label="Original")
ax.plot(f, P_qw,    color="#0052cc", linewidth=1.8, label="QWDAP")
ax.plot(f, P_arima, color="#d62728", linestyle="--", linewidth=1.8, label="ARIMA")
ax.plot(f, P_lstm,  color="#2ca02c", linestyle=":",  linewidth=2.2, label="LSTM")

# ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.5, 5)
ax.set_ylim(0.1)


ax.set_xlabel("Frequency (cycles per day)")
ax.set_ylabel("log(PSD)")
ax.set_title(f"Power Spectral Density — {node}", pad=18)

# ax.grid(True, which="both", linestyle="--", alpha=0.3)

# ======================
# 6. Vertical lines + CLEAN labels (fixed y in axes coords)
#    Use axis transform so text stays inside and does not overlap the title.
# ======================
# Text y-positions (axes fraction). Slightly staggered to avoid overlaps.
y_levels = [0.90, 0.82, 0.74, 0.66, 0.58]

# Sort by frequency (left to right) for cleaner staggering
marks = sorted(marks, key=lambda x: x[1])

for i, (lab, fx, c) in enumerate(marks):
    ax.axvline(x=fx, color=c, linestyle="--", linewidth=1.6, alpha=0.85, zorder=0)

    y_ax = y_levels[i] if i < len(y_levels) else 0.58
    ax.text(
        fx, y_ax, lab,
        transform=ax.get_xaxis_transform(),  # x in data coords, y in axes coords (0..1)
        ha="center", va="bottom",
        fontsize=22, color=c, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.75)
    )

ax.legend(loc="best")
fig.tight_layout()
plt.show()

print(f"[Info] n={n}, fs={fs} -> df={df:.3f} cycles/day")
print("[Info] Marked lines (period label, aligned frequency):")
for lab, fx, _ in marks:
    print(f"  - {lab}: {fx:.3f} c/d (T={24/fx:.2f} h)")
