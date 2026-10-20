# RESULTS — canonical index

Rule: the machine-readable file is authoritative; this index only points to
it. Never copy a number here without checking the file. Conflicts are listed
explicitly, never silently reconciled. `outputs/` is git-ignored (local, Mac):
paths below are relative to the repo root on the development Mac.
Evaluator for every row: internal class-agnostic protocol, HOTA TrackEval
12c8791, others motmetrics 1.4.0 (NOT official VisDrone).

## Canonical result sets
| Set | Commit | Status | Authoritative file(s) | Human summary |
|---|---|---|---|---|
| V4 held-out VisDrone2019-MOT-test-dev (E31) | a55b138 code / 9d9ebeb results | HELD-OUT (evaluated once) | `outputs/heldout_v4/pooled_metrics.json`, `outputs/heldout_v4/bootstrap.json` | `research/RESULTS_TESTDEV_V4.md` |
| V4 nested LOSO selection (E29) | fc003bf | DEVELOPMENT (val) | `outputs/opt_v4/v4_selection.json`, `outputs/opt_v4/grid.json` | research/EXPERIMENT_REGISTRY.md E29 |
| V3 selection (E22) | c1e799d | DEVELOPMENT (val), SUPERSEDED | `outputs/opt_v3/selection_report.json`, `response_surface.csv` | E22 |
| Stress / invariance (E20, E23) | c1e799d | DEVELOPMENT (val) | `outputs/stress/` | E20, E23 |
| BoT-SORT tracker transfer on val (V3) | pre-fc003bf | DEVELOPMENT (val) | `outputs/tracker_transfer_val/` | — (NEEDS VERIFICATION: summary not in registry) |
| V5 S1 headroom (E32) | 62111e8 | DEVELOPMENT (val) | `outputs/v5/s1/headroom.json`, `outputs/v5/s1b/headroom.json` | context E32 |
| V5 S2 cue utility (E33) | 62111e8 | DEVELOPMENT (val) | `outputs/v5/s2_cue_utility.json` | context E33 |
| V5 S3 attempts (E34, E35) | 62111e8 | DEVELOPMENT (val), FAILED | `outputs/v5/s3/full/`, `outputs/v5/s3b/full/` | Amendments 5b/5c |
| V5-TF dev validation (E36) | 71faf44 + Amendment 7 | DEVELOPMENT-40, COMPLETE | `outputs/v5tf_dev/` PKLs, `outputs/v5tf_dev/family_choice.json` | F3 selected; F5 did not beat F3 or F5R; D-022 |
| V5-TF constant audit (E39) | Amendment 7 | DEVELOPMENT-40, COMPLETE | `outputs/v5tf_dev/constant_audit.json` | bins/window sensitive E; history/warm-up insensitive A; D-023 |
| V5-TF exact-Otsu family (E41) | 240eba9 + Amendment 8 | DEVELOPMENT-40, COMPLETE | `outputs/v5tf_dev/E41/` | 80/80 PKLs; 15 catastrophic cells; worst-detector relative gain vs V4 +0.69%; no protected data; D-025 |
| V5-TF live/replay parity (E40) | fd44a11 / 50f2a6f | DEVELOPMENT FIDELITY, PASS | `outputs/v5tf_dev/live_replay_parity_v2.json` | exact tracks + controls, 80/80 frames; v1 preserved as harness failure |
| V6-TF development iterations (E43/E44) | Amendment 9 | DEVELOPMENT (val-7 sandbox; V4 in-sample) | `outputs/v6/val7/<system>/<det>/<seq>.pkl` (+ `.official.pkl`) | research/final/EXPERIMENT_LEDGER.md |
| V6-TF development-40 check (E45) | Amendment 9 | DEVELOPMENT (not iterated) | `outputs/v6/dev40/` | EXPERIMENT_LEDGER.md |
| V6-TF live/replay parity (E46) | Amendment 9 | FIDELITY PASS | `outputs/v6/live_replay_parity.json` | 80/80 frames |
| Faster R-CNN, UAVDT, BoT-SORT, confirmation-16 (V6-TF) | — | PROTECTED until universal-acmot-v6-freeze | post-freeze: `outputs/v6/<split>/` | research/final/FINAL_RESULTS.md |
| Official T4 timing | — | none official yet | will be `t4_benchmark*.json` from a T4 run | — |

