# PAPERS — publication registry (Paper 0, Paper 1, Paper 2)

Canonical record of every manuscript of the project: what each paper claims,
which frozen system and evidence it uses, every version folder, submission
state, supervisor and reviewer rounds, and what is still open. Numbers below
are copied from the manuscripts; their source of truth is the result file
named in each section. Last updated 2026-10-20.

Authors of all papers (same order): Ahmed Gouda Ismail (M.Sc. student,
corresponding, a7medgouda1@gmail.com), Mohamed S. Mohamed (Associate
Professor, Computer Engineering and Artificial Intelligence Department,
Military Technical College, Cairo), Tarek Ahmed Mahmoud (Professor, Computer
Engineering Department, Egypt University of Informatics, Cairo).

## Overview

| Paper | Title | Method / system | Venue | Status | Latest version |
|---|---|---|---|---|---|
| Paper 0 | Real-Time Object Detection and Tracking: Challenges, Innovations and Future Directions | survey (no new method) | IEEE ICMISI 2026, Alexandria, May 9-11, 2026, pp. 119-125 | PUBLISHED, DOI 10.1109/ICMISI69868.2026.11583994 | research/published_papers/Survey_ICMISI26/ |
| Paper 1 | Optimization-Guided Adaptive Detector Operating-Point Control for Multi-Object Aerial Tracking | AC-MOT: training-free scene-adaptive controller of the detector operating point (confidence threshold, NMS IoU, input resolution) | Journal of Aerospace Information Systems (JAIS, AIAA), Full Paper | SUBMITTED 18-Oct-2026, manuscript ID 2026-10-I012138 (submitted file = V12) | research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS/ (V13 = V12 + AI-use Acknowledgments, for the revision) |
| Paper 2 | Training-Free Self-Calibrating Control Layer for Heterogeneous Multi-Object Trackers | SCL = frozen Universal AC-MOT V7f between a frozen detector and a frozen tracker | target Journal of Real-Time Image Processing (JRTIP, Springer) | NOT SUBMITTED; V11 reviewed internally, V12 fixes pending | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11/ (Paper2_V11) |

Rules that apply to every manuscript version:
- Every change goes into a NEW version folder; old folders are never edited.
- Each version ships `<name>.pdf`, a standalone `for_overleaf/main.tex`
  (bibliography embedded), and `<name>_overleaf.zip`.
- Tests before delivery: build with 0 errors, 0 overfull boxes, 0 undefined
  references; integrity check against the previous version
  (`JAIS_PAPERS/CODEX_HANDOFF/tools/check_integrity.py OLD NEW`); compile of the
  standalone file in an empty folder with identical text.
- Standalone builder: `JAIS_PAPERS/CODEX_HANDOFF/tools/make_standalone.py main.tex main.bbl out`
  (multi-file papers: inline every \input first, then embed the .bbl).
- No new experiments, inference, or tuning for paper edits; numbers come
  only from the frozen result files. Protected data (confirmation-16, test-dev,
  UAVDT for the V7f line) is never opened for paper work.
- Commits and pushes happen only when the owner says "push"; `.zip` files are
  git-ignored and added with `git add -f` only when explicitly required.

## Paper 0 — published survey (ICMISI 2026)
- Title: Real-Time Object Detection and Tracking: Challenges, Innovations and Future Directions (7 pages).
- Objective: a deployment-oriented review of real-time object detection and tracking.
- Method: literature survey with a taxonomy (traditional, deep-learning, transformer-based), a quantitative
  comparison of detectors and trackers under real-time constraints (accuracy, latency, model size,
  hardware), datasets and metrics, limitations and failure cases, future directions (sections I–X of the PDF).
- Contributions (from the paper): structured taxonomy; up-to-date quantitative comparison of detectors and
  trackers under real-time constraints; deployment-focused analysis; open challenges for real-time and edge tracking.
- No experiment of this repository is reported in it; it is the literature basis for the later AC-MOT work
  (tracking-by-detection with fixed detector settings, real-time constraints).
- Files: `research/published_papers/Survey_ICMISI26/Survey_Camera_Ready_ICMISI26.pdf`,
  `Certificate_of_Participation_ICMISI26.png`, `CITATION.md` (BibTeX key ismail2026realtime).
