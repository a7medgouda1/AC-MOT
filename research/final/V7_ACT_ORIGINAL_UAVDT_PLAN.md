# Frozen V7f vs ACT in ACT's original setting (MOT17) and on held-out UAVDT — plan (written before the runs)

Date: 2026-10-21. Owner instruction (explicit, this session): "the priority is the ACT experiment on the original
conditions and on the external UAVDT data". Decision D-043. Follows E59 (KITTI, `V7_ACT_COMPARISON_PLAN.md`).
The frozen V7f code, configuration and results are not changed and V7f is NOT re-run: its existing outputs are
the comparison arm (MOT17: the runs behind Paper 2 Table 9; UAVDT: E56). Only ACT is run, once per cell, with the
implementation of E59 (`act_thresholds` in `tools/v7/act_baseline.py`, unchanged) and its published parameters
(tau_H0 0.6, tau_H1 0.3, tau_L0 0.1, tau_L1 0.2, tau_L2 0.15, delta_q 0.7, delta_n 100); no tuning, no re-run with
other settings. Host coupling as in E59: association (high) threshold = tau_high, low group = passed detections
below tau_high (all > tau_low), the host's own birth threshold and matching tolerance unchanged.

## Part A — ACT's original conditions (MOT17, development data)
ACT was designed and tested with ByteTrack in its official MOT17 setting on YOLOX-X detections (paper Sect. 4.1;
its tau_H0 = 0.6 and tau_L0 = 0.1 are that setting). Same here:
- MOT17 val-half (7 sequences), the published YOLOX-X detections, both streams of the paper: floor 0.01
  (SparseTrack's release, `st`) and floor 0.1 (BoostTrack's release, `bt`); original scores (no transform).
- Host: ByteTrack official MOT17 setting (assoc 0.6, birth 0.7 = track_thresh + 0.1, low 0.1, match 0.8,
  official output filter), exactly as `tools/v7/external/mot17_bytetrack_v7.py --host official`.
- New driver `tools/v7/external/mot17_act.py` (same loop as the frozen driver, ACT instead of the layer).
  Check before the ACT runs: the driver with the host thresholds must reproduce `BY_official_{st,bt}_BASELINE`
  byte for byte.
- Arms: host (`BY_official_*_BASELINE`), V7f (`BY_official_*_V7f`), ACT (`BY_official_*_ACT`).
- Evaluation: `tools/v7/mot17_eval_v7.py` (HOTA, MOTA, IDF1; TrackEval, MOT17 val-half GT) and its `--boot`.

## Part B — held-out UAVDT test (protected P4; owner-authorized use for this ACT comparison, D-043)
- The E56 setting unchanged: 20 sequences, 16,592 frames, the project's UAVDT protocol (single vehicle class,
  ignore regions; tools/seqstats.py), GT and view of E56, cached YOLOv8n and RT-DETR-L detections
  (`outputs/det_cache_uavdt_native`), ByteTrack host with its published library setting (assoc 0.25, birth 0.25,
  low 0.1, match 0.8). No Faster R-CNN (P2).
- New runner `tools/v7/act_external.py` (writes `outputs/v7/uavdt/<system>/<det>/<seq>.pkl` in the frozen
  runner's format). Check before the ACT runs: with the host thresholds it must reproduce the E56 `NATIVE`
  tracks and metrics byte for byte.
- Arms: host (`NATIVE`, E56), V7f (`V7f`, E56), ACT (`ACT`). Evaluation: `tools/v7/dev.py report` and
  `tools/v7/bootstrap.py <A> <B> --protocol internal`, per detector.

## Analysis
Paired bootstrap over sequences (10,000 resamples, seed 42) of V7f − ACT and ACT − host, per cell; HOTA primary,
MOTA and IDF1 secondary. A difference counts only if its 95% interval excludes zero.

## Predictions (stated before the runs)
No directional prediction for V7f − ACT is made in either part. Expected from the existing records (not a test):
V7f equals the host on MOT17 official ByteTrack (Paper 2 Table 9).

## Reporting
All cells are recorded as they come out (`research/final/V7_ACT_ORIGINAL_UAVDT_RESULT.json`, E60); nothing in V7f or
ACT is changed afterwards; the owner decides whether any part enters a manuscript.
