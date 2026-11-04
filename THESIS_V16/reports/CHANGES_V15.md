# Changes from Thesis V14 to Thesis V15

Final pass before the thesis goes to the supervisors: language, consistency of names and numbers, one font family, and clearer figures. No number in a result table, no equation and no citation was changed.

## Text
| # | Location | V14 | V15 |
|---|---|---|---|
| 1 | Abstract, SCL paragraph | Comparisons with adaptive-threshold baselines and ACT … | Comparisons with adaptive-threshold baselines and with the published ACT method … |
| 2 | Acknowledgments | the Computer Engineering and Artificial Intelligence Department of the Military Technical College | the Chair of Computing Engineering and Artificial Intelligence of the Military Technical College (the name on the title pages) |
| 3 | Chapter 1, Section 1.3, paragraph after RQ3 | The first concerns one place in the pipeline, the detector call, in aerial video, where the scores of the detector are read through the tracker's published thresholds. | The first concerns one point of the pipeline, the detector call, in aerial video, while the tracker keeps reading the detector scores through its published thresholds. |
| 4 | Chapter 3, Section 3.1 | On the VisDrone2019 dataset with ByteTrack | On VisDrone2019-MOT with ByteTrack |
| 5 | Chapter 3, Section 3.2 | c_t is the score threshold. | c_t is the confidence threshold, also called the score threshold. |
| 6 | Chapter 3, Section 3.3.4 | … thus has the smallest input. The search optimizes tracking quality: … | … has the smallest input, because the search optimizes tracking quality: … |
| 7 | Chapter 3, Section 3.4.2 | … 265 fewer IDS [82, 502] and −2.617 HOTA [−4.004, −1.694]. | … 265 fewer IDS [82, 502]. |
| 8 | Chapter 3, Section 3.4.3 | … reduces IDS from 136 to 123, with MOTA +0.0371 points [−0.041, +0.182]. | … reduces IDS from 136 to 123. |
| 9 | Chapter 3, Section 3.6.1 | … lie entirely on the side of improvement, while FN and recall move in the opposite direction. | … lie entirely on the side of improvement. |
| 10 | Chapter 3, Section 3.6.5 | … lanterns along the road, where they start short-lived tracks. | … lanterns along the road. |
| 11 | Chapter 3, Section 3.6.5 | … two with AC-MOT, and is followed in 70 of its 71 frames. | … two with AC-MOT, which follows it in 70 of its 71 frames. |
| 12 | Chapter 3, Section 3.6.5 | … against two identities over 149 frames. | … against two identities over 149 frames at the fixed operating point. |
| 13 | Chapter 3, text, captions and Table 3.8 | 5000 resamples; 1230; 2652 frames; 3282 frames; FN (25432 to 25057) | 5,000 resamples; 1,230; 2,652 frames; 3,282 frames; FN (25,432 to 25,057) — thousands separators as in the rest of the text |
| 14 | Arabic title page | الاصطناعى؛ الماجستير فى | الاصطناعي؛ الماجستير في (the spelling of the Arabic summary) |

## Fonts
- The whole thesis uses Times New Roman: the document defaults and the styles of the contents (all levels), the lists of figures and tables, the headings, the captions and the page numbers now name Times New Roman, as the body text and the first contents level already did (V14: Calibri in the second and third contents levels, the lists and the page numbers).
- The signature of the acknowledgments is set in Times New Roman italic, 14 pt (V14: a script font that is not installed on every computer).
- The PDF is produced with the Times New Roman font itself, so it shows the same font as the Word file.

## Figures
- Figs. 1.3, 2.2, 3.5, 3.6 and 3.7: Times New Roman, larger labels (track IDs 6–7.5 pt, panel text 8 pt, titles 9–10 pt), wider lines, and "tracked" instead of "tracked GT" in the panel text; the night frames are shown with a display gamma applied in the same way to every panel (1.3 for Figs. 1.3 and 3.5, 1.6 for Figs. 2.2 and 3.7). Same frames, objects, tracks and counts as in V14.
- Fig. 3.6: larger text; the HIGH label is placed clear of the SCI curve.
- Fig. 3.2 (state diagram): larger text and more space between the states.
- Fig. 4.5: larger value labels on the bars.

## Checks on the V15 build
| Check | Result |
|---|---|
| Word tables (38) | identical to V14 except the two cells of the list above (Table 3.8 "5,000"; Arabic title page) |
| Bibliography | unchanged; every reference keeps its number |
| Sources against V14 | word-by-word comparison: only the changes above |
| LaTeX build | 0 errors, 0 undefined references, 0 overfull boxes |
| Contents and lists | 139 of 139 page numbers correct; 139 of 139 entries linked |
| Figures, tables and algorithms after first mention | Word PDF 53 of 53 |
| Fonts in the Word PDF | Times New Roman for all text, Latin and Arabic; equation symbols in the fonts of the equation editor |
| Document properties | author and last editor Ahmed Gouda Ismail; title "Real-Time Target Detection and Tracking" |
| Pages | Word PDF 109 (abstract and acknowledgments one page each); LaTeX PDF 105; table of contents 3 |