- Publication: 2026 IEEE 3rd International Conference on Machine Intelligence and Smart Innovation
  (ICMISI 2026), Arab Academy for Science, Technology & Maritime Transport, Alexandria, May 9–11, 2026,
  pp. 119–125, IEEE catalog CFP26UT0-POD, DOI 10.1109/ICMISI69868.2026.11583994.
- Commits: 125ee1a (paper), 1043f8e (certificate), 6761e79 (DOI/citation).
- Role: the author block and affiliations of Papers 1 and 2 were taken from this paper (tag jais-overleaf-1).
- Self-overlap check (local 8-gram): 0.1% with Paper 1.

## Paper 1 — AC-MOT (JAIS)

### Claim and evidence
A training-free controller selects one of three detector operating points
(LOW / MEDIUM / HIGH) every 10 frames from scene cues (SCI) of the current
frame and past tracker output, with recovery probe, hysteresis and a 30-frame
dwell; the detector and tracker are not retrained. Evidence archive: tag
acmot-v3-exp-2026-10-04-freeze (280b4a2), folder
research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/ and
`research/acmot_paper_v2/FINAL_ACMOT_SYSTEMS_RESULT.json`,
`research/acmot_paper_v2/BOOTSTRAP_V3_RESULT.json`,
`research/acmot_paper_v2/UAVDT_BOOTSTRAP_V3_RESULT.json`,
`research/acmot_paper_v2/V3_RUNTIME_BENCHMARK_RESULT.json`.
Paper-number audit trail inside the archive: `PAPER_READY_RESULTS.md` and its README table.
Note: `research/acmot_paper_v2/FINAL_ACMOT_SYSTEMS_RESULT.json` is the static no-op control of the FIRST
val read (bfa5caf), not the headline; the headline is `SECOND_VAL_READ_V3_RESULT.json` (0af0066) against
`BASELINE_SYSTEMS_RESULT.json`. Algorithm 1 was checked line by line against the controller code
(acmot_sci.py SceneLayer.decide; confidence filter score >= c in run_v3_joint_search.run_policy_with_conf).

Headline results (VisDrone2019-MOT val, 7 sequences; relative to a fixed
operating point 1536 / 0.70):

| Tracker | HOTA | MOTA | IDF1 | IDS |
|---|---|---|---|---|
| ByteTrack | 41.586 -> 44.523 (+7.1%) | 9.876 -> 27.871 (+182%) | 48.569 -> 53.929 (+11.0%) | 1341 -> 1016 (-24.2%) |
| OATrack | 46.770 -> 48.095 (+2.8%) | 28.165 -> 34.483 (+22.4%) | 57.107 -> 59.364 (+4.0%) | 773 -> 604 (-21.9%) |

UAVDT (20 sequences, no retuning): MOTA ByteTrack -1.573 -> 16.028 (relative
change undefined, negative baseline); OATrack 19.607 -> 22.873 (+16.7%).
Controller cost about 4.2 ms per frame on a Tesla T4.

