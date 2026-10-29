"""
Fig. 6 of Paper2_V45: per-sequence HOTA differences (host with SCL minus host alone) on MOT17
val-half. Same numbers as Paper2_V27 Fig. 4 (PAPER2_UNIVERSAL_ACMOT_JAIS/scripts/evidence.py PER_SEQ,
from research/final/V7_MAIN_RESULTS.md Table 2 and V7_EXTERNAL_TRANSFER.md, transcribed below).
Every cell prints its value, so the figure does not depend on color; the text is black or white,
whichever gives the higher contrast with the cell.

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev45/scripts/make_fig4.py
"""
from pathlib import Path

import figstyle as S
import matplotlib.pyplot as plt
import numpy as np

V = Path(__file__).resolve().parents[1]
SEQS = ["02", "04", "05", "09", "10", "11", "13"]
PER_SEQ = {
    "OC-SORT (0.01)": [0.25, 0.54, 0.45, 2.90, 1.27, 0.34, 0.03],
    "OC-SORT (0.1)": [0.42, 0.21, 0.37, 1.40, 1.14, 0.71, 1.48],
    "PD-SORT": [0.11, 0.20, 1.23, 1.42, 2.39, 0.57, 1.55],
    "SparseTrack": [0.09, 0.00, 0.00, 0.00, 0.52, 0.00, -0.07],
    "ByteTrack (0.01)": [0.00, 0.00, -0.01, 0.00, 0.04, 0.00, -0.21],
    "BoostTrack": [0, 0, 0, 0, 0, 0, 0],
    "Hybrid-SORT": [0, 0, 0, 0, 0, 0, 0],
}
names = list(PER_SEQ)
M = np.array([PER_SEQ[k] for k in names], float)
lim = 3.0
cmap = plt.get_cmap("RdBu")
fig, ax = plt.subplots(figsize=(S.TEXT_IN, 2.25), layout="constrained")
im = ax.imshow(M, cmap=cmap, vmin=-lim, vmax=lim, aspect="auto")


def lum(rgb):
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb[:3]]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        L = lum(cmap((M[i, j] + lim) / (2 * lim)))
        txt = "black" if (L + 0.05) / 0.05 >= 1.05 / (L + 0.05) else "white"
        ax.text(j, i, f"{M[i, j]:+.2f}" if M[i, j] else "0", ha="center", va="center", color=txt)
ax.set_xticks(range(len(SEQS)), [f"MOT17-{s}" for s in SEQS])
ax.set_yticks(range(len(names)), names)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
cb = fig.colorbar(im, ax=ax, pad=0.01, fraction=0.03)
cb.set_label("ΔHOTA (points)")
cb.outline.set_linewidth(0.6)
fig.savefig(V / "Fig6.pdf")
print("wrote Fig6.pdf", fig.get_size_inches() * 25.4, "mm")
