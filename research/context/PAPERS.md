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
| Paper 2 | Training-Free Self-Calibrating Control Layer for Heterogeneous Multi-Object Trackers | SCL = frozen Universal AC-MOT V7f between a frozen detector and a frozen tracker | target The Visual Computer (Springer, ISSN 1432-2315; owner choice 2026-10-21, before: JRTIP) | NOT SUBMITTED; Paper2_V19 (= V18 + seven related The Visual Computer references; D-037, D-039 to D-042) for the supervisor and submission | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev19/ (Paper2_V19) |

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
| Paper2_V12 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev12 | for The Visual Computer: general Springer Nature template (sn-jnl, sn-mathphys-num, single column, 30 pages); audit items 1-10 and 12 fixed (VisDrone development data, all 6 KITTI cells, BoT-SORT 0020 failure, numeric contracts, rank memory, real-time wording, Hybrid-SORT cause, external scope, Statements and Declarations, submitted AC-MOT paper only in the text, all post-freeze externals incl. C-TWiX KITTI cars -1.52 and TrackTrack -0.013, regenerated fig3 with scripts/make_forest.py); item 11 (optional VisDrone val-7 result) not added; abstract 249 words; cover letter and author biographies; built from version_registry `new paper2` (exact copy of V11) | not committed yet; NOT USED by owner decision D-037 (it added content that V11 did not have) |
| Paper2_V13 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev13 | exact copy of V11 (same 12-page sn-jnl layout) with only: Statements and Declarations (required by The Visual Computer), the submitted AC-MOT paper moved from the reference list into the text (Springer rule), `CPU` written out in the abstract (no undefined abbreviations, 250 words), numeric host contracts instead of tau (+ BoT-SORT row), corrected KITTI caption for sequence 0020 (numerical error in the BoT-SORT Kalman update); cover letter and author biographies; integrity check against V11: equations, algorithm, figures, TikZ identical | not committed yet |
| Paper2_V14 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev14 | V13 content checked against The Visual Computer submission guidelines: standard sn-jnl two-column layout (custom margins, font and heading sizes removed; 17 pages), two tables narrowed to the standard column, CPU / GPU / GBI defined at first use, tables cited in numerical order (two early table references now point to their sections), no period at the end of figure captions, arXiv DOIs added; declarations confirmed by the owner (no funding, code on request); PDF compiled from the Overleaf main.tex (identical to the zip); integrity check against V13: numbers, equations, algorithm and figures unchanged | not committed yet |
| Paper2_V15 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev15 | V14 content checked against the official Springer Nature template package (Version 3.1, December 2024; sn-jnl.cls and sn-mathphys-num.bst byte-identical) and its user manual: single-column layout (iicol only when a journal asks for it), referee option (double line spacing for peer review), figure files on the same level as main.tex (no subfolder), the template's `algorithm` package, no float-tuning commands, all eight declaration headings (Consent for publication and Materials availability: Not applicable); four tables narrowed to the 131 mm text width and Fig. 1 scaled to the text width without other change; 36 pages, 0 errors, 0 overfull, 0 undefined; PDF compiled from the Overleaf main.tex (identical to the zip); integrity check against V14: all numbers, equations, algorithm and figure files unchanged | not committed yet |
| Paper2_V16 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev16 | V15 + the held-out VisDrone confirmation-16 result of the frozen V7f (E55, owner-authorized, D-041): new Table 1 row, data and metric sentences in Sect. 2, new Sect. 7.5 with Table 13, two VisDrone cells in Fig. 3 (regenerated by scripts/make_forest.py in the Paper2_V11 style, all earlier cells unchanged), "three datasets" in abstract, introduction and conclusion, VisDrone URL in Data availability, one sentence in the cover letter; 37 pages, 0 errors, 0 overfull, 0 undefined; zip identical to the PDF | not committed yet |
| Paper2_V17 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev17 | V16 checked line by line against The Visual Computer submission guidelines; two figure rules were not met and are now: figure parts lettered (Fig. 5 panels (a)-(d), regenerated by scripts/make_fig5.py with the Paper2_V11 data and style) and series distinguishable without color (Fig. 2 and Fig. 6 patterns, Fig. 3 filled/open markers, Fig. 5 hatching; captions updated); no number or other text changed; 37 pages, 0 errors, 0 overfull, 0 undefined; zip identical to the PDF | not committed yet |
| Paper2_V18 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev18 | V17 + the UAVDT test result of the frozen V7f (E56, owner-authorized, D-042): Table 1 row, data/role/metric sentences in Sect. 2, UAVDT paragraph in Sect. 7.5, UAVDT block in Table 13, two UAVDT cells in Fig. 3, "four datasets" in abstract, introduction and conclusion, UAVDT reference (du2018uavdt, DOI checked) and URL in Data availability, cover-letter sentence; 38 pages, 0 errors, 0 overfull, 0 undefined; zip identical to the PDF; no earlier number changed | not committed yet |
| Paper2_V19 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev19 | V18 + seven related articles of The Visual Computer (2024-2026; survey adzemovic2026survey, liang2024motiontrack, li2024fdbtrack, bao2024graphmatching, zhang2025sinkhorn, ding2025remot, sun2026bsr; metadata from Crossref, DOIs resolved, content from the abstracts) cited in the introduction and a new Related Work paragraph; lu2024uavdetection (unrelated federated-learning UAV detection, kept for the former JAIS target) no longer cited; 41 references; 39 pages, 0 errors, 0 overfull, 0 undefined; zip identical to the PDF | not committed yet |
| Paper2_V20 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev20 | owner-requested challenge copy for the supervisor (not for submission): V19 without the VisDrone result E55 (Table 1 row, data/metric/role sentences, Table 13 block, Fig. 3 group, URL, cover-letter mention), "three datasets", UAVDT paragraph without the missed-object sentence; 38 pages, clean build, zip identical to the PDF. The submission candidate remains Paper2_V19 with every result; E55 stays recorded | not committed yet |
| Paper2_V21 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev21 | supervisor copy: V20 with a writing polish in simple English: a short results paragraph in the introduction (numbers taken from the paper), neutral wording of the background check and of the variants not kept, MOTA and CPU defined at first use, stronger discussion and conclusion with the UAVDT result; no number or result changed (only rounded forms 24.7, 28.0, 3.3 of existing values); 39 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V22 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev22 | supervisor copy: V21 in the two-column layout (`iicol`), KITTI caption sentence about BoT-SORT sequence 0020 removed, "(20 sequences)" added to the BoT-SORT row; no number changed; 19 pages, clean build | not committed yet |
| Paper2_V23 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev23 | supervisor copy in the journal submission layout (single column + `referee`, as V19): V22 plus reference [19] fixed (publisher address of du2018uavdt, no "???"), the IoU-0.5 sentence for duplicates and rescue, the wording "no statistically significant HOTA loss in any tested cell", and a new Sect. 7.4 with Table 12 (E57 baselines, owner choice: only the cells C3-C5 where V7f is significantly above both baselines) and the E58 component results (rescue, mode decision, remap); C1 baseline cell and the MOTA comparisons (E57) not shown, as the owner asked for a positives-only supervisor copy; 40 pages, clean build, zip identical to the PDF. Paper2_V19 remains the submission candidate | not committed yet |
| Paper2_V24 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev24 | supervisor copy: the content of V23 in the two-column layout (`iicol`); only layout changes (document class, Table 12 full width); 19 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V25 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev25 | supervisor copy, two columns: V24 plus the exact definition of rho (over the logits of frames t-W..t-1, as in the frozen code; new symbol Z_t^W), Table 12 row spacing, Fig. 5 with larger horizontal axis labels (s^3, 0.5s, T=2, T=0.5), Sect. 7.4 renamed "Comparison with adaptive-threshold methods" with a paragraph on ACT (E59, owner choice: halved-score cells C4 and C5 only), ACT also in the introduction, contributions, conclusion and Table 1; 20 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V26 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev26 | supervisor copy, two columns: V25 plus the ACT comparison in ACT's own setting (MOT17, ByteTrack official, YOLOX-X) and on held-out UAVDT (E60): new Table 13 (ACT vs SCL, HOTA and IDF1 differences; KITTI halved-score rows of E59, both MOT17 floors, both UAVDT detectors), Sect. 7.4 paragraph rewritten (UAVDT RT-DETR-L MOTA +22.65), introduction and conclusion updated; KITTI normal-score ACT cells and MOTA cells where ACT was higher not shown (owner's positives-only choice; all in the result files); 20 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V27 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev27 | supervisor copy, two columns: V26 plus identity switches (IDS) in every result table (Tables 8, 10, 11, 12, 13, 14, 15, 16; counts with paired-bootstrap intervals, owner chose all tables; values and sources in `research/final/V7_IDS_TABLES.json`), IDS explained in the metrics table and the text (IDS read with FN: rises where more objects are followed), a new Table 1 of main terms in plain words, "host" defined in the introduction and every table caption, simpler wording of the abstract (247 words), data, related work, method, development and results; 22 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V28 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev28 | supervisor copy, two columns: V27 plus identity switches in the narrative (abstract 250 words, introduction, a method paragraph on how the layer helps identities, a discussion paragraph, conclusion) and all six figures redrawn to the journal's artwork rules (checked against the TVC submission guidelines page): separate files Fig1-Fig6.pdf at final size (76 or 160 mm), Helvetica/Arial-type lettering at 8-9 pt, lines >= 0.5 pt, colorblind-safe RGB colors with patterns or marker shapes (checked in grayscale), fonts embedded, captions without color words or end punctuation; same numbers; 23 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V29 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev29 | supervisor copy, two columns: V28 without the text of Sects. 7.7 (Running time) and 7.8 (Analysis), owner request; their runtime table and figure kept and cited from Sect. 4.7; clarity fixes (remap memory, motion history, ByteTrack official vs library setting, reason for BoT-SORT on 20 KITTI sequences as recorded in the ledger); two new figures: Fig. 2, the logits of the last 10 frames with the two Otsu splits for a clean (MOT17-02) and a noisy (KITTI 0001, RT-DETR-L) stream, computed by the frozen layer and checked equal to the stored per-frame logs, and Fig. 7, an example KITTI frame (sequence 0001, frame 102, read from the official archive, CRC-checked) with OC-SORT/YOLOv8n tracks alone vs with SCL (6 vs 9 of 10 objects; median-gain sequence, first frame with the largest gain); figure files renumbered Fig1-Fig8 in order of appearance; 23 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V30 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev30 | supervisor copy, two columns: V29 restructured to follow Paper 1's sections and style (owner request): 1 Introduction (Paper 1 flow, terms table), 2 Background and Related Work (2.1 Dataset Description with MOT17 / KITTI tracking / UAVDT subsections and the roles of the cells; 2.2 MOT Evaluation Metrics as equations in the text, owner's choice, metrics table dropped; 2.3 MOT Literature Survey), 3 Proposed SCL Framework (Overview and inputs; Selection of Parameter Values of SCL with a Value / Setting / Source table), 4 Development of the Final SCL (intro naming the three stages), 5 Results (setup in the intro; MOT17, KITTI, shifted scores, adaptive-threshold methods and ACT, frozen external trackers, frozen UAVDT transfer), 6 Discussion (short, owner's choice), 7 Conclusion with future work; abstract in Paper 1 sentence flow (249 words, same numbers), lowercase keywords as in Paper 1; no table or figure removed except the metrics table replaced by equations; result numbers unchanged from V29 (new facts only: 2,652 val-half frames and 8,008 KITTI training frames, checked on the ground-truth files; UAVDT description as in Paper 1); result floats allowed on float pages so all result tables appear before the Discussion; 26 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V31 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev31 | supervisor copy, two columns: V30 with the owner-pasted review applied as wording only (no algorithm or number change): clean/noisy defined as score-distribution modes, rho a heuristic indicator and not detection accuracy (intro, Sects. 3.2-3.3, terms table row); frozen host defined precisely (code, weights and stored settings unchanged; per-frame contract thresholds written into the tracker's existing parameters by the adapter, checked in tools/v7/external adapters); background-check reason stated as a heuristic; 0.5 mode level stated as a majority rule; whole-stream median trade-off (stable, slower to follow a lasting change; development evidence Sect. 4.2); rescue can pass a false box; constants called design choices, none chosen by a search (checked against V7_DEV_RESULTS variants); 'not on the dataset' replaced by a qualified statement; 'suitable for real-time' replaced by low overhead (+4.5% end to end, 60.44 ms pipeline); conclusion limited to the tested systems with the largest observed HOTA decrease 0.14 points; abstract states that gains are relative changes (249 words); interval-including-zero sentence and points/relative units in Sect. 2.2; host-only baseline named; 27 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V32 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev32 | supervisor challenge copy, two columns, positives-only (owner request): V31 without its self-critical caveat sentences (rho failure example, slower response of the whole-stream median, rescue can pass a false box, 'not the best values', interval-with-zero note, 0.14-point decrease and 'does not prove' note, dataset-influence clause, 60.44 ms pipeline remark); clean/noisy and rho framed as label-free score-distribution measures; identity-switch columns removed from the shift (now single-column), adaptive-threshold baseline (now single-column) and ACT tables, where SCL had more switches because it followed more objects (ByteTrack halved 501 vs 273/275; ACT KITTI halved +240/+214; shift-table host-vs-SCL counts); text keeps only true favourable IDS statements (OC-SORT vs baselines 170 vs 1,545/250 and 308 vs 1,975/492; vs ACT 18/22 fewer on MOT17, 185/418 fewer on UAVDT); PD-SORT FP +681 and ByteTrack-halved IDS sentences removed; KITTI OC-SORT +79 IDS kept in Table 11 and framed with 5,310 fewer missed objects and +9.60 IDF1; IDS kept in the host tables; no number changed; float settings tuned (floatpagefraction 0.8); 26 pages, clean build, zip identical to the PDF; V31 (all caveats) and the result files keep everything | not committed yet |
| Paper2_V33 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev33 | supervisor challenge copy, two columns, 25 pages (owner request, V32 had 26): V32 with tighter float spacing (floatsep/textfloatsep 12pt), the host-contract table made single-column (the identical 'decision mapped to' column moved into the caption: thresholds, candidates, scores), and shorter wording without dropping any result: background-check reason, adapter 'frozen' sentence, Discussion identity-switch and deployment paragraphs (the repeated 79/5,310 numbers stay in Results), survey intro last sentence, conclusion recap; no number changed; clean build, zip identical to the PDF | not committed yet |
| Paper2_V34 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev34 | supervisor challenge copy, two columns, 16 pages (owner request: 16 pages, shorten everything not needed): text cut by about 45% with every result kept (intro, background with datasets, three metric equations and a compact survey, method, development, results, discussion, conclusion); removed as duplicates or non-essential: terms table, data table, related-work table, symbols table, running-time figure (its table kept), AOB bar figure (its table kept), per-sequence heat map, shifted-score bar figure (its table kept); constants table single-column; figures renumbered Fig1 architecture, Fig2 score groups, Fig3 forest, Fig4 KITTI example (regenerated by the version's scripts, same content as V33 Fig5/Fig7); 12 tables, 4 figures, abstract unchanged (249 words); no number added (all numbers are a subset of V33); clean build, zip identical to the PDF | not committed yet |
| Paper2_V35 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev35 | supervisor challenge copy, two columns, 15 pages (owner request): Fig. 4 (KITTI 0001 frame 102, OC-SORT/YOLOv8n) now shows tracking, not only detection: each output track's path over the last 20 frames (bottom centre of its box, from the same run's track file) is drawn with its ID, caption says IDs are numbered separately per run (scripts/make_fig_kitti_example.py, 6 vs 9 of 10 objects unchanged); text condensed further without removing a result (intro results paragraph, MOT17/KITTI/ACT/ablation sentences, results intro, inputs paragraph, freeze, discussion, conclusion) and shorter declarations; all numbers already in V33; clean build, zip identical to the PDF | not committed yet |
| Paper2_V36 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev36 | supervisor challenge copy, two columns, 15 pages: V35 without the Statements and Declarations section (owner request; funding, competing interests, ethics, consent, data, materials, code availability, author contributions; the journal requires these at submission, the text is kept in Paper2_V35); nothing else changed; clean build, zip identical to the PDF | not committed yet |
| Paper2_V37 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev37 | supervisor challenge copy, two columns, 15 pages: Fig. 4 redrawn to show tracking (owner request): KITTI 0001, OC-SORT/YOLOv8n alone vs with SCL at frames 92, 97, 102 (3x2 panels), each track ID with its own colour kept over the frames and its path over the previous 20 frames; per-frame tracked counts 5/13 vs 6/13 (92), 5/12 vs 6/12 (97), 6/10 vs 9/10 (102), computed by scripts/make_fig_kitti_example.py from the run track files and the KITTI labels; frames 92 and 97 read from the official KITTI archive (CRC-checked; sha256 2e8fe3f2..., 713e59f7...), frame 102 re-read and identical to the stored copy; caption and one sentence updated; no other change; clean build, zip identical to the PDF | not committed yet |
| Paper2_V38 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev38 | supervisor challenge copy, two columns, 15 pages: owner-pasted review of V37 (Major Revision) applied as wording only, positives-only (owner request; no ablation table added, since every form of it has cells where removing a part does not lower HOTA, E58 file research/final/V7_REVIEWER_BASELINES_ABLATION_RESULT.json): M1 clean mode described as a minimal intervention (scores kept, Eq. 7 cap, identical output when the confident group lies above the host thresholds and no rescue applies) in abstract, intro, contribution, method, development, conclusion; M2 positive note that the splits and the clean-mode cap follow a score-scale change within W frames; M3 ACT run without retuning; M6 'no HOTA decrease was detected' and 'no statistically detected HOTA loss'; minor: remap mid-rank defined from acmot_v7.py (_ecdf: scores kept at frame 1 and every 10th frame, last 20, ties averaged), r_t = 1 during warm-up or zero median (online_calibration.RobustHistory.ratio), whole-stream median storage, frozen host defined; rescue ablation value corrected 3.34 -> 3.35 (44.175 - 40.828 in the E58 points); clean build, zip identical to the PDF | not committed yet |
| Paper2_V39 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev39 | supervisor challenge copy, two columns, 15 pages: V38 without Sect. 3.7 'Per-frame steps and cost' (owner request; heading, complexity and storage text removed); Algorithm 1 and the running-time table kept and cited from the end of Sect. 3.6; intro reference moved to Sect. 3.6; no number changed; clean build, zip identical to the PDF | not committed yet |
| Paper2_V40 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev40 | supervisor challenge copy, two columns, 15 pages: V39 without the running-time table (owner request); the runtime numbers kept in the text (2.95 ms, 42 ms detector, tracker 2.04 -> 1.43 ms, +4.5% end to end) with the measurement setting stated in the Discussion (4-vCPU Xeon 2.10 GHz, no GPU, YOLOv8n + ByteTrack, three KITTI sequences, 2,279 timed frames); intro reference moved to the Discussion; 11 tables; clean build, zip identical to the PDF | not committed yet |
| Paper2_V41 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev41 | supervisor challenge copy, two columns, 15 pages: V40 with the abstract shortened below 250 words (owner counted 251 by spaces in the PDF; now 246 by the same count, 244 in the source), same numbers and meaning; nothing else changed; clean build, zip identical to the PDF | not committed yet |
| Paper2_V42 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev42 | supervisor challenge copy, two columns, 15 pages: V41 with the meaning of the logit and the reason for using it in Sect. 3.1 (owner request, owner's sentence: log-odds transformation, unrestricted scale, order preserved; examples 0.5 -> 0, 0.9 -> 2.2, 0.1 -> -2.2; reasons: scores crowd near 0 and 1 so the splits separate the groups more clearly, and a temperature change is a stretch of the logits that the splits follow) and a forward reference from Sect. 2.1; clean build, zip identical to the PDF | not committed yet |
| Paper2_V43 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev43 | supervisor challenge copy, two columns, 15 pages: reader-clarity edits only (owner request): intro numeric example (ByteTrack official, birth 0.7, a 0.9 score halved to 0.45, HOTA 67.70 -> 0, with SCL 66.17; mode-agnostic wording), a paragraph at the start of Sect. 3 tracing one detection through SCL, 'clean/noisy describe the score distribution, not whether a single detection is correct', why Otsu and a nested Otsu example on seven scores (computed: background 0.02/0.03/0.05, uncertain 0.4/0.5, confident 0.9/0.95, rho 0.5), and that the rescue only makes a box visible while the tracker's own matching decides; no method or result change; clean build, zip identical to the PDF | not committed yet |
| Paper2_V44 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev44 | supervisor challenge copy, two columns, 16 pages: float placement fixed (owner request): \FloatBarrier (placeins) before Results and before Discussion, tables allowed on float pages, float-page fractions 0.5; every development table now precedes the Results heading and every result table precedes the Discussion, none after the References start (V43 had Tables 5-7 after the Discussion and 9-11 after References); text unchanged; 16 pages instead of 15 (forcing the floats adds space); clean build, zip identical to the PDF | not committed yet |
| Paper2_V45 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev45 | supervisor challenge copy, two columns, 15 pages: large blank spaces of V44 removed (owner request, option "no blank spaces, 15 pages"): \FloatBarrier before Results and before the back matter only, float-page fractions 0.8, float pages start at the top, single-column tables [!htbp], wide tables [!tp]; Tables 3-4 placed at the start of Sect. 4 with Table 3 cited in the Sect. 4 opening sentence (only text change: "(Table~3)"); result tables placed after Table 6; all 11 tables cited in order and placed before the Conclusion and References (Tables 9-11 at the top of p12, after the first Discussion paragraph); no blank gap except the end of the last page; text and numbers otherwise identical to V44; clean build (0 overfull, 0 undefined), zip identical to the PDF | not committed yet |
| Paper2_V46 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev46 | supervisor challenge copy, two columns, 15 pages: Fig. 1 (block diagram of SCL) redrawn on owner request (old one unclear): numbered steps 1-5 (score statistics, mode check, candidate choice, continuation rescue, matching tolerance), frozen detector and tracker, host contract; every arrow labelled with the data it carries (frame I_t, D_t boxes and scores, t1/t2/rho_t, mode, a/b/l/m0, K_t, scores, a_t/b_t, m_t, frames I_{t-1}/I_t, tracks T_t); dashed arrows = data kept from earlier frames (logits for later frames, tracks T_{t-1}); a_t, b_t, m_t now shown as outputs of the layer (V45 drew them from the host contract); caption shortened to point to Sects. 3.2-3.5. Layout kept at 15 pages without big gaps: Fig. 4 defined at the start of Sect. 5.2 and single-column tables [!tb]; all tables before the Conclusion and References (Tables 9-11 at the top of p12 as in V45). Text and numbers otherwise identical to V45; citation order Tables 1-11, Figs. 1-4; clean build (0 overfull, 0 undefined), zip identical to the PDF | not committed yet |

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
Status 2026-10-21: items 1-10 and 12 are fixed in Paper2_V12 (The Visual Computer). Paper2_V12 states: no
funding; no competing interests; data public, results and code on reasonable request; author contributions
(Ismail: conceptualization to draft; Mohamed and Mahmoud: supervision, review); new baselines not run and
named as a limitation. These statements are the defaults written into V12 and must be confirmed by the owner
before submission.

### Paper 2 claim map (Paper2_V11)
| Claim | Experiment | Result artifact | Config | Code | Commit | Dataset | Status |
|---|---|---|---|---|---|---|---|
| HOTA of two single-stage trackers +0.9% (OC-SORT dev, PD-SORT external) | P2-MOT17, V7-POST-PD | `research/final/V7_MAIN_RESULTS.json` (OC-SORT 66.428 → 67.041; PD-SORT 68.011 → 68.624) | configs/universal_acmot_policy_v7.json | acmot_v7.py, tools/v7/external/* | 488df9a | MOT17 val-half | VERIFIED |
| halved scores: both failing trackers recover ≥ 97% of original HOTA | P2-SHIFT | `research/final/paper2_calib_boot/calib_boot.json`; unshifted 67.698 / 66.428 in V7_DEV_RESULTS.json | same | tools/v7/ci/calib_boot.sh | 488df9a | MOT17, floor 0.01 | VERIFIED |
| RT-DETR-L MOTA +12.6% (ByteTrack), +16.3% (BoT-SORT) | P2-KITTI | `research/final/V7_STATISTICS.md` (47.265 → 53.241; 48.25 + 7.86) | same | tools/v7/kitti/kitti_eval.py | 488df9a | KITTI training | VERIFIED; omits the 3 non-positive cells (audit item 2) |
| two-stage well-matched hosts change < 0.1% | P2-MOT17, V7-POST-HS | V7_MAIN_RESULTS.json | same | same | 488df9a | MOT17 | VERIFIED |
| 2.95 ms per frame on a CPU | P2-RT | `research/final/V7_REALTIME_yolov8n.json` | same | tools/v7/benchmark.py | 488df9a | KITTI 3 seq | VERIFIED; "real-time" wording to narrow (item 6) |
| external validation | V7-POST-PD/HS (+ CTW/TOP/TT) | V7_EXTERNAL_RESULTS.json, V7_RECENT_EXTERNAL_RESULTS.json | same | tools/v7/external, tools/v7/recent | 488df9a | MOT17 (+ KITTIMOT, DanceTrack) | INCOMPLETE REPORTING in V11 (item 10); COMPLETE in V12 (tab:external generated from the JSON by scripts/make_external_table.py) |
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

Thesis V2 (2026-10-23, owner request: thesis in the layout of the faculty prototype
thesis_ibrahim_bassiony_v3.docx with the owner's content): THESIS_V2/ holds the LaTeX source
(main.tex, chapters/ch1-ch5, frontmatter/, arabic/arabic_summary.tex, figures/, references.bib merged
from Paper1_V13, Paper2_V45 and THESIS) and the Word build (word/build_all.sh: LaTeX numbering ->
prep_latex.py -> pandoc -> make_images.py -> build_docx.py with the prototype .docx as template ->
LibreOffice index pass -> second pass -> PDF). Deliverables: THESIS_V2/word/Thesis_Ahmed_Gouda_Ismail.docx
and .pdf (83 pages). Structure of the prototype: cover and approval pages, Abstract, Acknowledgments,
Contents, List of Figures/Tables/Abbreviations, Ch.1 Introduction (Overview, Motivation and Challenges,
Problem Statement, Proposed Solution, Thesis Organization), Ch.2 Background and Literature Review
(with a literature comparison table), Ch.3 Proposed Training-Free Adaptive Control Approach (AC-MOT from
Paper1_V13, SCL from Paper2_V45, each with its development), Ch.4 Experimental Results and Performance
Evaluation (setup, AC-MOT results, SCL results, comparison with existing approaches, discussion), Ch.5
Conclusions and Future Work, References (105, IEEE style), Publications (Paper 0 published, Paper 1 under
review at JAIS, Paper 2 to be submitted to The Visual Computer), Arabic summary and Arabic title page.
Numbers are copied from Paper1_V13 and Paper2_V45 (every table checked number by number against its
source table); no new experiments. Checks: LaTeX build 0 errors / 0 undefined; 131/131 contents and
list entries on the right page; Office schema validation passed against the template; no template
text left. The prototype .docx (another student's thesis) is not stored in the repository.

## Version numbering (D-035)
Completed manuscript versions are read-only; the next version is created with
`python3 tools/version_registry.py new paper1|paper2` (exact copy of the latest completed version, parent and
commit recorded in research/VERSION_REGISTRY.json). Next: Paper 1 = Paper1_V14_JAIS, Paper 2 = Paper2_V12
(`JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev12`). Status of every version: VERSION_REGISTRY.md.
