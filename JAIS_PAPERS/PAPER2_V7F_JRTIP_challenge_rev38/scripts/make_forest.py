"""
Fig. 3 of Paper2_V38: HOTA difference (host with SCL minus host alone) with the 95% paired-bootstrap
interval for every tested cell. Same cells and style as the Paper2_V11 figure, plus the held-out
VisDrone confirmation split. Sources: research/final/V7_STATISTICS.md, V7_EXTERNAL_TRANSFER.md and
sparsetrack_v7f/results.json (transcribed below, as in Paper2_V12 scripts/evidence.py) and
research/final/V7_CONF16_RESULT.json (read).

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev38/scripts/make_forest.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

V = Path(__file__).resolve().parents[1]
ROOT = V.parents[1]
plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "serif", "font.size": 6,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
                     "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
POS, ZERO, NEG = "#1f77b4", "#7f7f7f", "#d62728"

conf16 = json.load(open(ROOT / "research/final/V7_CONF16_RESULT.json"))["bootstrap"]["per_det"]
uav = json.load(open(ROOT / "research/final/V7_UAVDT_RESULT.json"))["bootstrap"]["per_det"]
ud = {d: (uav[d]["HOTA"]["diff"], uav[d]["HOTA"]["ci_lo"], uav[d]["HOTA"]["ci_hi"]) for d in uav}
vd = {d: (conf16[d]["HOTA"]["diff"], conf16[d]["HOTA"]["ci_lo"], conf16[d]["HOTA"]["ci_hi"]) for d in conf16}

GROUPS = [
    ("MOT17, published detections", [
        ("SparseTrack", (0.0551, -0.0112, 0.2537)),
        ("BoostTrack online", None),
        ("BoostTrack + GBI", None),
        ("ByteTrack floor 0.01", (-0.014, -0.058, 0.009)),
        ("ByteTrack floor 0.1", None),
        ("OC-SORT floor 0.01", (0.613, 0.363, 1.241)),
        ("OC-SORT floor 0.1", (0.464, 0.266, 1.086)),
    ]),
    ("KITTI, other detectors", [
        ("ByteTrack, RT-DETR-L", (0.91, 0.22, 1.55)),
        ("BoT-SORT, RT-DETR-L", (0.61, -0.39, 1.61)),
        ("OC-SORT, YOLOv8n", (7.91, 5.47, 9.98)),
    ]),
    ("Predeclared external: MOT17", [
        ("PD-SORT", (0.613, 0.268, 1.646)),
        ("Hybrid-SORT", None),
    ]),
    ("Held-out: UAVDT", [
        ("ByteTrack, RT-DETR-L", ud["rtdetr"]),
        ("ByteTrack, YOLOv8n", ud["yolov8"]),
    ]),
]

n = sum(1 + len(r) for _, r in GROUPS)
fig, ax = plt.subplots(figsize=(3.45, 0.205 * n))
y, yt, yl = 0.0, [], []
for title, rows in GROUPS:
    ax.text(-3.0, y, title, fontweight="bold", fontsize=6, va="center")
    y -= 1
    for lab, ci in rows:
        d, lo, hi = ci if ci else (0.0, 0.0, 0.0)
        col = POS if lo > 0 else NEG if hi < 0 else ZERO
        ax.plot([lo, hi], [y, y], color=col, lw=1.4)
        ax.plot(d, y, "o", color=col, ms=3.5, mfc=col if lo > 0 else "white", mew=1.0)
        yt.append(y)
        yl.append(lab)
        y -= 1
    y -= 0.4
ax.axvline(0, color="k", lw=0.6)
ax.set_yticks(yt, yl, fontsize=5.8)
ax.set_xlim(-3.0, 10.3)
ax.set_xticks([-2, 0, 2, 4, 6, 8, 10])
ax.tick_params(axis="x", labelsize=5.8)
ax.tick_params(axis="y", length=0)
ax.set_xlabel(r"$\Delta$HOTA, host + SCL minus host (points, 95% interval)", fontsize=6.3)
fig.savefig(V / "fig3_forest_col.pdf")
print("wrote fig3_forest_col.pdf:", sum(len(r) for _, r in GROUPS), "cells")
