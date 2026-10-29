"""
Fig. 5 of Paper2_V27: HOTA under shifted detector scores (MOT17 val-half, floor 0.01), host alone and
with SCL, one panel per tracker, labelled (a)-(d). Same data and style as the Paper2_V11 figure
(PAPER2_UNIVERSAL_ACMOT_JAIS/scripts/make_figures.py, Fig. 5); the SCL bars carry a hatch so that the
two series also differ without color. Data: research/final/V7_EXPERIMENT_LEDGER.md STRESS-L and
V7_MAIN_RESULTS.md Table 3 (as transcribed in that script's evidence.py).

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev27/scripts/make_fig5.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

V = Path(__file__).resolve().parents[1]
plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "serif", "font.size": 8,
                     "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
                     "axes.spines.top": False, "axes.spines.right": False, "savefig.bbox": "tight",
                     "savefig.pad_inches": 0.02, "hatch.linewidth": 0.6, "hatch.color": "white"})
KEYS = ["pow3", "scale05", "temp2", "temp05"]
LABELS = {"pow3": r"$s^3$", "scale05": r"$0.5s$", "temp2": r"$T{=}2$", "temp05": r"$T{=}0.5$"}
STRESS = {  # host: {transform: (host HOTA, host + SCL HOTA)}
    "ByteTrack (official)": {"pow3": (60.92, 65.81), "scale05": (0.00, 66.17), "temp2": (65.84, 66.95), "temp05": (67.30, 67.29)},
    "ByteTrack (library)": {"pow3": (66.31, 66.31), "scale05": (66.61, 66.48), "temp2": (63.97, 63.97), "temp05": (66.53, 66.53)},
    "OC-SORT": {"pow3": (58.34, 66.60), "scale05": (0.00, 66.72), "temp2": (65.99, 67.22), "temp05": (66.61, 67.06)},
    "BoostTrack (online)": {"pow3": (61.33, 64.84), "temp2": (67.59, 67.59)},
}
fig, axs = plt.subplots(1, 4, figsize=(6.9, 2.1), sharey=True)
for a, letter, host in zip(axs, "abcd", STRESS):
    d = STRESS[host]
    ks = [k for k in KEYS if k in d]
    xx = np.arange(len(ks))
    a.bar(xx - 0.19, [d[k][0] for k in ks], 0.38, color="#7f7f7f", label="host alone")
    a.bar(xx + 0.19, [d[k][1] for k in ks], 0.38, color="#1f77b4", hatch="////", label="host + layer")
    a.set_xticks(xx, [LABELS[k] for k in ks], fontsize=7.5)
    for i, k in enumerate(ks):
        if d[k][0] == 0:
            a.text(i - 0.19, 1.5, "0", ha="center", fontsize=7)
    a.set_title(f"({letter}) {host}", fontsize=7.5)
    a.set_ylim(0, 72)
axs[0].set_ylabel("HOTA (%)")
h, l = axs[0].get_legend_handles_labels()
fig.legend(h, l, frameon=False, fontsize=7, ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.08))
fig.tight_layout()
fig.savefig(V / "fig5_calibration_shift.pdf")
print("wrote fig5_calibration_shift.pdf")
