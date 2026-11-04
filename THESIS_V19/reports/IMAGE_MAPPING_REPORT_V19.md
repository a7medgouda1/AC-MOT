# Original Images of v4 in Thesis V19: Inventory and Mapping

## Source archive
- **Archive used:** `v4_all_images.zip`, the copy uploaded to this session. No file named `v4_all_images(1).zip` was present in the session uploads. The archive that was available holds the same 15 files, `image1.png` to `image15.png`.
- **Match with v4.docx:** every file is byte-identical to the file of the same name in `word/media/` of the uploaded `v4.docx` (same SHA-256). The archive therefore contains the original images of v4.
- **Unchanged copies:** the 15 files are stored in `THESIS_V19/figures/v4_original/`.
- **Hash record:** the SHA-256 of every file and the figure it became are listed in `reports/V19_ORIGINAL_IMAGE_RECORD.csv`.

No image was redrawn, regenerated, cropped, recolored or edited. They were only resized proportionally on the page.

## 1. Inventory of the 15 images

| File | Pixels | Content | Topic | Readability at thesis size | Equivalent already in V18 | Decision |
|---|---|---|---|---|---|---|
| image1.png | 728×486 | timeline: Traditional Approaches (pre-2012: HOG, SIFT), Deep Learning (2012: R-CNN 2014, YOLO 2016, RetinaNet 2017), Transformer Era (DETR 2020, TransTrack 2021) | evolution of detection and tracking | good, large text | none (the text of 2.3.1 describes the same three phases) | inserted, Fig. 2.7 |
| image2.png | 702×376 | Camera 1–4, each with photographs of pedestrians → Server → Person Re-ID → person icon | surveillance, multi-camera identity | good, large text | redrawn Fig. 2.1 of V18 | replaced Fig. 2.1 |
| image3.png | 810×540 | High-Resolution Cameras, LIDAR, RADAR → Sensor Fusion → Object Detection, Object Tracking, Safe Navigation | autonomous vehicles | good, large text | redrawn Fig. 2.2 of V18 | replaced Fig. 2.2 |
| image4.png | 535×709 | drone over a park; Scale Variation (small and large object), Camera Motion (blur and jitter); challenges box | UAV tracking | good | redrawn Fig. 2.3 of V18 | replaced Fig. 2.3 |
| image5.png | 618×583 | assembly cell with cameras → local processing units → central server → automated assembly processing → robot arm, operator dashboard | industrial robotics | readable; smallest labels are small in print | redrawn Fig. 2.4 of V18 | replaced Fig. 2.4 |
| image6.png | 673×623 | patient environment, wearable and ambient sensors → local data collection and pre-processing → cloud server, alerts, assistive devices, caregiver dashboard; key outcomes | healthcare and assistive systems | readable; smallest labels are small in print | redrawn Fig. 2.5 of V18 | replaced Fig. 2.5 |
| image7.png | 768×682 | retail environment (customer tracking, automated checkout) → local processing → cloud server, checkout processing → manager dashboard; key outcomes | retail analytics | readable; smallest labels are small in print | redrawn Fig. 2.6 of V18 | replaced Fig. 2.6 |
| image8.png | 722×471 | five column headings (Scale, Rotation, Partial Occlusion, Illumination, Background Clutter) above pictures and descriptions that do not match them | detection challenges | good | none | not used (see Section 3) |
| image9.png | 718×485 | Identity Switches, Data Association, Crowded Scene Handling, with pictures and explanations | MOT challenges | readable | none (the text of 2.3.3 names the same problems) | inserted, Fig. 2.8 |
| image10.png | 746×439 | Accuracy–Speed Trade-off, Computational Cost, Deployment Limitations | real-time constraints | readable | none (the text of 2.3.3 describes the same three factors) | inserted, Fig. 2.9 |
| image11.png | 556×319 | Input frames → Object Detector → Feature Extractor → Data Association → Track Management / Visualization | tracking-by-detection pipeline | good | Fig. 1.1 (tracking-by-detection pipeline) | not used (see Section 3) |
| image12.png | 569×569 | Shared backbone → Detection Head and Tracking Head → detected and tracked objects | joint detection and tracking | readable | none (the text of 2.3.4 describes JDE and FairMOT) | inserted, Fig. 2.10 |
| image13.png | 769×309 | Input Video → Deep Learning Model (feature extraction and association) → Tracking Output | generic deep-learning tracking | good | none | not used (see Section 3) |
| image14.png | 703×626 | target template and frames → transformer encoder–decoder with cross-attention → prediction head | transformer-based single-object tracking | readable | none | not used (see Section 3) |
| image15.png | 985×750 | table of seven datasets (COCO, ImageNet VID, KITTI, MOT17/20, TAO, LaSOT, UAV123) | datasets | good | Table 2.4 and the datasets paragraph of 2.3.7 | not used (see Section 3) |

