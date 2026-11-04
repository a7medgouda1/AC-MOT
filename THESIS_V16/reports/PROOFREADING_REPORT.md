# Thesis V7 — Proofreading Report

Thesis V7 is Thesis V6 after a full language, consistency and formatting correction. The scientific content (claims, methods, experiments, numbers, tables, equations, citations and conclusions) is unchanged; `PRESERVATION_VERIFICATION.md` gives the evidence and `CHANGE_LOG.md` lists every correction with its location, original and revised wording.

## 1. Files
| File | Content |
|---|---|
| `word/Thesis_V7.docx` | Thesis in the faculty Word layout (editable) |
| `word/Thesis_V7.pdf` | PDF of the Word thesis, 95 pages |
| `word/Thesis_V7_Table_of_Contents.docx` | Separate table of contents, 3 pages |
| `Thesis_V7_LaTeX.pdf` | PDF compiled from the LaTeX source, 92 pages |
| `main.tex`, `chapters/`, `frontmatter/`, `arabic/`, `references.bib`, `figures/` | LaTeX source (editable) |

## 2. Passes performed
1. **Language**: every paragraph, list, caption and table note of Chapters 1–5, the abstract, the acknowledgments and the publications page was read for grammar, punctuation, word choice, academic register, sentence structure, repetition and ambiguity. The Arabic summary was read for consistency with the English abstract (no change needed).
2. **Consistency**: terminology, hyphenation, capitalization, abbreviations, headings, captions, numbering and cross-reference style across the whole thesis.
3. **Formatting**: front pages, pagination, headings, tables, equations, figures, bibliography and the contents and lists.
4. **Build and inspection**: LaTeX and Word builds, automatic checks (Section 5) and a page-by-page visual inspection of all 95 pages of the Word PDF.

## 3. Corrections by category
| Category | Entries | Places in the text |
|---|---|---|
| Grammar (agreement, tense, articles, prepositions, parallel structure) | 16 | 16 |
| Punctuation (appositives, semicolons, comma splices, dashes, lists) | 25 | 25 |
| Word choice and register | 20 | 20 |
| Sentence structure and clarity (long sentences split, ambiguous references) | 16 | 16 |
| Headings and capitalization (incl. the degree line of the title pages) | 7 | 8 |
| Table layout | 1 | 1 |
| Bibliography: title capitalization | 33 | 33 |
| Bibliography: author names and venue details | 8 | 13 |
| **Total** | **126** | **132** |

By part of the thesis: Chapter 1: 13; Chapter 2: 15; Chapter 3: 21; Chapter 4: 26; Chapter 5: 4; abstract: 4; acknowledgments: 1; title pages: 1; bibliography: 41.

## 4. Consistency and formatting results
| Item | Result in V7 |
|---|---|
| Spelling | American English throughout; spell check of all chapters and front matter finds only technical names and terms |
| Tracking by detection | noun written open ("tracking by detection"), adjective hyphenated ("tracking-by-detection trackers") everywhere |
| Real-time | "real-time" as adjective, "in real time" as adverb; "realtime" only in the published name SORT |
| Cost wording | informal "cheap"/"cheaply" replaced by "inexpensive"/"at low cost" in all 6 places |
| Cross-references | "Fig." inside a sentence, "Figure" at the start of a sentence; "Table", "Section", "Chapter", "Eq." used the same way in every chapter |
| Headings | title case with lowercase prepositions in all headings; closing sections of Chapters 2–4 all titled "Summary" |
| Captions | every caption starts with a capital letter and ends with a period; table captions above the table, figure captions below the figure |
| Chapter list in Section 1.5 | "Chapter N. Title" for all four entries |
| Abbreviations | 43 entries in alphabetical order |
| Degree line (cover and inner title page) | "Master of Science in Computer Engineering" |
| Front matter pagination | Roman numerals I–X, matching the contents; chapters start at page 1 |
| Publications status | AC-MOT manuscript (Journal of Aerospace Information Systems) and SCL manuscript (The Visual Computer): "submitted (under review)" on the Publications page and in the bibliography; the survey: published, with DOI |
| Bibliography | IEEE style in citation order, 107 entries; all titles in title case; consistent author names (Leal-Taixé, Dollár); no publisher city in the place of a conference location |
| Table 2.4 in the LaTeX PDF | fits its page (smaller font, wider columns); the Word layout already split it across pages with the header repeated |
| Equations | 34 of 34 drawn in the PDF, numbered (2.1)–(2.15), (3.1)–(3.13), (4.1)–(4.6) |

