# Thesis V7 — Preservation Verification

Thesis V7 was compared with Thesis V6 to confirm that the language and formatting corrections left the scientific content unchanged. All checks below were run on the final V7 build.

## 1. LaTeX source (V6 against V7)
Each source file was compared after removing comments. Numbers are compared as a multiset (every occurrence counts); math expressions, table rows, citations, labels and references are compared exactly. Column widths and font size of tables are not part of the comparison (layout only).

| Part | Numbers | Math expressions | Table rows | Citations (in order) | Labels | Cross-references | Equation references | Algorithms |
|---|---|---|---|---|---|---|---|---|
| Chapter 1 | 19 identical | 6 identical | 8 identical | 25 identical | 9 identical | 21 identical | 0 identical | 0 identical |
| Chapter 2 | 105 identical | 60 identical | 48 identical | 167 identical | 38 identical | 30 identical | 2 identical | 0 identical |
| Chapter 3 | 694 identical | 316 identical | 97 identical | 19 identical | 50 identical | 78 identical | 18 identical | 1 identical |
| Chapter 4 | 878 identical | 412 identical | 152 identical | 39 identical | 57 identical | 89 identical | 14 identical | 1 identical |
| Chapter 5 | 30 identical | 9 identical | 6 identical | 1 identical | 4 identical | 5 identical | 0 identical | 0 identical |
| Abstract | 12 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical |
| Acknowledgments | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical |
| Abbreviations | 0 identical | 0 identical | 43 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical |
| Publications | 6 identical | 0 identical | 0 identical | 0 identical | 0 identical | 3 identical | 0 identical | 0 identical |
| Arabic summary | 17 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical |
| main.tex | 7 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical | 0 identical |
| **Total** | **1768** | **803** | **354** | **251** | **158** | **226** | **34** | **2** |

Result: every number, math expression, table row, citation (with its position), label, cross-reference, equation reference and algorithm line of V6 is present unchanged in V7.

## 2. Bibliography
| Check | Result |
|---|---|
| Entries in `references.bib` | 114 in V6, 114 in V7, same keys |
| Cited entries and their numbers | 107 in both, same order, so every citation number [1]–[107] points to the same work as in V6 |
| Year, volume, pages, DOI, journal, note, URL fields | unchanged in every entry |
| Fields changed | title (33 entries, capitalization only), author (6 entries, spelling of three names), booktitle and publisher (1 entry, written out in full), address (4 entries, publisher city removed), number (1 entry, dash) |

## 3. Word thesis (Thesis_V6.docx against Thesis_V7.docx)
| Check | Result |
|---|---|
| Tables | 36 in both; every cell identical |
| Equations | 34 in both; content identical |
| Pictures | 13 in both |
| Pages | 95 in both (LaTeX PDF: 92 in both) |
| Contents and lists | 129 entries; every page number matches the page that holds the entry; 129 of 129 entries linked |
| Separate contents file | 87 entries, all identical to the contents of the thesis |
| Figure, table and algorithm placement | 44 of 44 appear on or after the page of their first mention (LaTeX PDF: 42 of 42) |

## 4. Text differences in the PDF
A word-by-word comparison of the V6 and V7 PDFs shows only the corrections listed in `CHANGE_LOG.md` and the page numbers that moved with them in the contents (one entry moved from page 55 to 56).

## 5. Earlier versions
| Check | Result |
|---|---|
| Tracked files of THESIS_V3, THESIS_V4, THESIS_V5 and THESIS_V6 | no change (git) |
| `THESIS_V6/word/Thesis_V6.docx` and `Thesis_V6.pdf` | SHA-256 identical to the values recorded before the work started |

## 6. Build
LaTeX: 0 errors, 0 undefined references, 0 overfull boxes, no float larger than the page (V6 had one: Table 2.4 ran past the bottom margin of the LaTeX PDF; fixed in V7). BibTeX: 0 warnings.