## Headline held-out numbers (health-checked against pooled_metrics.json)
Tracker: ByteTrack. Dataset: VisDrone2019-MOT-test-dev (17 seq). Status HELD-OUT.
<!-- verify:outputs/heldout_v4/pooled_metrics.json -->
| tracker | system | detector | MOTA | HOTA | IDF1 |
|---|---|---|---:|---:|---:|
| bytetrack | V4_736 | yolov8 | 23.89 | 33.72 | 40.57 |
| bytetrack | V4_736 | rtdetr | 23.60 | 36.33 | 42.56 |
| bytetrack | V4_832 | yolov8 | 26.19 | 35.75 | 43.60 |
| bytetrack | V4_832 | rtdetr | 25.31 | 37.33 | 43.71 |
| bytetrack | shared_static_736 | yolov8 | 21.35 | 29.80 | 34.41 |
| bytetrack | shared_static_736 | rtdetr | 25.67 | 38.82 | 46.58 |
| bytetrack | default | yolov8 | 20.27 | 30.00 | 34.97 |
| bytetrack | default | rtdetr | 8.78 | 37.09 | 42.89 |
<!-- /verify -->
Reading (from RESULTS_TESTDEV_V4.md): YOLOv8n — V4 significantly better than
default and shared static at matched compute; RT-DETR-L — V4 removes the
default's collapse (6→0 catastrophic sequences) but is significantly below
shared static on HOTA (−2.49) and IDF1 (−4.02). Bootstrap: 10,000 resamples,
seed 42.

## Known conflicts / caveats
- Two evaluation protocols are kept strictly apart (never mixed in one
  comparison): INTERNAL class-agnostic (`tools/eval_local.py`: GT classes
  {1,4,5,6,9}, score==1, occlusion<2, truncation<2; no ignored-region
  handling) and OFFICIAL-COMPATIBLE VisDrone Task-4b port
  (`tools/v6/eval_official.py`: class-aware, ignored/others regions dropped,
  no occlusion filter). COCO detectors have no "van" class → van GT is all
  FN under the official protocol.
- E36 selected F3 over F5, but F3 has 17 catastrophic sequence-detector cells
  versus V4's 3 and worst-detector relative ½(HOTA+IDF1) gain −0.339%.
  This is development evidence, not protected confirmation; report honestly.
- E39's sensitive OTSU_BINS and Otsu-window findings apply to recorded F3 only.
  E41 is the predeclared training-free revision that removes both dependencies;
  the V5-TF policy is now locked to E41 pending the fixed T4 fidelity gate.
- UAVDT "never evaluated by any system" (Amendment 5) vs legacy branch
  `origin/freeze/final-after-uavdt-2026-09-12` (legacy AC-MOT UAVDT run):
  both true only if "system" means Universal AC-MOT. See DATASETS_AND_SPLITS.md.
- E32 headroom: Amendment 5a quotes "0.4–2.3" per-sequence; `s1b/headroom.json`
  gives 0.44–2.25 (sensitivity/assoc/τ/resolution) — consistent after rounding;
  which of s1 vs s1b the amendment used: NEEDS VERIFICATION.

