# Changes from Thesis V12 to Thesis V13

Figures of real tracked video frames were added to every chapter, together with Section 3.6.5 requested by the supervisor, a state diagram of AC-MOT and a chart of the SCL score-shift results. No existing number, table, equation, figure or citation was changed.

| # | Location | Added in V13 |
|---|---|---|
| 1 | Chapter 1, Section 1.4, before the list of contributions | Paragraph and **Fig. 1.3**: the two controllers on real tracked frames (VisDrone2019-MOT frame 278, baseline vs AC-MOT; KITTI 0001 frame 102, tracker alone vs SCL) |
| 2 | Chapter 2, Section 2.2.8, after the definition of identity switches | Paragraph and **Fig. 2.2**: outcomes counted by the MOT metrics (tracks with IDs and paths, false positives, missed objects, an identity switch) on frames 47 and 48 of a VisDrone2019-MOT video |
| 3 | Chapter 3, Section 3.3.3 | Sentence and **Fig. 3.2**: state diagram of AC-MOT (three states, operating point of each state, conditions of each change, dwell rule) |
| 4 | Chapter 3, new **Section 3.6.5 Qualitative Evaluation of Tracking Performance on Selected Video Frames** | Two qualitative experiments on VisDrone2019-MOT sequence uav0000117\_02622\_v with the same detector (YOLO11m) and tracker (ByteTrack): baseline at the fixed operating point (1536, 0.70) and AC-MOT. **Fig. 3.5** (frames 268, 273, 278: false tracks 47–54 → 22–28 per frame, same or more tracked objects), **Fig. 3.6** (whole video: SCI, state, annotated objects, false tracks per frame), **Fig. 3.7** (identities of single objects: 5 → 2, 6 → 3, 2 → 1) |
| 5 | Chapter 3, Section 3.7, paragraph "A more selective detection stream" | "…removing clutter and identity-confusing boxes**, as the tracked frames of Section 3.6.5 show**." |
| 6 | Chapter 3, Section 3.8 | One sentence on the qualitative experiments |
| 7 | Chapter 4, Section 4.6.3 | Sentence and **Fig. 4.5**: bar chart of Table 4.9 (HOTA of each tracker alone and with SCL under the three score changes) |
| 8 | Chapter 5, Section 5.1, paragraph on AC-MOT | One sentence on the qualitative experiments |

Figures renumbered by the insertions: Chapter 3, the VisDrone and UAVDT bar charts 3.2 → 3.3 and 3.3 → 3.4; all references in the text follow automatically. No table is renumbered.

Sources of the new figures: `research/acmot_paper_v2/qualitative_v1/` (`PROVENANCE.md`, `VERIFICATION.md`); `figures/acmot_states.tex` and `figures/scl_shift_bars.tex` (TikZ/pgfplots, values from Tables 3.1 and 4.9).

## Build script
- `word/build_all.sh`: the two new TikZ figures are compiled in step 1; step 3 has a second index pass, so that a list that grows by a page also moves the front-matter entries after it.
- `word/build_docx_v3.py`: the empty paragraph that closes each list field is one point high, so that a full list page does not push it onto an empty page.

## Checks on the V13 build
| Check | Result |
|---|---|
| Word tables (38) | identical to V12, cell for cell |
| Bibliography | unchanged; every reference keeps its number |
| Sources against V12 | word-by-word comparison: only insertions, plus the extended sentence of row 5 |
| LaTeX build | 0 errors, 0 undefined references, 0 overfull boxes |
| Contents and lists | 139 of 139 page numbers correct; 139 of 139 entries linked |
| Figures, tables and algorithms after first mention | Word PDF 53 of 53 |
| Pages | Word PDF 109; LaTeX PDF 104; table of contents 3 |