## 5. Automatic checks on the final build
| Check | Result |
|---|---|
| LaTeX errors / undefined references / overfull boxes / floats larger than the page | 0 / 0 / 0 / 0 |
| BibTeX warnings | 0 |
| Contents and lists: page number of each entry against the printed page that holds it | 129 of 129 correct |
| Linked entries in the contents and lists (Word and PDF) | 129 of 129 |
| Figures, tables and algorithms after their first mention | Word PDF 44 of 44; LaTeX PDF 42 of 42 |
| Doubled words, spaces before punctuation, missing spaces after periods | none found |
| Visual inspection of all 95 pages | no cut-off table, missing equation, broken figure, orphan heading or empty page; tables continued on a second page repeat their header row |

## 6. Items for the author to complete
1. **Date of discussion** (inner title page): the day and month are drop-down fields of the faculty template that still read "Choose an item.", and the line is in the template's red/yellow marking. Select the day and month in Word once the date is set, then remove the red color and yellow highlight.
2. **Committee approval table**: filled in by the department after the discussion.
3. **Department name**: the title pages (faculty template) read "Chair of Computing Engineering and Artificial Intelligence"; the acknowledgments read "Computer Engineering and Artificial Intelligence Department of the Military Technical College". Both were kept as they are; use the official English name from the department in both places.
4. **"Under supervision of"** on the title pages is the wording of the faculty template and was kept; "Under the supervision of" is the standard English form if the department allows the change.
5. **Publications**: when the journals decide on the AC-MOT and SCL manuscripts, update their status on the Publications page and in entries [27] and [28] of the bibliography.
6. **Word fields**: the contents and lists already hold the page numbers of the PDF. If Word offers to update fields when the file is opened, choose "Update entire table" so the numbers follow Word's own layout.

## 7. Points left unchanged (they touch content, numbers or sources)
1. **Section 2.2.7, MOT17 paragraph**: "The benchmark distributes detections of a published YOLOX-X detector [16] that are used by many trackers." The MOT17 benchmark itself provides DPM, Faster R-CNN and SDP detections; the YOLOX-X detections are released with published tracker code. Suggested wording, if confirmed: "Detections of a published YOLOX-X detector [16] on these sequences are used by many trackers."
2. **Thousands separators**: most counts use a comma (71,830; 16,592; 2,652), but some counts in Chapter 3 are written without one (1184, 1230, 1235, 5000). Left as they are because the task excludes any edit to numbers; adding the comma does not change a value if wanted. Image sizes (512, 1088, 1280, 1536) and sequence numbers (0001, 0020) are correctly written without a comma.
3. **BoostTrack with GBI**: Table 4.2 labels the row "BoostTrack, with GBI"; Table 4.7 and Fig. 4.3 use "BoostTrack, + GBI". Both mean the same setting; the labels were kept so that tables and figures stay exactly as in V6.
4. **Bibliography details that need the publisher's record** (no value was added without a source):
   - [1] Li et al. 2025 (IET Computer Vision) and [76] Stanojević and Todorović 2024 (Machine Vision and Applications): article number or pages not given.
   - [10] Cheng et al. 2023 (IEEE TPAMI): cited with the early-access pages "pp. 1–20"; the final volume, issue and pages can be added.
   - [45], [78], [101], [103], [105]: conference papers given without a publisher, while the other conference entries name one.
   - [17] Guo et al., [36] Vaswani et al., [37] Dosovitskiy et al. and [81] Wang et al. are cited as arXiv preprints; their peer-reviewed versions (ICML 2017, NeurIPS 2017, ICLR 2021, ICLR 2021) can be cited instead.
5. **Earlier open items** (from the V4–V6 reports, unchanged): disclosure items for the AC-MOT chapter, publisher reuse permissions for the submitted manuscripts, and confirmation of the Arabic title.
