"""
Fig. 4 of Paper2_V36: KITTI tracking training, sequence 0001, frame 102, OC-SORT with
YOLOv8n detections, the tracker alone (top) and with SCL (bottom). Boxes are the tracks that each run
output for this frame (outputs/v7/kitti/{NATIVE,V7f}@trk:ocsort/yolov8/0001.trk.pkl, the runs behind
Table 11); dashed boxes are labelled cars and pedestrians that no output box covers (IoU >= 0.5).
Lines: the path of each of these tracks over the last TRAIL frames (bottom centre of its output
box in frames FRAME-TRAIL..FRAME of the same run), so that each ID is followed over time.
Selection rule (stated in the caption): the sequence whose HOTA gain is the median of the 21
sequences (0001, +6.77), and in it the first frame with the largest gain in correctly tracked
objects (102: 6 to 9 of 10). The frame was read from the official KITTI archive
(data_tracking_image_2.zip, member training/image_02/0001/000102.png, CRC-checked;
sha256 ea73d08c9701b22811df473afca4a1e746ad5852ddc9b4574b0dc11875b6a95f).

  .venv/bin/python JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev36/scripts/make_fig_kitti_example.py
"""
import collections
import io
import pickle
import sys
from pathlib import Path

import numpy as np

V = Path(__file__).resolve().parents[1]
ROOT = V.parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import figstyle as S  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

SEQ, FRAME = "0001", 102
img = plt.imread(V / "figures/kitti/0001_000102.png")


TRAIL = 20


def load(system):
    t = pickle.load(open(ROOT / f"outputs/v7/kitti/{system}/yolov8/{SEQ}.trk.pkl", "rb"))["tracks_txt"]
    return np.loadtxt(io.StringIO(t), delimiter=",", ndmin=2)


def tracks(system):
    a = load(system)
    return [(r[2], r[3], r[2] + r[4], r[3] + r[5], int(r[1])) for r in a
            if int(r[0]) - 1 == FRAME and int(r[7]) in (0, 2)]


def trails(system, ids):
    """Bottom centre of each track's output box in frames FRAME-TRAIL..FRAME (0-based)."""
    a = load(system)
    out = {}
    for tid in ids:
        rows = sorted((int(r[0]) - 1, r[2] + r[4] / 2, r[3] + r[5]) for r in a
                      if int(r[1]) == tid and FRAME - TRAIL <= int(r[0]) - 1 <= FRAME)
        out[tid] = [(x, y) for _, x, y in rows]
    return out


gt = [tuple(map(float, l.split()[6:10])) for l in open(Path.home() / "acmot_work/kitti/gt/label_02/0001.txt")
      if int(l.split()[0]) == FRAME and l.split()[2] in ("Car", "Pedestrian")]


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    i = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i
    return i / u if u > 0 else 0


def missed(out):
    used, miss = set(), []
    for g in gt:
        best = max(((iou(g, o[:4]), k) for k, o in enumerate(out) if k not in used), default=(0, None))
        if best[0] >= 0.5:
            used.add(best[1])
        else:
            miss.append(g)
    return miss


SYSTEMS = (("(a) Tracker alone (OC-SORT)", "NATIVE@trk:ocsort"), ("(b) Tracker with SCL", "V7f@trk:ocsort"))
rows = [(title, tracks(sysname), sysname) for title, sysname in SYSTEMS]
h, w = img.shape[:2]
fig, axs = plt.subplots(2, 1, figsize=(S.TEXT_IN, 2 * S.TEXT_IN * h / w + 0.55), layout="constrained")
for ax, (title, out, sysname) in zip(axs, rows):
    ax.imshow(img)
    for tid, pts in trails(sysname, [o[4] for o in out]).items():
        if len(pts) > 1:
            xs, ys = zip(*pts)
            ax.plot(xs, ys, color="white", lw=2.4, solid_capstyle="round", zorder=3)
            ax.plot(xs, ys, color=S.BLUE, lw=1.2, solid_capstyle="round", zorder=4)
            ax.plot(xs[0], ys[0], "o", ms=2.6, mfc=S.BLUE, mec="white", mew=0.6, zorder=5)
    for x1, y1, x2, y2, tid in out:
        ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor=S.BLUE, lw=1.6))
        ax.text(x1, y1 - 2, f"{tid}", color="white", va="bottom", ha="left",
                bbox=dict(boxstyle="square,pad=0.12", facecolor=S.BLUE, edgecolor="none"))
    for x1, y1, x2, y2 in missed(out):
        ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor="white", lw=1.4, ls=(0, (3, 2))))
        ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor="black", lw=1.4, ls=(3, (3, 2))))
    n_ok = len(gt) - len(missed(out))
    ax.set_title(f"{title}: {n_ok} of {len(gt)} objects tracked", loc="left")
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
fig.savefig(V / "Fig4.pdf")
print("wrote Fig4.pdf", [len(r[1]) for r in rows], "gt", len(gt), [len(missed(r[1])) for r in rows],
      "trail lengths", [sorted(len(v) for v in trails(r[2], [o[4] for o in r[1]]).values()) for r in rows])
