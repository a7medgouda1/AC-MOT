# V7f on VisDrone confirmation-16 — preregistration (written before any run)

Date: 2026-10-21. Owner authorization: explicit, in the working session of 2026-10-21 (option
"confirmation-16" chosen by the owner for one evaluation of the frozen V7f, for Paper 2). Decision D-041.
Protected row: PROTECTED_EVALUATIONS.md P1. This is the ONE evaluation of this split; no redesign,
re-tuning or re-run with other settings follows it, and the result is reported whatever it is.

## Data
- Split: VisDrone2019-MOT-train confirmation-16, the 16 sequences fixed in `research/TRAIN_SPLIT_V5.json`
  (seed 20260927; created before any train result), 7,034 frames.
- Annotations: the official VisDrone2019-MOT-train annotation files, obtained from the public mirror
  `huggingface.co/datasets/huseyincavus/visdrone2019-mot` and accepted only because their fingerprint equals
  the one recorded in TRAIN_SPLIT_V5.json (sha256 `045620e4ba7009dba97e495271254b468b50c01db85ca80c4fe90871a1e17e81`,
  56 files, verified before any use). No annotation content was inspected.
- Frames: zero-byte placeholders (the ByteTrack-host runs read cached detections only).
- Detections: the existing native caches `outputs/det_cache_train_native` (YOLOv8n and RT-DETR-L at 736
  pixels, the detectors of the V7 VisDrone development), cached before the freeze; no new detection run.

## Systems (fixed before the run)
- Host: ByteTrack alone with its published setting (`NATIVE` in tools/v7/systems.py).
- Host + SCL: the frozen V7f (`V7f`; tag universal-acmot-v7-freeze → 488df9a; acmot_v7.py and
  tools/v7/systems.py byte-identical to the tag, checked before the run).
- The earlier P1 plan (V6-TF vs V4) is not run: V7 = V7f is the final target (Amendment 10) and the V4
  caches (`outputs/det_cache_train`) are not available; the single use of the split goes to V7f.

## Commands
`V7_SPLIT=conf16 V7_DETS=yolov8,rtdetr ACMOT_VISDRONE_TRAIN=<annotations root> python tools/v7/dev.py run NATIVE V7f`,
then `dev.py official NATIVE V7f` and `tools/v7/bootstrap.py NATIVE V7f --protocol official`.

## Metrics and analysis
- Primary: HOTA, official-compatible VisDrone protocol (tools/v6/eval_official.py via dev.py official).
  Secondary: MOTA, IDF1 (same protocol). Per detector, and pooled over both detectors.
- Paired sequence bootstrap: 10,000 resamples, numpy default_rng(42), percentile 95% interval of
  (host + SCL) − host.
- Reading rule: a change counts as a gain (loss) only if its 95% interval lies above (below) zero;
  otherwise "no significant change".

## Predictions (stated before the run)
1. Safety: V7f does not lower HOTA significantly with either detector.
2. RT-DETR-L (the noisy, over-confident stream in the V7 development) gains more from V7f than YOLOv8n.
Both predictions are reported as confirmed or not confirmed.
