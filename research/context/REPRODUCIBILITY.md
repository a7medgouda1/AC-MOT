# REPRODUCIBILITY — how every paper-relevant experiment can be re-run

Purpose: say, for each experiment that a paper or a version decision relies on,
exactly what is needed to re-run it, where every input and output lives, and
what is missing. Owns: reproducibility labels, environment records, the
reproducibility matrix, the missing-artifact list. Does not own: results
(RESULTS_CANONICAL.md and the files it names) or experiment questions
(EXPERIMENT_REGISTRY.md, same IDs). Update when an experiment is added, an
artifact moves, or a missing artifact is restored. Never invent a command,
checkpoint, value or hash: write NOT RECORDED and the minimum action instead.

Detailed run instructions already maintained elsewhere (not duplicated here):
`research/final/V7_REPRODUCIBILITY.md` (V7f), `research/final/REPRODUCIBILITY.md` (V6-TF),
`research/REPRODUCE.md` (V1–V4), `research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/README.md`
(Paper 1 archive with SHA256SUMS and a paper-number audit trail).

## Labels
| Label | Meaning |
|---|---|
| REPRODUCIBLE | code at a known commit, public or released inputs with hashes, a recorded command, and the committed outputs to compare with |
| PARTIALLY REPRODUCIBLE | code and outputs committed, but an input (dataset zip, detection cache, Drive/Kaggle copy) must be supplied by the owner; hashes are recorded |
| NOT YET REPRODUCIBLE | a required input or command is not recorded |
| HISTORICAL / ARTIFACTS MISSING | outputs survive only as transcribed numbers or external drives; re-running is not possible from the repository |

## Environments
| ID | Where | Hardware | Software | Used for | Record |
|---|---|---|---|---|---|
| ENV-MAC | owner's Mac (local) | Apple A18 Pro, 8 GB, CPU replay (no MPS for V7) | PyTorch 2.14, repo `.venv` | V7 development before 2026-09-28 instruction; V1–V6 | `research/final/V7_CLOUD_RUNS.md` |
| ENV-C1 | Claude cloud container | 4-vCPU Intel Xeon 2.10 GHz, 15 GB, no GPU | Python 3.12 venvs via `scripts/setup_research_assets.sh` | V7 labelled fallback E15–E19, runtime | `research/final/V7_CLOUD_RUNS.md`, `research/final/env/` |
| ENV-GHA | GitHub Actions ubuntu-24.04 | AMD EPYC 7763 × 4 | Python 3.12.3, OpenCV 4.6.0 (GMC) | SparseTrack + V7f, calibration bootstrap, recent externals, VisDrone val-7 V7f, SCI/G1/G2 caches | `research/final/sparsetrack_v7f/environment.txt`, `research/final/paper2_calib_boot/environment.txt`, `research/final/recent/*/environment.txt`, `.github/workflows/` |
| ENV-T4 | Google Colab / Kaggle Tesla T4 | NVIDIA T4 | ultralytics 8.3.200, numpy 2.2.6 (Paper 1 pins) | Paper 1 runtime and UAVDT cache | `research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/ENVIRONMENT.txt`, `uavdt/` |

Assets: release `v7-dev-assets-1` (detection caches, sha256 verified by
`scripts/setup_research_assets.sh`); external tracker repositories at pinned
commits (PD-SORT af21db6, Hybrid-SORT 396f8d3, SparseTrack 499844f, BoostTrack
fb5bfc3, C-TWiX 3cff9cc, TOPICTrack e7b260f, TrackTrack ee7f1c5); Paper 1
detector `dronefreak/visdrone-yolo11m` sha256 c6f98247….

## Experiment cards (paper-relevant)
Fields: ID · question · version · commit/tag · detector + checkpoint · tracker + config · dataset + split ·
sequences/frames · seeds · config files/args · software · hardware · command · inputs (+hash) · outputs (+hash) ·
protocol · metrics/units · baseline · result + uncertainty · limitations · label.

