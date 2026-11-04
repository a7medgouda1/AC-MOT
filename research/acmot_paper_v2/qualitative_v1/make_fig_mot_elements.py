"""
Background figure for Chapter 2: what a multi-object tracker outputs and which outcomes the metrics count,
on real frames of one VisDrone2019-MOT-val sequence tracked by ByteTrack with YOLO11m at the fixed
operating point (1536 px, NMS 0.70), i.e. the baseline run of run_tracks.py (no controller).

Drawn from files only: track boxes with their IDs and their path over the last TRAIL frames, false tracks
(red; no annotated object matches them), missed objects (white dashed; annotated, matched by no track), and
one identity switch (yellow ring): the annotated object whose matched track ID changes.
Matching as in make_fig_acmot_example.py (class-aware, IoU >= 0.5, CLEAR-MOT events of motmetrics).

Selection rule: among the identity switches of the run that follow the previous match of the object within
GAP frames, in which the old track is no longer output and the new track started within GAP frames (each track
with one class) after the first 2*TRAIL frames, the one of the largest annotated object (box area in the switch frame); panels show the last
frame with the old ID and the switch frame, cropped to a CROP-sized window centred on the object.

  python make_fig_mot_elements.py --seq uav0000117_02622_v --data <root> --tracks <dir> --out <pdf>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from make_fig_acmot_example import EVAL5_TO_VISDRONE, FALSE_C, PAL, TRAIL, frame_stats, load_tracks  # noqa: E402

GAP = 5
CROP_W, CROP_H = 960, 540
RING = "#FFD400"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--host", default="bytetrack")
    ap.add_argument("--gamma", type=float, default=1.0, help="display gamma, the same for both panels")
    a = ap.parse_args()
    import cv2
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import motmetrics as mm
    from matplotlib.lines import Line2D
    from matplotlib.patches import Circle, Rectangle
    from tools.v6.eval_official import drop_objects, break_gts
    import thesis_style
    thesis_style.apply()

    data = Path(a.data)
    frames = sorted((data / "sequences" / a.seq).glob("*.jpg"))
    n = len(frames)
    H, W = cv2.imread(str(frames[0])).shape[:2]
    gt_raw = np.loadtxt(data / "annotations" / f"{a.seq}.txt", delimiter=",", ndmin=2)
    gt = break_gts(drop_objects(gt_raw, gt_raw))
    gt = gt[np.isin(gt[:, 7], list(EVAL5_TO_VISDRONE.values()))]
    tr_all = drop_objects(load_tracks(Path(a.tracks) / f"{a.seq}_{a.host}_baseline.txt"), gt_raw)
    st = frame_stats(tr_all, gt, n)

    events = []
    for c in np.unique(gt[:, 7]):
        g, p = gt[gt[:, 7] == c], tr_all[tr_all[:, 7] == c]
        acc = mm.MOTAccumulator(auto_id=True)
        for t in range(1, n + 1):
            gg, pp = g[g[:, 0] == t], p[p[:, 0] == t]
            acc.update(gg[:, 1].astype(int).tolist(), pp[:, 1].astype(int).tolist(),
                       mm.distances.iou_matrix(gg[:, 2:6], pp[:, 2:6], max_iou=0.5))
        e = acc.mot_events
        e = e[e["Type"].isin(["MATCH", "SWITCH"])]
        last = {}
        for (fid, _), r in e.iterrows():
            t, oid, hid = int(fid) + 1, int(r["OId"]), int(r["HId"])
            if r["Type"] == "SWITCH" and oid in last and t - last[oid][1] <= GAP:
                gb = g[(g[:, 0] == t) & (g[:, 1] == oid)][0]
                events.append(dict(frame=t, prev_frame=last[oid][1], cls=int(c), oid=oid, old_id=last[oid][0],
                                   new_id=hid, area=float(gb[4] * gb[5]), box=gb[2:6].tolist()))
            last[oid] = (hid, t)
    def clean(d):
        """old ID absent from the switch frame and the new ID started within GAP frames: a track that was lost
        and replaced by a new one, with one class per track"""
        old = tr_all[tr_all[:, 1] == d["old_id"]]
        new = tr_all[tr_all[:, 1] == d["new_id"]]
        return (d["frame"] > 2 * TRAIL and not (old[:, 0] == d["frame"]).any() and d["frame"] - new[:, 0].min() <= GAP
                and len(np.unique(old[:, 7])) == 1 and len(np.unique(new[:, 7])) == 1)
    events = [d for d in events if clean(d)]
    ev = max(events, key=lambda d: (d["area"], -d["frame"]))
    t1 = ev["frame"]
    t0 = ev["prev_frame"]
    bx, by, bw, bh = ev["box"]
    x0 = int(np.clip(bx + bw / 2 - CROP_W / 2, 0, W - CROP_W))
    y0 = int(np.clip(by + bh / 2 - CROP_H / 2, 0, H - CROP_H))

    def draw(ax, t):
        img = cv2.cvtColor(cv2.imread(str(frames[t - 1])), cv2.COLOR_BGR2RGB)[y0:y0 + CROP_H, x0:x0 + CROP_W]
        ax.imshow(thesis_style.brighten(img, a.gamma))
        tr = tr_all[tr_all[:, 0] == t]
        fidx = set(st[t]["false_idx"])
        for i, r in enumerate(tr):
            tid = int(r[1])
            col = FALSE_C if i in fidx else PAL[tid % len(PAL)]
            if i not in fidx:
                hist = tr_all[(tr_all[:, 1] == tid) & (tr_all[:, 0] <= t) & (tr_all[:, 0] > t - TRAIL)]
                hist = hist[np.argsort(hist[:, 0])]
                if len(hist) > 1:
                    ax.plot(hist[:, 2] + hist[:, 4] / 2 - x0, hist[:, 3] + hist[:, 5] - y0, color=col, lw=1.1)
            ax.add_patch(Rectangle((r[2] - x0, r[3] - y0), r[4], r[5], fill=False, ec=col,
                                   lw=1.5 if i in fidx else 1.1))
            if i not in fidx:
                ax.text(r[2] - x0, r[3] - y0 - 2, str(tid), color=col, fontsize=7.5, va="bottom",
                        bbox=dict(facecolor="black", alpha=0.5, pad=0.3, lw=0), clip_on=True)
        g = gt[gt[:, 0] == t]
        for i in st[t]["missed_idx"]:
            r = g[i]
            ax.add_patch(Rectangle((r[2] - x0, r[3] - y0), r[4], r[5], fill=False, ec="white", lw=1.0, ls="--"))
        go = g[(g[:, 7] == ev["cls"]) & (g[:, 1] == ev["oid"])]
        if len(go):
            r = go[0]
            rad = 0.5 * np.hypot(r[4], r[5]) + 14
            ax.add_patch(Circle((r[2] + r[4] / 2 - x0, r[3] + r[5] / 2 - y0), rad, fill=False, ec=RING, lw=1.8))
        ax.set_xlim(0, CROP_W)
        ax.set_ylim(CROP_H, 0)
        ax.set_xticks([])
        ax.set_yticks([])

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 7.0 / 2 * CROP_H / CROP_W + 0.95))
    draw(axes[0], t0)
    draw(axes[1], t1)
    axes[0].set_title(f"(a) Frame {t0}: the ringed object is tracked as ID {ev['old_id']}", fontsize=9)
    axes[1].set_title(f"(b) Frame {t1}: the same object has the new ID {ev['new_id']}", fontsize=9)
    handles = [Line2D([], [], color=PAL[0], lw=1.2, label="track box, ID and path (last 20 frames)"),
               Line2D([], [], color=FALSE_C, lw=1.5, label="false track (no annotated object)"),
               Line2D([], [], color="black", lw=1.0, ls="--", label="missed object (annotated, not tracked)"),
               Line2D([], [], color=RING, lw=1.8, marker="o", ms=0, label="identity switch")]
    fig.legend(handles=handles, loc="lower center", ncol=2, fontsize=8.5, frameon=False)
    plt.subplots_adjust(left=0.005, right=0.995, top=0.925, bottom=0.2, wspace=0.02)
    fig.savefig(a.out, dpi=300)
    fig.savefig(str(Path(a.out).with_suffix(".png")), dpi=200)
    meta = dict(seq=a.seq, host=a.host, run="baseline (1536, 0.70)", event=ev, frames=[t0, t1],
                frames_used=[frames[t0 - 1].name, frames[t1 - 1].name], crop=dict(x0=x0, y0=y0, w=CROP_W, h=CROP_H),
                per_frame={t: {k: st[t][k] for k in ("tp", "false", "missed", "n_tracks")} for t in (t0, t1)},
                n_switch_events=len(events))
    Path(a.out).with_suffix(".json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
