"""
Fig. 5 of Paper2_V36: HOTA difference (host with SCL minus host alone) with the 95% paired-bootstrap
interval for every tested cell. Same cells and numbers as Paper2_V27 (scripts/make_forest.py); only
the artwork follows the journal rules (figstyle.py). Marker shape carries the meaning, color only
repeats it: filled circle = interval above zero; open circle = interval contains zero or identical
output. Sources: research/final/V7_STATISTICS.md, V7_EXTERNAL_TRANSFER.md, sparsetrack_v7f results
(transcribed as in Paper2_V12 scripts/evidence.py) and research/final/V7_UAVDT_RESULT.json (read).

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev36/scripts/make_fig3.py
"""
import json
from pathlib import Path

import figstyle as S
import matplotlib.pyplot as plt

V = Path(__file__).resolve().parents[1]
ROOT = V.parents[1]
uav = json.load(open(ROOT / "research/final/V7_UAVDT_RESULT.json"))["bootstrap"]["per_det"]
ud = {d: (uav[d]["HOTA"]["diff"], uav[d]["HOTA"]["ci_lo"], uav[d]["HOTA"]["ci_hi"]) for d in uav}

GROUPS = [
    ("MOT17, published detections", [
        ("SparseTrack", (0.0551, -0.0112, 0.2537)),
        ("BoostTrack, online", None),
        ("BoostTrack, + GBI", None),
        ("ByteTrack, floor 0.01", (-0.014, -0.058, 0.009)),
        ("ByteTrack, floor 0.1", None),
        ("OC-SORT, floor 0.01", (0.613, 0.363, 1.241)),
        ("OC-SORT, floor 0.1", (0.464, 0.266, 1.086)),
    ]),
    ("KITTI, other detectors", [
        ("ByteTrack, RT-DETR-L", (0.91, 0.22, 1.55)),
        ("BoT-SORT, RT-DETR-L", (0.61, -0.39, 1.61)),
        ("OC-SORT, YOLOv8n", (7.91, 5.47, 9.98)),
    ]),
    ("Predeclared external, MOT17", [
        ("PD-SORT", (0.613, 0.268, 1.646)),
        ("Hybrid-SORT", None),
    ]),
    ("Held-out, UAVDT", [
        ("ByteTrack, RT-DETR-L", ud["rtdetr"]),
        ("ByteTrack, YOLOv8n", ud["yolov8"]),
    ]),
]

n = sum(1 + len(r) for _, r in GROUPS) + 0.4 * (len(GROUPS) - 1)
fig, ax = plt.subplots(figsize=(S.COL_IN, 0.158 * n + 0.62), layout="constrained")
y, yt, yl = 0.0, [], []
for title, rows in GROUPS:
    ax.text(-3.0, y, title, fontweight="bold", va="center", ha="left")
    y -= 1
    for lab, ci in rows:
        d, lo, hi = ci if ci else (0.0, 0.0, 0.0)
        sig = lo > 0
        col = S.BLUE if sig else S.DARK
        ax.plot([lo, hi], [y, y], color=col, lw=1.2, solid_capstyle="butt")
        ax.plot(d, y, "o", ms=4.2, mew=1.0, color=col, mfc=col if sig else "white", zorder=3)
        yt.append(y)
        yl.append(lab)
        y -= 1
    y -= 0.4
ax.axvline(0, color="black", lw=0.6)
ax.set_yticks(yt, yl)
ax.set_ylim(y + 0.6, 0.7)
ax.set_xlim(-3.0, 10.3)
ax.set_xticks([-2, 0, 2, 4, 6, 8, 10])
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.set_xlabel("\u0394HOTA (points)")
fig.savefig(V / "Fig3.pdf")
print("wrote Fig3.pdf", fig.get_size_inches() * 25.4, "mm")
