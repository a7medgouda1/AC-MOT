"""
Fig. 2 of Paper2_V50: what the layer sees. The logits of the last W = 10 frames (Z_t^W) at one frame
of a clean stream (MOT17 val-half, published YOLOX-X detections, ByteTrack official setting) and of a
noisy stream (KITTI tracking training, RT-DETR-L, ByteTrack library setting), with the two nested Otsu
splits t1 and t2 and the three groups. The frozen layer (acmot_v7.py, spec V7f) is run unchanged on the
cached detections with its host in the loop, exactly as in the frozen drivers, and its window is read
just before the decision for frame t. The decision values printed by this script must equal the ones
stored in the original runs' per-frame logs (checked below).

  .venv/bin/python JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev50/scripts/make_fig_groups.py
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

V = Path(__file__).resolve().parents[1]
ROOT = V.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools/v7/external"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.chdir(ROOT)

from acmot_v7 import HostContract, V7Layer, spec_from_dict  # noqa: E402
from adapters.trackers.bytetrack import ByteTrackAdapter  # noqa: E402
from adapters.types import Detection  # noqa: E402
from tools.v7.systems import parse  # noqa: E402

base, ov, _, _, _ = parse("V7f")
SPEC = dict(ov, name=base)


def mot17_window(seq_prefix="MOT17-02", frame=101):
    import mot17_bytetrack_v7 as M
    from ultralytics.trackers.basetrack import BaseTrack
    ann = json.load(open(M.EXT / "data_mirror/MOT17/annotations/val_half.json"))
    dets = M.load_stream("st", ann)
    h = M.HOSTS["official"]
    host = HostContract(assoc=h["assoc"], birth=h["birth"], low=h["low"], match=h["match"])
    for im in ann["images"]:
        seq, fid = im["file_name"].split("/")[0], int(im["frame_id"])
        if not seq.startswith(seq_prefix):
            continue
        if fid == 1:
            BaseTrack.reset_id()
            tr = ByteTrackAdapter(high=h["assoc"], low=h["low"], new=h["birth"], buffer=30, match=h["match"], fuse=True)
            layer = V7Layer(spec_from_dict(SPEC), host)
        d = dets[im["file_name"]].copy()
        if fid == frame:
            Z = np.concatenate(list(layer.window))
        dec = layer.step(d[:, :4], d[:, 4], None, classes=np.zeros(len(d), int))
        if fid == frame:
            return Z, dec.log
        det_list = [Detection(x1=float(d[k, 0]), y1=float(d[k, 1]), x2=float(d[k, 2]), y2=float(d[k, 3]),
                              confidence=float(v), class_id=0) for k, v in zip(dec.keep, dec.scores)]
        tr.set_association_tolerance(dec.match)
        tracks = tr.update(det_list, (im["height"], im["width"]), association_threshold=dec.assoc,
                           birth_threshold=dec.birth)
        layer.observe([[t.x1, t.y1, t.x2, t.y2] for t in tracks], [t.track_id for t in tracks])


def kitti_window(seq="0001", frame=101, det="rtdetr"):
    from tools.run_policy_validation import CachedDetector
    from tools.v7.dev import HOST_BYTETRACK, SPLITS
    h = HOST_BYTETRACK
    cd = CachedDetector(f"{SPLITS['kitti']['native']}/{det}/{seq}.npz", transform=None)
    tr = ByteTrackAdapter(high=h["assoc"], low=h["low"], new=h["birth"], buffer=30, match=h["match"], fuse=True)
    layer = V7Layer(spec_from_dict(SPEC), HostContract(**h))
    for i in range(1, cd.frames + 1):
        cd.frame = i
        raw = cd.detect(None, 0.0, None, 736)
        b = np.array([[d.x1, d.y1, d.x2, d.y2] for d in raw]).reshape(-1, 4)
        s = np.array([d.confidence for d in raw])
        vis = cd.visual_dict(i)
        if i == frame:
            Z = np.concatenate(list(layer.window))
        dec = layer.step(b, s, vis.get("motion"), classes=[d.class_id for d in raw])
        if i == frame:
            return Z, dec.log
        dets = [Detection(x1=raw[k].x1, y1=raw[k].y1, x2=raw[k].x2, y2=raw[k].y2,
                          confidence=float(v), class_id=raw[k].class_id) for k, v in zip(dec.keep, dec.scores)]
        tr.set_association_tolerance(dec.match)
        tracks = tr.update(dets, cd.shape, association_threshold=dec.assoc, birth_threshold=dec.birth)
        layer.observe([[t.x1, t.y1, t.x2, t.y2] for t in tracks], [t.track_id for t in tracks])


Zm, Lm = mot17_window()
Zk, Lk = kitti_window()
# check against the stored per-frame logs of the original runs
pf = json.load(open("/root/acmot_work/acmot_external/runs/bytetrack_mot17/MOT17-val/BY_official_st_V7f/per_frame.json"))
ref_m = [r for r in pf["audit"] if r["seq"].startswith("MOT17-02") and r["frame"] == 101][0]
import pickle  # noqa: E402
ref_k = pickle.load(open(ROOT / "outputs/v7/kitti/V7f/rtdetr/0001.trk.pkl", "rb"))["audit"][100]
for L, R in ((Lm, ref_m), (Lk, ref_k)):
    for k in ("t1", "t2", "rho", "rho_bar", "regime"):
        assert (L[k] == R[k]) if isinstance(R[k], str) else abs(L[k] - R[k]) < 1e-9, (k, L[k], R[k])
print("decision values equal the stored logs")
print("MOT17", {k: Lm[k] for k in ("t1", "t2", "rho", "rho_bar", "regime")}, len(Zm))
print("KITTI", {k: Lk[k] for k in ("t1", "t2", "rho", "rho_bar", "regime")}, len(Zk))

import figstyle as S  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

fig, axs = plt.subplots(2, 1, figsize=(S.COL_IN, 4.2), layout="constrained")
bins = np.arange(-5.0, 5.01, 0.25)
panels = [(axs[0], Zm, Lm, "(a) Clean stream: MOT17, YOLOX-X"), (axs[1], Zk, Lk, "(b) Noisy stream: KITTI, RT-DETR-L")]
for ax, Z, L, title in panels:
    t1, t2 = L["t1"], L["t2"]
    Zc = np.clip(Z, bins[0], bins[-1] - 1e-6)
    groups = [(Zc < t1, S.GRAY, None, "background"), ((Zc >= t1) & (Zc < t2), "white", "////", "uncertain"),
              (Zc >= t2, S.BLUE, None, "confident")]
    for m, col, hat, lab in groups:
        ax.hist(Zc[m], bins=bins, color=col, hatch=hat, edgecolor="black", linewidth=0.4, label=lab)
    ymax = ax.get_ylim()[1]
    for t, name, ls in ((t1, "t₁", "--"), (t2, "t₂", "-")):
        ax.axvline(t, color="black", lw=1.0, ls=ls)
        ax.text(t + 0.08, ymax * 0.97, name, va="top", ha="left")
    mode = L["regime"]
    ax.text(0.98, 0.95, f"ρ = {L['rho']:.2f}\nmedian ρ = {L['rho_bar']:.2f}\n{mode} mode",
            transform=ax.transAxes, va="top", ha="right")
    ax.set_title(title, loc="left", pad=16)
    ax.set_xlim(bins[0], bins[-1])
    ax.set_ylabel("Candidates")
    top = ax.secondary_xaxis("top", functions=(lambda z: z, lambda z: z))
    sc = np.array([0.05, 0.2, 0.5, 0.8, 0.95])
    top.set_xticks(np.log(sc / (1 - sc)), [f"{v:g}" for v in sc])
    top.tick_params(length=2)
axs[1].set_xlabel("Logit z of the detector score (top axis: score)")
handles = [Patch(facecolor=S.GRAY, edgecolor="black", lw=0.4, label="background"),
           Patch(facecolor="white", edgecolor="black", lw=0.4, hatch="////", label="uncertain"),
           Patch(facecolor=S.BLUE, edgecolor="black", lw=0.4, label="confident")]
fig.legend(handles=handles, frameon=False, ncol=3, loc="outside lower center")
fig.savefig(V / "Fig2.pdf")
print("wrote Fig2.pdf", fig.get_size_inches() * 25.4, "mm")
