# Changes from Thesis V16 to Thesis V17

Thesis V17 implements the supervisor's revisions: the block diagrams of Chapter 1, a new applications section in Chapter 2, and a restructured Chapter 5 with research limitations and future work. All experimental results, tables of results, equations and earlier citations are unchanged.

- Previous version: `THESIS_V16` (Word PDF 109 pages, LaTeX PDF 105 pages); left unchanged.
- New version: `THESIS_V17` (Word PDF 118 pages, LaTeX PDF 114 pages).
- Supervisor checklist: `SUPERVISOR_REQUIREMENTS_CHECKLIST.md`.
- Page numbers below are the printed page numbers of `word/Thesis_V17.pdf`. Arabic page numbers are body pages; Roman numerals are front-matter pages.

## 1. Figures 1.1 and 1.2 (Chapter 1)

The supervisor asked for the block diagrams of Figures 1.1 and 1.2 to identify the inputs and outputs of every block and to show where the processing starts. Both figures were redrawn as vector diagrams, and their numbering is unchanged.

### Figure 1.1, "Tracking-by-detection pipeline with fixed operating points" (page 2)
- The figure now begins with an explicit **START: input video stream** block and ends with an **END: tracking result** block.
- Each processing block (Detector, Online tracker) states its **In**, **Does** and **Out** lines:
  - Detector: in frame *I_t*, out candidate detections *D_t*.
  - Tracker: in *D_t* and the tracks *T_{t−1}*, out tracks *T_t*.
- Every arrow carries a label naming what it carries: frame *I_t*, *D_t*, *T_t*.
- Three arrow types are explained in a legend:
  - solid arrows for data;
  - dotted arrows for the fixed settings, shown as separate panels: the detector operating point θ = (c, η, r) and the tracker thresholds a, b, ℓ, m0;
  - a dashed arrow for the tracks kept for the next frame.
- New caption, and a new sentence on page 1 that introduces the figure before it appears.

### Figure 1.2, "Outline of the proposed approach" (page 8)
- The figure starts from the same **START: input video stream** block, and the main path runs:
  Detector (frozen) → Controller 2: SCL (Chapter 4) → Tracker (frozen) → **END: tracking result**.
- Controller 1, AC-MOT (Chapter 3), sits beside the detector:
  - It reads frame *I_t* and the boxes tracked in frame *t − 1*.
  - It sends the operating point θ_t = (c_t, η_t, r_t) to the detector as a control signal (dotted arrow).
  - It has no connection to the tracker, so the figure does not show AC-MOT changing the tracker.
- SCL sits between the detector and the tracker:
  - It reads *D_t*, the recent score logits, *T_{t−1}*, the camera motion, and the host contract (a, b, ℓ, m0) of the tracker.
  - It outputs the tracker input (*K_t*, scores, *a_t*, *b_t*, *m_t*).
  - It has no arrow back to the detector, so the figure does not show SCL retraining or reconfiguring the detector.
- Every block lists In / Does / Out. A legend separates:
  - data arrows, control/settings arrows and feedback arrows;
  - frozen components (blue), AC-MOT (orange) and SCL (green).
- New caption, stating that the detector and tracker are not modified and that each controller can be used on its own. The introducing sentence on page 7 now describes the start of the pipeline and the inputs and outputs of both controllers.

### Editable sources
- LaTeX/TikZ sources: `figures/tbd_pipeline.tex` and `figures/outline.tex`, compiled by `word/build_all.sh`.
- Delivered copies in `deliverables/figures/`:
  - PDF and SVG (vector, editable in Inkscape, Illustrator or PowerPoint);
  - PNG at 300 dpi;
  - the `.tex` sources with `fig_preamble.tex`, which compile on their own with `pdflatex`.

## 2. New Section 2.2, Applications of Real-Time Object Detection and Multi-Object Tracking (Chapter 2)

### Structure of Chapter 2
| V16 | V17 |
|---|---|
| 2.1 Introduction | 2.1 Introduction (rewritten: applications first, then the technical roadmap) |
| — | **2.2 Applications of Real-Time Object Detection and Multi-Object Tracking** (new, pages 13–17) |
| 2.2 Technical Background (2.2.1–2.2.8) | 2.3 Technical Background (2.3.1–2.3.8), text unchanged |
| 2.3 Related Work (2.3.1–2.3.5) | 2.4 Related Work (2.4.1–2.4.5), text unchanged |
| 2.4 Summary | 2.5 Summary (first sentence now mentions the applications) |

