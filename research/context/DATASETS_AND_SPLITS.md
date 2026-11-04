# DATASETS AND SPLITS

Leakage status is time-dependent: every evaluation, inspection or tuning use
changes it. Update this file in the same commit as any new use.
Annotation fingerprint = sha256 over sorted "file:sha256(file)" lines of
`annotations/*.txt` (same definition as tools/make_train_split.py).
Evaluation filter everywhere: GT classes {1,4,5,6,9}, score==1, trunc<2,
occ<2, class-agnostic, IoU 0.5 (internal protocol, not official VisDrone).

## Dataset: VisDrone2019-MOT
### Split: VisDrone2019-MOT-val — DEVELOPMENT (heavily used), SECONDARY CHECK for V5-TF
- Path (Mac): `/Users/ahmedgouda/Desktop/CUE_SELECTION/VisDrone2019-MOT-val`
- 7 sequences, 2,846 frames, 67,345 GT boxes (research/EXPERIMENT_REGISTRY.md header)
- Fingerprint: a22a993fd46e77fa411f2b3b8ae31e7a8f4ef05b9a872fe7820da02ab3554d28 (computed 2026-09-27)
- Used for: all V1–V4 selection, V5 S1–S3 attempts (E32–E35). Inspected: yes.
- Clean for transfer: NO. For V5-TF: secondary check after freeze only.

### Split: VisDrone2019-MOT-train development-40 — DEVELOPMENT for V5-TF
- Path: Google Drive `…/My Drive/AC-MOT-shared/AC-MOT-data/VisDrone2019-MOT-train`
- Split file: `research/TRAIN_SPLIT_V5.json` (seed 20260927, length-quartile
  stratified, metadata only; created before any V5 train result)
- 40 sequences, 17,167 frames. Whole train fingerprint (56 files):
  045620e4ba7009dba97e495271254b468b50c01db85ca80c4fe90871a1e17e81
- Used for: V5-TF rule validation/ablation/stress (validate, never fit). No
  result yet (E36 pending). Caches: `outputs/det_cache_train*/` (in progress);
  `outputs/det_cache_train_native/{rtdetr,visual_cues}` are symlinks to `outputs/det_cache_train/`.

### Split: VisDrone2019-MOT-train confirmation-16 — PROTECTED
- 16 sequences, 7,034 frames (list in TRAIN_SPLIT_V5.json)
- Untouched: no metric computed. Caching is allowed (the train cache queue
  caches all 56 sequences; caches ≠ evaluation).
- Evaluated ONCE after the V5-TF freeze (V5-TF vs V4, Amendment-5a rule).

### Split: VisDrone2019-MOT-test-dev — HELD-OUT, USED ONCE → post-hoc only
- Path: Google Drive shortcut `…/visdrone goda1/VisDrone_Zips/VisDrone2019-MOT-test-dev/VisDrone2019-MOT-test-dev`
- 17 sequences, 6,635 frames; fingerprint 89d9dccbad509f1f8d34bb2afde32cb82490d34242b266345188107… (full value in research/TESTDEV_LOCK_V4.json)
- History: legacy AC-MOT exploratory comparisons (2026-09-10/11, README
  states "exploratory test-dev comparison, not a held-out benchmark");
  Universal V4 evaluated once (E31). Clean for V5-TF: NO (post-hoc label mandatory).

### Diagnostic subsets
- val sequences uav0000137_00458_v, uav0000268_05773_v ("0137", "0268"): V2-era diagnostics (E03–E15).
- Fidelity-gate subset (Amendment 5f): uav0000020_00406_v, uav0000315_00000_v,
  uav0000316_01288_v, uav0000342_04692_v (development-40 members; YOLOv8n,
  RT-DETR-L at 736). Never confirmation sequences.
- `outputs/calibration/{yolov8,rtdetr}_pr_50f.csv` (2026-09-26, untracked
  tools/calibrate_detector_pr.py, GT-based detection PR on 50 frames of ONE
  sequence at 640): which sequence/split — NEEDS VERIFICATION. If it was a
  train confirmation-16 sequence, record it as a detection-level GT inspection
  (created before the split existed; no tracking metric).

## Dataset: UAVDT
### Split: UAVDT test — PROTECTED (unseen dataset for Universal AC-MOT)
- Source: Google Drive `…/AC-MOT-shared/UAVDT_EXTERNAL_GENERALIZATION`;
  VisDrone-layout view `outputs/uavdt_view` (tools/build_uavdt_view.py)
