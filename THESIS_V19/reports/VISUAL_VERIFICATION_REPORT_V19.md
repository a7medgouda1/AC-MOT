# Visual Verification Report — Thesis V19

- **Files checked:**
  - `word/Thesis_V19.pdf` (126 pages, from the Word file);
  - `word/Thesis_V19.docx`;
  - `Thesis_V19_LaTeX.pdf` (122 pages, compiled directly from the LaTeX source).
- **Reference version:** Thesis V18.
- **Page numbers:** the printed page numbers of the Word PDF.

## 1. The inserted images are the original files

| Check | Method | Result |
|---|---|---|
| Archive files are the v4 originals | SHA-256 of `image1.png`–`image15.png` against `word/media/` of `v4.docx` | 15 of 15 identical |
| Thesis copies are unchanged | SHA-256 of `figures/v4_original/*.png` against the archive | 15 of 15 identical |
| Word file embeds the original files | SHA-256 of every file in `word/media/` of `Thesis_V19.docx` | 10 of 10 used images byte-identical to the archive (record in `V19_ORIGINAL_IMAGE_RECORD.csv`) |
| Word PDF shows the original pixels | every embedded image decoded and compared pixel by pixel with its archive file | 10 of 10 pixel-identical |
| LaTeX PDF shows the original pixels | same comparison | 10 of 10 pixel-identical |
| No redrawn figure remains | V18 media hashes against V19 media hashes | the six redrawn diagrams of V18 are absent; all other V18 images are present and unchanged |

How the Word PDF keeps the original pixels:
- **The problem.** The default PDF export of the word processor stores pictures as JPEG and changes their pixels. In a test with image5, the largest error was 38 of 255 grey levels.
- **The fix.** The V19 build exports the PDF with lossless image compression and without downsampling (`word/build_all.sh`, step 4).
- **The effect.** All pictures of the thesis, including the earlier figures and the logo, are now stored without loss. The Word PDF is therefore larger: 22 MB, against 7 MB for V18.

## 2. Placement of every inserted figure (Word PDF)

| Figure | File | Page | Size on page | Aspect ratio, file / page | Within margins | Introduced in the text before it |
|---|---|---|---|---|---|---|
| 2.1 | image2.png | 15 | 13.6 × 7.3 cm | 1.8670 / 1.8668 | yes | yes, p. 14 |
| 2.2 | image3.png | 16 | 12.8 × 8.5 cm | 1.5000 / 1.5000 | yes | yes, p. 15 |
| 2.3 | image4.png | 18 | 11.2 × 14.8 cm | 0.7546 / 0.7546 | yes | yes, p. 17 |
| 2.4 | image5.png | 19 | 15.2 × 14.3 cm | 1.0600 / 1.0600 | yes | yes, p. 18 |
| 2.5 | image6.png | 20 | 15.2 × 14.1 cm | 1.0803 / 1.0802 | yes | yes, p. 20 |
| 2.6 | image7.png | 21 | 14.4 × 12.8 cm | 1.1261 / 1.1261 | yes | yes, p. 21 |
| 2.7 | image1.png | 23 | 12.0 × 8.0 cm | 1.4979 / 1.4978 | yes | yes, p. 22 |
| 2.8 | image9.png | 26 | 15.2 × 10.3 cm | 1.4804 / 1.4803 | yes | yes, p. 26 |
| 2.9 | image10.png | 27 | 15.7 × 9.2 cm | 1.6993 / 1.6993 | yes | yes, p. 26 |
| 2.10 | image12.png | 28 | 11.2 × 11.2 cm | 1.0000 / 1.0000 | yes | yes, p. 27 |

Visual inspection of the rendered pages 13–31:
- every image is complete, with no cropping;
- no image overlaps text;
- every caption is below its image and readable;
- no page is left mostly empty.

During the check:
- **Fig. 2.6 page break:** the first build left most of page 21 empty, because Fig. 2.6 did not fit after the text. Its width was reduced proportionally from 98% to 90% of the text width, and the figure now follows the text on the same page.
- **Long captions:** the captions of Figs. 2.7–2.9 were split into a short title and a description, so that the List of Figures shows short titles.

## 3. Numbering, contents and lists

| Check | Result |
|---|---|
| Chapter 2 figure numbers | 2.1–2.12, in order of appearance (2.11 and 2.12 are the former 2.7 and 2.8) |
| Cross-references | all generated; no "??" and no "Error!" in the PDF; LaTeX build: 0 undefined references, 0 overfull boxes |
| Contents, List of Figures, List of Tables | 163 of 163 entries linked to their targets; every page number matches the page of its heading or caption (the checking script flags Table 2.3 only because its entry has no dot leader; the number, 30, is correct) |
| Figures, tables and algorithms after their first mention | 64 of 64 |
| Error marks (¿) in equations | 0 |

## 4. The scientific results are unchanged
| Check against V18 | Result |
|---|---|
| Source of Chapters 1, 3, 4 and 5 | byte-identical |
| `references.bib`, bibliography order, front matter and Arabic sources | identical |
| All 39 tables of the Word file (all experimental tables, including every HOTA, MOTA, IDF1, IDS, precision, recall, FP, FN and FPS value) | identical |
| Numbers in the PDF text | identical, except the new figure numbers 2.9–2.12 and one new "1.1" (the reference to Fig. 1.1 in Section 2.3.4) |
| Experimental figures (Figs. 1.3, 3.1–3.7 and 4.1–4.5, including Figs. 3.5, 3.6, 3.7, 4.4 and 4.5) | the embedded image files are byte-identical to V18; same numbers and captions (Fig. 3.5 p. 66, Fig. 3.6 p. 67, Fig. 3.7 p. 68, Fig. 4.4 p. 87, Fig. 4.5 p. 88) |
| Equations, experimental protocols and conclusions | unchanged (sources identical) |

No error was found in the scientific results, and none was changed.

## 5. First and last pages, Arabic content and names
| Check | Result |
|---|---|
| Cover, inner title page, abstract and acknowledgments (PDF pages 1–4) | text identical to V18; page 1 differs only in the quality of the logo, which is now stored without loss |
| Last two pages (Arabic title page and Arabic summary) | pixel-identical to V18 |
| Publications page | identical except its page number (111) |
| Supervisors | "Mohamed Sobhy Mohamed" and "Tarek" on the English title pages (PDF pages 1, 2 and 4); "محمد صبحي محمد" and "طارق" on the Arabic title page (PDF page 126) |
