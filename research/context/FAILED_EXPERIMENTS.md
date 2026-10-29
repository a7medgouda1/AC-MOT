# FAILED EXPERIMENTS — negative results are project knowledge

Retry = allowed only if the listed precondition changes AND the retry is
declared in the protocol before running.

| ID | Version / commit | Hypothesis | Result (evidence) | Why it failed | Lesson | Retry? |
|---|---|---|---|---|---|---|
| FX-01 | V1 (pre-freeze, Colab) | online percentile normalisation alone is enough | E01: RT-DETR MOTA −112 | equal percentage ≠ equal count → candidate explosion | need a detector-relative gate | no |
| FX-02 | V2b | density budget + Top-K | E02: HOTA/recall destroyed | budget applied twice | avoid count budgets | no |
| FX-03 | V2c A/B/C | additive-offset density thresholds | E03: each variant fails a different sequence | additive offsets over-suppress | structural, not tunable | no |
| FX-04 | V2d | reliability-scaled budget / birth / SCI feedback | E07: RT-0268 MOTA −91.5 | budget floor 12, births in dead zone | — | no |
| FX-05 | V2 diagnostics | temporal persistence separates FP clutter | E10, E14, E17: persistence high for clutter (0.92–0.96), AUC 0.53–0.67 | scene property, not failure signal | Cue: temporal persistence rejected | only with a new signal definition |
| FX-06 | V2 diagnostics | per-track continuity separates false tracks | E09: gating cuts 24–30% TP | not a clean separator | — | no |
| FX-07 | V2f | closed-loop trust controller (r* 0.80/0.85/0.90) | E13: 2 tracks/frame on RT-0268; YOLO HOTA 33.5→27 | reliability conflates hard scene with false candidates (windup) | avoid integrating a reliability error | no |
| FX-08 | V1 selection | J2 = max-min absolute ½(HOTA+IDF1) | E18 / Amendment 1: always attained by YOLOv8n | unnormalised max-min degenerates when capacities differ | use relative gains (J4) + catastrophic-cell rule | no |
| FX-09 | V1 | histogram normaliser + ratio gate is robust | E20: YOLO HOTA 32.1→25.7 at T=0.5; RT MOTA 24.1→7.9 at T=2 | not invariant to temperature | require exact Platt invariance | no |
| FX-10 | legacy SCI in V3 | SCI (crowd/tiny/edges/darkness/blur) predicts when to spend compute | E24–E26: ≤ RANDOM allocation, sign flips | handcrafted absolute thresholds, no generalisation | never restore legacy SCI blindly | only as online-normalised re-definitions (C4) |
| FX-11 | shared-static baseline | a static raw threshold is enough | E19 competitive, but E20: 0 tracks under score ×0.5 | depends on raw score scale | baseline fragility, not our method | n/a |
| FX-12 | V5 S3 attempt 1 | MOTA-aligned learned stump controller | E34: ½(HOTA+IDF1) −2.4/−2.6 vs V4 | objective mismatch (MOTA cost vs HOTA/IDF1 criterion) | align cost with adoption metric | no (val folds exhausted) |
| FX-13 | V5 S3 attempt 2 | identity-aligned learned controller | E35: YOLO −2.26 | overfitting by scarcity (7 sequences, ~190 windows) | learned mapping does not generalise; motivates training-free (D-015) | no on val |
| FX-14 | V5 S3 | adapt gate τ by a cue | 4 different cues across folds | unstable cue mapping | τ not adapted | no |
| FX-15 | V4 on test-dev (E31) | V4 ≥ shared static at matched compute (H2) | RT-DETR −2.49 HOTA, −4.02 IDF1 (sig.) | recall-limited: τ, s at catastrophe-constraint edge | V4's VisDrone constants not universally good → category E | not for V4 (frozen) |
| FX-16 | V5-TF F4 | z-gate with online τ adds something to F1 | identical to F1 by construction (71faf44) | redundancy | — | no |
| FX-17 | V5-TF F5, E36 | online-normalised object-size tertiles improve resolution allocation | F5: 18 catastrophic cells, worst-detector relative ½(HOTA+IDF1) −2.646%, versus F3 17/−0.339% and random F5R 17/−1.683%; F5 cost stayed under budget | tested size state did not beat random allocation or fixed-resolution F3 | scene-aware R-res adds insufficient benefit under the tested training-free rule | only as a new family declared before another development-40 run |
| FX-18 | V5-TF E41 (locked, never frozen) | exact current-frame 3-class Otsu bands are a sufficient training-free candidate control | dev-40: 15 catastrophic cells, precision 58/60, FP ≈ 4× V4, MOTA 12.7/19.1 vs 25.1/26.3; val-7: 6 cat | current-frame thresholds (also a C3 issue), 19% duplicate boxes from native suppression, 3-class Otsu boundary pulled down by the volume of background emissions, broad extension band sustaining ghosts | relative (rank/Otsu) thresholds need a precision safeguard; fixed in V6-TF by dedup + nested Otsu | no (superseded by V6-TF) |
| FX-19 | V6 dev X4 | an extension band as wide as the detector's own frame-to-frame logit jitter keeps real tracks but not ghosts | val-7: 3 cat, between X3 and X3b on every axis | the failures come from the primary band, not the extension band | fix the primary boundary first (H6) | no |

