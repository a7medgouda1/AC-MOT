"""
Side-by-side video of one VisDrone2019-MOT-val sequence: (left) baseline at the fixed operating point,
(right) with the frozen AC-MOT controller, same tracker. Boxes, IDs and trails come only from the track
files written by run_tracks.py; the right panel also prints the AC-MOT state of each frame (from the
levels file). False tracks (red) and missed objects (white dashed) use the same matching as
make_fig_acmot_example.py. Frames are drawn at half resolution.

  python make_video.py --seq uav0000117_02622_v --data <root> --tracks <dir> --out <mp4> [--host bytetrack]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from make_fig_acmot_example import EVAL5_TO_VISDRONE, PAL, TRAIL, frame_stats, load_tracks  # noqa: E402


def hex_bgr(h):
    h = h.lstrip("#")
    return int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)


def dashed_rect(img, p1, p2, color, dash=6):
    x1, y1 = p1
    x2, y2 = p2
    for x in range(x1, x2, 2 * dash):
        cv2.line(img, (x, y1), (min(x + dash, x2), y1), color, 1)
        cv2.line(img, (x, y2), (min(x + dash, x2), y2), color, 1)
    for y in range(y1, y2, 2 * dash):
        cv2.line(img, (x1, y), (x1, min(y + dash, y2)), color, 1)
        cv2.line(img, (x2, y), (x2, min(y + dash, y2)), color, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--host", default="bytetrack")
    ap.add_argument("--fps", type=int, default=10)
    a = ap.parse_args()
    from tools.v6.eval_official import drop_objects, break_gts

    data = Path(a.data)
    frames = sorted((data / "sequences" / a.seq).glob("*.jpg"))
    n = len(frames)
    gt_raw = np.loadtxt(data / "annotations" / f"{a.seq}.txt", delimiter=",", ndmin=2)
    gt = break_gts(drop_objects(gt_raw, gt_raw))
    gt = gt[np.isin(gt[:, 7], list(EVAL5_TO_VISDRONE.values()))]
    runs = {k: drop_objects(load_tracks(Path(a.tracks) / f"{a.seq}_{a.host}_{k}.txt"), gt_raw) for k in ("baseline", "acmot")}
    st = {k: frame_stats(v, gt, n) for k, v in runs.items()}
    levels = (Path(a.tracks) / f"{a.seq}_{a.host}_acmot_levels.txt").read_text().split()
    h0, w0 = cv2.imread(str(frames[0])).shape[:2]
    s = 0.5
    W, H = int(w0 * s), int(h0 * s)
    vw = cv2.VideoWriter(a.out, cv2.VideoWriter_fourcc(*"mp4v"), a.fps, (2 * W, H + 40))
    red = (28, 26, 228)
    for t in range(1, n + 1):
        panels = []
        for name in ("baseline", "acmot"):
            img = cv2.resize(cv2.imread(str(frames[t - 1])), (W, H))
            tr_all = runs[name]
            tr = tr_all[tr_all[:, 0] == t]
            false_idx = set(st[name][t]["false_idx"])
            for i, r in enumerate(tr):
                tid = int(r[1])
                col = red if i in false_idx else hex_bgr(PAL[tid % len(PAL)])
                if i not in false_idx:
                    hist = tr_all[(tr_all[:, 1] == tid) & (tr_all[:, 0] <= t) & (tr_all[:, 0] > t - TRAIL)]
                    hist = hist[np.argsort(hist[:, 0])]
                    pts = np.stack([(hist[:, 2] + hist[:, 4] / 2) * s, (hist[:, 3] + hist[:, 5]) * s], 1).astype(np.int32)
                    if len(pts) > 1:
                        cv2.polylines(img, [pts], False, col, 1, cv2.LINE_AA)
                p1 = (int(r[2] * s), int(r[3] * s))
                p2 = (int((r[2] + r[4]) * s), int((r[3] + r[5]) * s))
                cv2.rectangle(img, p1, p2, col, 2 if i in false_idx else 1)
                if i not in false_idx:
                    cv2.putText(img, str(tid), (p1[0], p1[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, col, 1, cv2.LINE_AA)
            g = gt[gt[:, 0] == t]
            for i in st[name][t]["missed_idx"]:
                r = g[i]
                dashed_rect(img, (int(r[2] * s), int(r[3] * s)), (int((r[2] + r[4]) * s), int((r[3] + r[5]) * s)), (255, 255, 255))
            bar = np.zeros((40, W, 3), np.uint8)
            x = st[name][t]
            title = "Baseline (1536, 0.70)" if name == "baseline" else f"AC-MOT (state {levels[t - 1]})"
            cv2.putText(bar, f"{title}  frame {t}  tracked GT {x['tp']}  false {x['false']}  missed {x['missed']}",
                        (8, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
            panels.append(np.vstack([bar, img]))
        vw.write(np.hstack(panels))
    vw.release()
    print("wrote", a.out, n, "frames")


if __name__ == "__main__":
    main()
