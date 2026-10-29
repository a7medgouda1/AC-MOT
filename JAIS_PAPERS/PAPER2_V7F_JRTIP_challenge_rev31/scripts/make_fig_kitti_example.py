"""
Fig. 7 of Paper2_V31: KITTI tracking training, sequence 0001, frame 102, OC-SORT with
YOLOv8n detections, the tracker alone (top) and with SCL (bottom). Boxes are the tracks that each run
output for this frame (outputs/v7/kitti/{NATIVE,V7f}@trk:ocsort/yolov8/0001.trk.pkl, the runs behind
Table 11); dashed boxes are labelled cars and pedestrians that no output box covers (IoU >= 0.5).
Selection rule (stated in the caption): the sequence whose HOTA gain is the median of the 21
sequences (0001, +6.77), and in it the first frame with the largest gain in correctly tracked
objects (102: 6 to 9 of 10). The frame was read from the official KITTI archive
(data_tracking_image_2.zip, member training/image_02/0001/000102.png, CRC-checked;
sha256 ea73d08c9701b22811df473afca4a1e746ad5852ddc9b4574b0dc11875b6a95f).

  .venv/bin/python JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev31/scripts/make_fig_kitti_example.py
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


def tracks(system):
    t = pickle.load(open(ROOT / f"outputs/v7/kitti/{system}/yolov8/{SEQ}.trk.pkl", "rb"))["tracks_txt"]
    a = np.loadtxt(io.StringIO(t), delimiter=",", ndmin=2)
    return [(r[2], r[3], r[2] + r[4], r[3] + r[5], int(r[1])) for r in a
            if int(r[0]) - 1 == FRAME and int(r[7]) in (0, 2)]


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


rows = [("(a) Tracker alone (OC-SORT)", tracks("NATIVE@trk:ocsort")), ("(b) Tracker with SCL", tracks("V7f@trk:ocsort"))]
h, w = img.shape[:2]
fig, axs = plt.subplots(2, 1, figsize=(S.TEXT_IN, 2 * S.TEXT_IN * h / w + 0.55), layout="constrained")
for ax, (title, out) in zip(axs, rows):
    ax.imshow(img)
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
fig.savefig(V / "Fig7.pdf")
print("wrote Fig7.pdf", [len(r[1]) for r in rows], "gt", len(gt), [len(missed(r[1])) for r in rows])
