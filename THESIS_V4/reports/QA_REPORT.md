# Thesis V4 — Quality Assurance Report

All checks below were run on the final files in `THESIS_V4/` on 2026-10-29.

## 1. Compilation
| Check | Result |
|---|---|
| LaTeX (`pdflatex` → `bibtex` → `pdflatex` ×2, report class) | 0 errors, 0 undefined references or citations, 0 overfull boxes; 92 pages (`Thesis_Ahmed_Gouda_Ismail_LaTeX.pdf`) |
| BibTeX | 0 warnings (the volume/number clash of `kim2026plugtrack` from V3 was fixed by keeping the AAAI volume only; DOI unchanged) |
| TikZ figures (6 standalone files) | all compile |
| Word build (`word/build_all.sh`, two passes, LibreOffice index update) | completes; `word/Thesis_Ahmed_Gouda_Ismail.docx` and `.pdf` (95 pages, faculty layout) and `word/Thesis_Table_of_Contents.docx` (3 pages) |
| Reproducibility | the full script was run end-to-end from a clean work folder: `PYTHON=python3.13 sh word/build_all.sh ../THESIS_V3/word/Thesis_Ahmed_Gouda_Ismail.docx word/build` |

## 2. Structure and cross-references
| Check | Result |
|---|---|
| Contents / List of Figures / List of Tables in Word: every entry's page compared with the page on which the heading or caption is printed | 124 of 124 correct |
| Captioned floats | 10 figures, 32 tables, 2 algorithms in both the LaTeX and the Word output |
| Every float after its first mention | source order: 0 violations (all chapters); LaTeX PDF reading order: 0 violations (42 captioned floats); `flafter` added; the Word build places floats at their source position |
| Equations | 34 numbered equations, numbered by chapter; symbols defined in the surrounding text |
| Abbreviations | list rebuilt (43 entries, 10 added: AF-JPDA, AP, GBI, ID, JDE, mAP, R-CNN, RQ, SORT, SSD); automatic first-use check run; definitions added at first use for AF-JPDA, CI, COCO, CPU, JDE, R-CNN, RT-DETR, SORT, RQ |
| Old V3 structure left in the build | none: no "Proposed Training-Free Adaptive Control Approach", "Experimental Results and Performance Evaluation", "to be submitted", template names or "??" in the Word PDF |
| Document properties | author and last-modified-by = Ahmed Gouda Ismail; empty description; no generator strings in the .docx files |

## 3. Numbers (traceability)
An automatic check extracted every number written in each chapter (tables included; references, labels and layout values excluded) and searched for it in the authoritative source:

| Chapter | Source searched | Numbers not found |
|---|---|---|
| Ch.1 | Survey text, Paper 2 (`Paper1_V13_JAIS/main.tex`), Paper 3 (V71 sections and tables actually input) | none |
| Ch.2 | same | none (330,000 COCO images: present in the survey PDF, split by the PDF text layout) |
| Ch.3 AC-MOT | Paper 2 only | **none** |
| Ch.4 SCL | Paper 3 only | 4, all verified: 0.02 and 0.03 (inputs of the worked Otsu example 0.02, 0.03, 0.05, 0.4, 0.5, 0.9, 0.95, which the thesis carries over from V3; recomputed: t1 = −1.67 (score 0.16), t2 = 1.10 (score 0.75), ρ = 2/4, as printed); 178,219 and 78,975 false positives of ACT and SCL on UAVDT with RT-DETR-L (`research/final/V7_ACT_ORIGINAL_UAVDT_RESULT.json`, keys `rtdetr|ACT` and `rtdetr|V7f`) |
| Ch.5 | all three papers | none |

Text present in THESIS_V3 but **not** in the submitted Paper 3 was removed from Ch.4: the identity-switch comparison with the Otsu baselines (170 vs 1,545/250; 308 vs 1,975/492) and the frame counts of the baseline runs (7,987 / 7,940). They came from an unused leftover file of the V71 folder (`sections/06_results.tex`).

