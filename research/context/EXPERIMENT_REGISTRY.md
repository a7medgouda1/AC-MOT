# EXPERIMENT REGISTRY — index

Authoritative detail:
- E01–E31: `research/EXPERIMENT_REGISTRY.md` (do not duplicate; append there
  only for V4-era corrections).
- E32+: THIS file is authoritative (V5 / V5-TF era).
Evaluation protocol for all rows unless stated: internal class-agnostic
protocol (GT classes {1,4,5,6,9}, score==1, trunc<2, occ<2, IoU 0.5) —
NOT official VisDrone. HOTA = TrackEval 12c8791; others = motmetrics 1.4.0.

## E01–E31 by theme (summary; see authoritative file)
| IDs | Theme | Version | Outcome |
|---|---|---|---|
| E01–E03 | candidate explosion / density budgets | V1, V2b, V2c | FAIL (see FAILED_EXPERIMENTS.md) |
| E04–E05 | evaluator and cache-replay fidelity | infra | PASS (exact) |
| E06–E14 | reliability, persistence, continuity, closed-loop trust | V2d–V2f | mostly FAIL; leader-relative score identified |
| E15–E17 | leader-relative gate; signal audit | V2g/V1g | gate is the core fix; temporal persistence rejected |
| E18–E19 | V1 selection grid + baselines | V1 | V1 frozen; shared-static competitive at 832 |
| E20–E23 | score-calibration stress; V3 invariant design | V3 | V3 exactly Platt-invariant |
| E24–E26 | SCI / cue audits at matched compute | V3→V4 | legacy SCI ≤ random → removed |
| E27–E30 | NMS audit, sensitivity, V4 selection, checks | V4 | V4 frozen |
| E31 | held-out VisDrone test-dev (once) | V4 | RESULTS_TESTDEV_V4.md |

## E32+ (V5 / V5-TF)
| ID | Commit | Hypothesis | Config | Data | Result | Status |
|---|---|---|---|---|---|---|
| E32 | 62111e8 | S1: which control targets have adaptation headroom | fixed-value runs around V4 at 736 (`tools/v5_s1_headroom.py`) | VisDrone2019-MOT-val × {YOLOv8n, RT-DETR-L} | headroom for gate τ, association offset, resolution, sensitivity (per-sequence ≈0.4–2.3 MOTA pts); retention ≈0 (`outputs/v5/s1/headroom.json`, `outputs/v5/s1b/headroom.json`) | DEVELOPMENT (val) |
| E33 | 62111e8 | S2: which cues predict headroom | single-cue LOSO + permutation null (`tools/v5_s2_cues.py`) | val-7 × 2 | candidates det_gap, det_count, trk_survival, trk_match, img_motion, img_motion_resp; edges/brightness/blur negative (`outputs/v5/s2_cue_utility.json`) | DEVELOPMENT (val, diagnostic) |
| E34 | 62111e8 | S3 attempt 1: learned stump controller | cost FP+FN+IDSW, nested LOSO (`outputs/v5/s3/full/`) | val-7 × 2 | ½(HOTA+IDF1) vs V4: YOLO −2.42 [−4.86,−0.61], RT-DETR −2.64 [−8.30,+0.57] (Amendment 5b text) | FAILED |
| E35 | 62111e8 | S3 attempt 2: identity-aligned cost | (FP+FN)+(IDFP+IDFN) (`outputs/v5/s3b/full/`) | val-7 × 2 | YOLO −2.26 [−4.77,−0.38]; RT-DETR −0.60 [−2.15,+1.10] (Amendment 5c text) | FAILED |
| E36 | 71faf44 + Amendment 7 | V5-TF families F1, F2, F3, F5 (+R-res) and control F5R vs references (static, shared-static, V4) at budget 736; choice among F3/F5 | `tools/v5tf_dev.py run/report` | VisDrone2019-MOT-train development-40 × {YOLOv8n, RT-DETR-L}, ByteTrack | F3 selected: catastrophic cells 17 vs F5 18; worst-detector relative ½(HOTA+IDF1) vs V4 −0.339% vs −2.646%; F5 pixel cost 0.954/0.952. F5R: 17 cells, −1.683%, cost 0.996/0.996. F5 did not beat F3 or random control. `outputs/v5tf_dev/family_choice.json`, per-sequence PKLs | DONE (development; no protected data) |
| E37 | — | Discovery: S1/S2/S3 on development-40 (research upper bound D, headroom, cue stability) | `tools/v5_train.py s1/s2/s3` (NOT `final`) | development-40 | — | PLANNED, optional |
| E39 | Amendment 7 | Constant audit on the chosen family (OTSU_BINS, Otsu window, RobustHistory window, warm-up; E28 criterion) | `tools/v5tf_dev.py sens` | development-40 × 2 detectors | OTSU_BINS and Otsu window sensitive E; RobustHistory window and warm-up insensitive A. Defaults kept; no best-value selection. `outputs/v5tf_dev/constant_audit.json` | DONE — category-E values block freeze under C5 |
| E38 | feff14f | Amendment 5f T4 fidelity gate | `tools/fidelity_gate.py`, `notebooks/Colab_T4_gate_and_benchmark.ipynb` | 4 predeclared dev sequences | — | PENDING (needs T4 session) |
| E40 | fd44a11, 50f2a6f | Live `UniversalACMOT` F3 motion path equals cached-cue replay | first 2 declared development sequences × first 20 frames × 2 detectors; no GT/quality metric | VisDrone2019-MOT-train development-40 | v1 interleaved trackers and exposed only Ultralytics' process-global ID counter offset; preserved. Corrected v2 runs paths sequentially from the same ID state: tracks and selected audit controls exactly equal on 80/80 frames. | PASS (`outputs/v5tf_dev/live_replay_parity_v2.json`) |
| E41 | 240eba9 / Amendment 8 | Predeclared exact 3-class Otsu candidate bands; removes fixed histogram bins and fixed Otsu memory | `PYTHONPATH=. .venv/bin/python tools/v5tf_dev.py run` | development-40 × 2 detectors | 80/80 PKLs; 15 catastrophic cells; worst-detector relative gain vs V4 +0.69%; no parameter search; E41 improves the recorded F3 comparison but does not alter the prior F3-vs-F5 selectable choice | DONE (development; no protected data) |

