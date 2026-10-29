"""
Fig. 3 of Paper2_V12: HOTA difference (host with the layer minus host alone) with the
95% paired-bootstrap interval for every tested cell. Data: scripts/evidence.py, which
transcribes research/final/V7_STATISTICS.md, V7_EXTERNAL_TRANSFER.md and reads
research/final/V7_RECENT_EXTERNAL_RESULTS.json.

  python3 JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev12/scripts/make_forest.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence as E  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "figures"
plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "serif", "font.size": 8,
                     "axes.spines.top": False, "axes.spines.right": False, "savefig.bbox": "tight",
                     "savefig.pad_inches": 0.02})
POS, NEG, ZERO = "#1f77b4", "#d62728", "#7f7f7f"

rows = []  # (label, (d, lo, hi) or None for identical output, group)
for h, v, _, dh, _, _ in E.MOT17_DEV:
    rows.append((f"{h} {v}".strip(), dh, "Development: MOT17, published detections"))
for h, det, _, _, dh, _, _ in E.KITTI:
    rows.append((f"{h}, {det}", dh, "Development: KITTI, other detectors"))
for n, _, _, dh, _, _ in E.EXT_PRE:
    rows.append((n, dh, "Predeclared at the freeze: MOT17"))
LAB = {"MOT17": "MOT17", "KITTIMOT": "KITTI", "DanceTrack_post": "DanceTrack", "DanceTrack": "DanceTrack"}
for key, s in E.RECENT["systems"].items():
    for ds, r in s["runs"].items():
        if r["reproduction"].startswith("FAILED"):
            continue  # failed reproduction: excluded by the registered protocol
        if key == "tracktrack" and not ds.endswith("_post"):
            continue  # TrackTrack is reproduced and reported on its post-processed output
        for c, v in r["classes"].items():
            d = v["delta"]["HOTA"]
            name = f"{s['name']}, {LAB[ds]}" + (f" {'cars' if c == 'car' else 'pedestrians'}"
                                               if len(r["classes"]) > 1 else "")
            rows.append((name, (d["diff"], d["ci_lo"], d["ci_hi"]), "Post-freeze predeclared"))

groups = []
for r in rows:
    if r[2] not in groups:
        groups.append(r[2])

fig, ax = plt.subplots(figsize=(4.8, 5.4))
y, yt, yl = 0.0, [], []
XMIN, XMAX = -5.0, 10.5
for g in groups:
    ax.text(XMIN, y, g, fontweight="bold", fontsize=7.5, va="center")
    y -= 1
    for lab, ci, gg in rows:
        if gg != g:
            continue
        if ci is None:
            ax.plot(0, y, "D", color=ZERO, ms=3.2)
            lab += " (identical)"
        else:
            d, lo, hi = ci
            col = POS if lo > 0 else NEG if hi < 0 else ZERO
            ax.plot([lo, hi], [y, y], color=col, lw=1.4)
            ax.plot(d, y, "o", color=col, ms=3.6)
        yt.append(y)
        yl.append(lab)
        y -= 1
    y -= 0.4
ax.axvline(0, color="k", lw=0.6)
ax.set_yticks(yt, yl, fontsize=7)
ax.set_xlim(XMIN, XMAX)
ax.set_xlabel(r"$\Delta$HOTA, host with SCL minus host alone (points, 95% interval)", fontsize=7.5)
ax.tick_params(axis="x", labelsize=7)
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.savefig(OUT / "fig3_forest.pdf")
print(f"wrote {OUT / 'fig3_forest.pdf'} ({len(rows)} cells)")
