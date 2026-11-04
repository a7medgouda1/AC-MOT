"""
Qualitative figure for Chapter 3: one VisDrone2019-MOT-val sequence tracked by ByteTrack with YOLO11m,
(a) at the fixed baseline operating point (1536 px, NMS 0.70) and (b) with the frozen AC-MOT controller.

Everything drawn comes from files:
  frames  : <data>/sequences/<seq>/<frame>.jpg
  tracks  : <tracks>/<seq>_bytetrack_{baseline,acmot}.txt      (written by run_tracks.py)
  GT      : <data>/annotations/<seq>.txt, filtered exactly as the official evaluator does
            (tools/v6/eval_official.drop_objects + break_gts: ignored regions and class 11 dropped,
            evaluated classes pedestrian, car, van, truck, bus)
Per frame, track boxes and GT boxes of the same class are matched one to one (Hungarian, IoU >= 0.5),
as in the CLEAR-MOT matching of the evaluator; a track box that matches no GT box and does not lie in an
ignored region is a false track, a GT box that no track box matches is a missed object.

Each track ID has its own colour within its run (IDs are numbered separately in each run and are not
matched across runs); its line is the path of the bottom centre of its box over the last TRAIL frames.

Frame selection (fixed before looking at the images), two modes:
  --mode false  : the frame t with the largest reduction in false tracks (baseline minus AC-MOT);
  --mode switch : the frame t whose 10-frame window (t-10, t] has the largest reduction in identity
                  switches (baseline minus AC-MOT; switches from the CLEAR-MOT events of motmetrics,
                  class-aware, as in the evaluator).
Earliest t on ties; the rows show t and the frames 5 and 10 earlier. The crop is the CROP-sized window, on
a 16-pixel grid, that holds the most selection events (false tracks in frame t, or GT objects that switch
identity in the window) of the two runs together; the same window is used in every panel.

  python make_fig_acmot_example.py --seq uav0000117_02622_v --data <root> --tracks <dir> --out <pdf>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

TRAIL, STEP = 20, 5
CROP_W, CROP_H = 1280, 720
EVAL5_TO_VISDRONE = {0: 1, 1: 4, 2: 5, 3: 6, 4: 9}
# Okabe-Ito based palette without red (red marks false tracks)
PAL = ["#0072B2", "#E69F00", "#009E73", "#56B4E9", "#CC79A7", "#F0E442", "#FFFFFF", "#8C564B", "#7FFFD4",
       "#1E90FF", "#ADFF2F", "#FF8C00", "#BA55D3", "#00CED1", "#FFD700"]
FALSE_C = "#E41A1C"


def load_tracks(path):
    a = np.loadtxt(path, delimiter=",", ndmin=2)
    a = a.copy()
    a[:, 7] = [EVAL5_TO_VISDRONE.get(int(c), -1) for c in a[:, 7]]
    return a


def iou_xywh(a, b):
    ax2, ay2 = a[:, 0] + a[:, 2], a[:, 1] + a[:, 3]
    bx2, by2 = b[:, 0] + b[:, 2], b[:, 1] + b[:, 3]
    ix = np.clip(np.minimum(ax2[:, None], bx2[None]) - np.maximum(a[:, 0][:, None], b[:, 0][None]), 0, None)
    iy = np.clip(np.minimum(ay2[:, None], by2[None]) - np.maximum(a[:, 1][:, None], b[:, 1][None]), 0, None)
    inter = ix * iy
    union = (a[:, 2] * a[:, 3])[:, None] + (b[:, 2] * b[:, 3])[None] - inter
    return np.where(union > 0, inter / union, 0.0)


def match_frame(tr, gt):
    """tr, gt: rows of one frame (MOT format). Returns matched track idx set, matched gt idx set."""
    mt, mg = set(), set()
    for c in np.unique(np.concatenate([tr[:, 7], gt[:, 7]])) if len(tr) and len(gt) else []:
        ti, gi = np.where(tr[:, 7] == c)[0], np.where(gt[:, 7] == c)[0]
        if not len(ti) or not len(gi):
            continue
        iou = iou_xywh(tr[ti, 2:6], gt[gi, 2:6])
        r, k = linear_sum_assignment(-iou)
        for x, y in zip(r, k):
            if iou[x, y] >= 0.5:
                mt.add(int(ti[x]))
                mg.add(int(gi[y]))
    return mt, mg


def frame_stats(tr_all, gt_all, n):
    out = {}
    for t in range(1, n + 1):
        tr, gt = tr_all[tr_all[:, 0] == t], gt_all[gt_all[:, 0] == t]
        mt, mg = match_frame(tr, gt)
        out[t] = dict(tp=len(mg), false=len(tr) - len(mt), missed=len(gt) - len(mg), n_tracks=len(tr),
                      false_idx=[i for i in range(len(tr)) if i not in mt],
                      missed_idx=[i for i in range(len(gt)) if i not in mg])
    return out


def switch_events(tr_all, gt_all, n):
    """Per frame: list of (gt_row_index_in_frame, x, y) of GT objects whose matched track ID switches,
    from motmetrics CLEAR-MOT events per class, as in tools/v6/eval_official.official_sequence_stats."""
    import motmetrics as mm
    ev = {t: [] for t in range(1, n + 1)}
    for c in np.unique(gt_all[:, 7]):
        g, p = gt_all[gt_all[:, 7] == c], tr_all[tr_all[:, 7] == c]
        acc = mm.MOTAccumulator(auto_id=True)
        for t in range(1, n + 1):
            gg, pp = g[g[:, 0] == t], p[p[:, 0] == t]
            acc.update(gg[:, 1].astype(int).tolist(), pp[:, 1].astype(int).tolist(),
                       mm.distances.iou_matrix(gg[:, 2:6], pp[:, 2:6], max_iou=0.5))
        e = acc.mot_events
        sw = e[e["Type"] == "SWITCH"]
        for (fid, _), row in sw.iterrows():
            t = int(fid) + 1
            gg = g[(g[:, 0] == t) & (g[:, 1] == row["OId"])]
            if len(gg):
                ev[t].append((float(gg[0, 2] + gg[0, 4] / 2), float(gg[0, 3] + gg[0, 5] / 2)))
    return ev


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--host", default="bytetrack")
    ap.add_argument("--mode", choices=("false", "switch"), default="false")
    ap.add_argument("--gamma", type=float, default=1.0, help="display gamma, the same for every panel")
    a = ap.parse_args()

    import cv2
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from tools.v6.eval_official import drop_objects, break_gts
    import thesis_style
    thesis_style.apply()

    data = Path(a.data)
    frames = sorted((data / "sequences" / a.seq).glob("*.jpg"))
    n = len(frames)
    gt_raw = np.loadtxt(data / "annotations" / f"{a.seq}.txt", delimiter=",", ndmin=2)
    gt = break_gts(drop_objects(gt_raw, gt_raw))
    gt = gt[np.isin(gt[:, 7], list(EVAL5_TO_VISDRONE.values()))]
    runs = {}
    for name in ("baseline", "acmot"):
        tr = load_tracks(Path(a.tracks) / f"{a.seq}_{a.host}_{name}.txt")
        tr = drop_objects(tr, gt_raw)          # boxes inside ignored regions are not judged, as in the evaluator
        runs[name] = tr
    st = {k: frame_stats(v, gt, n) for k, v in runs.items()}

    sw = {k: switch_events(v, gt, n) for k, v in runs.items()}
    win = lambda k, t: sum(len(sw[k][u]) for u in range(t - 2 * STEP + 1, t + 1))
    cand = [t for t in range(1 + 2 * STEP, n + 1)]
    if a.mode == "false":
        sel = max(cand, key=lambda t: (st["baseline"][t]["false"] - st["acmot"][t]["false"], -t))
    else:
        sel = max(cand, key=lambda t: (win("baseline", t) - win("acmot", t), -t))
    rows = [sel - 2 * STEP, sel - STEP, sel]
    levels = (Path(a.tracks) / f"{a.seq}_{a.host}_acmot_levels.txt").read_text().split()

    # crop: window holding the most false tracks of both runs in the selected frame
    H, W = cv2.imread(str(frames[sel - 1])).shape[:2]
    centers = []
    for name in runs:
        if a.mode == "false":
            tr = runs[name][runs[name][:, 0] == sel]
            for i in st[name][sel]["false_idx"]:
                centers.append((tr[i, 2] + tr[i, 4] / 2, tr[i, 3] + tr[i, 5] / 2))
        else:
            for u in range(sel - 2 * STEP + 1, sel + 1):
                centers.extend(sw[name][u])
    centers = np.asarray(centers) if centers else np.zeros((0, 2))
    best, x0, y0 = -1, 0, 0
    for yy in range(0, H - CROP_H + 1, 16):
        for xx in range(0, W - CROP_W + 1, 16):
            c = int(((centers[:, 0] >= xx) & (centers[:, 0] < xx + CROP_W) &
                     (centers[:, 1] >= yy) & (centers[:, 1] < yy + CROP_H)).sum())
            if c > best:
                best, x0, y0 = c, xx, yy

    def draw(ax, name, t):
        img = cv2.cvtColor(cv2.imread(str(frames[t - 1])), cv2.COLOR_BGR2RGB)[y0:y0 + CROP_H, x0:x0 + CROP_W]
        ax.imshow(thesis_style.brighten(img, a.gamma))
        tr_all = runs[name]
        tr = tr_all[tr_all[:, 0] == t]
        false_idx = set(st[name][t]["false_idx"])
        for i, r in enumerate(tr):
            tid = int(r[1])
            col = FALSE_C if i in false_idx else PAL[tid % len(PAL)]
            hist = tr_all[(tr_all[:, 1] == tid) & (tr_all[:, 0] <= t) & (tr_all[:, 0] > t - TRAIL)]
            hist = hist[np.argsort(hist[:, 0])]
            if len(hist) > 1 and i not in false_idx:
                ax.plot(hist[:, 2] + hist[:, 4] / 2 - x0, hist[:, 3] + hist[:, 5] - y0, color=col, lw=1.0)
            ax.add_patch(Rectangle((r[2] - x0, r[3] - y0), r[4], r[5], fill=False, ec=col,
                                   lw=1.6 if i in false_idx else 1.2))
            if i not in false_idx and 0 <= r[2] - x0 < CROP_W and 0 <= r[3] - y0 < CROP_H:
                ax.text(r[2] - x0, r[3] - y0 - 2, str(tid), color=col, fontsize=6.2, va="bottom",
                        bbox=dict(facecolor="black", alpha=0.45, pad=0.3, lw=0), clip_on=True)
        g = gt[gt[:, 0] == t]
        for i in st[name][t]["missed_idx"]:
            r = g[i]
            ax.add_patch(Rectangle((r[2] - x0, r[3] - y0), r[4], r[5], fill=False, ec="white", lw=0.9, ls="--"))
        ax.set_xlim(0, CROP_W)
        ax.set_ylim(CROP_H, 0)
        ax.set_xticks([])
        ax.set_yticks([])
        s = st[name][t]
        ax.set_ylabel(f"frame {t}", fontsize=9) if name == "baseline" else None
        extra = f"   ID switches (last 10 frames) {win(name, t)}" if a.mode == "switch" else ""
        state = f"   state {levels[t - 1]}" if name == "acmot" else ""
        ax.text(0.01, 0.985, f"tracked {s['tp']}   false {s['false']}   missed {s['missed']}{extra}{state}",
                transform=ax.transAxes, fontsize=8, color="white", va="top",
                bbox=dict(facecolor="black", alpha=0.6, pad=1.5, lw=0))

    fig, axes = plt.subplots(3, 2, figsize=(7.0, 3 * 7.0 / 2 * CROP_H / CROP_W + 0.45))
    for r, t in enumerate(rows):
        for c, name in enumerate(("baseline", "acmot")):
            draw(axes[r, c], name, t)
    axes[0, 0].set_title("(a) Baseline: fixed operating point (1536, 0.70)", fontsize=9.5)
    axes[0, 1].set_title("(b) With AC-MOT", fontsize=9.5)
    plt.subplots_adjust(left=0.035, right=0.995, top=0.955, bottom=0.005, wspace=0.02, hspace=0.03)
    fig.savefig(a.out, dpi=300)
    fig.savefig(str(Path(a.out).with_suffix(".png")), dpi=200)

    meta = dict(seq=a.seq, host=a.host, selected_frame=sel, rows=rows, crop=dict(x0=x0, y0=y0, w=CROP_W, h=CROP_H),
                frame_size=dict(w=W, h=H), trail=TRAIL,
                mode=a.mode,
                per_row={name: {t: dict(**{k: st[name][t][k] for k in ("tp", "false", "missed", "n_tracks")},
                                        id_switches_last10=win(name, t)) for t in rows} for name in runs},
                acmot_state_per_row={t: levels[t - 1] for t in rows},
                sequence_id_switches={name: int(sum(len(v) for v in sw[name].values())) for name in runs},
                sequence_totals={name: {k: int(sum(st[name][t][k] for t in st[name])) for k in ("tp", "false", "missed")}
                                 for name in runs},
                frames_used=[frames[t - 1].name for t in rows])
    Path(a.out).with_suffix(".json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
