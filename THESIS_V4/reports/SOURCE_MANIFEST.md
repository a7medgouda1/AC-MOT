# Thesis V4 — Source-of-Truth Manifest

Thesis: *Real-Time Target Detection and Tracking* (M.Sc., Ahmed Gouda Ismail); Arabic title: الكشف عن الأهداف وتتبعها في الزمن الحقيقي.
Version folder: `THESIS_V4/` (new; built from a copy of `THESIS_V3/`, which stays unchanged).
Repository state when V4 was written: branch `sci-v7f-general-layer-dev`, HEAD `eb1ba76`.

Supervisor numbering used below: **Paper 1 = Survey, Paper 2 = AC-MOT, Paper 3 = SCL**.
(In the repository records the same works are called Paper 0, Paper 1 and Paper 2.)

## 1. Authoritative manuscripts

| Supervisor no. | Work | Status (verified in repo) | Authoritative file used | Notes |
|---|---|---|---|---|
| Paper 1 | Survey: *Real-Time Object Detection and Tracking: Challenges, Innovations and Future Directions* | PUBLISHED, IEEE ICMISI 2026, pp. 119–125, DOI 10.1109/ICMISI69868.2026.11583994 | `research/published_papers/Survey_ICMISI26/Survey_Camera_Ready_ICMISI26.pdf` (7 pages, camera-ready) and `CITATION.md` | Only the PDF exists (no LaTeX source). Read in full (text extraction). |
| Paper 2 | AC-MOT: *Optimization-Guided Adaptive Detector Operating-Point Control for Multi-Object Aerial Tracking* | SUBMITTED to JAIS, 18-Oct-2026, manuscript ID 2026-10-I012138; submitted file = Paper1_V12_JAIS | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS/main.tex` (+ `references.bib`) | V13 = V12 + Acknowledgments; `diff` V12↔V13 shows only wording in the Discussion/Conclusion and the Acknowledgments; all numbers, tables, equations identical. Read in full. |
| Paper 3 | SCL: *Training-Free Self-Calibrating Control Layer for Heterogeneous Multi-Object Trackers* | SUBMITTED to The Visual Computer, 26-Oct-2026, submission ID aedd6959-d96a-4fb8-8868-35bd46b654a5 (CHANGELOG 2026-10-26; owner confirmation) | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev71/main.tex` and the files it actually inputs: `sections/01_introduction, 02_background, 03_method, 04_development, 05_results, 06_discussion, 07_conclusion` and `tables/tab_symbols, tab1_contracts, tab_compare, tab_prior, tab6_ablation, tab3_mot17, tab4_kitti, tab_shift, tab_baselines, tab_act, tab_compabl, tab_generalization`; figures `Fig1.pdf`–`Fig4.pdf` | The folder also holds unused leftover files (`sections/02_data, 03_related, 05_setup, 06_results, 07_discussion, 08_conclusion`, `tables/tab_visdrone` etc.). They are **not** the submitted text and were not used as thesis evidence. |

