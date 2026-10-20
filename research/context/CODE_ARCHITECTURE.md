# CODE ARCHITECTURE — what each module does, for which version and paper

Purpose: the hand-curated map from research concepts to source code. Owns:
module roles, data flow, version and paper attribution, "implemented vs only
described" verification. Symbols and line numbers for every module are in the
generated CODE_INVENTORY.md (`python3 tools/build_code_inventory.py`); line
numbers below were read from the working tree at commit ffa3013 and must be
refreshed from the inventory after code changes. Update this file when a
module is added, removed, re-purposed, or attributed to a new paper/version.

Rule: a mechanism counts as implemented only if it is found in the source
below. Manuscript text, comments and proposals are not evidence.

## 1. Data flow per line
```
Universal AC-MOT V7f (Paper 2 "SCL"):
frame t ─► frozen detector (adapters/detectors/*) ─► candidates (box, score, class)
        ─► V7Layer.step (acmot_v7.py) using logits of frames t-10..t-1, tracks of t-1, host contract
        ─► (K_t, scores, a_t, b_t, m_t) ─► tracker adapter / external tracker loop ─► tracks
        ─► V7Layer.observe(tracks of t)            (state for t+1)

Compute lines on V7f (C1 / G1 / G2):
frame t ─► LevelSource / Schedule (acmot_sci_v7.py / acmot_g2.py) ─► ComputeProfileAdapter
        ─► detector at the chosen native setting ─► frozen V7f ─► tracker (tools/sci_v7/hosts.py)

Paper 1 AC-MOT v3 (operating-point controller):
frame t ─► SceneLayer.decide (acmot_sci.py; crowd cue from tracks of frames < t, image stats of t)
        ─► level LOW/MEDIUM/HIGH ─► action (resolution, NMS IoU, confidence floor)
        ─► cached YOLO11m detections at that setting, score >= floor ─► ByteTrack / OATrack
        ─► SceneLayer.observe(track boxes)
   runner: research/acmot_paper_v2/controller_search/run_v3_joint_search.py::run_policy_with_conf (L50)

V1–V6-TF (history):
frame ─► UniversalACMOT (universal_acmot.py) ─► UniversalPolicyPipeline (universal_policy_pipeline.py)
        ─► online_calibration.py (ECDF, Otsu, dedup) ─► tracker adapters
```

## 2. Core modules
| Module | Key symbols (line) | Role | Inputs → outputs | Version / line | Experiments | Paper | Last commit |
|---|---|---|---|---|---|---|---|
| acmot_v7.py | `HostContract` L84, `V7Spec` L98, `V7Decision` L191, `V7Layer` L200, `_duplicates` L222, `_bands` L289 (nested Otsu + background check), `_ecdf` L319 (rank remap memory), `step` L326, `observe` L478, `motion_cue` L68, `spec_from_dict` L497 | the V7 layer; V7f = `configs/universal_acmot_policy_v7.json` | candidate boxes/scores/classes of frame t, optional motion cue, host contract → passed indices, scores, assoc/birth thresholds, match tolerance, log | U: V7a–V7f | V7-E*, V7-POST-* | Paper 2 (SCL) | b68e050 (frozen in lock `research/V7_POLICY_LOCK.json`) |
| acmot_sci.py | `SceneSpec` L44, `SceneDecision` L84, `SceneLayer` L93, `observe` L113, `decide` L117 | historical SCI scene layer (crowd/tiny/edge/dark/blur cues, levels, recovery probe, hysteresis, dwell) | image stats of t, track boxes of frames < t → level | P1 controller; C1 compute rule | P1-*, SCI-E1 | Paper 1 | see CODE_INVENTORY.md |
| acmot_sci_v7.py | `LevelSource` L35, `SciV7Pipeline` L63 (`step` L77) | compute level upstream of frozen V7f | image stats, detector callable → tracks | C1 / G1 | SCI-*, G1-* | — | see inventory |
| acmot_g2.py | `ComputeAction` L23, `StaticSchedule` L28, `Schedule` L43, `G2Pipeline` L60 | G2 compute schedules | observations → compute action | G2 | G2-* | — | f81c45d |
| online_calibration.py | `exact_otsu3` L57, `exact_otsu2` L84, `nested_otsu` L98, `dedup` L131, `RobustHistory` L175 | Otsu / dedup / robust history used by V5-TF and V6-TF | logits → thresholds | V5-TF, V6-TF | E36–E54 | prior design in Paper 2 | see inventory |
| universal_policy_pipeline.py | `PolicySpec` L39, `UniversalPolicyPipeline` L192 | V1–V6-TF policy pipeline (gate, bands, F3 motion rule, F5 R-res) | detections + cues → tracker input | V1–V6-TF | E01–E54 | thesis history | see inventory |
| universal_acmot.py | `ResolutionBudget` L50, `UniversalACMOT` L85, `load_policy` L43 | live entry for V1–V6 (compute budget) | frames → tracks | V4–V6-TF | E40, E46 parity | — | see inventory |
| scene_state.py | `image_stats` L44, `SceneStateAnalyzer` L62 | V5 scene-state vector | image, detector, tracker stats → state | V5 | E32–E35 | — | see inventory |
| core.py | `Config` L38, `Controller` L87 | legacy thesis AC-MOT controller (SCI) | — | L | legacy | thesis | see inventory |
| v5_controller.py | — | learned V5 controller (research only, forbidden as deployed) | — | V5 | E34–E35 | — | see inventory |
| run_universal_acmot.py | `run_video` L246, `run_image_folder` L161, `main` L464 | CLI demo of the universal pipeline | video / image folder → tracks, video | V1–V6 | — | — | see inventory |