Gate ablation note (not a failure of the method): V4 without the gate
collapses like V1 (test-dev RT-DETR 12 catastrophic sequences, E31).

## V6-TF, V7, compute lines and Paper 1 (added 2026-10-20; evidence files named per row)
| ID | Version / commit | Hypothesis | Result (evidence) | Why it failed | Lesson | Retry? |
|---|---|---|---|---|---|---|
| FX-20 | V6-TF 2cff95f | a layer that always applies the bands helps any tracker | SparseTrack −4.15, BoostTrack −5.89 HOTA (`research/final/EXTERNAL_PAPER_TRANSFER.md`, D-029) | duplicate removal deleted occluded people; thresholds stricter than strong hosts | decide from the scores whether to act (→ V7 clean mode) | no (V6-TF frozen) |
| FX-21 | V7 E4 | scene-evidence duplicate rule `ctx` | rejected (`research/final/V7_EXPERIMENT_LEDGER.md` E4) | no gain over the track-context rule | keep crowd-safe track rule | no |
| FX-22 | V7 E20 | host-relative noisy primary band | KITTI YOLOv8n +1.4 HOTA but VisDrone RT-DETR 26.9 vs 14.9 boxes/frame (ledger E20) | uncontrolled false tracks on a noisy aerial stream | noisy band must stay self-calibrated | no |
| FX-23 | V7 variants | no candidates at frame 1; rescue below a two-stage low stage; rank scores in clean frames | −0.3 to −0.5 HOTA; FP +700–1000; ByteTrack −0.2 / −1.6 (`research/final/V7_ABLATION.md`) | each removed host-native information | cold = host; rescue only for single-stage; raw scores when clean | no |
| FX-24 | V7f 488df9a (known regression) | V7f never harms a two-stage host | KITTI YOLOv8n ByteTrack MOTA −1.87, BoT-SORT −2.43 (CI < 0) (`research/final/V7_STATISTICS.md`) | noisy-regime birth restriction on a weak detector | report it; do not tune a frozen policy | only as a new version |
| FX-25 | V7f post-freeze | frozen V7f improves recent 2025 trackers | C-TWiX KITTIMOT car −1.52 HOTA (CI < 0); TrackTrack DanceTrack −0.012 (CI < 0); C-TWiX MOT17/DanceTrack n.s. negative (`research/final/V7_RECENT_EXTERNAL_RESULTS.json`) | strong coordinate/ReID trackers on clean streams; single-sequence collapses (KITTIMOT 0014, DanceTrack 0004) | V7f gains are limited to single-stage or mismatched hosts | analysis only |
| FX-26 | C1 5a8502f | historical SCI resolution rule adds value on top of V7f | SCI + V7f − V7f only −0.17 HOTA [−0.56, +0.21] (`research/final/SCI_V7F_RESULTS.md`) | no cue predicts per-segment compute benefit across detectors | constant compute point (G1) | only with a new pre-registered cue |
| FX-27 | G2 | compute adaptation (resolution, call rate, crops) has headroom at matched compute | all spaces fail the GT-oracle gate (`research/final/G2_EXPERIMENT_LEDGER.md`) | headroom too small or not scene-predictable | static compute + V7f | no |
| FX-28 | P1 Phase A | an adaptive policy beats the calibration-tuned matched-static point | null in 5 stages (`research/acmot_paper_v2/FINAL_REPORT.md` §1) | the best fixed point already captures most gain | objective redefined vs the host baseline r1536_n70 (Phase B) | recorded as a design pivot |
| FX-29 | P1 v3 | controller timing adds value beyond its action mix | shuffled same-distribution control not worse (`research/acmot_paper_v2/controller_search/SHUFFLED_CONTROL_RESULT.json`) | the action mix explains the gain | do not claim causal timing value | report in Paper 1 revision |
| FX-30 | TOPICTrack reproduction | faithful CPU reproduction within 1.0 HOTA | 67.538 vs 69.6 (`research/final/V7_RECENT_EXTERNAL_FAILURES.md`) | not isolated; the run used CPU fp32 instead of the authors' CUDA fp16 | exclude from claims | needs GPU fp16 run |