Relative values in the chapter openings were checked against the papers' abstracts: AC-MOT +7.1% / +182% / +11.0% / −24.2% (ByteTrack), +2.8% / +22.4% / +4.0% / −21.9% (OATrack), +16.7% UAVDT MOTA (OATrack); SCL ≥97% HOTA recovered, +12.6% / +16.3% MOTA, −43% / −47% IDS, +0.9% PD-SORT HOTA, four trackers within 0.1%, 2.95 ms.

## 4. Citations and bibliography
| Check | Result |
|---|---|
| Entries cited | 107 (all resolve; 7 further entries remain in `references.bib` but are not cited, so they do not print) |
| DOIs checked against Crossref (title and year) | 80 of 80 resolve to the cited work. Title differences only where Crossref stores the short title (Optuna, Chameleon, ApproxDet) or a subtitle (Efron and Hastie); year differences only where the journal issue year differs from the online-first year (2023 online / 2024 issue for three The Visual Computer papers; 2020 online / 2021 issue for HOTA and MOTChallenge) |
| arXiv identifiers checked against arXiv | 6 of 6 match (RF-DETR 2511.09554, MOT20 2003.09003, TransTrack 2012.15460, MOT16 1603.00831, YOLOv3 1804.02767, YOLOv4 2004.10934) |
| Entries without DOI | 16: software manuals (YOLOv8, YOLO11), arXiv preprints listed above, conference papers without DOI (AdaScale, ViT, Guo et al., Tent, Transformer, U2MOT, RANet), and the two submitted manuscripts of the author |
| Survey entry | completed from `CITATION.md` (full venue name, pages 119–125, publisher, DOI) |
| Author's submitted works | cited as "submitted (under review)"; Paper 3 author order taken from the V71 author block (Ismail, Mahmoud, Mohamed) |
| Style | IEEE (`ieeetr`), as in THESIS_V2/V3 |

## 5. Scientific consistency review (examiner pass)
Items found and fixed during the review:
1. Ch.2 said that published tracker comparisons use "the detector for which each tracker was tuned"; the survey's Table II uses one common set of public Faster R-CNN detections. Corrected to "compare trackers on one fixed set of detections".
2. Ch.3 first stated the frozen AC-MOT rule as the argmax of the search objective; the paper selects the frozen policy among eligible candidates by an additional rule. Eq. 3.3 now defines only the objective J(π), and the text refers to §3.4.4 for the selection.
3. Ch.5 attached the 43–56% identity-switch reduction to the held-out aerial data only; 43% is KITTI (ByteTrack, RT-DETR-L) and 56% is UAVDT. Corrected.
4. Ch.1 overstated what the survey showed ("deployed systems … with fixed settings"); rewritten to what the survey states (TBD dominant; accuracy–speed, hardware and deployment constraints; dependency between detection accuracy and association reliability).
5. Ch.2 listed "Four detection sources" while naming five; rewritten (AC-MOT: YOLO11m; SCL: four sources).
6. Descriptive labels for six recent trackers (frequency cues, Sinkhorn, …) were not verified and were removed.
7. Research questions rendered as "1, 2, 3" in Word; the Word converter now keeps the labels RQ1–RQ3.

Separation of evidence: VisDrone results appear only for AC-MOT (Ch.3). No V7c/V7d or V7f VisDrone result, no confirmation-16, test-dev or other protected split was opened or used for this work; the historical VisDrone test-dev numbers in §3.4 are copied from the submitted Paper 2 and are labelled historical.

## 6. Preservation
- Only new files were written, all inside `THESIS_V4/` (plus temporary files in the session scratchpad and the LibreOffice profile there).
- `THESIS_V3/` (including the Word file used as layout template), the papers, the result files and all tracked files are unchanged; `git status` shows no tracked change from this task.
- Nothing was committed or pushed.
