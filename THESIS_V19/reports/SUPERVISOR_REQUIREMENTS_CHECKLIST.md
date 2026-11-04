# Supervisor Requirements Checklist — Thesis V19

Every row was verified in the final PDF, `THESIS_V19/word/Thesis_V19.pdf` (126 pages). Page numbers are the printed page numbers of that PDF. A row is marked PASS only after it was checked in the rendered pages.

| Supervisor Requirement | Implemented | Verified | Location | Notes |
|---|---|---|---|---|
| Fig. 1.1: identify the starting block | Yes | PASS | Fig. 1.1, p. 2 | "START: input video stream" block at the top; "END: tracking result" at the bottom |
| Fig. 1.1: inputs and outputs of each processing block | Yes | PASS | Fig. 1.1, p. 2 | Detector and tracker blocks each list In / Does / Out; every arrow is labeled (frame I_t, D_t, T_t) |
| Fig. 1.1: distinguish settings and feedback from the data path | Yes | PASS | Fig. 1.1, p. 2 | solid = data, dotted = fixed settings (θ = (c, η, r); a, b, ℓ, m0), dashed = tracks kept for the next frame; legend under the figure |
| Fig. 1.2: identify the starting block | Yes | PASS | Fig. 1.2, p. 8 | Same START block; main path START → Detector → SCL → Tracker → END |
| Fig. 1.2: inputs and outputs of each processing block | Yes | PASS | Fig. 1.2, p. 8 | Detector, AC-MOT, SCL and Tracker list In / Does / Out; host contract panel shows the values read by SCL |
| Fig. 1.2: distinguish control and feedback flows | Yes | PASS | Fig. 1.2, p. 8 | dotted = settings (θ_t from AC-MOT, host contract), dashed = tracks of the previous frame; color legend: frozen / AC-MOT / SCL |
| Fig. 1.2: SCL not shown retraining the detector; AC-MOT not shown changing the tracker | Yes | PASS | Fig. 1.2 and caption, p. 8 | no SCL arrow to the detector; no AC-MOT arrow to the tracker; detector and tracker marked "frozen"; the caption states both facts |
| Figures keep numbers 1.1 and 1.2; captions revised | Yes | PASS | p. 2, p. 8; List of Figures p. VI | captions describe the start block, the inputs and outputs, and the arrow types |
| Figures introduced in the text before they appear | Yes | PASS | p. 1 (Fig. 1.1), p. 7 (Fig. 1.2) | the first mention precedes each figure |
| Editable figure sources | Yes | PASS | `THESIS_V19/figures/tbd_pipeline.tex`, `outline.tex`; `THESIS_V19/deliverables/figures/` | PDF, SVG (vector, editable), PNG 300 dpi and TikZ source; the sources compile on their own |
| Ch. 2: new Section 2.2 on applications (from v4 Section II) | Yes | PASS | Section 2.2, pp. 13–22; Contents p. III | placed after 2.1 Introduction and before 2.3 Technical Background |
| 2.2.1 Surveillance and Security | Yes | PASS | p. 14; Fig. 2.1, p. 15 | |
| 2.2.2 Autonomous Vehicles and ADAS | Yes | PASS | p. 15; Fig. 2.2, p. 16 | |
| 2.2.3 UAVs and Drone Tracking (emphasized) | Yes | PASS | pp. 16–17; Fig. 2.3, p. 18 | longest subsection; it covers the VisDrone and UAVDT benchmarks used in the thesis |
| UAV challenges: small objects, scale variation, camera motion, occlusion, crowds, lighting, real-time constraints | Yes | PASS | Section 2.2.3, pp. 16–17 | each challenge has its own bulleted item with a citation |
| Link the UAV challenges to AC-MOT without presenting the method | Yes | PASS | Section 2.2.3, last paragraph, p. 17 | within-flight changes and detector replacement motivate Chapters 3 and 4; no method details |
| 2.2.4 Industrial Robotics | Yes | PASS | p. 18; Fig. 2.4, p. 19 | |
| 2.2.5 Healthcare and Assistive Systems | Yes | PASS | pp. 19–20; Fig. 2.5, p. 20 | |
| 2.2.6 Retail and Marketing Analytics | Yes | PASS | p. 21; Fig. 2.6, p. 21 | |
| Summary table of the application domains | Yes | PASS | Table 2.1, p. 14; List of Tables p. VIII | objects, difficulties and operating constraints for each domain |
| Transition from 2.2 to 2.3 | Yes | PASS | end of Section 2.2, p. 22 | the paragraph "From applications to technical requirements" leads into 2.3 |
| Technical Background moved to 2.3 | Yes | PASS | Section 2.3, p. 22; Contents p. III | 2.3.1–2.3.8 unchanged in content; Related Work → 2.4, Summary → 2.5 |
| Chapter 2 introduction and roadmap updated | Yes | PASS | Section 2.1, p. 13; Summary 2.5, p. 43 | the introduction presents applications first, then the technical roadmap |
| Verifiable references; weak claims of v4 not copied | Yes | PASS | References pp. 102–110 | 11 new peer-reviewed references verified against Crossref; v4 citations that did not support their claims were replaced |
| Reuse v4 figures only with clear rights | Yes | OPEN (owner) | Figs. 2.1–2.10, pp. 15–28 | the original v4 images, supplied by the owner, are embedded unchanged (`IMAGE_MAPPING_REPORT_V19.md`); the source of the pedestrian photographs in Fig. 2.1 is not documented and must be confirmed by the owner |
| Application figures introduced before they appear | Yes | PASS | p. 14 (Figs. 2.1–2.6); one sentence in each of 2.2.1–2.2.6 | 64 of 64 floats after their first mention |
| Ch. 5 structure: 5.1 Conclusions, 5.2 Research Limitations, 5.3 Future Work | Yes | PASS | pp. 95, 97, 100; Contents p. V | |
| 5.2.1 Dependence on reliable scene cues (AC-MOT) | Yes | PASS | p. 98 | |
| 5.2.2 Sensitivity to detection-score distributions (SCL) | Yes | PASS | p. 98 | |
| 5.2.3 Limited detector coverage of AC-MOT | Yes | PASS | p. 99 | states the exact detector, datasets, trackers and action-map values evaluated |
| 5.2.4 Host contract of SCL | Yes | PASS | p. 99 | separates architectural requirements from implementation choices |
| 5.2.5 Incomplete embedded-hardware validation | Yes | PASS | p. 100 | states only the measured hardware (Tesla T4; 4-vCPU CPU); no embedded benchmark is claimed |
| Separate hypothetical failure modes from demonstrated behavior | Yes | PASS | Section 5.2 opening, p. 97; end of each 5.2.x | each limitation states what was shown and what was not tested |
| No invented benchmarks or results | Yes | PASS | Chapter 5 | all numbers come from Chapters 3 and 4; the Jetson platform appears only as a future target |
| 5.3: scene-cue robustness | Yes | PASS | 5.3 item 1, p. 100 | linked to 5.2.1 |
| 5.3: score-distribution robustness and alternative calibration | Yes | PASS | 5.3 item 2, p. 100 | linked to 5.2.2 |
| 5.3: more detectors and datasets for AC-MOT | Yes | PASS | 5.3 item 3, p. 100 | linked to 5.2.3 |
| 5.3: SCL portability to other trackers | Yes | PASS | 5.3 item 4, p. 101 | linked to 5.2.4 |
| 5.3: embedded-hardware evaluation | Yes | PASS | 5.3 item 5, p. 101 | linked to 5.2.5 |
| 5.3: deployment optimizations | Yes | PASS | 5.3 item 6, p. 101 | |
| Keep useful existing future-work items without duplication | Yes | PASS | 5.3 items 7–8, p. 101 | "Monitoring of detector updates" and "A combined pipeline" kept; three earlier items merged into items 3–5 |
| Thesis Organization updated | Yes | PASS | Section 1.5, pp. 11–12 | Chapter 2 and Chapter 5 descriptions updated |
| Contents, List of Figures and List of Tables updated | Yes | PASS | pp. III–IX | 163 of 163 entries linked; page numbers match the PDF |
| Cross-references and numbering | Yes | PASS | whole document | 0 broken references; LaTeX build: 0 undefined references, 0 overfull boxes |
| Floats after their first mention | Yes | PASS | whole document | 64 of 64 figures, tables and algorithms |
| Front matter preserved | Yes | PASS | PDF pages 1–4 (cover to Acknowledgments), p. X | cover, title pages, abstract, acknowledgments and abbreviations identical to V16, V17 and V18 |
| Experimental results unchanged | Yes | PASS | Chapters 3–5 | all result tables identical to V16, V17 and V18; no number of V16 is missing |
| New version kept; earlier versions preserved | Yes | PASS | `THESIS_V19/` | `THESIS_V18/`, `THESIS_V17/` and earlier versions unchanged |
| Word and PDF regenerated | Yes | PASS | `THESIS_V19/word/Thesis_V19.docx`, `Thesis_V19.pdf` | Word PDF 126 pages; separate contents file `Thesis_V19_Table_of_Contents.docx` |