Version check: Paper2_V71 is the latest Paper 2 folder and the one recorded as submitted; it was not assumed from its number alone (CHANGELOG line of 2026-10-26 and the owner's submission confirmation).

## 2. Experimental evidence behind the submitted numbers

### AC-MOT (Paper 2) — frozen AC-MOT v3, tag `acmot-v3-exp-2026-10-04-freeze` → 280b4a2
| Result in thesis | Evidence file (repo) |
|---|---|
| VisDrone val-7 results, Table 3.9, Fig. 3.2 | `research/acmot_paper_v2/SECOND_VAL_READ_V3_RESULT.json`, `research/acmot_paper_v2/BASELINE_SYSTEMS_RESULT.json` |
| Paired bootstrap, Table 3.10 | `research/acmot_paper_v2/BOOTSTRAP_V3_RESULT.json`, `research/acmot_paper_v2/UAVDT_BOOTSTRAP_V3_RESULT.json` |
| UAVDT transfer, Table 3.11, Fig. 3.3 | `research/acmot_paper_v2/UAVDT_TRANSFER_RESULT.json` |
| Runtime 4.26 / 4.20 ms | `research/acmot_paper_v2/V3_RUNTIME_BENCHMARK_RESULT.json` |
| τm, τh, action map, fold table (Tables 3.1, 3.2, 3.7) | `research/acmot_paper_v2/controller_search/V3_JOINT_SEARCH_RESULT.json`, `.../FREEZE_MANIFEST_V3_ADAPTIVE.json` |
| Historical profiles, historical UAVDT, U2MOT, SparseTrack (Tables 3.3–3.6) | `research/paper_split/evidence/legacy/`, `research/transfer_legacy/` (HISTORICAL; transcribed in the paper, labelled historical in the thesis) |
| Full experiment archive | `research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/` |

### SCL (Paper 3) — frozen V7f, tag `universal-acmot-v7-freeze` → 488df9a
| Result in thesis | Evidence file (repo) |
|---|---|
| MOT17, KITTI, shifted scores (Tables 4.7–4.9, Fig. 4.3) | `research/final/V7_MAIN_RESULTS.json`, `research/final/V7_DEV_RESULTS.json`, `research/final/paper2_calib_boot/calib_boot.json` |
| External trackers (Table 4.10) | `research/final/V7_EXTERNAL_RESULTS.json` |
| Held-out UAVDT (Table 4.11) | `research/final/V7_UAVDT_RESULT.json` |
| ACT comparison (Tables 4.13, 4.14) | `research/final/V7_ACT_COMPARISON_RESULT.json`, `research/final/V7_ACT_ORIGINAL_UAVDT_RESULT.json` |
| Otsu baselines, ablation (Tables 4.12, 4.15) | `research/final/V7_REVIEWER_BASELINES_ABLATION_RESULT.json` |
| Sensitivity analysis (Table 4.15, lower part) | `research/final/V7_SENSITIVITY_RESULT.json` |
| Runtime 2.95 ms | `research/final/V7_REALTIME_yolov8n.json` |

Numbers in the thesis were copied from the submitted manuscripts (Section 3 of the QA report lists the automatic check); the result files above were consulted directly only for the two values listed in the QA report.

## 3. Chapter-by-chapter mapping

| Thesis part | Source(s) | How used |
|---|---|---|
| Ch. 1 Introduction (1.1–1.5) | Survey §I–IV, IX–X; Paper 2 §1 (Introduction); Paper 3 §1 (Introduction); demonstrated effects from Paper 2 results and Paper 3 results | Newly written synthesis; research questions RQ1–RQ3 and Table 1.1 are new framing, no new results. |
| Ch. 2 §2.2 Technical background | Survey §I–VIII (taxonomy, problem definition, detectors, trackers, datasets, metrics); Paper 2 §2.1–2.2 (datasets, metric equations, bootstrap); Paper 3 §2.1–2.2 (MOT17/KITTI/UAVDT, TrackEval, bootstrap); Paper 3 §3.2 (logit), Otsu equation from THESIS_V3 | Reorganized into 2.2.1–2.2.8; survey tables I–III not reproduced (see gap report). |
| Ch. 2 §2.3 Related work | Paper 2 §2.3 (tracking by detection in aerial MOT, adaptive thresholds, adaptive inference, optimization tools, Table "related"); Paper 3 §2.3 (related work, Table "compare"); THESIS_V3 literature table | Organized by theme; Table 2.4 merges the comparison tables of both papers and V3. |
| Ch. 3 AC-MOT | Paper 2 abstract (chapter opening), §3 (method), §4 (development), §5 (results), §6 (discussion), §7 (conclusion) | Paper's Introduction/Related Work not reproduced. Eq. 3.3 (search objective) restates the paper's text "cross-validated mean change in HOTA against the baseline". |
| Ch. 4 SCL | Paper 3 abstract (chapter opening), §3 (method), §4 (development), §5 (results), §6 (discussion), §7 (conclusion) | Paper's Introduction/Related Work not reproduced. §4.2 (problem setting) is new framing of the paper's content. |
| Ch. 5 Conclusions and Future Work | Conclusions of all three papers; future work of Paper 2 (§7: more detectors, trackers, datasets) and Paper 3 (§7: end-to-end trackers, running check), plus two directions carried from THESIS_V3 (combined pipeline, onboard processors) phrased as not yet done | Integrated synthesis. |
| Publications page | `CITATION.md` (survey); SUBMISSION_HANDOFF.md (Paper 2); Paper2_V71 author block (Paper 3: Ismail, Mahmoud, Mohamed) | Statuses: published / submitted (under review). |

## 4. Figures and tables

| Thesis item | Source asset |
|---|---|
| Fig. 1.1 TBD pipeline, Fig. 1.2 outline, Fig. 2.1 score stages | TikZ sources in `THESIS_V4/figures/` (from THESIS_V2/V3; outline labels updated to the new chapter numbers) |
| Fig. 3.1 AC-MOT pipeline, Figs. 3.2–3.3 bar charts | TikZ in `THESIS_V4/figures/` reproducing Paper 2 figures with the paper's values |
| Fig. 4.1 SCL architecture, Fig. 4.2 score groups, Fig. 4.3 forest plot, Fig. 4.4 KITTI example | Paper2_V71 `Fig1.pdf`–`Fig4.pdf` (copied as `scl_*_v3.pdf`, unchanged) |
| Algorithms 3.1, 4.1 | Paper 2 Algorithm 1; Paper 3 Algorithm 1 |
| Tables 2.1–2.4 | literature (V3 tables, Paper 2 Table "related", Paper 3 Table "compare") |
| Tables 3.1–3.11 | Paper 2 tables (actions, constants, quality, identity, hist-uavdt, u2mot, folds, visdrone, bootstrap, uavdt); Table 3.8 (setup) is a new summary of the paper's setup text |
| Tables 4.1–4.15 | Paper 3 tables (symbols, contracts, constants, prior, ablation, mot17, kitti, shift, generalization a/b, baselines, act a/b, compabl); Table 4.6 (setup) is a new summary of the paper's setup text |
| Table 5.1 | summary of Tables 3.9, 3.11, 4.7–4.11 |