### Paper 1 claim map (Claim → Experiment → Result artifact → Config → Code → Commit → Dataset)
| Claim (V12) | Experiment | Result artifact (key) | Config | Code | Commit | Dataset | Status |
|---|---|---|---|---|---|---|---|
| ByteTrack HOTA +7.1%, MOTA +182%, IDF1 +11.0%, IDS −24.2% | P1-V3 vs P1-BASE | `SECOND_VAL_READ_V3_RESULT.json` (AC-MOT-v3+YOLO11m+ByteTrack.aggregate), `BASELINE_SYSTEMS_RESULT.json` | `controller_search/FREEZE_MANIFEST_V3_ADAPTIVE.json` | acmot_sci.py, run_v3_second_val_read.py | 309dca5 / 0af0066 | VisDrone-MOT val-7 (second read) | VERIFIED numbers; disclosure gap (see integrity notes) |
| OATrack +2.8% / +22.4% / +4.0%, IDS −21.9% | same, OATrack | same keys for OATrack | same | + adapters/trackers/oatrack.py | same | same | VERIFIED numbers |
| paired bootstrap supports the improvements | P1-V3 | `BOOTSTRAP_V3_RESULT.json` (bytetrack_v3_vs_system1, oatrack_v3_vs_system2), 5000 resamples, seed 42 | — | run_v3_second_val_read.py | 0af0066 | val-7 | VERIFIED |
| UAVDT MOTA raised with both trackers, +16.7% with OATrack | P1-UAVDT | `UAVDT_TRANSFER_RESULT.json`, `UAVDT_BOOTSTRAP_V3_RESULT.json` | same frozen policy | run_uavdt_transfer.py | 280b4a2 | UAVDT test 20 seq | VERIFIED |
| ≈ 4.2 ms per frame on a Tesla T4 | P1-RT | `V3_RUNTIME_BENCHMARK_RESULT.json` (4.256 / 4.201 ms) | — | archive scripts | 280b4a2 | — | VERIFIED |
| τm 0.297, τh 0.511 chosen by CV on calibration sequences | P1-B | `controller_search/V3_JOINT_SEARCH_RESULT.json` trial 7 | PREDECLARATION_V3_FINAL.json | run_v3_joint_search.py | 309dca5 | 8 train sequences | VERIFIED |
| historical quality / identity profiles, historical UAVDT, U2MOT, SparseTrack | P1-LEGACY | `research/paper_split/evidence/legacy/` (FINAL_TEST_*, V1_PAIRED_BOOTSTRAP_95CI.csv, V2_TRIAL22_TESTDEV_RESULT.json, UAVDT_FINAL_COMPARISON.json), `research/transfer_legacy/` | legacy freeze configs | legacy notebooks (Drive) | a6c1fa4, b591122 | VisDrone test-dev (exploratory), UAVDT, MOT17/MOT20 | numbers transcribed from snapshots; HISTORICAL |

### Paper 1 figure/table map (V12 labels)
| Label | Content | Data source | Generated by |
|---|---|---|---|
| tab:related | comparison with recent methods | literature | manual |
| fig:pipeline, alg:controller, tab:actions, tab:constants | method, frozen actions and constants | FREEZE_MANIFEST_V3_ADAPTIVE.json | TikZ / manual in main.tex |
| tab:quality, tab:identity | legacy profiles on VisDrone test-dev (historical protocol) | `research/paper_split/evidence/legacy/` | manual transcription |
| tab:hist-uavdt | legacy UAVDT transfer | legacy UAVDT_FINAL_COMPARISON.json | manual |
| tab:u2mot | U2MOT and SparseTrack cross-pipeline studies | `research/transfer_legacy/rescore/` | manual |
| tab:folds | frozen policy vs baseline on 4 calibration folds | V3_JOINT_SEARCH_RESULT.json / FREEZE_MANIFEST_V3_ADAPTIVE.json | manual |
| tab:visdrone, fig:visdrone, tab:bootstrap | main VisDrone results and bootstrap | BASELINE_SYSTEMS_RESULT.json, SECOND_VAL_READ_V3_RESULT.json, BOOTSTRAP_V3_RESULT.json | manual tables; TikZ bar chart in main.tex |
| tab:uavdt, fig:uavdt | UAVDT transfer | UAVDT_TRANSFER_RESULT.json, UAVDT_BOOTSTRAP_V3_RESULT.json | manual; TikZ |

### Paper 1 integrity notes (open, for the revision)
1. The seven VisDrone val sequences were read twice (static no-op first, bfa5caf; v3 second, 0af0066).
   The archive discloses this; Paper1_V12 describes them as evaluation sequences disjoint from calibration
   but does not state the second read. Add one sentence at revision.
2. The shuffled-schedule control (P1-SHUF) does not show that the controller's timing adds value beyond
   its action mix; V12 does not report this control. Report it or soften causal wording at revision.
3. The detector checkpoint is third-party (dronefreak/visdrone-yolo11m, AGPL-3.0, VisDrone-DET-trained);
   V12 cites it as a public VisDrone checkpoint; keep the licence disclosure in the data/code statement.

