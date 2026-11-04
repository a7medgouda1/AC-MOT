# Thesis V4 — Gaps, Limitations and Items Needing a Decision

Items are grouped by type. "Decision" items need the owner; nothing in this list was changed silently.

## 1. Scientific disclosure items (from the repository's own records)
These come from `research/context/PAPERS.md` ("Paper 1 integrity notes (open, for the revision)") and apply to the AC-MOT chapter, which follows the submitted JAIS manuscript.

| # | Item | Current thesis text | Decision needed |
|---|---|---|---|
| 1.1 | The seven VisDrone validation sequences were evaluated twice in the AC-MOT archive (a static no-op read first, commit bfa5caf; the frozen v3 read second, commit 0af0066). The submitted paper does not state the earlier read. | Ch.3 describes the seven sequences as evaluation data disjoint from calibration, as the paper does. | Whether to add one disclosure sentence to §3.5 (e.g., "The evaluation sequences had previously been run once with a static configuration of the controller during the development of the evaluation pipeline."). Recommended to align with the planned JAIS revision. |
| 1.2 | A shuffled-schedule control (P1-SHUF) did not show that the controller's timing adds value beyond its mix of actions; the paper does not report it. | Ch.3 does not make an explicit claim about timing versus action mix; the Discussion attributes the gain mainly to a more selective detection stream. | Whether to report the control or keep the current wording. |
| 1.3 | The YOLO11m checkpoint is third-party (dronefreak/visdrone-yolo11m, AGPL-3.0, trained on VisDrone2019-DET). | "a public version trained on VisDrone2019-DET". | Whether to name the checkpoint and its licence in §2.2.2/§3.5. |

## 2. Presentation choices inherited from the submitted papers
| # | Item | Note |
|---|---|---|
| 2.1 | SCL chapter follows the submitted Paper2_V71, which by the owner's decision (Paper2_V32 onward) omits caveats such as cells where SCL had more identity switches, and intervals that include zero. | The complete numbers remain in Paper2_V31 and in `research/final/`. An examiner may ask about identity switches in the shifted-score and ACT KITTI cells; the answers are in `research/final/V7_IDS_TABLES.json` and `V7_ACT_COMPARISON_RESULT.json`. |
| 2.2 | AC-MOT chapter keeps the trade-offs reported in the submitted Paper 2: higher FN and lower recall with ByteTrack, almost unchanged HOTA with OATrack on UAVDT (47.728 → 47.640), UAVDT IDS/FN intervals with OATrack that include zero, the historical IDS interval [−114, 219], and the historical identity-aware vs quality profile trade-off (−2.617 HOTA). | Kept because they are part of the submitted manuscript; removing them would make the thesis differ from the paper under review. |
| 2.3 | Limitations are written as "Scope of the evaluation" paragraphs (§3.7, §4.10, §5.1): what was tested and what was not. | Consistent with the positives-only decision for the papers. |

## 3. Survey (Paper 1) items
| # | Item | Handling |
|---|---|---|
| 3.1 | Only the camera-ready PDF of the survey exists in the repository (no LaTeX source, no .bib). | Text was extracted from the PDF; background text is rewritten, not copied. |
| 3.2 | The published survey's reference list has metadata problems: [34] gives C-BIoU as "Complete-IoU loss and cluster-NMS…", Pattern Recognition 146 (2024), while the C-BIoU tracker is Yang et al., WACV 2023; [35] cites arXiv:1803.02706 for MOT17; TransTrack appears twice ([7], [31]). | The thesis cites the verified records (C-BIoU: WACV 2023, DOI 10.1109/WACV56688.2023.00478; MOT16/MOT17: arXiv 1603.00831 and the MOTChallenge IJCV paper). The published survey itself cannot be changed. |
| 3.3 | The survey's quantitative tables (Table I detectors on COCO, Table II trackers on MOT17, Table III datasets) were not reproduced. | Reproducing them would require re-verifying every value against the original papers; the thesis uses the survey's taxonomy and statements instead. Can be added after verification if the supervisor wants them. |

## 4. Publication and reuse permissions (not verifiable from the repository)
| # | Item | Action for the owner |
|---|---|---|
| 4.1 | Ch.2 extends text of the published IEEE survey. | Check IEEE's author-reuse terms for theses (citation of the original and, where IEEE requires it, a copyright notice). |
| 4.2 | Ch.3 reuses the manuscript submitted to JAIS (AIAA). | Check AIAA's policy on prior posting/thesis reuse, and repeat the check at acceptance (copyright transfer). |
| 4.3 | Ch.4 reuses the manuscript submitted to The Visual Computer (Springer). | Check Springer's policy on theses and preprints for the submission and after acceptance. |
| 4.4 | Thesis text states the two journal papers as "submitted (under review)". | Update the Publications page and the two bibliography entries when a decision arrives. |

## 5. Template and front matter
| # | Item | Note |
|---|---|---|
| 5.1 | No official university formatting specification was found in the repository. | The Word layout is the one of THESIS_V2/V3, which reproduced the faculty prototype thesis; the original prototype .docx is not stored in the repository. |
| 5.2 | Cover pages keep the placeholders of the faculty template for the date of discussion and the committee names. | To be completed by the department / owner. |
| 5.3 | Abstract, Acknowledgments and Arabic summary are unchanged from V3. | They remain accurate for V4 (same results); they do not mention the survey or the new chapter structure. Optional update. |

## 6. Repository housekeeping
| # | Item | Note |
|---|---|---|
| 6.1 | `THESIS_V4/chapters/ch3_proposed.tex`, `THESIS_V4/chapters/ch4_results.tex`, and `THESIS_V4/figures/scl_architecture.pdf`, `scl_forest.pdf`, `scl_kitti_example.pdf`, `scl_score_groups.pdf` are unused copies carried over from V3. | Deleting them was blocked by the preservation guard; they are not included in the build. Owner may approve their removal. |
| 6.2 | Research-memory records (`research/context/PAPERS.md`, `CHANGELOG.md`, `KNOWLEDGE_GRAPH.md`) were not updated for V4, because this task required all pre-existing files to stay unchanged. | Suggested entries are in `HANDOFF.md`. |
| 6.3 | The THESIS_V2 / THESIS_V3 / THESIS_V4 folders are not registered in `research/VERSION_REGISTRY.json` (no thesis family exists). | Optional. |
| 6.4 | Nothing is committed. `THESIS_V3/` and `THESIS_V4/` are untracked. | Commit/push only on the owner's instruction. |
