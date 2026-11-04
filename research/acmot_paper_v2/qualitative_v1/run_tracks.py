"""
Baseline and frozen AC-MOT tracks for ONE VisDrone2019-MOT-val sequence, from the CPU detector cache
of make_cpu_cache.py. The tracking code is the archived code itself, imported unchanged:

  baseline : research/acmot_paper_v2/run_baseline_systems.run_tracker  (YOLO11m at 1536 px, NMS 0.70,
             cache floor 0.01, no extra score threshold)
  AC-MOT   : research/acmot_paper_v2/controller_search/run_v3_joint_search.run_policy_with_conf with the
             frozen action map and SCI thresholds of FREEZE_MANIFEST_V3_ADAPTIVE.json, exactly as in
             research/acmot_paper_v2/run_v3_second_val_read.py
  scoring  : tools/v6/eval_official.official_sequence_stats / combine_official (official VisDrone Task 4b)

Only two module-level paths of controller_search/sim.py are redirected at run time (VAL_ROOT, CACHE_ROOT)
to the cloud copies of the data; no file of the archived code is modified.

  python run_tracks.py --seq uav0000117_02622_v --data <VisDrone2019-MOT-val root> --cache <cache root> --out <dir>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

FREEZE = ROOT / "research/acmot_paper_v2/controller_search/FREEZE_MANIFEST_V3_ADAPTIVE.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--cache", required=True, help="root that holds visdrone_val/r<res>_n<nms>/<seq>.npz")
    ap.add_argument("--out", required=True)
    ap.add_argument("--trackeval", required=True)
    a = ap.parse_args()
    sys.path.insert(0, a.trackeval)

    import research.acmot_paper_v2.controller_search.sim as sim
    sim.VAL_ROOT = Path(a.data)
    sim.CACHE_ROOT = Path(a.cache)
    from research.acmot_paper_v2 import run_v3_second_val_read as v3
    from research.acmot_paper_v2.controller_search.run_v3_joint_search import run_policy_with_conf
    from research.acmot_paper_v2.run_baseline_systems import run_tracker, EVAL5_TO_VISDRONE
    from adapters.trackers.bytetrack import ByteTrackAdapter
    from adapters.trackers.oatrack import OATrackAdapter
    from tools.v6.eval_official import official_sequence_stats, combine_official

    freeze = json.loads(FREEZE.read_text())
    am = freeze["controller"]["action_mapping"]
    action_map = {lv: (am[lv]["resolution"], am[lv]["nms_iou"], am[lv]["confidence_floor"]) for lv in am}
    assert action_map == v3.ACTION_MAP, (action_map, v3.ACTION_MAP)
    th = freeze["controller"]["thresholds"]
    assert (th["t_med"], th["t_high"]) == (v3.SPEC.t_med, v3.SPEC.t_high)

    npz = np.load(Path(a.cache) / "visdrone_val" / "r1536_n70" / f"{a.seq}.npz")
    det_rows, shape = npz["det"], tuple(int(x) for x in npz["shape"])
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    summary = dict(seq=a.seq, action_map=v3.ACTION_MAP, t_med=v3.SPEC.t_med, t_high=v3.SPEC.t_high,
                   baseline=dict(resolution=1536, nms=0.70, extra_score_threshold=None), runs={})
    for host, factory in (("bytetrack", ByteTrackAdapter), ("oatrack", OATrackAdapter)):
        base = run_tracker(lambda: factory(), det_rows, shape)
        acm, levels = run_policy_with_conf("visdrone_val", a.seq, v3.ACTION_MAP, host, v3.SPEC)
        for name, tr in (("baseline", base), ("acmot", acm)):
            np.savetxt(out / f"{a.seq}_{host}_{name}.txt", tr, fmt="%d,%d,%.2f,%.2f,%.2f,%.2f,%.4f,%d,%d,%d")
            st = official_sequence_stats(a.data, a.seq, tr, class_map=EVAL5_TO_VISDRONE)
            summary["runs"][f"{host}_{name}"] = combine_official([st])
        (out / f"{a.seq}_{host}_acmot_levels.txt").write_text("\n".join(levels) + "\n")
        summary["runs"][f"{host}_acmot"]["level_frac"] = {lv: levels.count(lv) / len(levels) for lv in ("LOW", "MEDIUM", "HIGH")}
    (out / f"{a.seq}_summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
