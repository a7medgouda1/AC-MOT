"""
Per-frame trace of the frozen AC-MOT controller on one VisDrone2019-MOT-val sequence: the scene
complexity index (SCI) that the controller computed and the state it chose, for the ByteTrack host.
The loop is the loop of run_v3_joint_search.run_policy_with_conf, unchanged, with the decision of
every frame recorded; the states are checked against the levels file written by run_tracks.py.

  python scene_trace.py --seq uav0000117_02622_v --data <root> --cache <cache root> --tracks <dir> --trackeval <dir>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--trackeval", required=True)
    ap.add_argument("--host", default="bytetrack")
    a = ap.parse_args()
    sys.path.insert(0, a.trackeval)

    import research.acmot_paper_v2.controller_search.sim as sim
    sim.VAL_ROOT = Path(a.data)
    sim.CACHE_ROOT = Path(a.cache)
    from research.acmot_paper_v2 import run_v3_second_val_read as v3
    from research.acmot_paper_v2.controller_search.sim import get_sequence, make_tracker
    from acmot_sci import SceneLayer

    sd = get_sequence("visdrone_val", a.seq)
    scene = SceneLayer(v3.SPEC)
    tracker = make_tracker(a.host)
    rows = []
    for t in range(1, sd.n_frames + 1):
        decision = scene.decide(t, sd.image_stats(t))
        res, nms, conf = v3.ACTION_MAP[decision.level]
        dets = sd.detections(t, res, nms, conf)
        tracks = tracker.update(dets, sd.shape)
        scene.observe([[x.x1, x.y1, x.x2, x.y2] for x in tracks])
        rows.append(dict(frame=t, level=decision.level, sci=decision.sci, scene=decision.scene,
                         analysed=decision.analysed, resolution=res, nms=nms, conf_floor=conf))
    levels = (Path(a.tracks) / f"{a.seq}_{a.host}_acmot_levels.txt").read_text().split()
    assert levels == [r["level"] for r in rows], "trace differs from the levels of run_tracks.py"
    out = Path(a.tracks) / f"{a.seq}_{a.host}_scene_trace.json"
    out.write_text(json.dumps(dict(seq=a.seq, host=a.host, t_med=v3.SPEC.t_med, t_high=v3.SPEC.t_high,
                                   frames=rows), indent=0))
    changes = [r["frame"] for i, r in enumerate(rows) if i and r["level"] != rows[i - 1]["level"]]
    print("frames", len(rows), "state changes at", changes)


if __name__ == "__main__":
    main()
