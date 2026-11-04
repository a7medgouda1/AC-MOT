# Thesis V10 — Handoff

Title: **Real-Time Target Detection and Tracking** (Arabic: الكشف عن الأهداف وتتبعها في الزمن الحقيقي).
Thesis V10 = Thesis V9 with the supervisor's comments on the abstract and on Chapters 1, 2 and 5 (`CHANGES_V10.md`); V9 = V8 with two corrections in Chapter 5: the statement that the two controllers were evaluated separately is restored, and the combined-pipeline item of the Future Work is worded as an evaluation (`CHANGES_V9.md`); V8 = V7 with the requested corrections: Future Work, date line, scene complexity index in the abstract, acknowledgments signature, abbreviations heading and table readability (`CHANGES_V8.md`); V7 = V6 after a full language, consistency and formatting correction (`CHANGES_V7.md`, `PROOFREADING_REPORT.md`, `CHANGE_LOG.md`, `PRESERVATION_VERIFICATION.md`); V6 = V5 with linked contents and lists (`CHANGES_V6.md`); V5 = V4 after the submission-readiness review (`CHANGES_V5.md`).

## Version naming
Every delivered change gets a new thesis version folder (`THESIS_V11`, `THESIS_V12`, ...) copied from the previous one, and its files carry the version number. Earlier versions are never edited.

## Deliverables
| File | Content |
|---|---|
| `THESIS_V10/word/Thesis_V10.docx` | Thesis in the faculty Word layout — the file to submit |
| `THESIS_V10/word/Thesis_V10.pdf` | PDF of the Word thesis, 102 pages, equations drawn |
| `THESIS_V10/word/Thesis_V10_Table_of_Contents.docx` | Table of contents with the page numbers of the Word thesis, 3 pages |
| `THESIS_V10/Thesis_V10_LaTeX.pdf` | PDF compiled directly from the LaTeX source, 97 pages (no cover pages; for checking) |
| `THESIS_V10/main.tex`, `chapters/`, `frontmatter/`, `figures/`, `references.bib`, `arabic/` | LaTeX source |
| `THESIS_V10/word/` scripts | Word build |
| `THESIS_V10/reports/` | `CHANGES_V10.md`, `CHANGES_V9.md`, `CHANGES_V8.md`, `PROOFREADING_REPORT.md`, `CHANGE_LOG.md`, `PRESERVATION_VERIFICATION.md` (V7 pass), `CHANGES_V5.md`–`CHANGES_V7.md`, `SOURCE_MANIFEST.md`, `SUPERVISOR_CHECKLIST.md`, `QA_REPORT.md`, `GAPS_AND_LIMITATIONS.md`, this file |

## Rebuild
```
cd THESIS_V10
PYTHON=python3.13 sh word/build_all.sh ../THESIS_V3/word/Thesis_Ahmed_Gouda_Ismail.docx word/build
```
The script writes `word/Thesis_V10.docx`, `word/Thesis_V10.pdf`, `word/Thesis_V10_Table_of_Contents.docx` and `Thesis_V10_LaTeX.pdf`.
Needs TeX Live (pdflatex, bibtex), pandoc, LibreOffice Writer **and Math** with the `uno` module for `/usr/bin/python3`, and python-docx for `$PYTHON`. `word/build/` is git-ignored.

## Before submission (owner)
1. When the date is set, click the blanks of the date line on the inner title page and choose the day and month (template drop-down fields); the department fills in the committee table.
2. Confirm the official English department name and use it on the title pages and in the acknowledgments (PROOFREADING_REPORT §6.3); confirm the Arabic title.
3. Decide on the points listed in PROOFREADING_REPORT §7 (MOT17 sentence, thousands separators, bibliography details).
4. Decide on the AC-MOT disclosure items (GAPS §1) and check publisher reuse terms (GAPS §4).
5. When the journals decide, update the Publications page and bibliography entries [27] and [28].
6. In Microsoft Word, the contents and lists already hold page numbers; if Word asks to update fields when opening, choose "Update entire table" so the numbers follow Word's own layout.

## Suggested research-memory entries (not applied)
- `research/context/CHANGELOG.md`: "- 2026-10-29: Thesis V7 (`THESIS_V7/`): Thesis V6 after a full language, consistency and formatting correction (126 logged corrections; numbers, tables, equations and citations verified unchanged against V6). Thesis V8 (`THESIS_V8/`): V7 with the requested corrections (Future Work, date line, SCI description, acknowledgments signature, abbreviations heading, table readability). Thesis V9 (`THESIS_V9/`): V8 with the separate-evaluation statement of Chapter 5 restored and the combined-pipeline future-work item worded as an evaluation. Thesis V10 (`THESIS_V10/`): V9 with the supervisor's comments on the abstract and Chapters 1, 2 and 5; Word 102 pages, LaTeX 97 pages; reports in `THESIS_V10/reports/`."
- `research/context/PAPERS.md`, section Thesis: "Thesis V7–V10" paragraph with the QA results (0 errors/undefined/overfull; 131/131 contents and list entries; 46/46 floats after first mention; preservation checks against V6–V9 passed).
- `research/context/KNOWLEDGE_GRAPH.md`: row "Manuscript: Thesis V10 | ACTIVE (owner copy) | Real-Time Target Detection and Tracking, five chapters, 102 pages, THESIS_V10/word/ | PAPERS.md".
