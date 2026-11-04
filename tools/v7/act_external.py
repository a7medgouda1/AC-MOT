"""
ACT on the held-out UAVDT test split (plan: research/final/V7_ACT_ORIGINAL_UAVDT_PLAN.md, D-043).
Writes outputs/v7/<split>/<system>/<det>/<seq>.pkl in the frozen runner's format (sequence stats of
tools/seqstats.py, audit, tracks), so tools/v7/dev.py report and tools/v7/bootstrap.py read them
unchanged. Tracking: track_sequence of tools/v7/act_baseline.py (unchanged); 'HOSTCHK' passes the host
thresholds and must reproduce dev.py 'NATIVE'.

  V7_SPLIT=uavdt ACMOT_UAVDT_VIEW=<view> python tools/v7/act_external.py <det> <system> [...]
"""
from __future__ import annotations

import os
import pickle
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.v7.act_baseline import ACT, _code_sha, _parse, track_sequence  # noqa: E402
from tools.v7.dev import SPLITS, out_dir, split_sequences  # noqa: E402


def run_one(job):
    split, system, det, seq = job
    dest = out_dir(split) / system / det / f"{seq}.pkl"
    base, tf, ocsort = _parse(system)
    stamp = dict(code_sha=_code_sha(), method=base, params=ACT if base == "ACT" else None,
                 transform=tf, ocsort=ocsort)
    if dest.exists():
        raise SystemExit(f"{dest} exists (one run per cell)")
    sp = SPLITS[split]
    frames = sorted((Path(sp["data"]) / "sequences" / seq).glob("*.jpg"))
    lines, audit = track_sequence(split, system, det, seq)
    if len(frames) != len(audit):
        raise SystemExit(f"{seq}: {len(frames)} frames in the view, {len(audit)} in the cache")
    from tools.seqstats import sequence_stats
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
    f.writelines(lines)
    f.close()
    st = sequence_stats(sp["data"], seq, f.name)
    os.unlink(f.name)
    st["audit"] = audit
    st["tracks_txt"] = "".join(lines)
    st["v7_stamp"] = stamp
    dest.parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(st, open(dest, "wb"))


if __name__ == "__main__":
    split = os.environ["V7_SPLIT"]
    det, *systems = sys.argv[1:]
    jobs = [(split, sy, det, s) for sy in systems for s in split_sequences(split)]
    with ProcessPoolExecutor(int(os.environ.get("V7_WORKERS", 6))) as ex:
        list(ex.map(run_one, jobs, chunksize=1))
    print("done", split, det, systems, len(jobs), "jobs")
