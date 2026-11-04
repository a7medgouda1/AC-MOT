"""
Fig. 8 of Paper2_V47: HOTA under shifted detector scores (MOT17 val-half, floor 0.01; BoostTrack 0.1),
host alone and with SCL, one panel per tracker, labelled (a)-(d). Same numbers as Paper2_V27 Fig. 5
(research/final/V7_EXPERIMENT_LEDGER.md STRESS-L, V7_MAIN_RESULTS.md Table 3, as transcribed in
Paper2_V12 scripts/evidence.py). Artwork per the journal rules (figstyle.py): the two series differ
by fill pattern as well as by color.

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev47/scripts/make_fig5.py
"""
from pathlib import Path

import figstyle as S
import matplotlib.pyplot as plt
import numpy as np

V = Path(__file__).resolve().parents[1]
KEYS = ["pow3", "scale05", "temp2", "temp05"]
LABELS = {"pow3": "s\u00b3", "scale05": "0.5s", "temp2": "T=2", "temp05": "T=0.5"}
STRESS = {
    "ByteTrack (official)": {"pow3": (60.92, 65.81), "scale05": (0.00, 66.17), "temp2": (65.84, 66.95), "temp05": (67.30, 67.29)},
    "ByteTrack (library)": {"pow3": (66.31, 66.31), "scale05": (66.61, 66.48), "temp2": (63.97, 63.97), "temp05": (66.53, 66.53)},
    "OC-SORT": {"pow3": (58.34, 66.60), "scale05": (0.00, 66.72), "temp2": (65.99, 67.22), "temp05": (66.61, 67.06)},
    "BoostTrack (online)": {"pow3": (61.33, 64.84), "temp2": (67.59, 67.59)},
}
plt.rcParams["hatch.color"] = "white"
fig, axs = plt.subplots(1, 4, figsize=(S.TEXT_IN, 2.15), sharey=True, layout="constrained")
for a, letter, host in zip(axs, "abcd", STRESS):
    d = STRESS[host]
    ks = [k for k in KEYS if k in d]
    xx = np.arange(len(ks))
    a.bar(xx - 0.2, [d[k][0] for k in ks], 0.38, color=S.GRAY, edgecolor="black", linewidth=0.5,
          label="Host alone")
    b = a.bar(xx + 0.2, [d[k][1] for k in ks], 0.38, color=S.BLUE, edgecolor="white", linewidth=0,
              hatch="////", label="Host + SCL")
    a.bar(xx + 0.2, [d[k][1] for k in ks], 0.38, fill=False, edgecolor="black", linewidth=0.5)
    a.set_xticks(xx, [LABELS[k] for k in ks])
    for i, k in enumerate(ks):
        if d[k][0] == 0:
            a.text(i - 0.2, 1.5, "0", ha="center", va="bottom")
    a.set_title(f"({letter}) {host}", loc="left")
    a.set_ylim(0, 72)
    a.tick_params(axis="x", length=0)
axs[0].set_ylabel("HOTA (%)")
h, l = axs[0].get_legend_handles_labels()
fig.legend(h, l, frameon=False, ncol=2, loc="outside upper center")
fig.savefig(V / "Fig8.pdf")
print("wrote Fig8.pdf", fig.get_size_inches() * 25.4, "mm")
