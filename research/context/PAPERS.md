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
| Paper2_V47 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev47 | supervisor challenge copy, two columns, 15 pages: Sect. 3 rewritten on owner request to follow the Fig. 1 block diagram step by step, in simple wording: opening paragraph explains how to read the figure (top row = path of the detections through candidate choice and continuation rescue to the tracker; bottom row = score statistics, mode check, host contract, matching tolerance); 3.1 Inputs and outputs (logit, host contract, layer output = the arrows into the tracker); one subsection per step, each opening with its Input and Output as labelled in Fig. 1: 3.2 Step 1 score statistics, 3.3 Step 2 mode check, 3.4 Step 3 candidate choice (new label sec:choice; clean/cold and noisy modes), 3.5 Step 4 continuation rescue (rescued score just above l for a two-stage tracker, the lower of a_t and b_t for a single-stage one, checked against acmot_v7.py), 3.6 Step 5 matching tolerance (new label sec:motion); 3.7 host contract and adapters; 3.8 parameter values; Algorithm 1 comments now name Steps 1-5; Fig. 1 caption points to Sects. 3.2-3.6 and 3.7. All equations, values and results unchanged (only the illustrative 30-of-40 example removed for length); other sections identical to V46; same float placement as V46 (Discussion p11, Tables 9-11 and Conclusion p12, References p13); citation order Tables 1-11, Figs. 1-4; clean build (0 errors, 0 overfull, 0 undefined), zip identical to the PDF | not committed yet |
| Paper2_V48 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev48 | supervisor challenge copy, two columns, 15 pages: V47 with plainer headings and fewer references (owner request). Sect. 3 subsections renamed: 3.1 What SCL receives and returns, 3.2 Step 1: group the scores, 3.3 Step 2: clean or noisy?, 3.4 Step 3: choose candidates, 3.5 Step 4: rescue weak boxes, 3.6 Step 5: follow camera motion, 3.7 Connecting SCL to a tracker, 3.8 Fixed values of SCL; Fig. 1 block titles renamed to the same words (Group the scores, Clean or noisy?, Choose candidates, Rescue weak boxes, Follow camera motion); Sect. 4 renamed How SCL Was Developed (4.1 First design: always acting, 4.2 Improvements step by step, 4.3 Freezing before the tests). References 41 -> 36: removed wu2022uavsurvey, jiang2018chameleon, wang2024yolov9, carion2020detr, solano2025utrack (context-only citations); all 7 The Visual Computer references kept. Results and numbers unchanged; same float placement as V47; clean build, zip identical to the PDF | not committed yet |
| Paper2_V49 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev49 | anonymous copy of V48 (owner request, no names): author names, e-mails and affiliations removed from the title block; 'our earlier controller, AC-MOT' reworded to 'a separate controller, AC-MOT'; no identifying text left in the PDF, its metadata or the zip. Float barrier moved from before Sect. 5 to before Sect. 5.1 to avoid a gap on p7; 15 pages, all tables before the Conclusion, text and numbers otherwise identical to V48; clean build, zip identical to the PDF | not committed yet |
| Paper2_V50 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev50 | anonymous copy, supervisor notes applied to V49: headings as given by the supervisor (3.1-3.8, Sect. 4 SCL Development and Refinement 4.1-4.3, Sect. 5 Experimental Results and Evaluation 5.1-5.7 with the new 5.5 Component Ablation and Parameter Sensitivity, Sect. 6 Discussion and Practical Implications); Fig. 1 block titles matched (Logit partitioning, Stream classification, Candidate selection, Weak detection recovery, Motion-adaptive tolerance); Sect. 1 novelty and contributions rewritten around selective, host-aware adaptation; Sect. 2.3 new comparison paragraph and Table 1 (adaptive thresholding and score calibration vs SCL); Sect. 3.3 mode stability vs adaptation delay (N clean frames need more than N noisy frames; median over K frames bounds the delay to about K/2); Sect. 3.4 remap vs probability calibration; Sect. 4 note that the history is reported as recorded and post-freeze analyses changed no value; Sect. 5.4 logit-to-score check (E61) and stronger ACT description (coupling, HOSTCHK 84/14/40, no cell with SCL significantly below ACT in HOTA); new Sect. 5.5 with Table 11 (E58 ablation + E61 sensitivity, cells C3/C4/C5 as Table 9); Sect. 6 operational assumptions and limitations; Sect. 7 conclusion on detector-tracker compatibility. 17 pages, all tables before the Conclusion, clean build, zip identical to the PDF, no identifying text | not committed yet |
| Paper2_V51 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev51 | anonymous copy, V50 with the abstract rewritten on supervisor request in five parts (problem, method, novelty: selective host-aware adaptation, principal evidence: detector adaptation (halved scores >=97% HOTA recovered; RT-DETR-L MOTA +12.6%/+16.3%, IDS -43%/-47%) and cross-tracker transfer (PD-SORT unseen, four well-matched trackers within 0.1%), practical implication: 2.95 ms/frame, no retuning); same numbers as before; float barrier before Sect. 5.1 removed and Fig. 3 set to [!t] to avoid a gap; 17 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V52 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev52 | anonymous copy, V51 with the abstract checked and corrected (only the abstract changed): clean mode now described as keeping the scores and lowering a threshold only if it would reject the confident detections (the halved-score recovery comes from this cap; V51 said the thresholds are kept); weak detection recovery added to the method (mechanism behind the PD-SORT/OC-SORT gains); halved scores described as halved detector scores, not as a detector change; PD-SORT gain given (+0.9%); novelty split into short sentences; 250 words (Springer limit). Same numbers as V51; 17 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V53 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev53 | anonymous copy, V52 with the supervisor's red-text corrections (corr.docx): new paper-organization paragraph at the end of Sect. 1; new opening paragraphs of Sects. 4 and 5 (roadmaps of their subsections, Sect. 4 now defines AOB, so Sect. 4.1 no longer repeats the definition); the Sect. 3 opening paragraph in the file is identical to the existing text and stays unchanged; Sect. 2 had no red text. 17 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V54 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev54 | anonymous copy, V53 with the Sect. 3 opening paragraph (red in the supervisor's corr.docx) rewritten as a roadmap in the style of the new Sects. 4 and 5 openings: what SCL is, how Fig. 1 is read (top row Steps 3-4, bottom row Steps 1, 2, 5 and the host contract), Sect. 3.1 inputs and outputs, Sects. 3.2-3.6 Steps 1-5, Sect. 3.7 integration, Sect. 3.8 fixed parameters. Only this paragraph changed; 17 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V55 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev55 | anonymous copy, V54 with the Sect. 3 opening replaced by the red paragraph of the supervisor's corr.docx word for word (owner request: remove the old, put the file's text); this paragraph is identical to the one in V53, so the text of V55 equals V53 (checked: identical PDF text). 17 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V56 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev56 | anonymous copy, V55 with the Sect. 3 opening replaced by the owner's new paragraph (lightweight rule-based layer; Steps 1-5 described in order; host contract and unchanged tracker), word for word except frame $t$ in math. Layout kept at 17 pages: Fig. 1 defined right after Table 1 so both wide floats share p4 (removes a gap on p5 caused by the three-line Sect. 3.4 heading); three small trims after the floats: the result list of the Conclusion shortened to the main results (all numbers remain in Sect. 5), the Deployment sentence repeated from Sect. 3.7 and the last sentence of Limitations removed. Clean build, zip identical to the PDF | not committed yet |
| Paper2_V57 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev57 | anonymous copy, V56 with every figure and table made easier to read (owner request): the four result tables (MOT17, KITTI, external trackers, UAVDT) now show both runs, Host (tracker alone) and Host+SCL, next to the Change column (values read from V7_MAIN_RESULTS, V7_DEV_RESULTS, V7_EXTERNAL_RESULTS, V7_UAVDT_RESULT; BoT-SORT KITTI re-evaluated with kitti_eval V7_EXCLUDE=0020, equal to the paper; generated by scripts/make_ab_tables.py, which checks every Host value against the source); arrows mark higher/lower is better; other tables name what is compared in the headers (AOB - Host, SCL - Host, SCL - t2, SCL - ACT); every caption rewritten in simple English (what is compared, how to read each column, what bold and brackets mean); Fig. 3 shows each change as a number and the direction (alone better / with SCL better); new 'How to read the result tables' paragraph with a worked example at the start of Sect. 5; key results in the text given as 'from A to B'. No result changed; 18 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V58 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev58 | anonymous copy, V57 with Section 3 made easy to follow, every number traced to its source (owner request): new Table 2 'symbols in plain words' with the real values of Fig. 2a (MOT17-02 frame 101, ByteTrack official: 916 logits, t1 -0.78 (0.32), t2 0.95 (0.72), rho 175/263 = 0.67, median 0.63 clean, a 0.6, b 0.7, l 0.1, m0 0.8); host-contract table now wide with a column naming the published parameters behind each value (ByteTrack track_thresh/+0.1/match_thresh, Ultralytics bytetrack.yaml and botsort.yaml 0.25/0.25/0.1/0.8, SparseTrack, BoostTrack, Hybrid-SORT, OC-SORT, PD-SORT); worked examples with the actual numbers in every step: logit log 9 = 2.2, toy Otsu example with the real splits (t1 -1.67, t2 1.10 from nested_otsu), Fig. 2 counts (653/88/175 and 1037/99/83), background check, median over frames 2-101, clean cap min(0.6, 0.72), remap u 0.8 -> 0.9 and 0.3 -> 0.22, rescue 0.101 / 0.501, motion m_t = 0.9; Fig. 2 values recomputed with the frozen layer and checked against the run logs (scripts/make_fig_groups.py); captions of Figs. 1-2 and Table 4 extended. No result changed; 19 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V59 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev59 | anonymous copy, V58 with the supervisor's handwritten corrections from an older print applied to the latest text: abstract ', respectively' and 'adds on average no more than 2.95 ms' (2.95 ms is the recorded mean; P95 4.39), 250 words; introduction wording (HOTA of two trackers to 0, 'their authors', 'unchanged'); Sect. 2.2 new paragraphs before MOTA/IDF1 and before 'All metrics'; 'Figure' -> 'Fig.' in the text; Fig. 1 Step 2 drawn as a decision diamond (median of rho >= 0.5?) with Yes/clean and No/noisy branches; Fig. 2 lighter bars (light gray / light blue), panel titles under the panels, 'MOT17 sequence MOT17-02' and 'KITTI sequence 0001' in the caption; Fig. 4 frames cropped above the boxes and boxes drawn thicker with white outlines (clear in grayscale print); Algorithm 1 comments in round brackets; AOB-vs-SCL table full width with Host, Host+AOB, Host+SCL and changes on one line (scripts/make_tab_prior.py, values asserted against V7_DEV_RESULTS/V7_MAIN_RESULTS); half-up rounding of recorded 3-decimal values (44.175 -> 44.18, 51.785 -> 51.79, 71.725 -> 71.73, 66.525 -> 66.53; all 56 Host/Host+SCL cells re-checked; make_ab_tables.py fmt now half-up); ACT table panel (b) with UAVDT MOTA and IDS of ACT and SCL (E60 values, IDS intervals from V7_IDS_TABLES.json) so every number cited in Sect. 5.4 is in a table; baseline IDS and ACT FP numbers no longer cited in the text; Sect. 5.2 adds BoT-SORT +0.61 HOTA; conclusion in short sentences with a specific future-work sentence; references in title case, Bernardin volume removed. No result changed; 19 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V60 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev60 | anonymous copy, V59 in 16 pages (owner request) with the same content: only layout lines of main.tex changed (text block 160 x 240 mm instead of 160 x 216 mm, references in footnote size with 2 pt spacing, float spacing 9-10 pt, smaller space around section and subsection headings, floats flushed before the Conclusion); sections, tables, figures and references identical to V59 (same 49,430 letters in the PDF text, same numbers); all tables before the Conclusion, no large blank spaces; 16 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V61 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev61 | named copy of V60 (16 pages) with the author block as marked by the supervisor on the old print: author order Ahmed Gouda Ismail (1, corresponding), Tarek Ahmed Mahmoud (1), Mohamed S. Mohamed (2); affiliation numbers swapped, 1 = Computer Engineering Department, Egypt University of Informatics, 2 = Computer Engineering and Artificial Intelligence Department, Military Technical College; e-mails as in V48 in the new author order; Sect. 2.3 'our earlier controller, AC-MOT (submitted)' restored; everything else identical to V60; 16 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V62 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev62 | named copy, V61 with the affiliations corrected to those of Paper 1 and the ICMISI 2026 survey (owner first said V61 affiliations were wrong, then confirmed that the supervisor does want the V61 numbering, so V61 is the named copy to use and V62 is the alternative with the Paper 1 numbering): Ahmed Gouda Ismail (1, corresponding), Tarek Ahmed Mahmoud (2), Mohamed S. Mohamed (1); 1 = Computer Engineering and Artificial Intelligence Department, Military Technical College; 2 = Computer Engineering Department, Egypt University of Informatics; author order as marked by the supervisor; everything else identical to V61; 16 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V63 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev63 | named copy to use: author block exactly as marked by the supervisor, with every author at the right institution (owner: first author is MTC, not EUI): Ahmed Gouda Ismail (2, corresponding), Tarek Ahmed Mahmoud (1), Mohamed S. Mohamed (2); 1 = Computer Engineering Department, Egypt University of Informatics; 2 = Computer Engineering and Artificial Intelligence Department, Military Technical College (corresponding affiliation); everything else identical to V61/V62; 16 pages, clean build, zip identical to the PDF | not committed yet |
| Paper2_V64 | JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev64 | named copy to use: V63 with Fig. 4 boxes and ID labels drawn as in the first version of the figure (owner: the thick outlined boxes of V59-V63 looked heavy and their labels overlapped); thin coloured boxes (1.4 pt), plain ID labels, paths and dashed missed-object boxes as before; the crop above the boxes is kept; everything else identical to V63; 16 pages, clean build, zip identical to the PDF | not committed yet |

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
