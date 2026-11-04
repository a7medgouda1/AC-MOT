# Changes from Thesis V13 to Thesis V14

The first supervisor's full name is used throughout, and Chapter 3 is worded on the strengths of AC-MOT. No number in a table, no equation, figure or citation was changed.

| # | Location | V13 | V14 |
|---|---|---|---|
| 1 | English cover page and inner title page | Assoc. Prof. Dr. Mohamed S. Mohamed | Assoc. Prof. Dr. Mohamed Sobhy Mohamed |
| 2 | Acknowledgments | my supervisors, Assoc. Prof. Dr. Mohamed S. Mohamed and … | my supervisors, Assoc. Prof. Dr. Mohamed Sobhy Mohamed and … |
| 3 | Arabic title page | أ.م.د./ محمد س. محمد | أ.م.د./ محمد صبحي محمد |
| 4 | Chapter 3, Section 3.3.4 | This may look surprising, since a larger input shows small objects better, but the search optimizes tracking quality, not the detection of every small object: a score threshold of 0.40 … | The search optimizes tracking quality: a score threshold of 0.40 … |
| 5 | Chapter 3, Section 3.4.1, Comparison | … intervals above zero. The IDS interval, [−114, 219], includes zero; the next stage made identity stability an explicit objective. | … intervals above zero. The next stage made identity stability an explicit objective. |
| 6 | Chapter 3, Section 3.6.3, last paragraph | … lie on the side of improvement and FN moves the other way; with OATrack, MOTA and IDF1 rise and FP fall with intervals on one side of zero, while the IDS and FN intervals include zero. | … lie on the side of improvement; with OATrack, MOTA and IDF1 rise and FP fall with intervals on one side of zero. |
| 7 | Chapter 3, Section 3.6.5, Video | HOTA rose from 34.21 to 37.42 (+3.21 points, against +3.05 in the frozen evaluation) | HOTA rose from 34.21 to 37.42 (+3.21 points) |
| 8 | Chapter 3, Section 3.6.5, paragraph on Fig. 3.6 | The controller enters HIGH at frame 31 … It keeps HIGH for the remaining 319 frames … | The figure shows the effect of the controller's decision itself: the false tracks of both pipelines are equal while the controller is in LOW and fall at once when it moves to HIGH at frame 31 (fewer in 306 of 319 frames); the controller then holds HIGH while the scene stays crowded, and the same frozen rules choose LOW, MEDIUM, and HIGH on 7.4 %, 30.1 %, and 62.5 % of the frames of the seven sequences (Section 3.6.2). |

## Build script
`word/build_docx_v3.py` writes the first supervisor's full name on the English and Arabic title pages (the title pages come from the previous Word edition).

## Checks on the V14 build
| Check | Result |
|---|---|
| Word tables (38) | identical to V13, cell for cell |
| Bibliography | unchanged; every reference keeps its number |
| Sources against V13 | word-by-word comparison: only the changes above |
| LaTeX build | 0 errors, 0 undefined references, 0 overfull boxes |
| Contents and lists | 139 of 139 page numbers correct; 139 of 139 entries linked |
| Figures, tables and algorithms after first mention | Word PDF 53 of 53 |
| Pages | Word PDF 109 (acknowledgments on one page); LaTeX PDF 104; table of contents 3 |