### Version history
| Version | Folder | Template | Main change | Pushed in |
|---|---|---|---|---|
| JRTIP drafts | research/acmot_paper_v2/manuscript_jrtip*, manuscript_jrtip_supervisor_rev1-rev9, blind_challenge_v1 | Springer sn-jnl | first journal drafts (tags jrtip-submission-v1/v2, v3f-paper-first-journal) | earlier |
| Paper1_V1-V3 | research/acmot_paper_v2/manuscript_jrtip_supervisor_rev10-rev12 | Springer | supervisor edit rounds | earlier |
| Paper1_V4 | research/acmot_paper_v2/Paper1_Springer_Template/Paper1_V4 | Springer | all 12 handwritten supervisor comments applied | 9151751 |
| Paper1_V5 | .../Paper1_Springer_Template/Paper1_V5 | Springer | leftover long forms (FP, IDS) fixed; sent to supervisor | 9151751 |
| Paper1_V6 (Springer) | .../Paper1_Springer_Template/Paper1_V6 | Springer | Algorithm 1 with Input/Output and step comments | b00ef64 |
| Paper1_V6_JAIS | research/acmot_paper_v2/Paper1_JAIS/Paper1_V6_JAIS | AIAA new-aiaa (journal) | conversion to AIAA, 30 pages | d916d78 |
| Paper1_V7_JAIS | .../Paper1_V7_JAIS | AIAA | AIAA rules: job titles, software references, no acronyms in title/abstract | f9001aa |
| Paper1_V8_JAIS | .../Paper1_V8_JAIS | AIAA | trimmed to 26 pages | f9001aa |
| Paper1_V9_JAIS | .../Paper1_V9_JAIS | AIAA | Algorithm 1 clarity | b00ef64 |
| Paper1_V10_JAIS | .../Paper1_V10_JAIS | AIAA | 3 more JAIS references (7 JAIS citations) | f3832a9 |
| Paper1_V11_JAIS | .../Paper1_V11_JAIS | AIAA | author titles changed | 67b543c |
| Paper1_V12_JAIS | .../Paper1_V12_JAIS | AIAA | final titles (Mohamed S. Mohamed Associate Professor, Tarek Ahmed Mahmoud Professor); abstract numbers as relative percentages (supervisor comment); SUBMITTED | 67b543c |
| Paper1_V13_JAIS | .../Paper1_V13_JAIS | AIAA | V12 + Acknowledgments with AI-assisted language editing statement; four sentences tightened to stay at 26 pages; numbers unchanged | e8428eb |

Handoff for the submission: `research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS/SUBMISSION_HANDOFF.md`
(manuscript ID, portal state, reviewer and associate-editor candidates,
declarations, cover letter). AIAA rules saved in JAIS_PAPERS/refs/aiaa_rules/.

### Supervisor comments applied (Paper1_V4/V5, then V12)
1. Title wording "... for Multi-Object Aerial Tracking".
2. No ";" after the last e-mail (Springer \email redefinition).
3. Abstract: add OATrack IDF1; later (V12) all abstract numbers as relative
   percentages ("raised by %").
4. "how the detector is run" -> "is running".
5. VisDrone: ten categories annotated, five used by the official MOT evaluation.
6. Units sentence: percent for HOTA/MOTA/IDF1/precision/recall, counts for
   IDS/FP/FN, FPS defined.
7. Higher-is-better / lower-is-better sentence at the end of the metrics section.
8. Method section in present tense.
9. Algorithm 1 checked against the frozen code; symbols unified with the equations.
10. Long constants rounded (tau_m = 0.297, tau_h = 0.511).
11. Shorter conclusion without re-defined abbreviations.
12. Every abbreviation short after its first definition (MOT, UAV, NMS, IoU,
    SCI, HOTA, MOTA).

### Submission state (from the ScholarOne review copy)
- JAIS, manuscript ID 2026-10-I012138, type Full Paper, submitted 18-Oct-2026,
  subject categories 03410 Uninhabited and Unmanned Air Vehicles; 12110
  Artificial Intelligence Systems; 14200 Signal Processing.