### Content of Section 2.2
- The opening paragraph explains how the application domains differ: the objects, the camera platform, the recording conditions, and the delay and computation they can accept.
- New **Table 2.1** (page 14) lists, for each domain, the typical objects, the main difficulties and the operating constraints.
- 2.2.1 Surveillance and Security (page 14): single-camera and multi-camera tracking, anomaly detection, crowds, lighting, and many streams per server.
- 2.2.2 Autonomous Vehicles and Advanced Driver-Assistance Systems (page 15): KITTI, nuScenes, three-dimensional tracking, LiDAR and 4D-radar fusion, and strict latency.
- 2.2.3 Unmanned Aerial Vehicles and Drone Tracking (pages 15–16), emphasized:
  - UAV uses and the aerospace literature, and the VisDrone and UAVDT benchmarks used in the thesis;
  - a list of the aerial challenges: small objects, scale variation, camera motion, occlusion and crowded scenes, variable lighting and weather, and real-time processing constraints;
  - a closing paragraph that links these challenges to the motivation of AC-MOT and SCL without presenting the methods: conditions change within a flight, and the onboard detector is often replaced or compressed.
- 2.2.4 Industrial Robotics (page 16): grasp planning, visual SLAM, and human safety.
- 2.2.5 Healthcare and Assistive Systems (page 16): medical image analysis, surgical video, and fall detection.
- 2.2.6 Retail and Marketing Analytics (page 17): customer tracking, dense shelf detection, and product recognition.
- The section closes with a transition paragraph, "From applications to technical requirements", that leads into Section 2.3.
- The former "Applications and challenges" paragraph of the MOT fundamentals (V16 Section 2.2.3) duplicated the new section. It was shortened to the three core problems of MOT, and its aerospace citations now appear in Section 2.2.3.

### Sources
- The structure follows Section II of `v4.docx` and the published survey of the author (ICMISI 2026, reference [5]).
- Several citations in v4 did not support the statements they were attached to; for example, a company web page, a blog, and a medical-imaging article were cited for UAV tracking. These citations were not carried over.
- Each domain is instead supported by peer-reviewed sources. Eleven new references were added, each verified against its Crossref record (DOI, venue, volume and pages):
  - Ristani & Tomasi, CVPR 2018;
  - Sultani et al., CVPR 2018;
  - Caesar et al. (nuScenes), CVPR 2020;
  - Weng et al. (AB3DMOT), IROS 2020;
  - Mur-Artal & Tardós (ORB-SLAM2), IEEE T-RO 2017;
  - Mahler et al. (Dex-Net 2.0), RSS 2017;
  - Litjens et al., Medical Image Analysis 2017;
  - Twinanda et al. (EndoNet), IEEE TMI 2017;
  - Mubashir et al., Neurocomputing 2013;
  - Goldman et al., CVPR 2019;
  - Wei et al., Computational Intelligence and Neuroscience 2020.
- The figures of `v4.docx` were not reused, because their source and reuse rights are not documented.

## 3. Chapter 5 restructured: 5.1 Conclusions, 5.2 Research Limitations, 5.3 Future Work

### 5.1 Conclusions (pages 88–90)
- The conclusions of V16 are kept, with all numbers unchanged.
- A new paragraph states that the two controllers are distinct methods, each developed, frozen and evaluated on its own.
- The "Evaluation coverage" paragraph moved to Section 5.2.3, where it is stated as a limitation.
- RQ3 wording was corrected for accuracy, in the text and in the Table 5.2 cell:
  - V16: "effects kept on data, trackers, and detectors not used in design".
  - V17: "effects kept on held-out data and on trackers not used in design".
  - Reason: the UAVDT detectors of SCL had been used in its KITTI development, so "detectors not used in design" overstated the evidence.

### 5.2 Research Limitations (pages 90–93), new
The section opens by stating that each limitation is given together with what the experiments showed, so that demonstrated behavior is kept separate from untested conditions.

