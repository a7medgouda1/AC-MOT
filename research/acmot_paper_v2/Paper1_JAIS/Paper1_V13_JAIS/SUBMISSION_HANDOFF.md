# Paper 1 – JAIS Submission Handoff (V13)

## 0. Current status

| Item | Value |
|---|---|
| Status | **Submitted** to the Journal of Aerospace Information Systems |
| Manuscript ID | **2026-10-I012138** |
| Date submitted | 18-Oct-2026 |
| Manuscript type (portal) | Full Paper |
| Subject index categories | 03410 Uninhabited and Unmanned Air Vehicles; 12110 Artificial Intelligence Systems; 14200 Signal Processing |
| Review copy | 27 pages: 1 ScholarOne cover page + the 26-page V12 manuscript; no Acknowledgments section |
| Submitted file | Main Document from **V12** (`Paper1_V12_JAIS.pdf`), not V13 |
| Co-author confirmation | Pending: Dr. Mohamed S. Mohamed and Dr. Tarek Ahmed Mahmoud must confirm through the ScholarOne email |
| Declarations entered | Not shown in the review-copy PDF; check them in the Author Center (Submitted Manuscripts → View Submission → submission details) |

Sections 6–9 describe the draft state before submission and are kept for reference.

## 1. Location

| Item | Value |
|---|---|
| Repository | https://github.com/a7medgouda1/AC-MOT (old URL https://github.com/AhmedCode110/AC-MOT redirects here) |
| Branch | `sci-v7f-general-layer-dev` |
| Folder | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS/` |
| Final manuscript PDF | `Paper1_V13_JAIS.pdf` (26 pages) |
| LaTeX source archive | `Paper1_V13_JAIS_overleaf.zip` (standalone `main.tex` with embedded bibliography + `new-aiaa.cls` + `new-aiaa.bst`) |
| Journal | Journal of Aerospace Information Systems (JAIS), AIAA |
| Portal | https://mc.manuscriptcentral.com/aiaa |
| Article type | Full-Length Paper |

## 2. Folder contents

| File | Purpose |
|---|---|
| `main.tex` | Manuscript source (AIAA `new-aiaa` class, `journal` option) |
| `references.bib` | Bibliography database (34 entries cited) |
| `main.bbl` | BibTeX output used by `main.tex` |
| `new-aiaa.cls`, `new-aiaa.bst` | AIAA class and bibliography style |
| `for_overleaf/main.tex` | Single-file version with the bibliography embedded; compiles with only the `.cls` file |
| `Paper1_V13_JAIS.pdf` | Compiled manuscript to upload as Main Document |
| `Paper1_V13_JAIS_overleaf.zip` | Source archive (for the revision stage or if the portal requests source files) |

All three figures are drawn with TikZ/pgfplots inside `main.tex`; there are no external image files.

## 3. Compilation

Multi-file build (from this folder):

```
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Single-file build (from `for_overleaf/` with `new-aiaa.cls` beside it, or from the extracted zip):

```
pdflatex main.tex
pdflatex main.tex
```

Verified on 2026-10-18 (TeX Live, pdflatex):

- 26 pages, 0 errors, 0 overfull boxes, 0 undefined references or citations.
- The single-file build in a clean folder gives text identical to the multi-file build.
- Integrity check against V12: no numbers lost or added, no citations removed or added, all 3 figures (`tikzpicture`) identical.

On macOS, install MacTeX (full TeX Live distribution: `brew install --cask mactex`). Overleaf: upload the zip and compile with pdfLaTeX.

## 4. Changes from V12 to V13

1. Added an `Acknowledgments` section before the references:
   "AI-assisted tools were used for language editing and LaTeX formatting; the authors are responsible for all content."
2. Wording tightened in four sentences of the Discussion and Conclusion so the paper stays at 26 pages; no numbers or claims were changed:
   - "therefore depends … also showed" → "thus depends … showed"
   - "so it is suitable for real-time use" → "and suitable for real-time use"
   - "The SCI, which is based on" → "The SCI, based on"
   - "paired bootstrap analysis gave confidence intervals for these differences. On UAVDT, the same controller improved" → "paired bootstrap analysis supports these gains. On UAVDT, it improved"
   - Two Conclusion paragraphs merged into one.

