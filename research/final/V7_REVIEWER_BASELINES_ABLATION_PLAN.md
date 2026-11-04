# Adaptive-threshold baselines and component ablation of the frozen V7f — plan (written before the runs)

Date: 2026-10-21. Owner instruction (reviewer concerns 1 and 3). Development data only (KITTI tracking training,
non-protected); the frozen V7f code and configuration are not changed — every variant is a runner override of
tools/v7/systems.py (`<base>@key=value`), with the frozen acmot_v7.py.

## Cells (fixed before the runs)
- C1 ByteTrack, RT-DETR-L; C2 BoT-SORT, RT-DETR-L (sequence 0020 excluded in every arm, as in the paper);
  C3 OC-SORT, YOLOv8n — the three KITTI cells of the manuscript.
- C4 ByteTrack, RT-DETR-L with halved scores (`t:scale05`); C5 OC-SORT, YOLOv8n with halved scores.
Cached detections `outputs/det_cache_kitti_native`; official KITTI HOTA (car/pedestrian average,
tools/v7/kitti/kitti_eval.py); paired bootstrap over sequences (10,000, seed 42) against the host alone.

## Experiment 1 — simple adaptive-threshold baselines (same input, same window)
- OTSU-1: the tracker's matching and birth thresholds are set every frame to the first Otsu split t1 of the logits
  of the last 10 frames; raw scores, no mode decision, no remap, no duplicate rule, no rescue, no motion
  (`NATIVE@regime=noisy@noisy_primary=t1@noisy_ext=host`).
- OTSU-2: the same with the second split t2 (`NATIVE@regime=noisy@noisy_primary=t2@noisy_ext=host`).
Compared with host alone and with V7f on C1-C5.

## Experiment 3 — component ablation of the final V7f (one component removed at a time)
no rescue (`rescue=none`); no motion tolerance (`motion=0`); no score remap (`scores=raw`); no background check
(`bg_check=0`); overlap-only duplicates instead of track context (`dup=iou`); always noisy (`regime=noisy`);
always clean (`regime=clean`). Reported as HOTA (and MOTA, IDF1) on C1-C5 next to the full V7f.

## Reporting
All variants and cells are reported as they come out; nothing in V7f is changed afterwards.
