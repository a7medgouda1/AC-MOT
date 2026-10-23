"""
ACT (Gwon & Lee, Electronics 15(17) 4047, 2026) in its original setting: ByteTrack with its official MOT17
arguments on the published YOLOX-X detections of MOT17 val-half (plan: research/final/V7_ACT_ORIGINAL_UAVDT_PLAN.md).
Same loop, streams, host contracts and output writer as the frozen driver mot17_bytetrack_v7.py (imported
read-only); the frozen layer is replaced by ACT's per-frame thresholds (act_thresholds of
tools/v7/act_baseline.py, unchanged). Mode HOSTCHK passes the host thresholds and must reproduce the
driver's BASELINE output byte for byte.

  python tools/v7/external/mot17_act.py --mode ACT|HOSTCHK --stream st|bt --host official --name N
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[3]))
sys.path.insert(0, str(HERE.parent))

import mot17_bytetrack_v7 as M  # noqa: E402  (frozen driver, read-only)
from tools.v7.act_baseline import ACT, act_thresholds  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["ACT", "HOSTCHK"])
    ap.add_argument("--stream", required=True, choices=["st", "bt"])
    ap.add_argument("--host", required=True, choices=["official", "ultra"])
    ap.add_argument("--name", required=True)
    ap.add_argument("--root", default=str(M.EXT / "runs/bytetrack_mot17"))
    a = ap.parse_args()
    from adapters.trackers.bytetrack import ByteTrackAdapter
    from adapters.types import Detection
    from ultralytics.trackers.basetrack import BaseTrack

    ann = json.load(open(M.EXT / "data_mirror/MOT17/annotations/val_half.json"))
    dets = M.load_stream(a.stream, ann)
    h = M.HOSTS[a.host]
    out = Path(a.root) / "MOT17-val" / a.name / "data"
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"{out} exists and is not empty; choose a new --name")
    out.mkdir(parents=True, exist_ok=True)
    rows, audit, tr = {}, [], None
    for im in ann["images"]:
        seq, fid = im["file_name"].split("/")[0], int(im["frame_id"])
        if fid == 1:
            BaseTrack.reset_id()
            tr = ByteTrackAdapter(high=h["assoc"], low=h["low"], new=h["birth"], buffer=30,
                                  match=h["match"], fuse=True)
            rows[seq] = []
        d = dets[im["file_name"]].copy()
        if a.mode == "ACT":
            hi, lo, q1, n = act_thresholds(d[:, 4])
            keep = np.flatnonzero(d[:, 4] > lo)
        else:
            hi, lo, q1, n = h["assoc"], None, None, len(d)
            keep = np.arange(len(d))
        det_list = [Detection(x1=float(d[k, 0]), y1=float(d[k, 1]), x2=float(d[k, 2]), y2=float(d[k, 3]),
                              confidence=float(d[k, 4]), class_id=0) for k in keep]
        tr.set_association_tolerance(h["match"])
        tracks = tr.update(det_list, (im["height"], im["width"]), association_threshold=hi,
                           birth_threshold=h["birth"])
        n_out = 0
        for t in tracks:
            w, hh = t.x2 - t.x1, t.y2 - t.y1
            if h["filt"] and (w / max(hh, 1e-9) > 1.6 or w * hh <= h.get("min_area", 100)):
                continue
            rows[seq].append(f"{fid},{t.track_id},{t.x1:.2f},{t.y1:.2f},{w:.2f},{hh:.2f},{t.confidence:.2f},-1,-1,-1\n")
            n_out += 1
        audit.append(dict(seq=seq, frame=fid, n_det=len(d), n_out=n_out, tracks=len(tracks),
                          tau_high=hi, tau_low=lo, q1=q1, n=n))
    for s, r in rows.items():
        open(out / f"{s}.txt", "w").writelines(r)
    json.dump(dict(audit=audit, mode=a.mode, act_params=ACT if a.mode == "ACT" else None, stream=a.stream,
                   host=a.host, code_sha=__import__("hashlib").sha256(HERE.read_bytes()).hexdigest()),
              open(out.parent / "per_frame.json", "w"))
    print("wrote", a.name)


if __name__ == "__main__":
    main()
