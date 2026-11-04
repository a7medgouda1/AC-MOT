# Thesis V7 — Handoff

Title: **Real-Time Target Detection and Tracking** (Arabic: الكشف عن الأهداف وتتبعها في الزمن الحقيقي).
Thesis V7 = Thesis V6 after a full language, consistency and formatting correction (`CHANGES_V7.md`); V6 = V5 with linked contents and lists (`CHANGES_V6.md`); V5 = V4 after the submission-readiness review (`CHANGES_V5.md`).

## Version naming
Every delivered change gets a new thesis version folder (`THESIS_V8`, `THESIS_V9`, ...) copied from the previous one, and its files carry the version number. Earlier versions are never edited.

## Deliverables
| File | Content |
|---|---|
| `THESIS_V7/word/Thesis_V7.docx` | Thesis in the faculty Word layout — the file to submit |
| `THESIS_V7/word/Thesis_V7.pdf` | PDF of the Word thesis, 95 pages, equations drawn |
| `THESIS_V7/word/Thesis_V7_Table_of_Contents.docx` | Table of contents with the page numbers of the Word thesis, 3 pages |
| `THESIS_V7/Thesis_V7_LaTeX.pdf` | PDF compiled directly from the LaTeX source, 92 pages (no cover pages; for checking) |
| `THESIS_V7/main.tex`, `chapters/`, `frontmatter/`, `figures/`, `references.bib`, `arabic/` | LaTeX source |
| `THESIS_V7/word/` scripts | Word build |
| `THESIS_V7/reports/` | `PROOFREADING_REPORT.md`, `CHANGE_LOG.md`, `PRESERVATION_VERIFICATION.md`, `CHANGES_V5.md`–`CHANGES_V7.md`, `SOURCE_MANIFEST.md`, `SUPERVISOR_CHECKLIST.md`, `QA_REPORT.md`, `GAPS_AND_LIMITATIONS.md`, this file |

## Rebuild
```
cd THESIS_V7
PYTHON=python3.13 sh word/build_all.sh ../THESIS_V3/word/Thesis_Ahmed_Gouda_Ismail.docx word/build
```
The script writes `word/Thesis_V7.docx`, `word/Thesis_V7.pdf`, `word/Thesis_V7_Table_of_Contents.docx` and `Thesis_V7_LaTeX.pdf`.
Needs TeX Live (pdflatex, bibtex), pandoc, LibreOffice Writer **and Math** with the `uno` module for `/usr/bin/python3`, and python-docx for `$PYTHON`. `word/build/` is git-ignored.

## Before submission (owner)
1. Select the day and month of the discussion on the inner title page (template drop-down fields), then remove the red color and yellow highlight of that line; the department fills in the committee table.
2. Confirm the official English department name and use it on the title pages and in the acknowledgments (PROOFREADING_REPORT §6.3); confirm the Arabic title.
3. Decide on the points listed in PROOFREADING_REPORT §7 (MOT17 sentence, thousands separators, bibliography details).
4. Decide on the AC-MOT disclosure items (GAPS §1) and check publisher reuse terms (GAPS §4).
5. When the journals decide, update the Publications page and bibliography entries [27] and [28].
6. In Microsoft Word, the contents and lists already hold page numbers; if Word asks to update fields when opening, choose "Update entire table" so the numbers follow Word's own layout.

## Suggested research-memory entries (not applied)
- `research/context/CHANGELOG.md`: "- 2026-10-29: Thesis V7 (`THESIS_V7/`): Thesis V6 after a full language, consistency and formatting correction (126 logged corrections, scientific content, numbers, tables, equations and citations unchanged and verified against V6); Word 95 pages, LaTeX 92 pages; reports in `THESIS_V7/reports/`."
- `research/context/PAPERS.md`, section Thesis: "Thesis V7" paragraph with the QA results (0 errors/undefined/overfull; 129/129 contents and list entries; 44/44 floats after first mention; preservation check against V6 passed).
- `research/context/KNOWLEDGE_GRAPH.md`: row "Manuscript: Thesis V7 | ACTIVE (owner copy) | Real-Time Target Detection and Tracking, five chapters, 95 pages, THESIS_V7/word/ | PAPERS.md".