### P2-MOT17 (Paper 2 Table "baseline comparison of the development trackers"; registry V7-E15–E18, V7-POST-ST)
- Question: does frozen V7f keep well-matched two-stage hosts and help the single-stage OC-SORT?
- Version V7f, tag universal-acmot-v7-freeze → 488df9a (SparseTrack run at repo commit 79749c5 with lock 10/10).
- Detector: published YOLOX-X detections of each tracker (MOT17 val-half), emission floor 0.01 or 0.1.
- Trackers: SparseTrack 499844f (0.6/0.7/0.1/0.85), BoostTrack fb5bfc3 (0.6/0.6/0.1/0.7), ByteTrack official (0.6/0.7/0.1/0.8), OC-SORT (0.6/0.6/0.6/0.7).
- Data: MOT17 val-half, 7 sequences (02, 04, 05, 09, 10, 11, 13).
- Seeds: bootstrap 10,000 resamples, seed 42.
- Commands: `research/final/V7_REPRODUCIBILITY.md` "Development matrix"; SparseTrack via `.github/workflows/sparsetrack_v7f.yml`.
- Outputs: `research/final/V7_MAIN_RESULTS.json`, `research/final/V7_DEV_RESULTS.json`, `research/final/sparsetrack_v7f/results.json` (+ tracks.tar.gz).
- Protocol: TrackEval 12c8791, MOT17 val-half GT; HOTA/MOTA/IDF1 in percent.
- Baseline: host alone (our reproduction), same detections.
- Result: OC-SORT floor 0.01 +0.613 [+0.363, +1.241] HOTA; ByteTrack −0.014 [−0.058, +0.009]; SparseTrack +0.055 [−0.011, +0.254]; BoostTrack identical.
- Limitation: development data (visible during design).
- Label: REPRODUCIBLE.

### P2-SHIFT (Paper 2 score-shift table and figure; registry V7-STRESS-L)
- Hosts ByteTrack (official, library), OC-SORT, BoostTrack; transforms s³, 0.5 s, T = 2, T = 0.5; floor 0.01 (BoostTrack 0.1).
- Command: `.github/workflows/paper2_calib_boot.yml` → `tools/v7/ci/calib_boot.sh`.
- Output: `research/final/paper2_calib_boot/calib_boot.json` (+ environment.txt, lock_check.txt, pip_freeze.txt).
- Result: 14 conditions, 7 significant recoveries, 0 significant degradations; halving 0 → 66.166 / 66.72.
- Label: REPRODUCIBLE.

