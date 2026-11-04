# Changes from Thesis V9 to Thesis V10

Comments of the supervisor applied in this version.

| Comment | Location | Change |
|---|---|---|
| Abstract (copy and replace) | Abstract | Replaced by the text provided in the comments, including the new keywords; the abstract stays on one page (line spacing of the abstract page slightly reduced). |
| Chapter 1, Comment 1: real-time requirement | Section 1.3 | New paragraph "Real-time requirement": a 30 FPS stream gives about 33.3 ms per frame for the whole pipeline; AC-MOT adds about 4.2 ms per frame on a Tesla T4 GPU (about 13% of the interval) and SCL 2.95 ms per frame on a 4-vCPU processor (about 9%); the first development stages of AC-MOT required 25 FPS or more. |
| Chapter 1, Comment 2: one representation of the pipeline | Section 1.3, Eqs. (1.1)–(1.2) | New paragraph "One representation of the pipeline": $D_t=f_{\mathrm{det}}(I_t;\theta_t)$ and $\mathcal{T}_t=f_{\mathrm{trk}}(D_t,\mathcal{T}_{t-1};\phi_t)$; AC-MOT controls $\theta_t$ and SCL controls $\phi_t$, two complementary control points of one pipeline. The descriptions of the two controllers in the same section now refer to Eqs. (1.1) and (1.2). |
| Chapter 1, Comment 3: definition of training-free | Section 1.4 | New paragraph "Training-free": no learned model is trained, the detector and tracker are not retrained, and no parameter is fitted while the system runs; AC-MOT fixes its values once by cross-validation on calibration sequences, SCL uses standard values. |
| Chapter 2, Comment 1: critical analysis by requirement | Section 2.3.5, new Table 2.5 | Families of related methods against four questions: adapts detector settings, needs trained parts or labels, changes the tracker, use when the detector or tracker is exchanged. |
| Chapter 2, Comment 2: novelty statement | Section 2.3.5, after Table 2.4 | New paragraphs separating established methods used as components, new combinations, and new control rules and findings, and stating the algorithmic differences from AdaScale, ApproxDet, Chameleon, Adaptive ByteTrack, and ACT. |
| Chapter 2, Comment 3: threshold rules compared | Section 2.3.3, Eqs. (2.16)–(2.17) | New paragraph comparing how ACT, a sliding-window controller, and SCL derive their thresholds, and which information each one uses (current frame, temporal history, tracks, classes). |
| Chapter 5, Comment 2: research questions | Section 5.1, new Table 5.2 | Each research question with its principal evidence and main finding. |
| Chapter 5, Comment 4: combined evaluation | Section 5.2, item 4 | Planned evaluation of four configurations (original pipeline, AC-MOT alone, SCL alone, both) by HOTA, MOTA, IDF1, IDS, stability of states and modes, and time per frame. |
| Chapter 5, Comment 5: concrete objectives | Section 5.2, items 1, 2, 3, 5 | Each direction now has an evaluation objective: frozen transfer and recalibration reported separately for new detectors; HOTA and IDS for end-to-end trackers; logged mode and confident share for detector updates; an embedded GPU target at 30 FPS (33.3 ms per frame) for onboard deployment. |

Comments not applied in this version: Chapter 3, Comments 1–5; Chapter 5, Comments 1 and 3.

## Checks on the V10 build
| Check | Result |
|---|---|
| Chapters 3 and 4 (LaTeX source, against V9) | numbers, math, table rows, citations, labels and references identical |
| Chapters 1, 2 and 5 | only additions; every number, equation, table row and citation of V9 is still present |
| Bibliography | unchanged; every reference keeps its number [1]–[107] |
| Word tables and equations | all 36 tables and 34 equations of V9 unchanged; 2 new tables (2.5, 5.2) and 4 new equations (1.1, 1.2, 2.16, 2.17) |
| LaTeX build | 0 errors, 0 undefined references, 0 overfull boxes, no float larger than the page |
| Contents and lists | 131 of 131 page numbers correct; 131 of 131 entries linked |
| Figures, tables and algorithms after first mention | Word PDF 46 of 46; LaTeX PDF 44 of 44 |
| Pages | Word PDF 102; LaTeX PDF 97; abstract on one page |