## 2. Mapping of the images used

The pages are the printed page numbers of `word/Thesis_V19.pdf`.

| Original file | Thesis figure | Chapter / section | Page | Status | Introduced in the text on page |
|---|---|---|---|---|---|
| image2.png | Fig. 2.1 Multi-camera surveillance system for consistent identity tracking | Ch. 2, 2.2.1 Surveillance and Security | 15 | replaced (the redrawn V18 figure was removed) | 14 |
| image3.png | Fig. 2.2 Multi-modal perception system of an autonomous vehicle based on the fusion of three sensors | Ch. 2, 2.2.2 Autonomous Vehicles and ADAS | 16 | replaced | 15 |
| image4.png | Fig. 2.3 UAV-based object tracking under scale variation and camera motion | Ch. 2, 2.2.3 UAVs and Drone Tracking | 18 | replaced | 17 |
| image5.png | Fig. 2.4 Industrial robotics system with multi-camera tracking for automated assembly operations | Ch. 2, 2.2.4 Industrial Robotics | 19 | replaced | 18 |
| image6.png | Fig. 2.5 Healthcare monitoring system for patient safety and assistive care | Ch. 2, 2.2.5 Healthcare and Assistive Systems | 20 | replaced | 20 |
| image7.png | Fig. 2.6 Retail analytics system for customer tracking and automated checkout | Ch. 2, 2.2.6 Retail and Marketing Analytics | 21 | replaced | 21 |
| image1.png | Fig. 2.7 Evolution of object detection and tracking methods | Ch. 2, 2.3.1 Object Detection Fundamentals | 23 | newly inserted | 22 |
| image9.png | Fig. 2.8 Main challenges of multi-object tracking | Ch. 2, 2.3.3 Multi-Object Tracking Fundamentals | 26 | newly inserted | 26 |
| image10.png | Fig. 2.9 Constraints on real-time performance | Ch. 2, 2.3.3 Multi-Object Tracking Fundamentals | 27 | newly inserted | 26 |
| image12.png | Fig. 2.10 Joint detection and tracking with a dual-head architecture | Ch. 2, 2.3.4 Tracking-by-Detection Architectures | 28 | newly inserted | 27 |

### Renumbering
- The figures of V18 that follow in Chapter 2 were renumbered:
  - Fig. 2.7 → Fig. 2.11 (score use of trackers);
  - Fig. 2.8 → Fig. 2.12 (outcomes counted by the MOT metrics).
- All references to them in the text are generated by cross-references and were updated automatically.
- No figure of Chapters 1, 3, 4 or 5 changed number.

### Captions and text
- Each caption describes only what the original image shows. Where v4 had a caption for the image, the v4 caption was used as the title.
- All ten images are conceptual illustrations, and no caption presents them as experimental results.
- Section 2.3.4 now refers to Fig. 1.1 for the tracking-by-detection pipeline. This avoids adding image11 as a second figure of the same pipeline.

## 3. Images not used, and why

| File | Reason |
|---|---|
| image8.png | The headings do not match the pictures and descriptions below them. For example, the column headed "Partial Occlusion" shows the description "Varying lighting conditions", and the column headed "Illumination Changes" shows a cup and the description "Fast movement causes blur". An accurate caption is therefore not possible without changing the image. Its topics are already covered by the text of 2.2.3 and 2.3.7. |
| image11.png | It duplicates Fig. 1.1, which already shows the tracking-by-detection pipeline with the input and output of each block. Section 2.3.4 refers to Fig. 1.1 instead. |
| image13.png | It is a generic "deep learning model → tracking output" diagram. The thesis has no separate "tracking by deep learning" paradigm: Section 2.3.4 describes three paradigms, and this image would not match any of them without being forced. |
| image14.png | It shows a single-object transformer tracker driven by a target template and a search region. Section 2.3.4 describes query-based multi-object transformer trackers (TransTrack, TrackFormer, MOTR and MOTIP). Placing it there would misrepresent those methods. |
| image15.png | It is a table stored as a picture. Four of its seven datasets (ImageNet VID, TAO, LaSOT and UAV123) are not cited in the thesis, so their figures would be unsupported. The datasets of the field are described in 2.3.7, and the datasets of the thesis are listed in Table 2.4. If this table is wanted, it should be set as a real table with verified references. |