## 3. Adapters
| Module | Class (line) | Role | Used by |
|---|---|---|---|
| adapters/detectors/base.py | `DetectorAdapter` L7 | detector interface (candidates with score floor) | all lines |
| adapters/detectors/yolov8.py, rtdetr.py, fasterrcnn.py, retinanet.py, fcos.py | `YOLOv8Adapter` L26, `RTDETRAdapter` L26, `FasterRCNNAdapter` L27, `RetinaNetAdapter` L15, `FCOSAdapter` L15 | COCO detectors; RetinaNet = G1 unseen detector; FCOS = G2 planned | V1–V7, G1, G2 |
| adapters/detectors/compute_profile.py | `ComputeProfileAdapter` L20 | maps a generic compute level to a native detector setting (`configs/sci_v7_profiles.json`) | C1, G1, G2 |
| adapters/detectors/online_normalizer.py | `OnlineScoreNormalizer` L8, `EmpiricalCDFNormalizer` L206 | V1 histogram normaliser; V3/V4 ECDF | V1–V4 |
| adapters/detectors/tiling.py | `merge` L33 | crop refinement for G2 S3 | G2 |
| adapters/detectors/factory.py | `create_detector` L42 | detector construction | live runs |
| adapters/trackers/base.py, bytetrack.py, botsort.py | `TrackerAdapter` L6, `ByteTrackAdapter` L13, `BoTSORTAdapter` L10 | Ultralytics ByteTrack / BoT-SORT behind one interface | V1–V7 dev, KITTI, P1 (ByteTrack) |
| adapters/trackers/oatrack.py | `OATrack` L62, `OATrackAdapter` L158 | OATrack re-implementation (quality gate 0.40) | Paper 1 |
| tools/sci_v7/hosts.py | `make_host` L31 | ByteTrack / BoT-SORT / OC-SORT hosts for compute lines | C1, G1, G2 |