Numbers in E34/E35 are quoted from the committed protocol text
(research/OPTIMIZATION_PROTOCOL.md Amendments 5b/5c); they were not re-derived
from `outputs/v5/s3*/` during the context build → re-derive before citing in a paper.

## V6-TF era (Amendment 9) — authoritative detail: research/final/EXPERIMENT_LEDGER.md
| ID | Commit / protocol | Question | Command | Data | Result | Status |
|---|---|---|---|---|---|---|
| E42 | Amendment 9 | Why does E41 fail? (D1–D6: candidate inflation, duplicates, ghost births, extension band, oracle threshold) | `tools/v6/det_audit.py`, ledger scripts | development-40 + val-7 (development) | primaries 2–3× GT in catastrophic cells; 19% duplicate boxes; no birth-time feature separates ghost births (AUC 0.43–0.58) | DONE |
| E43 | Amendment 9 | V6 development iterations X1–X5j | `PYTHONPATH=. .venv/bin/python tools/v6/dev.py run <sys>` | val-7 × 2 detectors | X5: 0 cat; 18.6/34.3/38.6 · 25.0/41.6/48.1 (MOTA/HOTA/IDF1) vs V4 17.5/33.2/36.6 · 21.5/39.0/42.4 | DONE → X5 selected (D-027) |
| E44 | Amendment 9 | X5 robustness pass (Platt, monotone, emission floor, memory constants, ablations) | `tools/v6/dev.py run "X5@..."` | val-7 | exact Platt invariance; memory constants insensitive (A); non-affine monotone and emission floor sensitive (limitations) | DONE |
| E45 | Amendment 9 | development-40 robustness check + ablations (not iterated on) | `V6_SPLIT=dev40 tools/v6/dev.py run ...` | development-40 | X5 2 cat vs V4 3 / E41 15; 25.5/35.8/43.5 · 29.6/39.9/47.7 vs V4 25.1/35.2/42.2 · 26.3/38.4/44.4 | DONE |
| E46 | Amendment 9 | live == replay parity of V6-TF (real detector + image cues) | `tools/v6/live_replay_parity.py` | 2 val seq × 20 frames × 2 det, no GT | PASS 80/80 frames | DONE |
| E47 | Amendment 9 | official-compatible VisDrone evaluation (class-aware, ignored regions) of development runs | `tools/v6/dev.py official <sys>` | val-7 | X5 4 cat vs V4 5; 10.7/30.4/32.4 · 10.9/35.0/37.7 vs V4 10.4/29.6/30.7 · 10.3/32.9/33.3 | DONE (development) |
| E48 | 2cff95f (frozen) / TRANSFER_LOCK_V6TF | confirmation-16, ONE-WAY | `V6_SPLIT=conf16 tools/v6/dev.py run V6TF V4 shared_static static_default E41`; `tools/v6/confirm_report.py` | confirmation-16 × YOLOv8n, RT-DETR-L; ByteTrack | internal: V6-TF 1 cat vs V4 3 / shared 3 / default 6 / E41 9. YOLO 20.2/33.6/37.9 vs V4 20.6/34.1/38.1 (n.s.); RT 26.6/39.7/46.0 vs 24.2/39.4/44.4 (n.s. internal). Official: RT HOTA +2.78 [0.67, 5.37], MOTA +4.62 [0.87, 9.63] vs V4. vs shared-static YOLO HOTA +3.7, IDF1 +7.7 (sig.) | DONE (outputs/v6/conf16/{pooled_metrics,bootstrap}.json) |
| E49 | frozen | test-dev POST-HOC | `V6_SPLIT=testdev tools/v6/dev.py run ...` | test-dev 17 seq | V4 reproduces E31 exactly; V6-TF 0 cat; YOLO ≈ V4 (n.s.); RT MOTA +3.98 [0.01, 8.69]; vs shared-static RT HOTA −2.41 (sig.), YOLO HOTA +3.9 (sig.) | DONE (post-hoc) |
| E50 | frozen | UAVDT dataset transfer | `V6_SPLIT=uavdt tools/v6/dev.py run ...` | UAVDT test 20 seq, internal protocol | V6-TF 12 cat = V4 12, shared-static 6; YOLO HOTA −0.48 / IDF1 −0.99 vs V4 (sig., small); RT n.s.; vs shared-static YOLO HOTA +4.4 (sig.) | DONE |
| E51 | frozen | tracker transfer BoT-SORT | `V6_SPLIT=conf16 tools/v6/dev.py run "V6TF@trk:botsort" ...` | confirmation-16 × 2 det | V6-TF 1 cat vs V4 2 / shared 3 / default 8; RT official HOTA +3.09 [0.41, 6.08], MOTA +5.56 [1.09, 11.36] vs V4; YOLO n.s. | DONE |
| E52 | frozen | detector transfer Faster R-CNN R50-FPN v2 | `V6_DETS=fasterrcnn V6_SPLIT=val7 tools/v6/dev.py run ...` (+ test-dev, UAVDT via tools/v6/after_frcnn_caches.sh) | val-7 (+ test-dev post-hoc, UAVDT) | val-7: V6-TF 0 cat; official HOTA +2.52 [0.25, 5.02], IDF1 +4.08 [1.20, 7.09] vs V4; MOTA +16.9 vs shared static. test-dev (post-hoc): official HOTA +1.46 [0.53, 2.55], IDF1 +1.85, MOTA +1.66 vs V4; UAVDT: ≈ V4 | DONE |
| E53 | frozen / external | BoostTrack (MVA 2024) faithful execution + frozen V6-TF | `tools/v6/external/boosttrack_v6.py` | MOT17 val-half (owner's Drive, split verified) | execution 68.49/75.50/81.41 (authors 68.37/75.56/81.35); + V6-TF 62.61/66.64/75.19; ΔHOTA −5.89 [−7.76, −2.87], ΔIDS −38 [−81, −1] | DONE (negative transfer) |
| E54 | frozen / external | SparseTrack (IEEE TCSVT 2025, headline) faithful execution + frozen V6-TF on identical detections | `tools/v6/external/sparsetrack_v6.py` | MOT17 val-half | execution 68.88/77.85/81.97 (paper 69.2/76.8/81.4); + V6-TF 64.72/71.71/77.49; ΔHOTA −4.15 [−5.54, −1.66], ΔMOTA −6.14, ΔIDF1 −4.49, ΔFP −1630, ΔFN +4955; diagnostic: dedup causes ~62% of the loss | DONE (negative transfer) |


## V7 era, compute lines, Paper 1 line (added 2026-10-20; index only — detail in the ledger named per block)
Reproducibility labels (definitions in REPRODUCIBILITY.md): REPRODUCIBLE · PARTIALLY REPRODUCIBLE ·
NOT YET REPRODUCIBLE · HISTORICAL / ARTIFACTS MISSING. IDs are stable; never renumber.
Protocols are never mixed across rows: MOT17 = TrackEval on MOT17 val-half with published detections;
KITTI = official KITTI HOTA averaged over car and pedestrian; VisDrone "internal" = class-agnostic
protocol above; VisDrone "official" = class-aware official-compatible port (`tools/v6/eval_official.py`).

### V7 development (ledger `research/final/V7_EXPERIMENT_LEDGER.md`; ablation `research/final/V7_ABLATION.md`)
| ID | Version | Question | Data | Command | Result (headline) | Status | Repro |
|---|---|---|---|---|---|---|---|
| V7-E0 | infra | runner identities (replay = official output) | MOT17 val-half, KITTI | `tools/v7/external/*_v7.py --system BASELINE` | identical outputs | ACCEPTED | REPRODUCIBLE (assets release v7-dev-assets-1) |
| V7-E1–E5 | V7a | track-context duplicates, per-frame ρ regime, duplicate scope/memory | MOT17 (SparseTrack), val-7 | `tools/v7/external/sparsetrack_v7.py`, `tools/v7/dev.py run` | crowd-safe duplicates needed; `ctx` rule rejected (E4) | DONE | PARTIALLY (val-7 needs VisDrone caches) |
| V7-E6 | V6EMU | one-factor ablations from V6 emulation | VisDrone val-7 × YOLOv8n/RT-DETR-L | `tools/v7/dev.py run` | per-factor effects | DONE | PARTIALLY |
| V7-E7–E10 | V7b–V7d | noisy-only duplicates, auto scores, clean = min(host, t2), motion only in noisy frames | MOT17 hosts, val-7 | `tools/v7/dev.py`, external runners | SparseTrack 64.72 → 68.93, BoostTrack 62.61 → 68.37 | DONE | PARTIALLY |
| V7-E12-LF, STRESS-LF | V7c/d | label-free ID churn; calibration/floor stress without labels | val-7, KITTI | ledger cloud C1 | diagnostic | DIAGNOSTIC | PARTIALLY |
| V7-E15 | V7c/d | identity/floor stress on MOT17 hosts | MOT17 | `tools/v7/external/mot17_bytetrack_v7.py` | per-floor table | DONE | REPRODUCIBLE |
| V7-E16 | V7f part | regime from the whole stream (rho_frames 0) | MOT17 | same | ByteTrack (0.1) 67.561 → 67.702; OC-SORT (0.1) 65.697 → 66.071 | ADOPTED | REPRODUCIBLE |
| V7-E17 | V7f part | track-consistent rescue | MOT17, KITTI YOLOv8n | same + `tools/v7/dev.py` | OC-SORT (0.01) 66.405 → 66.619; KITTI YOLOv8n OC 41.14 → 44.15 | ADOPTED | REPRODUCIBLE |
| V7-E18 | V7f | background (interpretability) check | MOT17 | same | OC-SORT floor 0.01 67.041 (+0.61 vs host) | ADOPTED = V7f | REPRODUCIBLE |
| V7-STRESS-L | V7f | labelled score transforms (pow3, scale05, temp2, temp05) | MOT17, floor 0.01 | `tools/v7/ci/calib_boot.sh` | 7 of 14 conditions significantly better, 0 worse (`research/final/paper2_calib_boot/calib_boot.json`) | DONE | REPRODUCIBLE (GitHub Actions workflow paper2_calib_boot.yml) |
| V7-E19 | V7d/f | motion rule vs CMC on KITTI (YOLOv8n) | KITTI training 21 seq (BoT-SORT 20: seq 0020 Cholesky error with layer-filtered input) | `V7_SPLIT=kitti tools/v7/dev.py track …`, `tools/v7/kitti/kitti_eval.py` | effects ≤ 0.12 HOTA; motion kept noisy-only | DONE | PARTIALLY (KITTI frames via remotezip) |
| V7-E20 | rejected | host-relative noisy band | KITTI YOLOv8n, VisDrone RT-DETR label-free | ledger | +1.4 HOTA but uncontrolled boxes (26.9 vs 14.9 per frame) | REJECTED | PARTIALLY |
| V7-FREEZE | V7f | freeze + statistics + external predeclaration | — | `tools/v7/freeze.py V7f` | tag universal-acmot-v7-freeze → 488df9a; `research/V7_POLICY_LOCK.json` | FROZEN | REPRODUCIBLE |

### V7f post-freeze evaluations (frozen V7f, lock checked)
| ID | Question | Host · data | Command / workflow | Result | Status | Repro |
|---|---|---|---|---|---|---|
| V7-POST-ST | SparseTrack + V7f on verified MOT17 frames | SparseTrack · MOT17 val-half | `.github/workflows/sparsetrack_v7f.yml` → `tools/v7/ci/sparsetrack_v7f.sh`; record `research/final/sparsetrack_v7f/` | 68.876 → 68.931 HOTA, +0.055 [−0.011, +0.254] | DONE | REPRODUCIBLE |
| V7-POST-PD | predeclared external PD-SORT | PD-SORT · MOT17 val-half (released detections) | `tools/v7/external/pdsort_v7.py`, `tools/v7/mot17_eval_v7.py --boot` | HOTA 68.011 → 68.624, +0.61 [+0.27, +1.65]; MOTA +1.13; IDF1 +0.82; 7/7 | DONE | REPRODUCIBLE |
| V7-POST-HS | predeclared external Hybrid-SORT | Hybrid-SORT · MOT17 val-half | `tools/v7/external/hybridsort_v7.py` (Python 3.11 venv) | identical output; reproduction CLOSE 66.698 vs 67.1 | DONE | REPRODUCIBLE |
| V7-POST-CTW | recent external C-TWiX (Pattern Recognition 2025) | C-TWiX · MOT17 val-half, KITTIMOT val, DanceTrack val | `.github/workflows/recent_ctwix.yml` → `tools/v7/recent/ctwix_run.sh`; `research/final/recent/ctwix/` | MOT17 −0.05 HOTA [−0.46, +0.40]; KITTIMOT car −1.52 [−4.05, −0.13]; ped −0.10 [−2.16, +0.03]; DanceTrack −1.00 [−2.62, +0.65] | DONE (negative / neutral) | REPRODUCIBLE |
| V7-POST-TOP | recent external TOPICTrack (IEEE TIP 2025) | TOPICTrack · MOT17 val-half | `.github/workflows/recent_topictrack.yml`; `research/final/recent/topictrack/` | reproduction FAILED (67.538 vs 69.6); exploratory V7f arm −0.016 HOTA (post) | EXCLUDED from claims | REPRODUCIBLE (as a failed reproduction) |
| V7-POST-TT | recent external TrackTrack (CVPR 2025) | TrackTrack · DanceTrack val | `.github/workflows/recent_tracktrack*.yml`; `research/final/recent/tracktrack/` | reproduction CLOSE; −0.012 HOTA [−0.032, −0.001], 0/21/4 W/T/L | DONE (tiny negative) | REPRODUCIBLE |
| V7-POST-VD | frozen V7f on VisDrone val-7 (development split) | ByteTrack · YOLOv8n, RT-DETR-L | `tools/v7/ci/aerial_v7f_val.sh` (needs own VisDrone val zip); `research/final/aerial_v7f_val/` | internal HOTA YOLOv8n +2.17 [+1.20, +3.58]; official-compatible: catastrophic cells 7 → 4 | DONE (development evidence) | PARTIALLY (dataset zip not public via script) |
| V7-POST-RT | runtime | ByteTrack · KITTI 0001/0009/0019, live YOLOv8n, 4-vCPU Xeon | `tools/v7/benchmark.py --weights yolov8n.pt --seqs 0001 0009 0019` | layer 2.95 ms mean / 4.39 ms P95; pipeline 57.85 → 60.44 ms | DONE | REPRODUCIBLE |

### Compute lines on frozen V7f (ledgers `research/final/SCI_V7F_EXPERIMENT_LEDGER.md`, `research/final/G2_EXPERIMENT_LEDGER.md`)
| ID | Question | Data | Command | Result | Status | Repro |
|---|---|---|---|---|---|---|
| SCI-E1 (E-SCI-1) | pre-registered historical SCI + V7f (C1 = 5a8502f) | VisDrone val-7, ByteTrack, YOLOv8n/RT-DETR-L | `tools/sci_v7/dev.py run`; `research/final/sci_v7f/C1_5a8502f/` | SCI + V7f − V7f only −0.17 HOTA [−0.56, +0.21]; not adopted | DONE (negative) | PARTIALLY |
| SCI-D1 | GT-oracle headroom | val-7 | `tools/sci_v7/oracle.py` | oracle at matched compute +0.47 [+0.005, +0.97] | DONE | PARTIALLY |
| SCI-D2–D4, P-GSCI-1 | cue audit 640/736/832; resolution sweep 512–960 | val-7 | `tools/sci_v7/cue_audit.py`, `tools/sci_v7/sweep_cache.py` | 13 causal cues, none passes the pre-registered rule | DONE (negative) | PARTIALLY |
| G1-FREEZE | constant compute + V7f | — | tag general-acmot-g1-freeze → 751c602; `research/GENERAL_ACMOT_G1_LOCK.json` | development candidate | FROZEN (candidate) | REPRODUCIBLE |
| G1-T-OCSORT / T-RETINANET / T-BOTSORT | G1 transfer to hosts and an unseen detector | val-7 | `research/final/sci_v7f/G1_transfer*/`; lock `research/TRANSFER_LOCK_RETINANET_G1.json` | see SCI ledger §4 | DONE | PARTIALLY |
| G2-S1/S2/S3, G2-REGIME, P-GSCI-2 | GT-oracle gate per compute space | val-7 | `tools/g2/dev.py`, `tools/g2/oracle.py`; `research/final/g2/` | all spaces fail the gate → static compute + V7f | DONE (negative) | PARTIALLY |

### Paper 1 line (AC-MOT v3 operating-point controller; archive `research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/`)
| ID | Question | Data | Command | Result | Status | Repro |
|---|---|---|---|---|---|---|
| P1-DET | freeze a public detector | — | `research/acmot_paper_v2/frozen_detector/DETECTOR_PROVENANCE.json` | YOLO11m dronefreak/visdrone-yolo11m sha256 c6f98247… (AGPL-3.0) | DONE | REPRODUCIBLE (public checkpoint) |
| P1-BASE | baseline systems r1536_n70 + ByteTrack / OATrack | VisDrone val-7 | `python research/acmot_paper_v2/run_baseline_systems.py` | ByteTrack HOTA 41.586; `research/acmot_paper_v2/BASELINE_SYSTEMS_RESULT.json` | DONE | PARTIALLY (detection cache external, hash-listed) |
| P1-A1–A5 | Phase A searches (resolution map, NMS map, cue subset, joint) vs calibration matched-static | 8 VisDrone-MOT-train calibration sequences, 4 folds | `research/acmot_paper_v2/controller_search/run_stage1.py` … `run_stage3b4_joint.py` | null: no policy beat the best fixed point | DONE (negative) | PARTIALLY |
| P1-ORACLE | oracle gates, segment headroom, confidence oracle | calibration | `controller_search/oracle_gate*.py`, `segment_headroom.py`, `confidence_oracle.py` | headroom recorded in `controller_search/*_RESULT.json` | DONE | PARTIALLY |
| P1-B (V3 joint) | Phase B: 60-trial TPE over τm, τh and actions incl. confidence floor vs r1536_n70 | calibration, 4 folds | `controller_search/run_v3_joint_search.py` | trial 7 frozen (commit 309dca5): τm 0.297, τh 0.511 | DONE | PARTIALLY |
| P1-SHUF | same-action-distribution shuffled control | calibration | `controller_search/run_shuffled_control.py` | does not establish that timing adds value beyond the action mix | DONE (limitation) | PARTIALLY |
| P1-STATIC | static no-op policy, FIRST val read | VisDrone val-7 | `python research/acmot_paper_v2/run_final_acmot_systems.py` (commit bfa5caf) | `research/acmot_paper_v2/FINAL_ACMOT_SYSTEMS_RESULT.json` | DONE | PARTIALLY |
| P1-V3 | frozen v3, SECOND val read | VisDrone val-7, ByteTrack / OATrack | `python research/acmot_paper_v2/run_v3_second_val_read.py` (commit 0af0066) | ByteTrack HOTA 41.586 → 44.523; OATrack 46.770 → 48.095; bootstrap 5000, seed 42 (`research/acmot_paper_v2/BOOTSTRAP_V3_RESULT.json`) | DONE | PARTIALLY |
| P1-UAVDT | frozen transfer without retuning | UAVDT test 20 seq (Kaggle kernel) | `research/acmot_paper_v2/run_uavdt_transfer.py`, `python research/acmot_paper_v2/run_uavdt_bootstrap.py` | MOTA ByteTrack −1.573 → 16.028; OATrack 19.607 → 22.873 | DONE | PARTIALLY (cache on Kaggle/Drive) |
| P1-RT | runtime on Tesla T4 | — | `research/acmot_paper_v2/V3_RUNTIME_BENCHMARK_RESULT.json` | controller ≈ 4.2 ms/frame | DONE | PARTIALLY |
| P1-LEGACY | U2MOT and SparseTrack scene-adaptive Colab runs (Sept 2026) | VisDrone val/test-dev; MOT17/MOT20 | audit `research/transfer_legacy/U2MOT_SPARSETRACK_EVIDENCE_AUDIT.md`; re-scoring `research/transfer_legacy/rescore/` | used in Paper 1 legacy section | DONE (audited) | HISTORICAL / ARTIFACTS MISSING (runs on Drive) |

## Post-freeze V7f evaluation on VisDrone confirmation-16 (2026-10-21)

| ID | Commit | Hypothesis | Config | Data | Result | Status |
|---|---|---|---|---|---|---|
| E55 | frozen V7f (tag universal-acmot-v7-freeze → 488df9a) | the frozen layer does not lower HOTA on held-out aerial data; RT-DETR-L gains more than YOLOv8n | `V7_SPLIT=conf16 V7_DETS=yolov8,rtdetr tools/v7/dev.py run NATIVE V7f`; `dev.py official`; `tools/v7/bootstrap.py NATIVE V7f --protocol official`; preregistration `research/final/V7_CONF16_PREREGISTRATION.md` (sha256 ad7764b9…) | VisDrone2019-MOT-train confirmation-16 (16 seq, 7,034 frames; official annotations, fingerprint verified), ByteTrack host, cached YOLOv8n / RT-DETR-L at 736 | official-compatible: RT-DETR-L MOTA −3.46 → 13.02 (+16.48 [+4.65, +31.49]), HOTA −0.93 [−2.59, +1.22], IDF1 −0.93 n.s., IDS −85 %, FP −62 %, FN +25 %; YOLOv8n HOTA +0.42 [−0.60, +1.58], MOTA −1.08 n.s., IDF1 +1.42 n.s., IDS −51 %. Prediction 1 (no significant HOTA loss) confirmed; prediction 2 not confirmed on HOTA (holds on MOTA). `research/final/V7_CONF16_RESULT.json` | DONE (single run; second use of the split after E48, see the correction in the result file); PARTIALLY reproducible (detection caches and outputs are local and git-ignored; annotations re-obtainable and checked by fingerprint) |
| E56 | frozen V7f (tag universal-acmot-v7-freeze → 488df9a) | the frozen layer does not lower HOTA on UAVDT; RT-DETR-L gains more MOTA than YOLOv8n | `V7_SPLIT=uavdt V7_DETS=yolov8,rtdetr tools/v7/dev.py run NATIVE V7f`; `dev.py report`; `tools/v7/bootstrap.py NATIVE V7f --protocol internal`; preregistration `research/final/V7_UAVDT_PREREGISTRATION.md` (sha256 a370bdac…) | UAVDT test (20 seq, 16,592 frames; official GT, per-sequence box counts equal to the Paper 1 record 20/20), ByteTrack host, cached YOLOv8n / RT-DETR-L at 736 | internal UAVDT protocol: YOLOv8n HOTA +1.77 [+0.70, +2.94], IDF1 +3.97 [+1.88, +6.17], MOTA +1.02 n.s., IDS −45 %; RT-DETR-L MOTA 3.29 → 27.99 (+24.70 [+10.06, +51.08]), IDF1 +5.74 [+0.13, +13.11], HOTA +2.30 n.s., FP −58 %, IDS −56 %, FN +17 %. Both predictions confirmed. `research/final/V7_UAVDT_RESULT.json` | DONE (single run); PARTIALLY reproducible (detection caches and outputs local and git-ignored; GT re-obtainable and checked by box counts) |
| E57 | frozen V7f (unchanged; runner overrides) | V7f beats simple adaptive Otsu thresholds on the same input | `V7_SPLIT=kitti tools/v7/dev.py track` with `NATIVE@regime=noisy@noisy_primary={t1,t2}@noisy_ext=host`; `tools/v7/kitti/kitti_eval.py --boot`; plan `research/final/V7_REVIEWER_BASELINES_ABLATION_PLAN.md` | KITTI training, cells ByteTrack RT-DETR-L, OC-SORT YOLOv8n, and both with halved scores (BoT-SORT run invalid: frames missing) | HOTA V7f − OTSU-2: −0.52 n.s. (C1), +3.09, +2.29, +2.74 (sig.); MOTA OTSU-2 higher in C1 and C4. `research/final/V7_REVIEWER_BASELINES_ABLATION_RESULT.json` | DONE; PARTIALLY reproducible (caches local) |
| E58 | frozen V7f (unchanged; runner overrides) | each component's contribution on the final configuration | V7f with one of rescue=none, motion=0, scores=raw, bg_check=0, dup=iou, regime=noisy, regime=clean | same 4 KITTI cells | rescue and mode decision carry most of the effect; motion, background check and duplicate rule ≤ 0.15 HOTA on KITTI. Same result file | DONE; PARTIALLY reproducible (caches local) |
| E59 | frozen V7f (unchanged) vs ACT (Gwon & Lee 2026, published parameters) | V7f vs a published adaptive-threshold method on the same input | new runner `tools/v7/act_baseline.py` (HOSTCHK reproduces dev.py NATIVE byte for byte, 84/84); `tools/v7/kitti/kitti_eval.py --boot`; plan `research/final/V7_ACT_COMPARISON_PLAN.md` (sha256 9bcf5314…, written first) | KITTI training, 4 cells: ByteTrack RT-DETR-L, OC-SORT YOLOv8n (ACT extended), both also with halved scores | HOTA V7f − ACT: +0.34 n.s. (C1), +2.01 [+0.01, +4.76] (C4), −0.65 n.s. (C3), +10.06 [+6.88, +12.01] (C5); MOTA: ACT significantly higher in C4 (−4.35) and C3 (−3.62). Prediction 1 (V7f > ACT under halved scores) confirmed. `research/final/V7_ACT_COMPARISON_RESULT.json` | DONE; PARTIALLY reproducible (caches local) |
| E60 | frozen V7f (existing outputs, not re-run) vs ACT (published parameters) | V7f vs ACT in ACT's original setting and on held-out UAVDT | `tools/v7/external/mot17_act.py` (MOT17; HOSTCHK byte-identical to BY_official_*_BASELINE, 14/14) and `tools/v7/act_external.py` (UAVDT; HOSTCHK identical to E56 NATIVE, 40/40); `tools/v7/mot17_eval_v7.py --boot`, `tools/v7/bootstrap.py --protocol internal`; plan `research/final/V7_ACT_ORIGINAL_UAVDT_PLAN.md` (sha256 8dbf759f…, written first); D-043 | MOT17 val-half ByteTrack official, YOLOX-X floors 0.01/0.1; UAVDT test ByteTrack, YOLOv8n and RT-DETR-L | MOT17: V7f − ACT HOTA +0.22/+0.23 n.s. UAVDT: YOLOv8n HOTA +1.82 [+0.65, +3.00], IDF1 +4.00 (sig.); RT-DETR-L MOTA +22.65 [+9.03, +47.21] (sig.), HOTA +2.23 n.s. No cell with V7f significantly below ACT. `research/final/V7_ACT_ORIGINAL_UAVDT_RESULT.json` | DONE; PARTIALLY reproducible (caches and GT local) |
| E61 | frozen V7f (unchanged; runner overrides) | V7f is insensitive to its fixed values (HOTA within 1 point) | `V7_SPLIT=kitti tools/v7/dev.py track V7f@<k=v>` for window=5/20, rho_frames=100/300, dup_iou=0.4/0.6, hist=50/200 (rho_frames=300 re-run as `rho_frames=300@window=10` after a disk-full interruption; window=10 is the frozen value); `tools/v7/kitti/kitti_eval.py`; plan `research/final/V7_SENSITIVITY_PLAN.md` (sha256 7aad4ba6…, written first); also a logit-to-score check of the recorded thresholds of the E57 baselines and V7f | KITTI training, cells C1, C3, C4, C5 of E57/E58 | max abs HOTA change 0.62 (C3 IoU 0.6); C1 within 0.24; prediction confirmed. Conversion check: thresholds = sigmoid(split) with zero difference in every frame of all 8 baseline runs, V7f clean = min(a, sigmoid(t2)) and noisy = 0.5 in all frames. `research/final/V7_SENSITIVITY_RESULT.json` | DONE; PARTIALLY reproducible (caches local) |