## 4. Content of the original images, as found
Following the instruction not to alter the images, the following points were left exactly as they are in the originals. They are reported here so that the owner can decide whether to replace an image with a corrected original.

| File (figure) | What is visible in the original |
|---|---|
| image1 (Fig. 2.7) | the block "Traditional Approaches (Pre-2012) • HOG • SIFT" appears twice; the heading reads "Deep Learning Revolution)" with an unmatched parenthesis; the transformer heading reads "(2020·4)" |
| image2 (Fig. 2.1) | the arrow from "Camera 4" does not end at the server |
| image3 (Fig. 2.2) | the label "Perception" appears twice |
| image4 (Fig. 2.3) | "Global Trackies", "Unprexictable", "Robost", "due altitude/zoom" |
| image5 (Fig. 2.4) | "Camera 1 1", "Camera 2 3", "Object Detsction", "Feature Extraction Extraction", "Inecal Database", "Ineal Database", "Grobal Tracker" |
| image6 (Fig. 2.5) | "eCG", a garbled example list under "Ambient Sensors", "Cloud-based Central Central Server", "Global Datation)", "Electronic Health Reord (EHR Integration", "Anoamaly Detection" with a garbled example list, "Caregariver" (twice); two blocks named "Local Data Collection (&) Pre-processing" |
| image7 (Fig. 2.6) | "(e. gl. Pick, Pick-up,", "Recongiition", "Preditive", "Demand Forecasing", "Froud" |
| image9 (Fig. 2.8) | "reaissms", "reaissnss", "occusion", "baunding", "video ideo frames", "trajajetries", "especially, especially", "mijects", "densityof", "compix complex", "mdividual", "diffult", "Apperance" |
| image10 (Fig. 2.9) | "Trade-ofs", "GPUS", "Throufgut", "Embeded", "Metency", "Bandwath, Bandwath", "Ofline", "Connecivity", "reduces reduces", "complexiy" |
| image12 (Fig. 2.10) | single-letter labels "B", "S", "E", "G" and the block "+ G −" are not explained in the image; the "Association" block appears twice |

## 5. Source, ownership and permission
- **Origin.** All 15 images come from the owner's earlier draft `v4.docx` and were supplied by the owner. They do not appear in the published survey [5] (ICMISI 2026), whose camera-ready PDF contains no raster figures. No publisher copyright on that paper therefore covers them.
- **No invented attribution.** The repository does not document who created the images or with which tools. No attribution line was added, because inventing a source is not allowed. **Owner to confirm** that the images are their own work, or name the source.
- **Unresolved: photographs in image2 (Fig. 2.1).** The image contains photographs of real pedestrians. Their source is not documented: they may come from a public person re-identification dataset. **Owner to confirm** the source and the permission to reproduce these photographs. If the source is a dataset, add its citation to the caption.

## 6. Size on the page and readability
- Each image was scaled proportionally to fit the text width, and the aspect ratio of every placed image matches its file to four decimals.
- No image was enlarged beyond the text width, and none is upscaled by resampling: the pixels are the original ones.
- Effective print resolution in the Word PDF is between 103 and 161 pixels per inch:

| Image | Effective resolution (ppi) |
|---|---|
| image5 | 103 |
| image6 | 112 |
| image9 | 120 |
| image4 | 121 |
| image10 | 121 |
| image12 | 129 |
| image2 | 131 |
| image7 | 135 |
| image1 | 154 |
| image3 | 161 |

- The smallest labels in image5, image6 and image7 are legible but small in print. This limit comes from the resolution of the original files and cannot be improved without a higher-resolution original.
- Placing the images on a landscape page would not help, because the images are already at or near full text width at their native resolution.
