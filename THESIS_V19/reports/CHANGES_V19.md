# Changes from Thesis V18 to Thesis V19

Thesis V19 uses the original images of `v4.docx` (archive `v4_all_images.zip`) in place of the redrawn diagrams of V18, and adds four more original images where they illustrate existing text. The images are embedded unchanged.

- Previous version: `THESIS_V18` (Word PDF 122 pages); left unchanged.
- New version: `THESIS_V19` (Word PDF 126 pages, LaTeX PDF 122 pages).
- Details:
  - `IMAGE_MAPPING_REPORT_V19.md`: inventory, mapping, unused images, source and permission;
  - `VISUAL_VERIFICATION_REPORT_V19.md`: checks;
  - `V19_ORIGINAL_IMAGE_RECORD.csv`: hashes.

## Figures
| Figure | Original file | Section | Page | Change |
|---|---|---|---|---|
| 2.1 | image2.png | 2.2.1 | 15 | replaces the redrawn diagram of V18 |
| 2.2 | image3.png | 2.2.2 | 16 | replaces the redrawn diagram of V18 |
| 2.3 | image4.png | 2.2.3 | 18 | replaces the redrawn diagram of V18 |
| 2.4 | image5.png | 2.2.4 | 19 | replaces the redrawn diagram of V18 |
| 2.5 | image6.png | 2.2.5 | 20 | replaces the redrawn diagram of V18 |
| 2.6 | image7.png | 2.2.6 | 21 | replaces the redrawn diagram of V18 |
| 2.7 | image1.png | 2.3.1 | 23 | new |
| 2.8 | image9.png | 2.3.3 | 26 | new |
| 2.9 | image10.png | 2.3.3 | 27 | new |
| 2.10 | image12.png | 2.3.4 | 28 | new |
| 2.11, 2.12 | — | 2.3.6, 2.3.8 | 31, 35 | former Figs. 2.7 and 2.8, renumbered only |

Images 8, 11, 13, 14 and 15 were not used; the reasons are given in `IMAGE_MAPPING_REPORT_V19.md`, Section 3.

## Text
- Section 2.2:
  - The opening paragraph no longer describes block colors, which belonged to the redrawn diagrams.
  - The sentences that introduce Figs. 2.1–2.4 now describe the content of the original images.
- Section 2.3:
  - One sentence introduces each of Figs. 2.7–2.10.
  - Section 2.3.4 refers to Fig. 1.1 for the tracking-by-detection pipeline.
- Captions describe the original images. No other text changed.

## Build
- `word/make_images.py`: PNG figures are copied byte for byte into the Word file instead of being re-rendered.
- `word/build_all.sh`:
  - the final PDF is exported with lossless image compression and without downsampling, so the PDF shows the original pixels;
  - the six redrawn diagrams are no longer compiled.
- The original images are stored in `figures/v4_original/`.

## Unchanged
- All tables and all experimental values.
- Equations, references and the order of the bibliography.
- Chapters 1, 3, 4 and 5.
- The experimental figures, including Figs. 3.5–3.7, 4.4 and 4.5.
- The front matter and the Arabic pages.

## Open items for the owner
1. Confirm the source of the pedestrian photographs in Fig. 2.1 (image2) and the permission to reproduce them. If they come from a dataset, add its citation to the caption.
2. The original images contain spelling errors and a few drawing errors, listed in `IMAGE_MAPPING_REPORT_V19.md`, Section 4. They were not corrected, because the images had to stay unchanged. If corrected originals exist, they can replace the files in `figures/v4_original/` under the same names.
3. The Word template of the thesis uses US Letter pages (21.6 × 27.9 cm), not A4. This was inherited from the faculty template used since V3 and was not changed. If A4 printing is required, the page size of the template should be confirmed.