- Review copy = 1 cover page + the 26-page V12 manuscript (no Acknowledgments).
- Pending: both co-authors must confirm through the ScholarOne e-mail;
  declarations as entered are not in the review copy (check Author Center);
  if the AI-language question was answered Yes, use V13 at revision.
- The older unsubmitted 01-Oct draft "Calibration Versus Scene Switching ..."
  (JAIS_PAPERS/PAPER1_SCENE_ADAPTIVE_JAIS) is an earlier version of this paper
  and must not be submitted.
- Do not submit Paper 1 to a second venue while it is under review (the
  Springer-format Paper1_V6 has 42% 8-gram overlap with the JAIS version).

## Paper 2 — SCL / V7f (JRTIP)

### Claim and evidence
SCL reads the detector scores of recent frames (logits of frames t-10..t-1,
nested Otsu), decides clean or noisy from the median confident share rho,
keeps the tracker's settings on clean streams, remaps scores and sets the
thresholds on noisy streams, and adds a continuation rescue for single-stage
trackers. It is the frozen Universal AC-MOT V7f, the approved final version of the project (Amendment 10): tag universal-acmot-v7-freeze
(488df9a), config `configs/universal_acmot_policy_v7.json`, lock
`research/V7_POLICY_LOCK.json`, code acmot_v7.py. Evidence:
`research/final/V7_MAIN_RESULTS.md`, `research/final/V7_STATISTICS.md`,
`research/final/V7_EXPERIMENT_LEDGER.md`, `research/final/V7_ABLATION.md`,
`research/final/V7_EXTERNAL_SELECTION.md`, `research/final/V7_EXTERNAL_TRANSFER.md`,
`research/final/V7_DEV_RESULTS.json`, `research/final/V7_EXTERNAL_RESULTS.json`.

Headline results in Paper2_V11:
- MOT17 val-half: OC-SORT HOTA 66.428 -> 67.041 (+0.61, +0.9%), 7/7
  sequences; two-stage trackers identical or within 0.06 HOTA.
- External predeclared PD-SORT: HOTA 68.011 -> 68.624 (+0.61), MOTA +1.13,
  IDF1 +0.82; Hybrid-SORT identical output (reproduction CLOSE, 66.70 vs 67.1).
- Score shifts (floor 0.01): halving 0 -> 66.17 (ByteTrack official) and
  0 -> 66.72 (OC-SORT); 7 of 14 conditions significantly better, none worse.
- KITTI RT-DETR-L: MOTA ByteTrack +5.98 (+12.6%), BoT-SORT +7.86 (+16.3%);
  YOLOv8n OC-SORT HOTA +7.91.
- Runtime: SCL 2.95 ms per frame on a 4-vCPU CPU; pipeline 57.85 -> 60.44 ms.

### Version history
| Version | Folder | Main change |
|---|---|---|
| older variants | JAIS_PAPERS/PAPER2_UNIVERSAL_ACMOT_JAIS (AIAA, never submitted), JAIS_PAPERS/PAPER2_SIVP_SPRINGER (SIVP format) | earlier targets |
| challenge v1, full v1/rev1 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_v1, PAPER2_V7F_JRTIP_full_v1, PAPER2_V7F_JRTIP_full_rev1 | first JRTIP drafts |
| Paper2_V1-V8 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev1-rev8 | clarity rounds |
| Paper2_V9 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev9 | comparison table with recent methods (pushed 347577c) |
| Paper2_V10 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev10 | Paper 1 supervisor comments applied (e-mail ";", abbreviations, units, higher/lower better, Algorithm 1 check), AC-MOT reference title (pushed 9151751) |
| Paper2_V11 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11 | abstract as relative percentages (249 words), Algorithm 1 with Input/Output and comments, shorter conclusion, no re-defined SCL/AOB, "each tracker runs", AC-MOT reference = submitted JAIS title; 12 pages (pushed dbf162c; registered COMPLETED in VERSION_REGISTRY.md) |

### Internal reviewer audit of Paper2_V11 (2026-10-20), verified against the evidence
Open items to fix in Paper2_V12 (text only, no new experiments):
1. Development data missing from the data table: VisDrone val (7 sequences,
   YOLOv8n / RT-DETR-L, labelled and label-free) was used in development
   (ledger E20; the "noisy aerial stream, 26.9 vs 14.9 boxes/frame" in the
   ablation table). These are the same seven sequences Paper 1 evaluates on.
