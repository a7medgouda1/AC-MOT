# Changes from Thesis V17 to Thesis V18

Thesis V18 adds the figures of Section II of `v4.docx` (the application figures, v4 Figures 2–7) to Section 2.2 of the thesis. Nothing else changed: all text outside Section 2.2, the results, the tables, the equations and the references are identical to V17.

- Previous version: `THESIS_V17` (Word PDF 118 pages, LaTeX PDF 114 pages); left unchanged.
- New version: `THESIS_V18` (Word PDF 122 pages, LaTeX PDF 117 pages).
- Page numbers below are the printed page numbers of `word/Thesis_V18.pdf`.

## 1. Application figures of v4, redrawn

The owner supplied the v4 figures (`v4_all_images.zip`), so their reuse is cleared.

The original images contain misspelled labels, for example:
- "Unprexictable", "Robost" and "Global Trackies" (v4 Fig. 4);
- "Detsction", "Grobal Tracker" and "Inecal Database" (v4 Fig. 5);
- "Caregariver" and "Health Reord" (v4 Fig. 6);
- "Froud" and "Preditive" (v4 Fig. 7).

They also contain repeated labels ("Perception" twice in v4 Fig. 3) and text too small to read in print. For these reasons, each figure was redrawn as a vector diagram. The redrawn figure keeps the content and structure of the v4 original, corrects the labels, and uses the style of the other diagrams of the thesis.

| Thesis figure | Page | v4 source | Content |
|---|---|---|---|
| Fig. 2.1 Multi-camera surveillance system with one identity per person | 15 | v4 Fig. 2 | four cameras with local detection and tracking → central server with person re-identification → global identities |
| Fig. 2.2 Multi-sensor perception of an autonomous vehicle | 16 | v4 Fig. 3 | cameras, LiDAR, radar → sensor fusion → object detection → multi-object tracking → motion planning |
| Fig. 2.3 Scale variation and camera motion in UAV video | 17 | v4 Fig. 4 | scale variation (high vs. low altitude) and camera motion (frame *t* vs. frame *t*+1 with shifted, blurred boxes) → requirements: reliable features for small objects, association under camera motion, real-time processing on board |
| Fig. 2.4 Multi-camera tracking of parts for automated assembly | 18 | v4 Fig. 5 | assembly cell → three local units (detection, local IDs, features, local tracker) → central server (global IDs, trajectories) → robot controller, robot arm, operator dashboard |
| Fig. 2.5 Monitoring system for patient safety and assistive care | 19 | v4 Fig. 6 | wearable and ambient sensors → local processing unit (monitoring, activity recognition, fall and distress detection) → central server, alerts, assistive devices |
| Fig. 2.6 Retail analytics system for customer tracking and automated checkout | 20 | v4 Fig. 7 | customer tracking and smart shelves → local processing unit → automated checkout and central server → manager dashboard |

- Each figure is introduced in the text before it appears:
  - the opening paragraph of Section 2.2 (page 14) refers to Figures 2.1–2.6 and explains the colors of the blocks: gray = sensors, blue = local processing, green = blocks that combine several sources, orange = outputs;
  - each subsection also has a sentence that describes its own figure.
- The former Figures 2.1 and 2.2 (score use of trackers; outcomes counted by the MOT metrics) are now Figures 2.7 and 2.8. All references to them are updated.
- The v4 images not related to the applications were not added, because the thesis already covers their topics with its own figures and tables:
  - Fig. 1, the timeline;
  - Figs. 8–10, the challenges;
  - Figs. 11–14, the tracking paradigms;
  - the dataset table image.

## 2. Files
- `figures/app_surveillance.tex`, `app_av.tex`, `app_uav.tex`, `app_robotics.tex`, `app_health.tex` and `app_retail.tex`: TikZ sources, compiled by `word/build_all.sh`.
- `deliverables/figures/Figure_2_1_…` to `Figure_2_6_…`: each figure as PDF, SVG (vector, editable), PNG at 300 dpi, and its source. Each source compiles on its own with `fig_preamble.tex`.
- `chapters/ch2_applications.tex`: six figure environments and the sentences that introduce them.

## 3. Verification against V17
| Check | Result |
|---|---|
| Word tables (39) | identical to V17 |
| Numbers in the PDF text | unchanged; the only differences are figure numbers of Chapter 2 |
| References | identical to V17 (118 entries, same numbering) |
| Front matter and Arabic pages | identical to V17 |
| Contents, List of Figures, List of Tables | 159 of 159 entries linked; page numbers match the PDF |
| Figures, tables and algorithms placed after their first mention | 60 of 60 |
| Broken cross-references; error marks (¿) | 0; 0 |
| LaTeX build | 0 errors, 0 undefined references, 0 overfull boxes |
| Pages | Word PDF 122 (V17: 118); LaTeX PDF 117 (V17: 114) |
