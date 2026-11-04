"""
Fig. 4 of Paper2_V70: tracking example on KITTI tracking training, sequence 0001, OC-SORT with
YOLOv8n detections, the tracker alone (left column) and with SCL (right column), at frames 92, 97
and 102 (rows). Boxes are the tracks that each run output for the frame
(outputs/v7/kitti/{NATIVE,V7f}@trk:ocsort/yolov8/0001.trk.pkl, the runs behind the KITTI table);
each track ID has its own colour in its column, and the line of that colour is the path of the
track over the previous TRAIL frames (bottom centre of its box), so that each object is followed
over time with one ID. Dashed boxes: labelled cars and pedestrians that no output box covers
(IoU >= 0.5). Selection rule (stated in the caption): the sequence whose HOTA gain is the median of
the 21 sequences (0001, +6.77), its first frame with the largest gain in correctly tracked objects
(102: 6 to 9 of 10), and the frames 5 and 10 earlier. Frames read from the official KITTI archive
(data_tracking_image_2.zip, members training/image_02/0001/000092.png, 000097.png, 000102.png,
CRC-checked; sha256 2e8fe3f2..., 713e59f7..., ea73d08c...).

  .venv/bin/python JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev70/scripts/make_fig_kitti_example.py
"""
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

SEQ, FRAMES, TRAIL = "0001", (92, 97, 102), 20
# rows above Y0 (sky and tree tops) hold no box in these frames (all boxes lie in y = 126..375), so the
# images are cropped there; boxes and ID labels are drawn as in the first version of the figure
Y0 = 92
SYSTEMS = (("(a) Alone", "NATIVE@trk:ocsort"), ("(b) With SCL", "V7f@trk:ocsort"))
# Okabe-Ito based palette without yellow (low contrast on bright images)
PAL = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#000000", "#8C564B", "#7A7A00"]
LIGHT = {"#E69F00", "#56B4E9", "#7A7A00"}
GTL = [l.split() for l in open(Path.home() / "acmot_work/kitti/gt/label_02/0001.txt")]


def load(system):
    t = pickle.load(open(ROOT / f"outputs/v7/kitti/{system}/yolov8/{SEQ}.trk.pkl", "rb"))["tracks_txt"]
    a = np.loadtxt(io.StringIO(t), delimiter=",", ndmin=2)
    return a[np.isin(a[:, 7].astype(int), (0, 2))]


def boxes(a, f):
    return [(r[2], r[3], r[2] + r[4], r[3] + r[5], int(r[1])) for r in a if int(r[0]) - 1 == f]


def trail(a, tid, f):
    rows = sorted((int(r[0]) - 1, r[2] + r[4] / 2, r[3] + r[5]) for r in a
                  if int(r[1]) == tid and f - TRAIL <= int(r[0]) - 1 <= f)
    return [(x, y) for _, x, y in rows]


def gt(f):
    return [tuple(map(float, l[6:10])) for l in GTL if int(l[0]) == f and l[2] in ("Car", "Pedestrian")]


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    i = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i
    return i / u if u > 0 else 0


def missed(out, g):
    used, miss = set(), []
    for b in g:
        best = max(((iou(b, o[:4]), k) for k, o in enumerate(out) if k not in used), default=(0, None))
        if best[0] >= 0.5:
            used.add(best[1])
        else:
            miss.append(b)
    return miss


imgs = {f: plt.imread(V / f"figures/kitti/{SEQ}_{f:06d}.png") for f in FRAMES}
h, w = imgs[FRAMES[0]].shape[:2]
pw = (S.TEXT_IN - 0.08) / 2
fig, axs = plt.subplots(len(FRAMES), 2, figsize=(S.TEXT_IN, len(FRAMES) * (pw * (h - Y0) / w + 0.17) + 0.2),
                        layout="constrained")
fig.get_layout_engine().set(w_pad=0.01, h_pad=0.01, wspace=0.02, hspace=0.02)
report = []
for c, (title, sysname) in enumerate(SYSTEMS):
    a = load(sysname)
    ids = sorted({int(r[1]) for r in a if FRAMES[0] - TRAIL <= int(r[0]) - 1 <= FRAMES[-1]})
    col = {tid: PAL[k % len(PAL)] for k, tid in enumerate(i for i in ids if any(
        int(r[1]) == i and int(r[0]) - 1 in FRAMES for r in a))}
    for r_, f in enumerate(FRAMES):
        ax = axs[r_, c]
        ax.imshow(imgs[f])
        out = boxes(a, f)
        for x1, y1, x2, y2, tid in out:
            pts = trail(a, tid, f)
            if len(pts) > 1:
                xs, ys = zip(*pts)
                ax.plot(xs, ys, color="white", lw=2.6, solid_capstyle="round", zorder=3)
                ax.plot(xs, ys, color=col[tid], lw=1.5, solid_capstyle="round", zorder=4)
            ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor=col[tid], lw=1.4, zorder=5))
            ax.text(x1, y1 - 2, f"{tid}", color="black" if col[tid] in LIGHT else "white", va="bottom",
                    ha="left", zorder=6, bbox=dict(boxstyle="square,pad=0.1", facecolor=col[tid], edgecolor="none"))
        g = gt(f)
        miss = missed(out, g)
        for x1, y1, x2, y2 in miss:
            ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor="white", lw=1.1, ls=(0, (3, 2))))
            ax.add_patch(Rectangle((x1, y1), x2 - x1, y2 - y1, fill=False, edgecolor="black", lw=1.1, ls=(3, (3, 2))))
        n_ok = len(g) - len(miss)
        head = f"{title}, " if r_ == 0 else ""
        ax.set_title(f"{head}frame {f}: {n_ok} of {len(g)} objects tracked", loc="left", pad=2)
        ax.set_xlim(0, w)
        ax.set_ylim(h, Y0)
        ax.axis("off")
        report.append((sysname.split("@")[0], f, sorted(o[4] for o in out), n_ok, len(g)))
fig.savefig(V / "Fig4.pdf")
print("wrote Fig4.pdf", fig.get_size_inches() * 25.4, "mm")
for r in report:
    print(r)