Title, abstract, authors, tables, figures, equations, and references are unchanged from V12.

## 5. Manuscript metadata (source of truth: `Paper1_V13_JAIS.pdf`)

**Title**
Optimization-Guided Adaptive Detector Operating-Point Control for Multi-Object Aerial Tracking

**Abstract (184 words; identical to V12)**
Multi-object tracking in unmanned aerial vehicle video is difficult because object density, size, illumination, and blur change over time, while most tracking-by-detection systems run the detector with fixed settings. This paper proposes a training-free controller that adjusts the detector operating point online: the confidence threshold, the overlap threshold of non-maximum suppression, and the input resolution. Using only the current frame and past tracker output, it selects one of three operating points without modifying or retraining the detector or the tracker. On the VisDrone2019 dataset with ByteTrack, the controller raises, relative to a fixed operating point, the higher order tracking accuracy by 7.1%, the multiple object tracking accuracy by 182%, and the identity F1 score by 11.0%, and it reduces identity switches by 24.2%. With OATrack, the same three scores rise by 2.8%, 22.4%, and 4.0%, and identity switches fall by 21.9%. Paired bootstrap analysis supports these improvements. On a second aerial benchmark, the controller raises the multiple object tracking accuracy with both trackers without retuning, including a 16.7% gain with OATrack. It adds about 4.2 milliseconds per frame on a Tesla T4 graphics processor.

**Keywords** (the manuscript has none; used in the portal):
Multi-Object Tracking; Unmanned Aerial Vehicles; Object Detection; Adaptive Control; Computer Vision

**Authors (order as in the PDF)**

| # | Name | Position | Department | Institution | Email |
|---|---|---|---|---|---|
| 1 | Ahmed Gouda Ismail (corresponding, submitting) | M.Sc. Student | Computer Engineering and Artificial Intelligence | Military Technical College, Cairo, Egypt | a7medgouda1@gmail.com |
| 2 | Mohamed S. Mohamed | Associate Professor | Computer Engineering and Artificial Intelligence | Military Technical College, Cairo, Egypt | mohamedms@mtc.edu.eg |
| 3 | Tarek Ahmed Mahmoud | Professor | Computer Engineering | Egypt University of Informatics, Cairo, Egypt | tarek.mohamed@eui.edu.eg |

**Counts**

| Item | Value |
|---|---|
| Pages | 26 |
| Figures | 3 (all in color) |
| Tables | 11 |
| Words (PDF text, including references) | 10,857 |
| Words for the portal field (portal rule: each figure counts as 200 words) | 10,857 + 3 × 200 = 11,457 |

## 6. ScholarOne status (as reported by the browser session on 2026-10-18)

Nothing has been submitted.

| Step | Status |
|---|---|
| 1. Type, Title, Abstract | Saved (draft) |
| 2. File Upload | Main Document uploaded from **V12**; must be replaced with `Paper1_V13_JAIS.pdf`. LaTeX zip not uploaded (source files are required only at revision). |
| 3. Attributes / Keywords | Saved |
| 4. Authors & Institutions | Saved; 3 authors in the order above; institutions typed manually, not linked to the Ringgold list |
| 5. Reviewers & Editors | **Pending** – portal requires at least 3 recommended reviewers and 1 recommended associate editor |
| 6. Details & Comments | **Pending** – declarations not answered |
| 7. Review & Submit | Not reached; PDF proof not generated yet |

Other items in the account:

- An older unsubmitted JAIS draft dated 01-Oct titled "Calibration Versus Scene Switching…" exists. It is an earlier version of this paper line and was never submitted. Delete it before submitting, to avoid a duplicate.
- Profile address shows ZIP "12345" (placeholder) and should be corrected by the author.
- The Step 4 label shows "Dr. Ahmed Ismail"; the corresponding author is an M.Sc. student, so the salutation should be removed.

## 7. Reviewer and Associate Editor selections

**Status: not entered in the portal. Final choice is the authors'.**

