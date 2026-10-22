# V7f on UAVDT test — preregistration (written before any run)

Date: 2026-10-21. Owner authorization: explicit, in the working session of 2026-10-21 (one evaluation of the
frozen V7f on UAVDT for Paper 2). Decision D-042. Protected row: PROTECTED_EVALUATIONS.md P4. One run; no
redesign, re-tuning or re-run with other settings follows it. The owner decides after the result whether it
enters the manuscript; the result is recorded in the project records in every case.

## Data
- UAVDT test split of the frozen external protocol (`research/uavdt_protocol/UAVDT_EXTERNAL_PROTOCOL_FREEZE.json`):
  20 sequences, 16,592 frames; GT and ignore rules of `UAVDT_ADAPTER_V1_FREEZE.json` (rows with score 0 or
  frame < 1 removed; predictions fully inside an ignore box removed), as in tools/build_uavdt_view.py.
- Ground truth: official `UAV-benchmark-MOTD_v1.0` GT from the public mirror
  `huggingface.co/datasets/vanthanh/UAVDT-Benchmark-M`, accepted because, after the protocol filters, the number of
  ground-truth boxes of every one of the 20 sequences equals the count recorded from the official GT in
  `research/acmot_paper_v2/UAVDT_TRANSFER_RESULT.json` (20/20 equal; frame counts equal the protocol's 16,592).
- Detections: the existing caches `outputs/det_cache_uavdt_native` (YOLOv8n and RT-DETR-L, COCO weights, vehicle
  classes car/bus/truck, 736 pixels), made before the V7 freeze. Faster R-CNN is not used (protected detector P2).
- Frames: zero-byte placeholders (the ByteTrack-host runs read cached detections only).

## Systems
- Host: ByteTrack alone with its published setting (`NATIVE`).
- Host + SCL: frozen V7f (`V7f`; tag universal-acmot-v7-freeze; acmot_v7.py and tools/v7/systems.py identical to the tag).

## Commands
`V7_SPLIT=uavdt V7_DETS=yolov8,rtdetr ACMOT_UAVDT_VIEW=<view> python tools/v7/dev.py run NATIVE V7f`, then
`dev.py report NATIVE V7f` and `tools/v7/bootstrap.py NATIVE V7f --protocol internal`.

## Metrics and analysis
- Single vehicle class, the project's UAVDT protocol (class-agnostic, tools/seqstats.py, ignore regions applied),
  as in E50 and Paper 1. Primary: HOTA; secondary: MOTA, IDF1. Per detector and pooled.
- Paired sequence bootstrap: 10,000 resamples, numpy default_rng(42), percentile 95% interval of (host + SCL) − host.
- A change counts as a gain (loss) only if its interval lies above (below) zero.

## Predictions (stated before the run)
1. Safety: V7f does not lower HOTA significantly with either detector.
2. RT-DETR-L (over-confident, many false positives) gains more than YOLOv8n in MOTA.
