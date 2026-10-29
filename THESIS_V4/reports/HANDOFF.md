# Thesis V4 — Handoff

## Version naming
Every delivered change gets a new thesis version folder (`THESIS_V5`, `THESIS_V6`, ...) copied from the previous one, and its files carry the version number (`Thesis_V<n>.docx`, `Thesis_V<n>.pdf`, `Thesis_V<n>_Table_of_Contents.docx`, `Thesis_V<n>_LaTeX.pdf`). Earlier versions are never edited.

Thesis V4 files: `word/Thesis_V4.docx`, `word/Thesis_V4.pdf`, `word/Thesis_V4_Table_of_Contents.docx`, `Thesis_V4_LaTeX.pdf` (same content as the files listed below; title: Real-Time Target Detection and Tracking).

## Deliverables
| File | Content |
|---|---|
| `THESIS_V4/word/Thesis_Ahmed_Gouda_Ismail.docx` | Thesis in the faculty Word layout (front pages of V3, contents and lists rebuilt) |
| `THESIS_V4/word/Thesis_Ahmed_Gouda_Ismail.pdf` | PDF of the Word thesis, 95 pages |
| `THESIS_V4/word/Thesis_Table_of_Contents.docx` | Table of contents with the page numbers of the Word thesis, 3 pages |
| `THESIS_V4/Thesis_Ahmed_Gouda_Ismail_LaTeX.pdf` | PDF compiled directly from the LaTeX source, 92 pages |
| `THESIS_V4/main.tex`, `chapters/`, `frontmatter/`, `figures/`, `references.bib`, `arabic/` | LaTeX source (main file + one file per chapter) |
| `THESIS_V4/word/` scripts | Word build: `build_all.sh`, `prep_latex.py`, `make_images.py`, `build_docx.py`, `build_docx_v3.py`, `build_toc_docx.py`, `update_fields.py` |
| `THESIS_V4/reports/` | `SOURCE_MANIFEST.md`, `SUPERVISOR_CHECKLIST.md`, `QA_REPORT.md`, `GAPS_AND_LIMITATIONS.md`, this file |

Chapter files used by `main.tex`: `ch1_introduction.tex`, `ch2_background.tex`, `ch3_acmot.tex`, `ch4_scl.tex`, `ch5_conclusions.tex`.

## Rebuild
```
cd THESIS_V4
PYTHON=python3.13 sh word/build_all.sh ../THESIS_V3/word/Thesis_Ahmed_Gouda_Ismail.docx word/build
cp word/build/thesis.docx word/Thesis_Ahmed_Gouda_Ismail.docx
cp word/build/thesis.pdf  word/Thesis_Ahmed_Gouda_Ismail.pdf
cp word/build/Thesis_Table_of_Contents.docx word/
cp main.pdf Thesis_Ahmed_Gouda_Ismail_LaTeX.pdf
```
Needs TeX Live (pdflatex, bibtex), pandoc, LibreOffice with the `uno` module for `/usr/bin/python3`, and python-docx for `$PYTHON`. `word/build/` is git-ignored.

## What changed from THESIS_V3
- New five-chapter structure required by the supervisor: Ch.3 is now the whole AC-MOT study (method, development, setup, results, discussion) and Ch.4 the whole SCL study; V3's combined "Proposed Approach" and "Experimental Results" chapters are gone.
- Ch.1 rewritten: overview of the field and the research direction, motivation separated into literature-based and demonstrated effects, problem statement with RQ1–RQ3 and the relation of the two problems, solution approach with Table 1.1.
- Ch.2 rewritten as Background and Related Work: §2.2 technical background (eight subsections, now also holding the datasets, metrics and protocols that V3 kept in Ch.4), §2.3 related work by theme with one merged comparison table, §2.4 summary.
- Ch.3 and Ch.4 each open with the paper's abstract adapted to thesis prose, state their own problem and requirements, and end with discussion, scope and summary.
- Ch.5 rewritten as an integrated conclusion for the whole thesis.
- Bibliography: survey entry completed; Paper 3 entry added; one BibTeX warning fixed.
- Publications page: Paper 3 author order as in the submitted manuscript; mapping of the three publications to Chapters 2–4.
- List of Abbreviations: 10 entries added.
- Two sentences of V3 that were not in the submitted Paper 3 were removed (QA report §3).

## Decisions for the owner
1. Disclosure items for the AC-MOT chapter (GAPS §1.1–1.3).
2. Publisher reuse permissions (GAPS §4).
3. Optional update of the abstract and Arabic summary (GAPS §5.3).
4. Removal of the six unused V3 copies inside `THESIS_V4/` (GAPS §6.1) — needs explicit approval.
5. Research-memory update (below) and commit/push — only on instruction.

## Suggested research-memory entries (not applied)
- `research/context/CHANGELOG.md`: "- 2026-10-29: Thesis V4 (`THESIS_V4/`): five-chapter structure required by the supervisor (1 Introduction; 2 Background and Related Work; 3 AC-MOT from Paper1_V13; 4 SCL from the submitted Paper2_V71; 5 Conclusions and Future Work), survey as basis of Ch.2; Word 95 pages, LaTeX 92 pages, separate contents file; source manifest, checklist, QA and gap reports in `THESIS_V4/reports/`."
- `research/context/PAPERS.md`, section Thesis: a "Thesis V4" paragraph with the same content and the QA results (0 errors/undefined/overfull; 124/124 contents entries; 80/80 DOIs; all chapter numbers traced to the submitted manuscripts).
- `research/context/KNOWLEDGE_GRAPH.md`: row "Manuscript: Thesis V4 | ACTIVE (owner copy) | five-chapter supervisor structure, 95 pages, THESIS_V4/word/ | PAPERS.md".