Proposed reviewers (authors of JAIS papers cited in the manuscript, outside the authors' institutions). Emails must be taken from each person's paper or institutional page:

| Candidate | Institution | Cited work |
|---|---|---|
| Hyo-Sang Shin | Cranfield University | AFJPDA (JAIS, 2024) |
| Jonathan Rogers | Georgia Institute of Technology | Multirotor ground-target tracking (JAIS, 2015) |
| Dah-Jye Lee | Brigham Young University | UAV ground moving-object tracking (JAIS, 2017) |
| Moongu Jeon | Gwangju Institute of Science and Technology | Adaptive confidence threshold for ByteTrack (ICCAIS, 2023) |

Do not propose the authors of TOReN (Fathy, Elhadad, Elshafey): possible same-institution conflict of interest.

Proposed associate editor: Mykel J. Kochenderfer (Stanford University). Alternative: Peng Wei (The George Washington University). Other options shown by the portal: Ella Atkins (Virginia Tech), Max Z. Li (MIT).

## 8. Declarations

| Question | Status / proposed answer |
|---|---|
| Funding | **Pending – author to confirm** (No, unless a grant exists) |
| Not published / not under consideration elsewhere | **Pending – author to confirm** that the Springer-format version of this paper is not under review anywhere |
| Previous AIAA submission of this or similar work | No (the 01-Oct draft was never submitted) |
| AI generated significant content | **Pending – author decision**; answer truthfully |
| AI used to improve language | Yes; the required description is now in the V13 Acknowledgments section |
| Work is unclassified / cleared for public release | **Pending – confirm with Military Technical College** before ticking |
| Original work, no rights infringed | Author to tick |
| Read and complied with AIAA ethical standards | Author to read and tick |
| All co-authors approve | Dr. Mohamed S. Mohamed approved; **Dr. Tarek Ahmed Mahmoud to confirm** |
| Open Access | No choice at submission; opt-in is offered after acceptance (AIAA lists an APC of USD 2,700) |
| Conflict of interest | None, unless the authors state otherwise |

Portal AI-use text (matches the Acknowledgments):
"AI-assisted tools were used for language editing and LaTeX formatting. All technical content, experiments, and results are the authors' own, and the authors reviewed the manuscript and take full responsibility for it."

## 9. Cover letter

```
Dear Editor,

We submit the manuscript "Optimization-Guided Adaptive Detector Operating-Point Control for Multi-Object Aerial Tracking" for consideration as a Full-Length Paper in the Journal of Aerospace Information Systems.

The manuscript presents a training-free controller that adjusts the detector operating point of a tracking-by-detection system online, using only the current frame and past tracker output, without retraining the detector or the tracker. It is evaluated on VisDrone2019 with ByteTrack and OATrack and on a second aerial benchmark without retuning, and it adds about 4.2 milliseconds per frame on a Tesla T4 graphics processor. The work addresses onboard perception for unmanned aerial systems, which falls within the scope of the journal.

The manuscript is original, has not been published, and is not under consideration elsewhere. All authors have approved the submission and declare no conflict of interest.

Sincerely,
Ahmed Gouda Ismail (corresponding author)
Military Technical College, Cairo, Egypt
a7medgouda1@gmail.com
```

The last paragraph is valid only after the "not under consideration elsewhere", conflict-of-interest, and co-author approval items in Section 8 are confirmed.

## 10. Remaining tasks for Codex

1. Track manuscript 2026-10-I012138 in the ScholarOne Author Center; do not resubmit.
2. Confirm that both co-authors have completed the ScholarOne contribution confirmation.
3. Record the declarations as entered, from the submission proof, in Section 8.
4. If the AI-language question was answered Yes: V12 has no Acknowledgments section, while V13 has the required AI-use statement. Use V13 at the first revision, or send it to the editorial office through the Author Center if they request it.
5. At revision: start a new version folder from V13, address the reviewer comments, keep 20–26 pages, and upload the LaTeX source (`Paper1_V13_JAIS_overleaf.zip` or its successor).
6. Delete the older 01-Oct unsubmitted draft from the ScholarOne account, if it still exists.

Do not modify frozen tags, locks, or protected evaluation data in this repository.