2. KITTI: the ledger has 6 host x detector cells; Paper2_V11 shows 3. Missing:
   ByteTrack-YOLOv8n (HOTA +0.06, MOTA -1.87), BoT-SORT-YOLOv8n (HOTA -1.02,
   MOTA -2.43 with interval below zero), OC-SORT-RT-DETR-L (HOTA +0.19,
   MOTA -0.57). The freeze decision names the YOLOv8n two-stage regression.
3. BoT-SORT KITTI sequence 0020: the caption says the unmodified tracker gives
   no valid output; the ledger (E19) records that the BoT-SORT Kalman update
   raised a Cholesky error when fed the layer's output, while the native run
   was valid. Must be described as a failure case, excluded from both arms.
4. Host-contract table: replace tau / "published" by values (a / b / l / m0):
   SparseTrack 0.6/0.7/0.1/0.85, BoostTrack 0.6/0.6/0.1/0.7, Hybrid-SORT
   0.6/0.6/0.1/0.75, PD-SORT 0.6/0.6/0.6/0.7; add BoT-SORT (KITTI, library
   contract 0.25/0.25/0.1/0.8).
5. Eq. 5 rank: mid-rank ECDF against a memory of the scores (after duplicate
   removal) of frame 1 and every 10th frame, last 20 samples; separate from
   the W = 10 statistics window; current-frame scores when the memory is empty.
6. Real-time wording: SCL adds 2.95 ms (4.5%); the full pipeline runs at about
   16.5 FPS in that test; do not call the whole system real-time.
7. Hybrid-SORT CLOSE cause: released detections fp16 vs README fp32 and the
   environment (documented as likely, not isolated).
8. External validation is on new trackers with MOT17 data and one detector,
   not on new data.
9. Springer rules: remove the submitted AC-MOT paper from the reference list
   (mention it in the text); add Statements and Declarations (funding,
   competing interests, data/code availability); note that intervals are
   per comparison without multiple-comparison correction.
10. Post-freeze predeclared recent externals are not reported in Paper2_V11: C-TWiX (Pattern
    Recognition 2025) KITTIMOT car −1.52 HOTA [−4.05, −0.13], MOT17 −0.05 and DanceTrack −1.00 (n.s.);
    TrackTrack (CVPR 2025) DanceTrack −0.012 HOTA [−0.032, −0.001]; TOPICTrack reproduction failed
    (`research/final/V7_RECENT_EXTERNAL_RESULTS.json`). Reporting only PD-SORT and Hybrid-SORT as
    "external" is selective; Paper2_V12 must report all predeclared external runs or state the selection.
11. Frozen V7f on VisDrone val-7 (development split, post-freeze run, `research/final/aerial_v7f_val/`)
    is positive (YOLOv8n HOTA +2.17 [+1.20, +3.58], internal protocol) and unreported; optional to add,
    labelled development evidence.
12. Figure fig3_forest_col.pdf of the JRTIP versions (md5 6d64acca…) has no generation script in the
    repository; fig4 and fig5 are byte-identical to the outputs of
    `JAIS_PAPERS/PAPER2_UNIVERSAL_ACMOT_JAIS/scripts/make_figures.py` (data module `scripts/evidence.py`).
Owner decisions still needed: funding statement, code-availability wording,
and whether new baselines (threshold-only, rescue-only, ACT, Adaptive
ByteTrack) are run before submission or at revision.