- 20 sequences, 16,592 frames; view fingerprint
  aceae1c89eb4de05526bfa96f42da38ff1c6a474861bddaa1fbfd3044728184a
- Protocol: UAVDT_EXTERNAL_PROTOCOL_FREEZE.json + UAVDT_ADAPTER_V1_FREEZE.json (frozen 2026-09-12)
- Universal AC-MOT quality metrics: none (locks LOCKED_BEFORE_EVALUATION; no transfer output dir).
- CAVEAT: the legacy AC-MOT line ran a frozen UAVDT external generalization
  (branch origin/freeze/final-after-uavdt-2026-09-12). Whether any legacy UAVDT
  result informed Universal design: NEEDS VERIFICATION (no evidence found in
  research/). Caches `outputs/det_cache_uavdt*/` exist (caching only).

## Status updates (dated, append-only; the sections above are kept as written)
- 2026-09-28 → 2026-10-05 (from research/context/EXPERIMENT_REGISTRY.md): confirmation-16 was evaluated ONCE
  with frozen V6-TF (E48); test-dev post-hoc (E49); UAVDT test by frozen V6-TF (E50) and by the Paper 1
  AC-MOT v3 controller (P1-UAVDT, different detector and protocol). These sets are no longer untouched for
  any later version; for the V7f line they stay protected (PROTECTED_EVALUATIONS.md) and were not opened.
- VisDrone2019-MOT-val (val-7) is also the evaluation set of Paper 1 (read twice: bfa5caf, 0af0066) and a
  development set of V7 (E6, E20, V7-POST-VD) and of the compute lines (SCI/G1/G2).

## Datasets added after V6-TF (V7f line and Paper 1)
| Dataset / split | Size | Role | Protocol | Used by | Source / hashes |
|---|---|---|---|---|---|
| MOT17 val-half (ByteTrack split: second half of each train sequence) | 7 sequences (02, 04, 05, 09, 10, 11, 13) | V7 development hosts; predeclared externals PD-SORT, Hybrid-SORT; TOPICTrack; C-TWiX (CenterTrack split) | TrackEval 12c8791, MOT17 GT; HOTA/MOTA/IDF1 | V7-E*, V7-POST-* | frames mirrored and verified 2669/2669 sha256 (`MOT17_mirror_manifest.json` per V7_MAIN_RESULTS.md); published YOLOX-X detections per tracker |
| KITTI tracking training | 21 sequences (BoT-SORT 20; 0020 excluded) | V7 development detector change | official KITTI HOTA, car/ped averaged | V7-E19, P2-KITTI | official zip via `tools/v7/kitti/remotezip.py` |
| KITTIMOT val | per C-TWiX release | recent external (C-TWiX) | TrackEval, car and pedestrian separately | V7-POST-CTW | released Permatrack detections (hash in V7_RECENT_EXTERNAL_RESULTS.json) |
| DanceTrack val | 25 sequences | recent externals (C-TWiX, TrackTrack) | TrackEval | V7-POST-CTW, V7-POST-TT | released detections / FastReID (hashes in results JSON) |
| MOT20 val-half | — | TOPICTrack candidate | — | not completed (see V7_RECENT_EXTERNAL_FAILURES.md) | — |
| VisDrone2019-MOT-train calibration-8 | 8 sequences, 3282 frames | Paper 1 calibration (4 folds of 2 held-out sequences) | official-compatible VisDrone | P1-A*, P1-B | `research/acmot_paper_v2/DETECTOR_SPLIT.json` |
| VisDrone2019-DET (third party) | — | training data of the Paper 1 detector checkpoint (not trained by us) | — | P1-DET | `research/acmot_paper_v2/frozen_detector/DETECTOR_PROVENANCE.json` |

Evaluation protocols in use (never mixed in one comparison): internal class-agnostic VisDrone
(`tools/eval_local.py`); official-compatible VisDrone (`tools/v6/eval_official.py`, Paper 1 and V6/V7
official rows); TrackEval MOT17 val-half (`tools/v7/mot17_eval_v7.py`); official KITTI HOTA
(`tools/v7/kitti/kitti_eval.py`); system-specific TrackEval runs for the recent externals
(`tools/v7/recent/te_eval.py`).