## 4. Experiment runners and external hosts
| Path | Role | Version | Registry IDs |
|---|---|---|---|
| tools/v7/dev.py (`track_sequence` L89, `guard` L73), tools/v7/systems.py (`parse` L55, `HOST_BYTETRACK`) | development runner on cached detections; refuses protected splits | V7 | V7-E*, V7-POST-VD |
| tools/v7/external/{mot17_bytetrack,sparsetrack,boosttrack,pdsort,hybridsort}_v7.py | official tracker loops with the layer inserted; contract set from published arguments | V7 | V7-E15–E18, V7-POST-PD/HS/ST |
| tools/v7/recent/{ctwix,topictrack,tracktrack}_v7.py, *.sh | recent 2025 external systems (GitHub Actions) | V7f | V7-POST-CTW/TOP/TT |
| tools/v7/kitti/kitti_eval.py (`evaluate` L77) | official KITTI HOTA, car/ped average, bootstrap | V7 | V7-E19, P2-KITTI |
| tools/v7/mot17_eval_v7.py | TrackEval MOT17 val-half evaluation + bootstrap | V7 | P2-MOT17, P2-EXT |
| tools/v7/bootstrap.py (`paired` L55, `run` L81) | paired sequence bootstrap (10,000, seed 42) | V7 | all V7 rows |
| tools/v7/benchmark.py (`run` L30) | live runtime benchmark | V7f | V7-POST-RT |
| tools/v7/freeze.py (`main` L34) | writes the policy lock | V7f | V7-FREEZE |
| tools/v7/ci/*.sh | GitHub Actions jobs (SparseTrack, calibration bootstrap, aerial val) | V7f | V7-POST-* |
| tools/v6/dev.py, tools/v6/external/*, tools/v6/eval_official.py (`official_sequence_stats` L87, `combine_official` L120), tools/v6/stats.py (`bootstrap` L10) | V6-TF runner, external transfers, official-compatible VisDrone evaluation (also used by Paper 1) | V6-TF, P1 | E42–E54, P1-* |
| tools/eval_local.py (`motmetrics_rows` L107) | internal class-agnostic VisDrone protocol | V1–V7 | E01+ |
| tools/sci_v7/{dev,oracle,cue_audit,sweep_cache,benchmark}.py | SCI/G1 runner, GT oracle, cue audit, sweeps | C1, G1 | SCI-*, G1-* |
| tools/g2/{dev,oracle,controllers,latency,build_tile_cache}.py | G2 runner and gate | G2 | G2-* |
| research/acmot_paper_v2/controller_search/sim.py (`run_policy_on_sequence` L115, `get_sequence` L99) | cached-detection simulator for Paper 1 searches | P1 | P1-A*, P1-B |
| research/acmot_paper_v2/controller_search/run_v3_joint_search.py (`run_policy_with_conf` L50, `spec_for` L31) | Phase B TPE joint search; policy with confidence floor | P1 | P1-B, P1-V3 |
| research/acmot_paper_v2/run_v3_second_val_read.py, run_baseline_systems.py, run_final_acmot_systems.py, run_uavdt_transfer.py, run_uavdt_bootstrap.py | Paper 1 final runs | P1 | P1-V3, P1-BASE, P1-STATIC, P1-UAVDT |
| tools/cache_detections.py | detector caches for replay | all | — |
| JAIS_PAPERS/CODEX_HANDOFF/tools/{make_standalone,check_integrity}.py | manuscript standalone builder and integrity check | papers | PAPERS.md |
| tools/build_context_graph.py, tools/context_health_check.py, tools/update_project_context.py, tools/build_code_inventory.py | knowledge-base maintenance | — | README.md |

## 5. Tests
| Test | Guards |
|---|---|
| tests/test_v7_adaptive_layer.py | V7 layer behaviour: causality, state reset, clean pass-through, name independence, affine invariance, policy lock integrity |
| tests/test_v7_bootstrap.py | bootstrap implementation |
| tests/test_sci_v7.py, tests/test_g2_gsci.py | compute lines: causality, no names in generic files |
| tests/test_v6_adaptive_layer.py | V6-TF layer |
| tests/test_oatrack.py | OATrack re-implementation |
| tests/test_*_equivalence.py, tests/test_universal_separation.py, tests/test_online_universal_smoke.py, tests/test_rtdetr_universal_pipeline_smoke.py | adapter equivalence and pipeline smoke tests (V1–V4) |
| tests/test_legacy_rescore.py | legacy U2MOT/SparseTrack re-scoring |

## 6. Mechanism verification (described in a paper → found in code)
| Mechanism | Paper | Code evidence |
|---|---|---|
| nested Otsu on logits of frames t−10..t−1 | Paper 2 Eq. ρ | `acmot_v7.py` `_bands` L289, window `V7Spec.window` = 10 |
| background (interpretability) check | Paper 2 | `acmot_v7.py` `_bands` (sets ρ = 1 without a background mode), `bg_check: true` in the config |
| whole-stream clean/noisy mode (median ρ ≥ ½) | Paper 2 | `acmot_v7.py` `step`, config `regime: rho`, `rho_frames: 0` |
| clean mode min(host, σ(t2)) | Paper 2 Eq. clean | config `clean: upper`; `step` |
| rank remap 0.5 + 0.5u / 0.1 + 0.4u, thresholds 0.5 | Paper 2 Eq. remap | `acmot_v7.py` L391–L393 (`_ecdf` memory of 20 samples, frame 1 and every 10th frame, L473–L475) |
| crowd-safe track-context duplicates | Paper 2 | `_duplicates` L222, config `dup: track`, `dup_regime: noisy`, `dup_clean: xclass` |
| continuation rescue | Paper 2 | `step` (`rescue: track`, `rescue_band: fg`) |
| motion tolerance min(0.95, 1 − (1 − m0)/max(1, r)) | Paper 2 Eq. motion | `motion_cue` L68, `step`; config `motion_regime: noisy`, `hist: 100`, `warmup: 5` |
| SCI from crowd cue, three levels, recovery probe, hysteresis, dwell 30 | Paper 1 Alg. 1 | `acmot_sci.py` `SceneLayer.decide` L117 |
| confidence floor applied as score ≥ c | Paper 1 | `controller_search/run_v3_joint_search.py` L50–L70 via `sd.detections(t, res, nms, conf)` |
| adaptive resolution before the detector (V5-TF F5 R-res) | rejected | `universal_policy_pipeline.py` `_tf_level` (FX-17); not part of V7f |