### Paper 2 claim map (Paper2_V11)
| Claim | Experiment | Result artifact | Config | Code | Commit | Dataset | Status |
|---|---|---|---|---|---|---|---|
| HOTA of two single-stage trackers +0.9% (OC-SORT dev, PD-SORT external) | P2-MOT17, V7-POST-PD | `research/final/V7_MAIN_RESULTS.json` (OC-SORT 66.428 → 67.041; PD-SORT 68.011 → 68.624) | configs/universal_acmot_policy_v7.json | acmot_v7.py, tools/v7/external/* | 488df9a | MOT17 val-half | VERIFIED |
| halved scores: both failing trackers recover ≥ 97% of original HOTA | P2-SHIFT | `research/final/paper2_calib_boot/calib_boot.json`; unshifted 67.698 / 66.428 in V7_DEV_RESULTS.json | same | tools/v7/ci/calib_boot.sh | 488df9a | MOT17, floor 0.01 | VERIFIED |
| RT-DETR-L MOTA +12.6% (ByteTrack), +16.3% (BoT-SORT) | P2-KITTI | `research/final/V7_STATISTICS.md` (47.265 → 53.241; 48.25 + 7.86) | same | tools/v7/kitti/kitti_eval.py | 488df9a | KITTI training | VERIFIED; omits the 3 non-positive cells (audit item 2) |
| two-stage well-matched hosts change < 0.1% | P2-MOT17, V7-POST-HS | V7_MAIN_RESULTS.json | same | same | 488df9a | MOT17 | VERIFIED |
| 2.95 ms per frame on a CPU | P2-RT | `research/final/V7_REALTIME_yolov8n.json` | same | tools/v7/benchmark.py | 488df9a | KITTI 3 seq | VERIFIED; "real-time" wording to narrow (item 6) |
| external validation | V7-POST-PD/HS (+ CTW/TOP/TT) | V7_EXTERNAL_RESULTS.json, V7_RECENT_EXTERNAL_RESULTS.json | same | tools/v7/external, tools/v7/recent | 488df9a | MOT17 (+ KITTIMOT, DanceTrack) | INCOMPLETE REPORTING (item 10) |
| AOB lowered strong trackers by 4.15–5.89 HOTA | P2-PRIOR | `research/final/EXTERNAL_PAPER_TRANSFER.md` (frozen V6-TF) | configs/universal_acmot_policy_v6tf.json | tools/v6/external/* | 2cff95f | MOT17 | VERIFIED (AOB = frozen V6-TF behaviour) |

### Paper 2 figure/table map (Paper2_V11 labels)
| Label | Content | Data source | Generated by |
|---|---|---|---|
| fig:arch, alg:layer, tab:symbols, tab:constants | method | acmot_v7.py, V7f config | TikZ / manual |
| tab:data, tab:metrics, tab:related, tab:contracts | protocol, metrics, related work, host contracts | V7_EXTERNAL_SELECTION.md, adapters | manual (contracts to be made numeric, audit item 4) |
| tab:prior, fig:prior (TikZ) | AOB vs SCL on strong hosts | EXTERNAL_PAPER_TRANSFER.md, V7_MAIN_RESULTS.json | manual / TikZ |
| tab:ablation | design steps and rejected versions | V7_ABLATION.md | manual |
| tab:mot17, fig:forest, fig:perseq | MOT17 development results | V7_MAIN_RESULTS.json, V7_MAIN_RESULTS.md Table 2 | fig:perseq = make_figures.py; fig:forest = script NOT FOUND (item 12) |
| tab:kitti | detector change | V7_STATISTICS.md | manual (3 of 6 cells) |
| tab:shift, fig:shift | score shifts | paper2_calib_boot/calib_boot.json | fig:shift = make_figures.py |
| tab:external | external systems | V7_EXTERNAL_RESULTS.json | manual |
| tab:runtime, fig:runtime (TikZ) | runtime | V7_REALTIME_yolov8n.json | manual / TikZ |

## Thesis
LaTeX and Word versions of the M.Sc. thesis live in THESIS/ (Word file
THESIS/word/Thesis_Ahmed_Gouda_Ismail.docx), last committed 2026-10-03,
before the Paper1_V4-V13 and Paper2_V10-V11 rounds.

## Version numbering (D-035)
Completed manuscript versions are read-only; the next version is created with
`python3 tools/version_registry.py new paper1|paper2` (exact copy of the latest completed version, parent and
commit recorded in research/VERSION_REGISTRY.json). Next: Paper 1 = Paper1_V14_JAIS, Paper 2 = Paper2_V12
(`JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev12`). Status of every version: VERSION_REGISTRY.md.
