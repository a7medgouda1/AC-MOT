"""
Track-continuity measures of the reproduced baseline and AC-MOT runs of one sequence (ByteTrack host by
default): identity switches, fragmentations, and mostly tracked / partially tracked / mostly lost GT
trajectories, computed with motmetrics per evaluated class on the GT filtered as in
tools/v6/eval_official (ignored regions dropped, trajectories split per class), and summed over classes.

  python continuity_metrics.py --seq <seq> --data <root> --tracks <dir> [--host bytetrack]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from make_fig_acmot_example import EVAL5_TO_VISDRONE, load_tracks  # noqa: E402

KEYS = ["num_objects", "num_switches", "num_fragmentations", "mostly_tracked", "partially_tracked",
        "mostly_lost", "num_unique_objects"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--tracks", required=True)
    ap.add_argument("--host", default="bytetrack")
    a = ap.parse_args()
    import motmetrics as mm
    from tools.v6.eval_official import drop_objects, break_gts

    data = Path(a.data)
    n = len(list((data / "sequences" / a.seq).glob("*.jpg")))
    gt_raw = np.loadtxt(data / "annotations" / f"{a.seq}.txt", delimiter=",", ndmin=2)
    gt = break_gts(drop_objects(gt_raw, gt_raw))
    out = {}
    for name in ("baseline", "acmot"):
        tr = drop_objects(load_tracks(Path(a.tracks) / f"{a.seq}_{a.host}_{name}.txt"), gt_raw)
        tot = dict.fromkeys(KEYS, 0)
        for c in EVAL5_TO_VISDRONE.values():
            g, p = gt[gt[:, 7] == c], tr[tr[:, 7] == c]
            if not len(g):
                continue
            acc = mm.MOTAccumulator(auto_id=True)
            for t in range(1, n + 1):
                gg, pp = g[g[:, 0] == t], p[p[:, 0] == t]
                acc.update(gg[:, 1].astype(int).tolist(), pp[:, 1].astype(int).tolist(),
                           mm.distances.iou_matrix(gg[:, 2:6], pp[:, 2:6], max_iou=0.5))
            r = mm.metrics.create().compute(acc, metrics=KEYS, name=str(c))
            for k in KEYS:
                tot[k] += int(r[k].iloc[0])
        out[name] = tot
    path = Path(a.tracks) / f"{a.seq}_{a.host}_continuity.json"
    path.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
