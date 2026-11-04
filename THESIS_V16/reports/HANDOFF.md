# Thesis V16 — Handoff

Title: **Real-Time Target Detection and Tracking** (Arabic: الكشف عن الأهداف وتتبعها في الزمن الحقيقي).
Thesis V16 = Thesis V15 with three equation symbols that the PDF showed as error marks drawn correctly (`CHANGES_V16.md`); V15 = Thesis V14 after the final pass before submission to the supervisors: language and consistency, Times New Roman throughout, and clearer figures (`CHANGES_V15.md`); V14 = Thesis V13 with the full name of the first supervisor (Assoc. Prof. Dr. Mohamed Sobhy Mohamed) on the title pages, in the acknowledgments and on the Arabic title page, and with Chapter 3 worded on the strengths of AC-MOT only (`CHANGES_V14.md`); V13 = Thesis V12 with figures of real tracked video frames in every chapter, the new Section 3.6.5 (qualitative evaluation on selected video frames), a state diagram of AC-MOT and a chart of the SCL score-shift results (`CHANGES_V13.md`; figure sources in `research/acmot_paper_v2/qualitative_v1/`); V12 = V11 with the remaining limiting statements removed (`CHANGES_V12.md`); V11 = V10 with the limiting statements of Chapters 1, 3 and 4 removed or reworded (`CHANGES_V11.md`); V10 = V9 with the supervisor's comments on the abstract and on Chapters 1, 2 and 5 (`CHANGES_V10.md`); V9 = V8 with two corrections in Chapter 5: the statement that the two controllers were evaluated separately is restored, and the combined-pipeline item of the Future Work is worded as an evaluation (`CHANGES_V9.md`); V8 = V7 with the requested corrections: Future Work, date line, scene complexity index in the abstract, acknowledgments signature, abbreviations heading and table readability (`CHANGES_V8.md`); V7 = V6 after a full language, consistency and formatting correction (`CHANGES_V7.md`, `PROOFREADING_REPORT.md`, `CHANGE_LOG.md`, `PRESERVATION_VERIFICATION.md`); V6 = V5 with linked contents and lists (`CHANGES_V6.md`); V5 = V4 after the submission-readiness review (`CHANGES_V5.md`).

## Version naming
Every delivered change gets a new thesis version folder (`THESIS_V16`, `THESIS_V17`, ...) copied from the previous one, and its files carry the version number. Earlier versions are never edited.

## Deliverables
| File | Content |
|---|---|
| `THESIS_V16/word/Thesis_V16.docx` | Thesis in the faculty Word layout — the file to submit |
| `THESIS_V16/word/Thesis_V16.pdf` | PDF of the Word thesis, 109 pages, equations drawn |
| `THESIS_V16/word/Thesis_V16_Table_of_Contents.docx` | Table of contents with the page numbers of the Word thesis, 3 pages |
| `THESIS_V16/Thesis_V16_LaTeX.pdf` | PDF compiled directly from the LaTeX source, 105 pages (no cover pages; for checking) |
| `THESIS_V16/main.tex`, `chapters/`, `frontmatter/`, `figures/`, `references.bib`, `arabic/` | LaTeX source |
| `THESIS_V16/word/` scripts | Word build |
| `THESIS_V16/reports/` | `CHANGES_V16.md`, `CHANGES_V15.md`, `CHANGES_V14.md`, `CHANGES_V13.md`, `CHANGES_V12.md`, `CHANGES_V11.md`, `CHANGES_V10.md`, `CHANGES_V9.md`, `CHANGES_V8.md`, `PROOFREADING_REPORT.md`, `CHANGE_LOG.md`, `PRESERVATION_VERIFICATION.md` (V7 pass), `CHANGES_V5.md`–`CHANGES_V7.md`, `SOURCE_MANIFEST.md`, `SUPERVISOR_CHECKLIST.md`, `QA_REPORT.md`, `GAPS_AND_LIMITATIONS.md`, this file |

## Rebuild
```
cd THESIS_V16
PYTHON=python3.13 sh word/build_all.sh ../THESIS_V3/word/Thesis_Ahmed_Gouda_Ismail.docx word/build
```
The script writes `word/Thesis_V16.docx`, `word/Thesis_V16.pdf`, `word/Thesis_V16_Table_of_Contents.docx` and `Thesis_V16_LaTeX.pdf`.
The PDF shows the font of the Word file when Times New Roman is installed (Liberation Serif, with the same metrics, is used otherwise). Needs TeX Live (pdflatex, bibtex), pandoc, LibreOffice Writer **and Math** with the `uno` module for `/usr/bin/python3`, and python-docx for `$PYTHON`. `word/build/` is git-ignored.

## Before submission (owner)
1. When the date is set, click the blanks of the date line on the inner title page and choose the day and month (template drop-down fields); the department fills in the committee table.
2. The English department name of the title pages (Chair of Computing Engineering and Artificial Intelligence) is also used in the acknowledgments since V15; confirm the Arabic title.
3. Decide on the points listed in PROOFREADING_REPORT §7 (MOT17 sentence, thousands separators, bibliography details).
4. Decide on the AC-MOT disclosure items (GAPS §1) and check publisher reuse terms (GAPS §4).
5. When the journals decide, update the Publications page and bibliography entries [27] and [28].
6. In Microsoft Word, the contents and lists already hold page numbers; if Word asks to update fields when opening, choose "Update entire table" so the numbers follow Word's own layout.

## Suggested research-memory entries (not applied)
- `research/context/CHANGELOG.md`: "- 2026-10-29: Thesis V7 (`THESIS_V7/`): Thesis V6 after a full language, consistency and formatting correction (126 logged corrections; numbers, tables, equations and citations verified unchanged against V6). Thesis V8 (`THESIS_V8/`): V7 with the requested corrections (Future Work, date line, SCI description, acknowledgments signature, abbreviations heading, table readability). Thesis V9 (`THESIS_V9/`): V8 with the separate-evaluation statement of Chapter 5 restored and the combined-pipeline future-work item worded as an evaluation. Thesis V10 (`THESIS_V10/`): V9 with the supervisor's comments on the abstract and Chapters 1, 2 and 5. Thesis V11 (`THESIS_V11/`) and V12 (`THESIS_V16/`): V10 with the limiting statements removed; Word 102 pages, LaTeX 96 pages; reports in `THESIS_V16/reports/`."
- `research/context/PAPERS.md`, section Thesis: "Thesis V7–V15" paragraph with the QA results (0 errors/undefined/overfull; 131/131 contents and list entries; 46/46 floats after first mention; preservation checks against V6–V11 passed).
- `research/context/KNOWLEDGE_GRAPH.md`: row "Manuscript: Thesis V16 | ACTIVE (owner copy) | Real-Time Target Detection and Tracking, five chapters, 109 pages, THESIS_V16/word/ | PAPERS.md".
- `research/context/EXPERIMENT_REGISTRY.md` / `CHANGELOG.md`: "- 2026-10-30: Thesis V13 (`THESIS_V13/`–`THESIS_V16/`): figures of real tracked frames in every chapter and Section 3.6.5; illustrative CPU re-run of the frozen AC-MOT v3 pipeline on VisDrone2019-MOT-val uav0000117_02622_v (`research/acmot_paper_v2/qualitative_v1/`, HOTA gain +3.21 vs archived +3.05); no frozen file or result changed."
