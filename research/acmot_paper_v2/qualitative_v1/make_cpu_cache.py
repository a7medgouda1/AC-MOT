"""
CPU re-run of the detector cache for ONE VisDrone2019-MOT-val sequence, for the qualitative figure of
Chapter 3 (illustrative reproduction; the archived GPU cache of 2026-10-04 is not available here).

Same frozen checkpoint (dronefreak/visdrone-yolo11m best.pt, revision ed725b7, sha256 c6f98247...),
same resolutions {1088, 1280, 1536}, NMS values {0.45, 0.60, 0.70}, confidence floor 0.01, max_det 1000,
and the same eval5 class filter as notebooks/lightning/run_cache_generation.py. The only differences:
CPU in FP32 instead of a T4 GPU in FP16, and one forward pass per (frame, resolution) instead of two
(the original called model.predict once only to set up the predictor and then repeated the forward
pass; --verify checks on the first frames that both paths give identical boxes).

  python make_cpu_cache.py --seq uav0000117_02622_v --data <VisDrone2019-MOT-val root> --out <cache root>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import cv2
import numpy as np
import torch
from ultralytics import YOLO

FROZEN_SHA256 = "c6f98247e7c731a567aaf37ca7b808beff588b687623e028b25a2e1d846e96e7"
CACHE_RES = [1088, 1280, 1536]
NMS_IOU = [0.45, 0.60, 0.70]
CKPT_TO_EVAL5 = {0: 0, 3: 1, 4: 2, 5: 3, 8: 4}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _clone(x):
    if isinstance(x, torch.Tensor):
        return x.clone()
    if isinstance(x, (list, tuple)):
        return type(x)(_clone(v) for v in x)
    return x


def original_multi_nms_predict(model, path, imgsz, nms_list):
    """Verbatim copy of run_cache_generation.multi_nms_predict, with half=False (CPU)."""
    model.predict(path, imgsz=imgsz, conf=0.01, iou=nms_list[0], max_det=1000, half=False, verbose=False)
    p = model.predictor
    im0 = cv2.imread(path)
    with torch.inference_mode():
        im = p.preprocess([im0])
        raw = p.inference(im)
        out = {}
        for tau in nms_list:
            p.args.iou = tau
            b = p.postprocess(_clone(raw), im, [im0])[0].boxes
            out[tau] = torch.cat([b.xyxy, b.conf[:, None], b.cls[:, None]], 1).cpu().numpy()
    return out, im0.shape[:2]


class OnePass:
    """One model per resolution; the predictor is set up once (first frame) and then reused, so every
    later frame costs one forward pass. Preprocess, inference and postprocess are the predictor's own."""

    def __init__(self, ckpt, imgsz, first_path):
        self.m = YOLO(ckpt)
        self.m.predict(first_path, imgsz=imgsz, conf=0.01, iou=NMS_IOU[0], max_det=1000, half=False, verbose=False)
        self.p = self.m.predictor

    def __call__(self, path):
        im0 = cv2.imread(path)
        p = self.p
        with torch.inference_mode():
            im = p.preprocess([im0])
            raw = p.inference(im)
            out = {}
            for tau in NMS_IOU:
                p.args.iou = tau
                b = p.postprocess(_clone(raw), im, [im0])[0].boxes
                out[tau] = torch.cat([b.xyxy, b.conf[:, None], b.cls[:, None]], 1).cpu().numpy()
        return out, im0.shape[:2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seq", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--verify", type=int, default=2, help="frames on which the one-pass path is checked")
    a = ap.parse_args()
    assert sha256(a.ckpt) == FROZEN_SHA256, "frozen checkpoint sha256 mismatch"
    frames = sorted(str(f) for f in (Path(a.data) / "sequences" / a.seq).glob("*.jpg"))
    out_root = Path(a.out)
    log = dict(seq=a.seq, frames=len(frames), device="cpu", fp="fp32", torch=torch.__version__,
               threads=torch.get_num_threads(), checkpoint_sha256=FROZEN_SHA256, verify={})
    for res in CACHE_RES:
        dirs = {t: out_root / f"r{res}_n{int(round(100 * t))}" for t in NMS_IOU}
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        if all((d / f"{a.seq}.npz").exists() for d in dirs.values()):
            print("skip", res)
            continue
        runner = OnePass(a.ckpt, res, frames[0])
        ref = YOLO(a.ckpt)
        for k in range(min(a.verify, len(frames))):
            o1, _ = original_multi_nms_predict(ref, frames[k], res, NMS_IOU)
            o2, _ = runner(frames[k])
            same = all(o1[t].shape == o2[t].shape and np.array_equal(o1[t], o2[t]) for t in NMS_IOU)
            log["verify"][f"r{res}_frame{k + 1}"] = bool(same)
            assert same, f"one-pass path differs from the original at res {res}, frame {k + 1}"
        rows = {t: [] for t in NMS_IOU}
        times, shape = [], None
        for t_, f in enumerate(frames, 1):
            t0 = time.perf_counter()
            out, shape = runner(f)
            times.append(time.perf_counter() - t0)
            for tau, arr in out.items():
                for r in arr:
                    c = int(r[5])
                    if c in CKPT_TO_EVAL5:
                        rows[tau].append([t_, *r[:4].tolist(), float(r[4]), CKPT_TO_EVAL5[c]])
            if t_ % 50 == 0:
                print(res, t_, "/", len(frames), round(float(np.mean(times[-50:])), 2), "s/frame", flush=True)
        for tau, d in dirs.items():
            np.savez_compressed(d / f"{a.seq}.npz", det=np.asarray(rows[tau], np.float64).reshape(-1, 7),
                                shape=np.asarray(shape), frames=len(frames))
        log[f"mean_s_per_frame_r{res}"] = float(np.mean(times))
        print(res, "done", {t: len(v) for t, v in rows.items()}, flush=True)
    (out_root / f"{a.seq}.cpu_cache_log.json").write_text(json.dumps(log, indent=1))
    print(json.dumps(log, indent=1))


if __name__ == "__main__":
    main()
