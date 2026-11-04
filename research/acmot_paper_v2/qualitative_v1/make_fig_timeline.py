"""
Timeline figure for Chapter 3: one VisDrone2019-MOT-val sequence, frame by frame,
  (a) the scene complexity index (SCI) computed by the frozen AC-MOT controller, its two thresholds, the
      state it chose (shaded), and the number of annotated objects of the evaluated classes;
  (b) the false tracks of every frame for the baseline at the fixed operating point (1536, 0.70) and with
      AC-MOT (track boxes that match no annotated object, as in make_fig_acmot_example.py).
Data: <tracks>/<seq>_<host>_scene_trace.json (scene_trace.py), the track files of run_tracks.py and the GT.

  python make_fig_timeline.py --seq uav0000117_02622_v --data <root> --tracks <dir> --out <pdf>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from make_fig_acmot_example import EVAL5_TO_VISDRONE, frame_stats, load_tracks  # noqa: E402

STATE_C = {"LOW": "#DDEEDD", "MEDIUM": "#FFF2CC", "HIGH": "#F8DCDC"}
BASE_C, ACMOT_C = "#7F7F7F", "#0072B2"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--host", default="bytetrack")
    a = ap.parse_args()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from tools.v6.eval_official import drop_objects, break_gts
    import thesis_style
    thesis_style.apply()

    data = Path(a.data)
    n = len(list((data / "sequences" / a.seq).glob("*.jpg")))
    gt_raw = np.loadtxt(data / "annotations" / f"{a.seq}.txt", delimiter=",", ndmin=2)
    gt = break_gts(drop_objects(gt_raw, gt_raw))
    gt = gt[np.isin(gt[:, 7], list(EVAL5_TO_VISDRONE.values()))]
    runs = {k: drop_objects(load_tracks(Path(a.tracks) / f"{a.seq}_{a.host}_{k}.txt"), gt_raw)
            for k in ("baseline", "acmot")}
    st = {k: frame_stats(v, gt, n) for k, v in runs.items()}
    trace = json.loads((Path(a.tracks) / f"{a.seq}_{a.host}_scene_trace.json").read_text())
    fr = trace["frames"]
    t = np.arange(1, n + 1)
    sci = np.array([r["sci"] for r in fr])
    lev = [r["level"] for r in fr]
    ngt = np.array([(gt[:, 0] == k).sum() for k in t])
    fb = np.array([st["baseline"][k]["false"] for k in t])
    fa = np.array([st["acmot"][k]["false"] for k in t])

    plt.rcParams.update({"font.size": 9, "axes.linewidth": 0.6})
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.0, 4.6), sharex=True,
                                   gridspec_kw=dict(height_ratios=[1, 1.15], hspace=0.2))
    runs_of = []
    s = 0
    for k in range(1, n + 1):
        if k == n or lev[k] != lev[s]:
            runs_of.append((s + 1, k, lev[s]))
            s = k
    for f0, f1, lv in runs_of:
        ax1.axvspan(f0 - 0.5, f1 + 0.5, color=STATE_C[lv], lw=0, zorder=0)
    for f0, f1, lv in runs_of[1:]:
        ax2.axvline(f0 - 0.5, color="black", lw=0.7, ls=":")
        ax2.text(f0 + 2, fb.max() * 1.21, f"AC-MOT enters {lv}", fontsize=8.5, va="top")
    ax1.step(t, sci, where="post", color="black", lw=1.2, label="SCI $S_j$")
    ax1.axhline(trace["t_high"], color="#B22222", lw=0.8, ls="--")
    ax1.axhline(trace["t_med"], color="#B8860B", lw=0.8, ls="--")
    ax1.text(n - 4, trace["t_high"] + 0.015, r"$\tau_h$", ha="right", va="bottom", fontsize=10, color="#B22222")
    ax1.text(n - 4, trace["t_med"] + 0.015, r"$\tau_m$", ha="right", va="bottom", fontsize=10, color="#B8860B")
    ax1.set_ylim(0, 1.05)
    ax1.set_ylabel("SCI")
    ax1b = ax1.twinx()
    ax1b.plot(t, ngt, color="#2E8B57", lw=0.9, alpha=0.9, label="annotated objects")
    ax1b.set_ylabel("annotated objects", color="#2E8B57")
    ax1b.tick_params(axis="y", colors="#2E8B57")
    ax1b.set_ylim(0, max(ngt.max() * 1.1, 10))
    for f0, f1, lv in runs_of:
        top = sci[f0 - 1:f1].max() < 0.85            # label above the SCI line where there is room, else below it
        ax1.text((f0 + f1) / 2, 1.0 if top else 0.03, lv, ha="center", va="top" if top else "bottom", fontsize=9,
                 fontweight="bold")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax1b.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="lower right", fontsize=8.5, frameon=True, framealpha=0.9)
    ax1.set_title("(a) Scene complexity and AC-MOT state", fontsize=9.5, loc="left")

    ax2.fill_between(t, fa, fb, where=fb >= fa, color=ACMOT_C, alpha=0.18, lw=0, step="mid",
                     label="false tracks removed by AC-MOT")
    ax2.step(t, fb, where="mid", color=BASE_C, lw=0.9, label=f"Baseline (1536, 0.70): mean {fb.mean():.1f} per frame")
    ax2.step(t, fa, where="mid", color=ACMOT_C, lw=1.1, label=f"With AC-MOT: mean {fa.mean():.1f} per frame")
    ax2.set_ylabel("false tracks per frame")
    ax2.set_xlabel("frame")
    ax2.set_xlim(0.5, n + 0.5)
    ax2.set_ylim(0, fb.max() * 1.25)
    ax2.legend(loc="upper center", bbox_to_anchor=(0.56, 1.0), fontsize=8.5, frameon=True, framealpha=0.9, ncol=1)
    ax2.set_title("(b) False tracks", fontsize=9.5, loc="left")
    plt.subplots_adjust(left=0.075, right=0.905, top=0.95, bottom=0.1)
    fig.savefig(a.out)
    fig.savefig(str(Path(a.out).with_suffix(".png")), dpi=200)
    meta = dict(seq=a.seq, host=a.host, state_runs=runs_of,
                false_mean=dict(baseline=float(fb.mean()), acmot=float(fa.mean())),
                frames_acmot_fewer=int((fa < fb).sum()), frames_equal=int((fa == fb).sum()),
                frames_acmot_more=int((fa > fb).sum()),
                annotated_objects=dict(min=int(ngt.min()), max=int(ngt.max())),
                sci_after_first_change=dict(min=float(sci[runs_of[0][1]:].min()) if len(runs_of) > 1 else None,
                                            max=float(sci.max())))
    Path(a.out).with_suffix(".json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