### P2-KITTI (Paper 2 detector-change table; registry V7-E19 / KITTI matrix)
- Detectors RT-DETR-L and YOLOv8n (COCO weights), caches from `tools/cache_detections.py`; frames from the official zip via `tools/v7/kitti/remotezip.py`.
- Hosts ByteTrack and BoT-SORT with the library contract (0.25/0.25/0.1/0.8); OC-SORT official.
- Data: KITTI tracking training, 21 sequences; BoT-SORT 20 (sequence 0020: Kalman Cholesky error when fed the layer's output; ledger E19).
- Commands: `V7_SPLIT=kitti V7_DETS=<det> tools/v7/dev.py track NATIVE V7f "V7f@trk:ocsort"`; `tools/v7/kitti/kitti_eval.py <det> NATIVE V7f`; `--boot`.
- Output: `research/final/V7_STATISTICS.md` (six cells), `research/final/V7_DEV_RESULTS.json`.
- Protocol: official KITTI HOTA averaged over car and pedestrian.
- Result: six cells; three positive (ByteTrack/BoT-SORT RT-DETR-L MOTA +5.98 / +7.86; OC-SORT YOLOv8n HOTA +7.91), three not (ByteTrack-YOLOv8n MOTA −1.87; BoT-SORT-YOLOv8n MOTA −2.43, CI < 0; OC-SORT-RT-DETR-L ≈ 0).
- Label: PARTIALLY REPRODUCIBLE (KITTI frames must be fetched; caches in the assets release).

### P2-EXT (Paper 2 external table; registry V7-POST-PD, V7-POST-HS, V7-POST-CTW/TOP/TT)
- Predeclaration: `research/final/V7_EXTERNAL_SELECTION.md` (PD-SORT, Hybrid-SORT) and `research/final/V7_RECENT_EXTERNAL_PROTOCOL.md` (C-TWiX, TOPICTrack, TrackTrack), both before any run.
- Commands: `research/final/V7_REPRODUCIBILITY.md` "External"; recent systems via `.github/workflows/recent_*.yml`.
- Outputs: `research/final/V7_EXTERNAL_RESULTS.json`, `research/final/V7_RECENT_EXTERNAL_RESULTS.json`, `research/final/recent/<system>/`.
- Results: PD-SORT +0.61 HOTA (CI > 0); Hybrid-SORT identical; C-TWiX KITTIMOT car −1.52 (CI < 0), MOT17/DanceTrack n.s. negative; TrackTrack −0.012 (CI < 0); TOPICTrack reproduction failed.
- Label: REPRODUCIBLE.

### P2-RT (Paper 2 runtime table)
- Command: `tools/v7/benchmark.py --weights yolov8n.pt --seqs 0001 0009 0019 --out research/final/V7_REALTIME_yolov8n.json` on ENV-C1.
- Output: `research/final/V7_REALTIME_yolov8n.json`, `research/final/V7_REALTIME.md`.
- Label: REPRODUCIBLE (timings depend on hardware).

### P2-PRIOR (Paper 2 AOB-vs-SCL table)
- AOB = V6-TF emulated inside the V7 framework (V6EMU) on MOT17 hosts; frozen V6-TF external runs `tools/v6/external/sparsetrack_v6.py`, `tools/v6/external/boosttrack_v6.py`.
- Outputs: `research/final/EXTERNAL_PAPER_TRANSFER.md`, `research/final/V7_DEV_RESULTS.json`.
- Label: REPRODUCIBLE.

### P1-MAIN (Paper 1 VisDrone table and abstract; registry P1-BASE, P1-V3)
- Version: AC-MOT v3 controller frozen at 309dca5 (`research/acmot_paper_v2/controller_search/FREEZE_MANIFEST_V3_ADAPTIVE.json`); archive tag acmot-v3-exp-2026-10-04-freeze → 280b4a2.
- Detector: YOLO11m `dronefreak/visdrone-yolo11m` best.pt, sha256 c6f98247e7c731a567aaf37ca7b808beff588b687623e028b25a2e1d846e96e7, half precision; classes pedestrian, car, van, truck, bus.
- Trackers: ByteTrack (Ultralytics defaults 0.25 / 0.10 / 0.25, buffer 30, match 0.80); OATrack re-implementation (`adapters/trackers/oatrack.py`, gate 0.40).
- Data: calibration = 8 VisDrone2019-MOT-train sequences (3282 frames, `research/acmot_paper_v2/DETECTOR_SPLIT.json`); evaluation = VisDrone2019-MOT-val 7 sequences, SECOND read (first read: static no-op, bfa5caf).
- Seeds: TPE search seeds in `EXPERIMENT_MANIFEST.json`; bootstrap 5000 resamples, seed 42.
- Commands: `python research/acmot_paper_v2/run_baseline_systems.py`; `python research/acmot_paper_v2/run_v3_second_val_read.py`.
- Inputs: detection cache `research/acmot_paper_v2/cache/` (EXTERNAL, hash-listed in the archive ARTIFACT_INDEX.csv).
- Outputs: `research/acmot_paper_v2/BASELINE_SYSTEMS_RESULT.json`, `research/acmot_paper_v2/SECOND_VAL_READ_V3_RESULT.json`, `research/acmot_paper_v2/BOOTSTRAP_V3_RESULT.json`; archive `hashes/SHA256SUMS.txt`.
- Protocol: official-compatible VisDrone (`tools/v6/eval_official.py` combine_official).
- Result: ByteTrack HOTA 41.586 → 44.523, MOTA 9.876 → 27.871, IDF1 48.569 → 53.929, IDS 1341 → 1016; OATrack HOTA 46.770 → 48.095.
- Limitations: val read twice; shuffled control does not show that timing adds value beyond the action mix; detector checkpoint third-party (AGPL-3.0).
- Label: PARTIALLY REPRODUCIBLE (owner must supply the detection cache or regenerate it with `tools/cache_detections.py` at 1088/1280/1536 × NMS 0.45/0.60/0.70).

### P1-UAVDT (Paper 1 UAVDT table)
- Data: UAVDT test, 20 sequences, 16,592 frames, one vehicle class; Kaggle kernel record in the archive `uavdt/`.
- Commands: `research/acmot_paper_v2/run_uavdt_transfer.py`; `python research/acmot_paper_v2/run_uavdt_bootstrap.py`.
- Outputs: `research/acmot_paper_v2/UAVDT_TRANSFER_RESULT.json`, `research/acmot_paper_v2/UAVDT_BOOTSTRAP_V3_RESULT.json`.
- Result: MOTA ByteTrack −1.573 → 16.028; OATrack 19.607 → 22.873 (count metrics bootstrapped only).
- Label: PARTIALLY REPRODUCIBLE (cache on Kaggle/Drive; view `outputs/uavdt_view` local).

### P1-RT (Paper 1 runtime)
- Output: `research/acmot_paper_v2/V3_RUNTIME_BENCHMARK_RESULT.json` (mean controller overhead 4.256 ms ByteTrack, 4.201 ms OATrack, Tesla T4).
- Label: PARTIALLY REPRODUCIBLE (T4 session).

## Reproducibility matrix
| Experiment | Code | Data | Checkpoint | Config | Outputs | Paper | Label |
|---|---|---|---|---|---|---|---|
| P2-MOT17 | acmot_v7.py, tools/v7/external/*, tools/v7/mot17_eval_v7.py | MOT17 val-half (assets release) | published YOLOX-X detections | configs/universal_acmot_policy_v7.json | V7_MAIN_RESULTS.json, sparsetrack_v7f/ | Paper 2 | REPRODUCIBLE |
| P2-SHIFT | tools/v7/ci/calib_boot.sh | MOT17 val-half | same | same | paper2_calib_boot/calib_boot.json | Paper 2 | REPRODUCIBLE |
| P2-KITTI | tools/v7/dev.py, tools/v7/kitti/kitti_eval.py | KITTI training (zip) | RT-DETR-L, YOLOv8n COCO | same | V7_STATISTICS.md, V7_DEV_RESULTS.json | Paper 2 | PARTIALLY |
| P2-EXT | tools/v7/external/pdsort_v7.py, hybridsort_v7.py, tools/v7/recent/* | MOT17, KITTIMOT, DanceTrack | released detections / weights (hashes in results JSON) | same | V7_EXTERNAL_RESULTS.json, V7_RECENT_EXTERNAL_RESULTS.json | Paper 2 (PD-SORT, Hybrid-SORT only so far) | REPRODUCIBLE |
| P2-RT | tools/v7/benchmark.py | KITTI 0001/0009/0019 | yolov8n.pt | same | V7_REALTIME_yolov8n.json | Paper 2 | REPRODUCIBLE |
| V7-POST-VD | tools/v7/ci/aerial_v7f_val.sh | VisDrone val zip (owner) | YOLOv8n, RT-DETR-L caches | same | aerial_v7f_val/ | not in Paper 2 | PARTIALLY |
| P1-MAIN | acmot_sci.py, research/acmot_paper_v2/controller_search/*, run_v3_second_val_read.py, adapters/trackers/oatrack.py | VisDrone-MOT train (8 calib), val-7 | YOLO11m sha256 c6f98247… | FREEZE_MANIFEST_V3_ADAPTIVE.json | SECOND_VAL_READ_V3_RESULT.json, BOOTSTRAP_V3_RESULT.json | Paper 1 | PARTIALLY |
| P1-UAVDT | run_uavdt_transfer.py, run_uavdt_bootstrap.py | UAVDT test | same | same | UAVDT_TRANSFER_RESULT.json | Paper 1 | PARTIALLY |
| P1-LEGACY | external Colab notebooks (U2MOT, SparseTrack) | VisDrone val/test-dev, MOT17/MOT20 | U2MOT visdrone.pth.tar | Drive FREEZE_DECLARATION.txt | research/transfer_legacy/rescore/ | Paper 1 (legacy section) | HISTORICAL / ARTIFACTS MISSING |
| V1–V4 (E01–E31) | universal_policy_pipeline.py, tools/* | VisDrone val, test-dev | YOLOv8n, RT-DETR-L COCO | configs/universal_acmot_policy*.json | outputs/ (local, git-ignored) | thesis history | PARTIALLY (outputs local to ENV-MAC) |
| V6-TF (E42–E54) | tools/v6/* | val-7, dev-40, conf16, test-dev, UAVDT, MOT17 | COCO detectors, Faster R-CNN | configs/universal_acmot_policy_v6tf.json | research/final/*.md, outputs/ (local) | Paper 2 prior design | PARTIALLY |

## Missing artifacts and the minimum action to restore them
| Missing | Affects | Minimum action |
|---|---|---|
| Paper 1 detection cache `research/acmot_paper_v2/cache/` (git-ignored, hash-listed) | P1-MAIN, P1-UAVDT | publish the cache (release asset) or regenerate with the frozen YOLO11m and compare hashes in ARTIFACT_INDEX.csv |
| VisDrone2019-MOT val/train zips (not downloadable by CI from the public Drive id) | V7-POST-VD, P1, SCI/G1/G2 | owner provides `VISDRONE_VAL_ZIP`; record the zip sha256 in DATASETS_AND_SPLITS.md |
| Local `outputs/` trees (V1–V6 runs, heldout_v4) | E01–E54 re-checks; RESULTS_CANONICAL verify block | copy from the owner's Mac to a release asset, or accept as PARTIALLY |
| Legacy U2MOT/SparseTrack Drive packages | P1-LEGACY | keep the read-only audit; re-running needs the Drive folders named in the audit |
| JRTIP-version figure `fig3_forest_col.pdf` (md5 6d64acca…) generation script | Paper 2 Fig. 3 | not found in the repository: regenerate from `research/final/V7_MAIN_RESULTS.json` with a committed script, or locate the script |
| T4 fidelity gate / official GPU timing for V7f | real-time claims on GPU | run `notebooks/Colab_T4_gate_and_benchmark.ipynb` retargeted to 488df9a |
