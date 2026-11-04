# Changes from Thesis V8 to Thesis V9

| # | Location | Original (V8) | Revised (V9) |
|---|---|---|---|
| 1 | Chapter 5, Section 5.1, Evaluation coverage (page 75) | … including two predeclared external trackers and a held-out test split. | … including two predeclared external trackers and a held-out test split. The two controllers were developed and evaluated separately; their joint use in one pipeline was not part of the evaluation. |
| 2 | Chapter 5, Section 5.2, item 4 "A combined pipeline" (page 75) | Since the two controllers act on different parts of the pipeline, they can run in one pipeline, in which AC-MOT sets the detector operating point and SCL adapts the tracker input to the resulting scores, to combine the gains of both. | Since the two controllers act on different parts of the pipeline, they can be run together, with AC-MOT setting the detector operating point and SCL adapting the tracker input to the resulting scores, to evaluate whether their improvements are complementary. |

## Checks on the V9 build
| Check | Result |
|---|---|
| Numbers, math, table rows, citations, labels, references (LaTeX source, against V8) | all identical |
| Bibliography | unchanged; citation numbers [1]–[107] unchanged |
| Word tables (36) and equations (34) | identical to V8 |
| Text of the Word PDF against V8 | only the two changes above |
| LaTeX build | 0 errors, 0 undefined references, 0 overfull boxes, no float larger than the page |
| Contents and lists | 129 of 129 page numbers correct; 129 of 129 entries linked |
| Figures, tables and algorithms after first mention | Word PDF 44 of 44; LaTeX PDF 42 of 42 |
| Pages | Word PDF 98 (as V8); LaTeX PDF 93 |
