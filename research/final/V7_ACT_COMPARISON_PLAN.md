# Frozen V7f vs a published adaptive-threshold method (ACT) — plan (written before the runs)

Date: 2026-10-21. Owner instruction (reviewer concern: comparison with a published adaptive-threshold method).
Development data only (KITTI tracking training, non-protected). The frozen V7f code and configuration are not
changed; ACT runs through a new, separate runner (`tools/v7/act_baseline.py`) that writes the same output format
as the frozen runner, so the frozen evaluator `tools/v7/kitti/kitti_eval.py` and `tools/v7/bootstrap.py` are used
unchanged. The result is recorded in every case; the owner decides afterwards whether it enters a manuscript.

## Method compared: ACT
Gwon, D.U., Lee, W.I.: Adaptive Threshold Control Scheme Based on Detection Confidence Distribution for Data
Association in Multi-Object Tracking. Electronics 15(17), 4047 (2026), doi:10.3390/electronics15174047
(cited in Paper 2 as `act2026adaptive`). Implemented exactly as its Algorithm 1, with its published global
parameter set (Sect. 4.1), no tuning:
- pre-filter S_v = {s > tau_L0}; if S_v is empty: tau_high = tau_H0, tau_low = tau_L0;
- else Q1 = 25th percentile of S_v (numpy default linear percentile), N = |S_v|;
  if Q1 > delta_q: tau_high = tau_H0, tau_low = tau_L1 if N > delta_n else tau_L2;
  else: tau_high = tau_H1, tau_low = tau_L0;
- D_high = {score >= tau_high}, D_low = {tau_low < score < tau_high}; detections with score <= tau_low are dropped.
- tau_H0 = 0.6, tau_H1 = 0.3, tau_L0 = 0.1, tau_L1 = 0.2, tau_L2 = 0.15, delta_q = 0.7, delta_n = 100.
- Per frame, on the current frame's scores (as in the paper). Scores are passed unchanged.

Host coupling (the paper defines only the partition):
- ByteTrack (two-stage, the paper's own tracker family): association (high) threshold = tau_high; low group =
  the passed detections below tau_high (all > tau_low); the birth threshold stays the host's own (0.25), so new
  tracks start from the high group as in the paper's pipeline; matching tolerance unchanged (0.8).
- OC-SORT (single threshold, an extension beyond the paper's two trackers): its one threshold = tau_high
  (association = birth, as in the host contract); detections <= tau_low dropped.

## Cells (the four valid KITTI cells of E57/E58; BoT-SORT is not run: KITTI frames not on the machine)
- C1 ByteTrack, RT-DETR-L; C4 the same with halved scores (`t:scale05`) — primary (ACT's tracker family).
- C3 OC-SORT, YOLOv8n; C5 the same with halved scores — secondary (extension of ACT to a single-stage tracker).
Cached detections `outputs/det_cache_kitti_native`, all 21 sequences.

## Metrics and analysis
Official KITTI HOTA (car/pedestrian average) via `tools/v7/kitti/kitti_eval.py`; MOTA, IDF1 secondary.
Paired bootstrap over sequences (10,000 resamples, seed 42): V7f − ACT and ACT − host per cell.
A difference counts only if its 95% interval excludes zero.

## Predictions (stated before the run)
1. Under halved scores (C4, C5), V7f reaches higher HOTA than ACT (ACT's thresholds are absolute scores).
2. No prediction for C1 and C3.

## Reporting
All four cells are recorded as they come out (research/final/V7_ACT_COMPARISON_RESULT.json, E59); nothing in
V7f or in ACT is changed after the run.
