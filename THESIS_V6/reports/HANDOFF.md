# Thesis V6 — Handoff

Title: **Real-Time Target Detection and Tracking** (Arabic: الكشف عن الأهداف وتتبعها في الزمن الحقيقي).
Thesis V6 = Thesis V5 with linked contents and lists (`CHANGES_V6.md`); V5 = V4 after the submission-readiness review (`CHANGES_V5.md`).

## Version naming
Every delivered change gets a new thesis version folder (`THESIS_V7`, `THESIS_V8`, ...) copied from the previous one, and its files carry the version number. Earlier versions are never edited.

## Deliverables
| File | Content |
|---|---|
| `THESIS_V6/word/Thesis_V6.docx` | Thesis in the faculty Word layout — the file to submit |
| `THESIS_V6/word/Thesis_V6.pdf` | PDF of the Word thesis, 95 pages, equations drawn |
| `THESIS_V6/word/Thesis_V6_Table_of_Contents.docx` | Table of contents with the page numbers of the Word thesis, 3 pages |
| `THESIS_V6/Thesis_V6_LaTeX.pdf` | PDF compiled directly from the LaTeX source, 92 pages (no cover pages; for checking) |
| `THESIS_V6/main.tex`, `chapters/`, `frontmatter/`, `figures/`, `references.bib`, `arabic/` | LaTeX source |
| `THESIS_V6/word/` scripts | Word build |
| `THESIS_V6/reports/` | `CHANGES_V5.md`, `SOURCE_MANIFEST.md`, `SUPERVISOR_CHECKLIST.md`, `QA_REPORT.md`, `GAPS_AND_LIMITATIONS.md`, this file |

## Rebuild
```
cd THESIS_V6
PYTHON=python3.13 sh word/build_all.sh ../THESIS_V3/word/Thesis_Ahmed_Gouda_Ismail.docx word/build
```
The script writes `word/Thesis_V6.docx`, `word/Thesis_V6.pdf`, `word/Thesis_V6_Table_of_Contents.docx` and `Thesis_V6_LaTeX.pdf`.
Needs TeX Live (pdflatex, bibtex), pandoc, LibreOffice Writer **and Math** with the `uno` module for `/usr/bin/python3`, and python-docx for `$PYTHON`. `word/build/` is git-ignored.

## Before submission (owner)
1. Fill in the date of discussion on the inner title page and let the department fill in the committee table.
2. Confirm the English department name on the cover (GAPS §5.4) and the Arabic title (GAPS §5.5).
3. Decide on the AC-MOT disclosure items (GAPS §1) and check publisher reuse terms (GAPS §4).
4. When the journals decide, update the Publications page and the two bibliography entries.
5. In Microsoft Word, the contents and lists already hold page numbers; if Word asks to update fields when opening, choose "Update entire table" so the numbers follow Word's own layout. The separate contents file and the PDF hold the page numbers of the LibreOffice layout used for the PDF.

## Suggested research-memory entries (not applied)
- `research/context/CHANGELOG.md`: "- 2026-10-29: Thesis V4 (`THESIS_V4/`): five-chapter structure required by the supervisor (1 Introduction; 2 Background and Related Work; 3 AC-MOT from Paper1_V13; 4 SCL from the submitted Paper2_V71; 5 Conclusions and Future Work), survey as basis of Ch.2, title Real-Time Target Detection and Tracking." and "- 2026-10-29: Thesis V5 (`THESIS_V6/`): V4 after the submission-readiness review (equations drawn in the PDF, abstract/Arabic summary aligned with the title, wording corrections, American spelling); Word 95 pages, LaTeX 92 pages; reports in `THESIS_V6/reports/`."
- `research/context/PAPERS.md`, section Thesis: "Thesis V4/V5" paragraph with the QA results (0 errors/undefined/overfull; 126/126 contents entries; 80/80 DOIs; all chapter numbers traced to the submitted manuscripts).
- `research/context/KNOWLEDGE_GRAPH.md`: row "Manuscript: Thesis V5 | ACTIVE (owner copy) | Real-Time Target Detection and Tracking, five chapters, 95 pages, THESIS_V6/word/ | PAPERS.md".
