"""
ACT baseline (Gwon & Lee, Electronics 15(17) 4047, 2026, doi:10.3390/electronics15174047) on the
cached KITTI streams, for the comparison with the frozen V7f (plan:
research/final/V7_ACT_COMPARISON_PLAN.md). The frozen runner tools/v7/dev.py is not changed; this
runner reuses its read-only pieces and writes the same files
(outputs/v7/<split>/<system>/<det>/<seq>.trk.pkl), so the frozen evaluator
tools/v7/kitti/kitti_eval.py reads them unchanged.

  V7_SPLIT=kitti python tools/v7/act_baseline.py <det> <system> [<system> ...]

system: 'ACT' with the runner modifiers 't:<transform>' and 'trk:ocsort' of dev.py,
        or 'HOSTCHK' (host thresholds through this runner; must equal dev.py 'NATIVE').
"""
from __future__ import annotations

import hashlib
import os
import pickle
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.v7.dev import (HOST_BYTETRACK, HOST_OCSORT, SPLITS, _ocsort_classes,  # noqa: E402
                          _ocsort_host, out_dir, split_sequences)

# Published global parameter set of ACT (Sect. 4.1 of the paper), used unchanged.
ACT = dict(tau_H0=0.6, tau_H1=0.3, tau_L0=0.1, tau_L1=0.2, tau_L2=0.15, delta_q=0.7, delta_n=100)


def act_thresholds(scores, p=ACT):
    """Algorithm 1 of the paper: (tau_high, tau_low, Q1, N) for one frame."""
    s = np.asarray(scores, float)
    sv = s[s > p["tau_L0"]]
    if len(sv) == 0:
        return p["tau_H0"], p["tau_L0"], None, 0
    q1 = float(np.percentile(sv, 25))
    n = int(len(sv))
    if q1 > p["delta_q"]:
        return p["tau_H0"], (p["tau_L1"] if n > p["delta_n"] else p["tau_L2"]), q1, n
    return p["tau_H1"], p["tau_L0"], q1, n


def _code_sha():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _parse(system):
    base, *mods = system.split("@")
    tf = next((m[2:] for m in mods if m.startswith("t:")), None)
    ocsort = "trk:ocsort" in mods
    assert base in ("ACT", "HOSTCHK"), system
    assert all(m.startswith("t:") or m == "trk:ocsort" for m in mods), system
    return base, tf, ocsort


def track_sequence(split, system, det, seq):
    os.chdir(ROOT)
    from adapters.trackers.bytetrack import ByteTrackAdapter
    from adapters.types import Detection
    from tools.run_policy_validation import CachedDetector
    base, tf, ocsort = _parse(system)
    sp = SPLITS[split]
    cd = CachedDetector(f"{sp['native']}/{det}/{seq}.npz", transform=tf)
    h = HOST_OCSORT if ocsort else HOST_BYTETRACK
    if ocsort:
        tr = _ocsort_host(h)
    else:
        tr = ByteTrackAdapter(high=h["assoc"], low=h["low"], new=h["birth"], buffer=30,
                              match=h["match"], fuse=True)
    lines, audit = [], []
    for i in range(1, cd.frames + 1):
        cd.frame = i
        raw = cd.detect(None, 0.0, None, 736)
        s = np.array([d.confidence for d in raw])
        if base == "ACT":
            hi, lo, q1, n = act_thresholds(s)
            keep = [k for k in range(len(raw)) if s[k] > lo]
        else:                                   # host thresholds, every candidate passed
            hi, lo, q1, n = min(h["assoc"], h["birth"]) if ocsort else h["assoc"], None, None, len(raw)
            keep = list(range(len(raw)))
        dets = [Detection(x1=raw[k].x1, y1=raw[k].y1, x2=raw[k].x2, y2=raw[k].y2,
                          confidence=float(raw[k].confidence), class_id=raw[k].class_id) for k in keep]
        tr.set_association_tolerance(h["match"])
        if ocsort:
            tracks = tr.update([[x.x1, x.y1, x.x2, x.y2, x.confidence] for x in dets], cd.shape, hi)
            _ocsort_classes(tracks, dets, tr)
        else:
            tracks = tr.update(dets, cd.shape, association_threshold=hi, birth_threshold=h["birth"],
                               image=None)
        for t in tracks:
            lines.append(f"{i},{t.track_id},{t.x1:.3f},{t.y1:.3f},{t.x2 - t.x1:.3f},"
                         f"{t.y2 - t.y1:.3f},{t.confidence:.6f},{t.class_id},-1,-1\n")
        audit.append(dict(tau_high=hi, tau_low=lo, q1=q1, n=n, passed=len(dets), tracks=len(tracks)))
    return lines, audit


def track_one(job):
    split, system, det, seq = job
    dest = out_dir(split) / system / det / f"{seq}.trk.pkl"
    base, tf, ocsort = _parse(system)
    stamp = dict(code_sha=_code_sha(), method=base, params=ACT if base == "ACT" else None,
                 transform=tf, ocsort=ocsort)
    if dest.exists() and pickle.load(open(dest, "rb")).get("v7_stamp") == stamp:
        return
    lines, audit = track_sequence(split, system, det, seq)
    dest.parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(dict(audit=audit, tracks_txt="".join(lines), v7_stamp=stamp), open(dest, "wb"))


if __name__ == "__main__":
    split = os.environ.get("V7_SPLIT", "kitti")
    det, *systems = sys.argv[1:]
    jobs = [(split, sy, det, s) for sy in systems for s in split_sequences(split)]
    with ProcessPoolExecutor(int(os.environ.get("V7_WORKERS", 6))) as ex:
        list(ex.map(track_one, jobs, chunksize=1))
    print("done", det, systems, len(jobs), "jobs")