| Section | Limitation | Demonstrated | Not tested (stated as open) |
|---|---|---|---|
| 5.2.1 | Dependence on reliable scene cues (AC-MOT) | all three states used, few state changes on the evaluated sequences; SCI averaging, hysteresis, dwell and recovery limit short disturbances | sequences with deliberately corrupted or misleading cues |
| 5.2.2 | Sensitivity to detection-score distributions (SCL) | correct operation under halved, cubed and temperature-scaled scores and with replacement detectors; cold-mode fallback when no valid split exists | detectors with uninformative or strongly overlapping score distributions |
| 5.2.3 | Limited detector coverage of AC-MOT | frozen controller: YOLO11m on VisDrone2019-MOT and UAVDT with ByteTrack and OATrack; action map {1088, 1280, 1536} × {0.45, 0.60, 0.70} × {0.10, 0.25, 0.40} | other detector families (two-stage, transformer-based) and detectors trained on other data |
| 5.2.4 | Host contract of SCL | seven published trackers, including two external trackers chosen before the run, served by one configuration | joint detection-and-tracking, transformer-based, and appearance-only trackers; separates architectural requirements from implementation choices (per-family adapter) |
| 5.2.5 | Incomplete embedded-hardware validation | controller cost measured: AC-MOT on a Tesla T4 (200 frames); SCL and a YOLOv8n + ByteTrack pipeline on a 4-vCPU CPU | end-to-end latency, memory, power and thermal behavior on embedded UAV processors (no benchmark is claimed) |

### 5.3 Future Work (pages 93–94), revised
- The section states that none of the listed studies has been carried out.
- Each of the first five items refers to the limitation it addresses:
  1. Robust scene cues and controller reliability (5.2.1)
  2. Score-distribution robustness of SCL, with alternative label-free partitions (5.2.2)
  3. More detectors and datasets for AC-MOT, transferred and recalibrated (5.2.3); extends V16 item "New detectors and aerial platforms"
  4. Portability of SCL to other tracker interfaces (5.2.4); extends V16 item "End-to-end trackers"
  5. Embedded-hardware evaluation (5.2.5); extends V16 item "Onboard deployment"
  6. Deployment optimizations (new)
  7. Monitoring of detector updates (kept from V16)
  8. A combined pipeline (kept from V16)

## 4. Other consistency updates
- Section 1.5 (Thesis Organization, pages 11–12): the descriptions of Chapter 2 and Chapter 5 now mention the applications review and the research limitations.
- Fig. 1.2 caption: the scores of SCL are named in words (the Word caption cannot show the tilde accent).
- Cross-references to the renumbered Chapter 2 sections are updated automatically, for example 2.2.6 → 2.3.6 in Chapters 3 and 4.
- Because the bibliography is ordered by first citation, reference numbers shift after the new citations in Section 2.2. No reference was removed: 118 entries, against 107 in V16.

## 5. Verification against V16

| Check | Result |
|---|---|
| Source files changed | `ch1_introduction.tex`, `ch2_background.tex`, `ch5_conclusions.tex`, `figures/tbd_pipeline.tex`, `figures/outline.tex`, `references.bib`; new `ch2_applications.tex`; Word build scripts changed only in the version name |
| Chapters 3 and 4 source text | identical to V16 |
| Word tables (V16: 38, V17: 39) | all identical to V16 after renumbering citations, except the new Table 2.1 and the RQ3 cell of Table 5.2 |
| Experimental numbers in the PDF text | no number of V16 missing in V17; the only new numbers are section numbers, the action-map search values already given in Table 3.2, and "2.0" in the title of the Dex-Net reference |
| References | all 107 V16 entries still cited; 11 new entries |
| Front matter (cover, title pages, abstract, acknowledgments, abbreviations) | text identical to V16 |
| Arabic pages | pixel-identical to V16 |
| Contents, List of Figures, List of Tables | 153 of 153 entries linked; page numbers checked against the PDF |
| Figures, tables and algorithms placed after their first mention | 54 of 54 |
| Broken cross-references ("??", "Error!") | 0 |
| Error marks (¿) in equations | 0 |
| LaTeX build | 0 errors, 0 undefined references, 0 overfull boxes |
| Fonts | Times New Roman in the text; equation fonts of the equation editor |
| Pages | Word PDF 118 (V16: 109); LaTeX PDF 114 (V16: 105) |

## 6. Open items for the owner
- `v4.docx` figures: not reused because their reuse rights are unknown. Add them only if their source and license are confirmed.
- Figures 1.1 and 1.2 are drawn in TikZ to match the other diagrams of the thesis. The SVG copies can be edited in a vector editor if a different layout is wanted.
