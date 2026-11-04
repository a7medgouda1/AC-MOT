"""
Overview figure for Chapter 1: one tracking example of each controller, taken from the qualitative
figures of Chapters 3 and 4 (same pixels, no new drawing of tracks):
  top    : the last row of the AC-MOT figure (VisDrone2019-MOT-val, ByteTrack, baseline vs AC-MOT),
           rendered from <acmot_pdf>;
  bottom : the last row of the SCL figure (KITTI 0001, OC-SORT alone vs with SCL), rendered from <scl_pdf>.
Rows are found as the bands of non-white pixel rows of each rendered page.

  python make_fig_overview.py --acmot <pdf> --scl <pdf> --out <pdf>
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np


def render(pdf, dpi):
    import cv2
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", str(pdf), f"{d}/p"], check=True)
        return cv2.cvtColor(cv2.imread(f"{d}/p.png"), cv2.COLOR_BGR2RGB)


def bands(img, thr=245, min_gap=3):
    nonwhite = (img < thr).any(axis=2).any(axis=1)
    out, start, gap = [], None, 0
    for y, v in enumerate(nonwhite):
        if v:
            if start is None:
                start = y
            gap = 0
        elif start is not None:
            gap += 1
            if gap >= min_gap:
                out.append((start, y - gap + 1))
                start, gap = None, 0
    if start is not None:
        out.append((start, len(nonwhite)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--acmot", required=True)
    ap.add_argument("--scl", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    A = render(a.acmot, 300)
    ba = bands(A)
    top = A[ba[-1][0]:ba[-1][1]]
    K = render(a.scl, 600)
    bk = bands(K)
    bot = K[bk[-2][0]:bk[-1][1]] if len(bk) >= 6 else K[bk[-1][0]:bk[-1][1]]

    def trim_cols(img, thr=245):
        cols = np.where((img < thr).any(axis=2).any(axis=0))[0]
        return img[:, cols[0]:cols[-1] + 1]

    top, bot = trim_cols(top), trim_cols(bot)
    wt, wb = top.shape[1], bot.shape[1]
    ht, hb = top.shape[0] / wt, bot.shape[0] / wb
    import thesis_style
    thesis_style.apply()
    W = 7.0
    head_t, gap, foot = 0.46, 0.30, 0.02          # inches: titles above the top row, title above the bottom row
    tot = W * (ht + hb) + head_t + gap + foot
    fig = plt.figure(figsize=(W, tot))
    y_b = foot / tot
    h_b = W * hb / tot
    h_t = W * ht / tot
    y_t = y_b + h_b + gap / tot
    ax_t = fig.add_axes([0, y_t, 1, h_t])
    ax_b = fig.add_axes([0, y_b, 1, h_b])
    for ax, im in ((ax_t, top), (ax_b, bot)):
        ax.imshow(im)
        ax.axis("off")
    fig.text(0.27, y_t + h_t + 0.03 / tot, "(a) Baseline: fixed operating point (1536, 0.70)", ha="center", va="bottom",
             fontsize=9)
    fig.text(0.76, y_t + h_t + 0.03 / tot, "(b) With AC-MOT", ha="center", va="bottom", fontsize=9)
    fig.text(0.5, y_t + h_t + 0.24 / tot, "AC-MOT: VisDrone2019-MOT, ByteTrack with YOLO11m", ha="center",
             va="bottom", fontsize=10, fontweight="bold")
    fig.text(0.5, y_b + h_b + 0.07 / tot, "SCL: KITTI tracking, OC-SORT with YOLOv8n (left: tracker alone; right: with SCL)",
             ha="center", va="bottom", fontsize=10, fontweight="bold")
    fig.savefig(a.out, dpi=300)
    fig.savefig(str(Path(a.out).with_suffix(".png")), dpi=200)
    Path(a.out).with_suffix(".json").write_text(json.dumps(dict(acmot_source=str(a.acmot), scl_source=str(a.scl),
                                                                acmot_band=ba[-1], scl_bands=bk[-2:]), indent=1))
    print("bands acmot", ba, "scl", bk)


if __name__ == "__main__":
    main()
