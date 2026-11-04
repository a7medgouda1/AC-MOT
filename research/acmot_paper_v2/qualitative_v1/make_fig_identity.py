"""
Identity figure for Chapter 3: the path of single annotated objects of one VisDrone2019-MOT-val sequence,
coloured by the track identity that each run assigned to the object, for (a) the baseline at the fixed
operating point (1536 px, NMS 0.70) and (b) the frozen AC-MOT controller, same detector and tracker.

Data: frames, the track files of run_tracks.py and the GT filtered as in tools/v6/eval_official.
The identity of an object in a frame is the track ID matched to it by the CLEAR-MOT matching of
motmetrics (class-aware, IoU >= 0.5, MATCH and SWITCH events), as in the evaluator.

Object selection (rule fixed before looking at the images): annotated objects present in at least 40
frames that AC-MOT follows in at least as many frames as the baseline, ranked by the ratio of their
identity counts (AC-MOT / baseline, ascending), then by the baseline count (descending); the first ROWS
objects are shown. Each panel shows the last annotated frame of the object, cropped around its path;
the line is the bottom centre of the matched track box, one colour per identity, with the ID at the
start of each identity.

  python make_fig_identity.py --seq uav0000117_02622_v --data <root> --tracks <dir> --out <pdf>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from make_fig_acmot_example import EVAL5_TO_VISDRONE, load_tracks  # noqa: E402

ROWS, MIN_LIFE, MARGIN = 3, 40, 90
PAL = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#F0E442", "#D55E00", "#FFFFFF", "#8C564B",
       "#7FFFD4", "#ADFF2F", "#FF8C00", "#BA55D3"]
CLASS_NAME = {1: "pedestrian", 4: "car", 5: "van", 6: "truck", 9: "bus"}


def object_identities(tr_all, gt_all, n):
    """{(class, gt_id): [(frame, track_id, x, y, w, h), ...]} from the CLEAR-MOT events of motmetrics."""
    import motmetrics as mm
    out = {}
    for c in np.unique(gt_all[:, 7]):
        g, p = gt_all[gt_all[:, 7] == c], tr_all[tr_all[:, 7] == c]
        acc = mm.MOTAccumulator(auto_id=True)
        for t in range(1, n + 1):
            gg, pp = g[g[:, 0] == t], p[p[:, 0] == t]
            acc.update(gg[:, 1].astype(int).tolist(), pp[:, 1].astype(int).tolist(),
                       mm.distances.iou_matrix(gg[:, 2:6], pp[:, 2:6], max_iou=0.5))
        e = acc.mot_events
        e = e[e["Type"].isin(["MATCH", "SWITCH"])]
        for (fid, _), r in e.iterrows():
            t = int(fid) + 1
            box = p[(p[:, 0] == t) & (p[:, 1] == r["HId"])][0, 2:6]
            out.setdefault((int(c), int(r["OId"])), []).append((t, int(r["HId"]), *box.tolist()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--host", default="bytetrack")
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
    H, W = cv2.imread(str(frames[0])).shape[:2]
    gt_raw = np.loadtxt(data / "annotations" / f"{a.seq}.txt", delimiter=",", ndmin=2)
    gt = break_gts(drop_objects(gt_raw, gt_raw))
    gt = gt[np.isin(gt[:, 7], list(EVAL5_TO_VISDRONE.values()))]
    runs = {k: drop_objects(load_tracks(Path(a.tracks) / f"{a.seq}_{a.host}_{k}.txt"), gt_raw)
            for k in ("baseline", "acmot")}
    ids = {k: object_identities(v, gt, n) for k, v in runs.items()}

    cand = []
    for key in set(ids["baseline"]) | set(ids["acmot"]):
        g = gt[(gt[:, 7] == key[0]) & (gt[:, 1] == key[1])]
        b, m = ids["baseline"].get(key, []), ids["acmot"].get(key, [])
        nb, nm = len({x[1] for x in b}), len({x[1] for x in m})
        if len(g) < MIN_LIFE or nb == 0 or len(m) < len(b) or nm >= nb:
            continue
        cand.append(dict(key=key, life=len(g), first=int(g[:, 0].min()), last=int(g[:, 0].max()),
                         ids_baseline=nb, ids_acmot=nm, frames_baseline=len(b), frames_acmot=len(m)))
    cand.sort(key=lambda d: (d["ids_acmot"] / d["ids_baseline"], -d["ids_baseline"], -d["life"]))
    sel = cand[:ROWS]

    def crop_box(key):
        g = gt[(gt[:, 7] == key[0]) & (gt[:, 1] == key[1])]
        x1, y1 = g[:, 2].min() - MARGIN, g[:, 3].min() - MARGIN
        x2, y2 = (g[:, 2] + g[:, 4]).max() + MARGIN, (g[:, 3] + g[:, 5]).max() + MARGIN
        w, h = x2 - x1, y2 - y1
        w, h = max(w, h * 16 / 9, 480), max(h, w * 9 / 16, 270)
        w, h = max(w, h * 16 / 9), max(h, w * 9 / 16)
        w, h = min(w, W), min(h, H)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        x0 = int(np.clip(cx - w / 2, 0, W - w))
        y0 = int(np.clip(cy - h / 2, 0, H - h))
        return x0, y0, int(w), int(h)

    def draw(ax, name, d, box):
        x0, y0, w, h = box
        t = d["last"]
        img = cv2.cvtColor(cv2.imread(str(frames[t - 1])), cv2.COLOR_BGR2RGB)[y0:y0 + h, x0:x0 + w]
        ax.imshow(thesis_style.brighten(img, a.gamma))
        path = ids[name].get(d["key"], [])
        order = []
        for row in path:
            if row[1] not in order:
                order.append(row[1])
        for k, tid in enumerate(order):
            col = PAL[k % len(PAL)]
            pts = [r for r in path if r[1] == tid]
            seg = [pts[0]]
            for r in pts[1:] + [None]:
                if r is not None and r[0] - seg[-1][0] <= 2:
                    seg.append(r)
                    continue
                xs = [p[2] + p[4] / 2 - x0 for p in seg]
                ys = [p[3] + p[5] - y0 for p in seg]
                ax.plot(xs, ys, color=col, lw=2.0, solid_capstyle="round")
                if r is not None:
                    seg = [r]
            s0 = pts[0]
            ax.plot(s0[2] + s0[4] / 2 - x0, s0[3] + s0[5] - y0, "o", ms=4.0, color=col, mec="black", mew=0.5)
            ax.text(s0[2] + s0[4] / 2 - x0 + 4, s0[3] + s0[5] - y0 - 4, str(tid), color=col, fontsize=7,
                    bbox=dict(facecolor="black", alpha=0.55, pad=0.4, lw=0), clip_on=True)
        g = gt[(gt[:, 7] == d["key"][0]) & (gt[:, 1] == d["key"][1]) & (gt[:, 0] == t)][0]
        ax.add_patch(Rectangle((g[2] - x0, g[3] - y0), g[4], g[5], fill=False, ec="white", lw=1.0, ls="--"))
        ax.set_xlim(0, w)
        ax.set_ylim(h, 0)
        ax.set_xticks([])
        ax.set_yticks([])
        k = "ids_baseline" if name == "baseline" else "ids_acmot"
        f = "frames_baseline" if name == "baseline" else "frames_acmot"
        ax.text(0.01, 0.98, f"{d[k]} identit{'y' if d[k] == 1 else 'ies'}   tracked in {d[f]} of {d['life']} frames",
                transform=ax.transAxes, fontsize=8, color="white", va="top",
                bbox=dict(facecolor="black", alpha=0.65, pad=1.5, lw=0))

    fig, axes = plt.subplots(len(sel), 2, figsize=(7.0, len(sel) * 7.0 / 2 * 9 / 16 + 0.35))
    for r, d in enumerate(sel):
        box = crop_box(d["key"])
        d["crop"] = dict(x0=box[0], y0=box[1], w=box[2], h=box[3])
        for c, name in enumerate(("baseline", "acmot")):
            draw(axes[r, c], name, d, box)
        axes[r, 0].set_ylabel(f"{CLASS_NAME[d['key'][0]]}\nframes {d['first']}–{d['last']}", fontsize=9)
    axes[0, 0].set_title("(a) Baseline: fixed operating point (1536, 0.70)", fontsize=9.5)
    axes[0, 1].set_title("(b) With AC-MOT", fontsize=9.5)
    plt.subplots_adjust(left=0.07, right=0.995, top=0.955, bottom=0.005, wspace=0.02, hspace=0.04)
    fig.savefig(a.out, dpi=300)
    fig.savefig(str(Path(a.out).with_suffix(".png")), dpi=200)
    meta = dict(seq=a.seq, host=a.host, rule=dict(min_life=MIN_LIFE, rows=ROWS), n_candidates=len(cand),
                selected=[dict(d, key=list(d["key"]), class_name=CLASS_NAME[d["key"][0]],
                               frame_shown=frames[d["last"] - 1].name) for d in sel],
                objects_fewer_identities_with_acmot=sum(
                    1 for key in set(ids["baseline"]) | set(ids["acmot"])
                    if len({x[1] for x in ids["acmot"].get(key, [])}) < len({x[1] for x in ids["baseline"].get(key, [])})),
                identities_total={k: int(sum(len({x[1] for x in v}) for v in ids[k].values())) for k in ids})
    Path(a.out).with_suffix(".json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
