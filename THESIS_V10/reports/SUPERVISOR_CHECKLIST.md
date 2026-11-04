# Thesis V5 — Supervisor Requirements Checklist

Status: DONE = present and checked; PARTIAL = present with a note; OPEN = needs the owner.

## Overall structure
| Requirement | Where | Status |
|---|---|---|
| Exactly five chapters in the required order | Ch.1 Introduction; Ch.2 Background and Related Work; Ch.3 AC-MOT; Ch.4 SCL; Ch.5 Conclusions and Future Work | DONE |
| Paper 1 (Survey) → background; Paper 2 (AC-MOT) → Ch.3; Paper 3 (SCL) → Ch.4 | Publications page states the mapping; Ch.2 §2.1 cites the survey as the basis of §2.2 | DONE |
| One coherent research story, not concatenated papers | §1.1 (research direction), §1.3 (relation of the two problems), §1.4 (narrative), chapter openings/summaries link 2→3→4→5 | DONE |
| Contents, List of Figures, List of Tables, List of Abbreviations | Word front matter (page numbers checked: 126/126 entries correct) | DONE |
| Thesis title *Real-Time Target Detection and Tracking* on all title pages, abstract, keywords and Arabic summary | Word front matter; Ch.1 §1.1 | DONE |

## Chapter 1 — Introduction
| Item | Section | Status |
|---|---|---|
| 1.1 Overview: computer vision and detection, MOT, UAV context, detector–tracker interaction, reliability, direction linking AC-MOT and SCL | §1.1, Fig. 1.1 | DONE |
| 1.2 Motivation and Challenges from all three papers; demonstrated vs general motivation separated | §1.2 (each paragraph says whether it is literature-based or demonstrated in Ch.3/Ch.4), challenge list | DONE |
| Scene complexity, small/crowded objects, motion/occlusion/degradation, operating-point sensitivity, score dependence, variation across detectors/trackers/datasets, limits of fixed settings | §1.2 paragraphs 2–8 | DONE |
| 1.3 Problem Statement: overall problem, shortcomings, research questions, relation of AC-MOT and SCL, formal notation only where grounded | §1.3 (RQ1–RQ3; notation from the two papers) | DONE |
| States that AC-MOT and SCL are different and neither replaces the other | §1.3 last paragraph | DONE |
| 1.4 Solution Approach: A. AC-MOT, B. SCL — intervention point, mechanism, inputs, outputs, assumptions, scope; novelty vs reused components | §1.4, Fig. 1.2, Table 1.1, contribution list, last paragraph of §1.4 | DONE |
| 1.5 Thesis Organization matching the final chapters | §1.5 | DONE |

## Chapter 2 — Background and Related Work
| Item | Section | Status |
|---|---|---|
| 2.1 Introduction with roadmap and why it is needed for Ch.3/Ch.4 | §2.1 | DONE |
| 2.2 Technical background (survey + papers) | §2.2.1 detection fundamentals (IoU, NMS, operating point, AP/mAP); §2.2.2 detectors (incl. YOLO11m, YOLOX-X, YOLOv8n, RT-DETR-L used here); §2.2.3 MOT fundamentals; §2.2.4 TBD architectures/paradigms; §2.2.5 association and track management (incl. ByteTrack, OC-SORT, BoT-SORT, SparseTrack, BoostTrack, PD-SORT, Hybrid-SORT, OATrack, U2MOT); §2.2.6 confidence scores, calibration, logit, Otsu; §2.2.7 aerial challenges and datasets; §2.2.8 metrics (MOTA, IDF1, HOTA, IDS, …) and protocols | DONE |
| 2.3 Related Work as a dedicated section near the end, by theme, deduplicated | §2.3.1 TBD and aerial MOT; §2.3.2 adaptive inference; §2.3.3 adaptive thresholds; §2.3.4 score calibration and tracker interfaces; §2.3.5 comparison and gap | DONE |
| Comparison table with properties and limitations | Table 2.4 | DONE |
| 2.4 Chapter Summary with transition to Ch.3 | §2.4 | DONE |