## V6-TF, V7f, compute lines and Paper 1 result sets (added 2026-10-20)
Evaluators differ per set (stated); never pool across sets.
| Set | Commit | Status | Authoritative file(s) | Human summary |
|---|---|---|---|---|
| V6-TF development and post-freeze (E42–E54) | 2cff95f | DEVELOPMENT / POST-FREEZE | research/final/FINAL_RESULTS.md and the files it names | research/final/FINAL_SUMMARY.md |
| V7 development matrix | 488df9a | DEVELOPMENT (contaminated) | `research/final/V7_DEV_RESULTS.json` | `research/final/V7_STATISTICS.md` |
| V7 main table (MOT17 hosts, paper vs reproduction vs + V7f) | 488df9a | DEVELOPMENT + EXTERNAL | `research/final/V7_MAIN_RESULTS.json` | `research/final/V7_MAIN_RESULTS.md` |
| V7 predeclared externals (PD-SORT, Hybrid-SORT) | 488df9a | POST-FREEZE EXTERNAL | `research/final/V7_EXTERNAL_RESULTS.json` | `research/final/V7_EXTERNAL_TRANSFER.md` |
| V7 recent externals (C-TWiX, TOPICTrack, TrackTrack) | 488df9a | POST-FREEZE EXTERNAL | `research/final/V7_RECENT_EXTERNAL_RESULTS.json` | `research/final/V7_RECENT_EXTERNAL_SYSTEMS.md`, `research/final/V7_RECENT_EXTERNAL_FAILURES.md` |
| V7 score-shift bootstrap | 488df9a | DEVELOPMENT | `research/final/paper2_calib_boot/calib_boot.json` | PAPERS.md Paper 2 |
| V7f VisDrone val-7 | 488df9a | DEVELOPMENT (post-freeze run) | `research/final/aerial_v7f_val/bootstrap_val7.json` | `research/final/aerial_v7f_val/official_val7.txt` |
| V7f runtime | 488df9a | MEASURED | `research/final/V7_REALTIME_yolov8n.json` | `research/final/V7_REALTIME.md` |
| SCI + V7f, G1 | 5a8502f, 751c602 | DEVELOPMENT (val-7) | research/final/sci_v7f/ | `research/final/SCI_V7F_RESULTS.md` |
| G2 gate | g2-s3-1 | DEVELOPMENT (val-7) | research/final/g2/ | `research/final/G2_EXPERIMENT_LEDGER.md` |
| Paper 1 VisDrone (second val read) | 0af0066 | EVALUATION (second read) | `research/acmot_paper_v2/SECOND_VAL_READ_V3_RESULT.json`, `research/acmot_paper_v2/BASELINE_SYSTEMS_RESULT.json`, `research/acmot_paper_v2/BOOTSTRAP_V3_RESULT.json` | archive PAPER_READY_RESULTS.md |
| Paper 1 UAVDT transfer | 280b4a2 | TRANSFER | `research/acmot_paper_v2/UAVDT_TRANSFER_RESULT.json`, `research/acmot_paper_v2/UAVDT_BOOTSTRAP_V3_RESULT.json` | same |
| Paper 1 legacy stages | a6c1fa4 / b591122 | HISTORICAL | research/paper_split/evidence/legacy/ | evidence README |

## Conflict and discrepancy register (append-only; never resolved silently)
| ID | Records in conflict | Evidence | Status |
|---|---|---|---|
| CF-01 | HARD_CONSTRAINTS C0 named V6-TF as FINAL TARGET while V7f (later, frozen) backed Paper 2 | Amendment 10, D-032 | RESOLVED by owner decision 2026-10-20 |
| CF-02 | Paper2_V11 KITTI caption: "the unmodified tracker gives no valid output on one sequence" vs ledger E19: Cholesky error when fed the layer's output | `research/final/V7_EXPERIMENT_LEDGER.md` E19 | OPEN (fix in Paper2_V12) |
| CF-03 | Paper2_V11 reports 3 KITTI cells; the canonical matrix has 6 | `research/final/V7_STATISTICS.md` | OPEN (fix in Paper2_V12) |
| CF-04 | Paper2_V11 "external" = PD-SORT, Hybrid-SORT; the predeclared recent externals (negative/neutral) are omitted | `research/final/V7_RECENT_EXTERNAL_RESULTS.json` | OPEN (owner decision for Paper2_V12) |
| CF-05 | `research/final/aerial_v7f_val/README.md` run table says no metric computed (run 36910783384) while `STATUS.txt` = OK with metrics from later runs 36994862846 / 36995662755 (commits 852071e, 741813a) | folder files | EXPLAINED (later successful runs); README run table not yet updated |
| CF-06 | DATASETS_AND_SPLITS.md original text called confirmation-16 and UAVDT untouched; later evaluated (E48, E50, P1-UAVDT) | EXPERIMENT_REGISTRY.md | RECORDED as dated status update |
| CF-07 | Paper 1 val-7 = evaluation set, read twice; V12 text does not state the second read | archive README disclosures | OPEN (Paper 1 revision) |