## Chapter 3 — AC-MOT (Paper 2)
| Item | Section | Status |
|---|---|---|
| No separate Introduction/Related Work copied from the paper; opening from the abstract | §3.1 | DONE |
| Objectives, problem formulation, requirements | §3.2 (Eqs. 3.1–3.3) | DONE |
| Architecture, signals, mechanisms, constraints, algorithm, equations | §3.3, Fig. 3.1, Algorithm 3.1, Eqs. 3.4–3.12 | DONE |
| Frozen final configuration clearly identified | Tables 3.1, 3.2; §3.4.4 | DONE |
| Development path; historical results labelled as historical | §3.4 (first three stages explicitly historical, own baselines, not pooled) | DONE |
| Experimental setup, datasets, protocols, baselines | §3.5, Table 3.8 (splits also in Table 2.3) | DONE |
| Main quantitative results | §3.6, Tables 3.9–3.11, Figs. 3.2–3.3 | DONE |
| Ablation | §3.4 states that the cue audit and score-threshold sweep act as the ablation; the paper has no separate ablation table | PARTIAL (as in the paper) |
| Cross-tracker / cross-dataset validation | ByteTrack and OATrack; UAVDT transfer; historical U2MOT and SparseTrack | DONE |
| Runtime | §3.6.4 | DONE |
| Interpretation, scope, summary | §3.7, §3.8 | DONE |

## Chapter 4 — SCL (Paper 3)
| Item | Section | Status |
|---|---|---|
| No paper Introduction/Related Work; short opening from the abstract | §4.1 | DONE |
| Problem setting specific to SCL; label-free and causal requirements | §4.2 | DONE |
| Design: score-distribution analysis, Otsu, clean/noisy branching, score transformation, threshold control, recovery, motion tolerance | §4.3.1–4.3.7, Fig. 4.1, Fig. 4.2, Eqs. 4.1–4.6 | DONE |
| Implementation and fixed values; heterogeneous tracker compatibility | §4.3.8–4.3.9, Tables 4.2, 4.3, Algorithm 4.1 | DONE |
| Development vs final (AOB → SCL), freeze | §4.4, Tables 4.4–4.5 | DONE |
| Experiments across trackers, detection sources, datasets | §4.5–4.6, Tables 4.6–4.11, Figs. 4.3–4.4 | DONE |
| Baselines and ACT | §4.7, Tables 4.12–4.14 | DONE |
| Ablation and sensitivity | §4.8, Table 4.15 | DONE |
| Robustness to score perturbations | §4.6.3, Table 4.9 | DONE |
| No VisDrone V7c/V7d or invented V7f VisDrone results | none in Ch.4 (VisDrone appears only in Ch.3 for AC-MOT) | DONE |
| No claim that all trackers/datasets improve | text states which trackers gained, which were unchanged (identical output) | DONE |
| Discussion, scope, summary | §4.10, §4.11 | DONE |

## Chapter 5 — Conclusions and Future Work
| Item | Section | Status |
|---|---|---|
| Integrated conclusion: problem, survey role, AC-MOT findings, SCL findings, joint contribution, practical implications, scope | §5.1, Table 5.1 | DONE |
| Future work only from the papers or clearly motivated, not presented as done | §5.2 (5 items) | DONE |

## Writing and referencing
| Item | Status |
|---|---|
| Formal academic English; abbreviations defined at first use; List of Abbreviations updated (43 entries) | DONE (automatic first-use check, see QA report) |
| Submitted papers not described as published or accepted | DONE (Publications page: "submitted (under review)") |
| Consolidated, deduplicated bibliography; every citation resolves | DONE (107 cited, 0 undefined) |
| Every figure/table after its first mention | DONE (42 captioned floats + 2 algorithms, checked in source order and in the LaTeX PDF) |
| Publisher reuse permissions | OPEN (see GAPS_AND_LIMITATIONS.md §4) |
