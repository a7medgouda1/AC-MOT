# Task: submit a research paper to the journal "The Visual Computer" (Springer)

You control my computer and my web browser. Submit the manuscript below to the Springer journal
**The Visual Computer** (journal number 371) as a new **Original Article**. Work step by step, take
a screenshot after each page, and follow the rules at the end.

## 1. Files (already on my computer)

Look for them in my Downloads folder first; if they are not there, ask me where they are.

| File | What it is |
|---|---|
| `Paper2_V71_anonymous.pdf` | manuscript without author names (use when the system asks for an anonymous / blinded manuscript) |
| `Paper2_V71_anonymous_overleaf.zip` | LaTeX source of the anonymous manuscript |
| `Paper2_V71_title_page.pdf` | separate title page with names, affiliations, e-mails, contributions |
| `Paper2_V71.pdf` | manuscript with author names (use only if the system does NOT ask for blinding) |
| `Paper2_V71_overleaf.zip` | LaTeX source of the named manuscript |
| `cover_letter_TheVisualComputer.md` | cover letter text (copy its text into the cover-letter box, or save it as PDF if a file is required) |

Do not edit, rename or regenerate any file.

## 2. Where to submit

1. Open https://link.springer.com/journal/371 and click **Submit manuscript** (or "Submit your
   manuscript"). If several journals or systems are offered, choose only **The Visual Computer**.
2. Log in with my Springer / Editorial Manager account. I will type the password myself: when a
   login, password, two-factor code or CAPTCHA appears, stop and ask me to do it.
3. If no account exists, ask me before creating one.

## 3. Data to enter

- **Article type:** Original Article (or "Research Article" / "Regular Paper" if that is the name).
- **Title:** Training-Free Self-Calibrating Control Layer for Heterogeneous Multi-Object Trackers
- **Running title (if asked):** Self-Calibrating Control Layer for Multi-Object Trackers
- **Abstract:**

  Multi-object trackers rely on score thresholds tuned for one detector. When the detector is replaced, retrained, or compressed, its scores shift, and the tuned thresholds silently stop fitting. This paper proposes a training-free self-calibrating control layer (SCL) between an unchanged detector and tracker. SCL splits the logits of recent scores twice with Otsu's method and classifies the stream as clean or noisy, without labels or future frames. Its novelty is selective, host-aware adaptation. On clean streams it keeps the tracker's scores and lowers a threshold only if it would reject the confident detections; on noisy streams it selects and rescores the detections and sets the thresholds. It acts through four published tracker settings and passes on weak detections that continue tracks, so one frozen configuration serves single-stage and two-stage trackers. It was evaluated on seven trackers, four detection sources, and three datasets; changes are relative to the tracker alone. When detector scores were halved, two trackers fell to zero higher order tracking accuracy (HOTA); with SCL both recovered at least 97% of it. With a replacement detector, RT-DETR-L, SCL raised the multiple object tracking accuracy (MOTA) of ByteTrack and BoT-SORT by 12.6% and 16.3% and cut their identity switches by 43% and 47%, respectively. It also raised the HOTA of PD-SORT, unseen during design, by 0.9%, and kept four well-matched trackers within 0.1%. SCL adds on average no more than 2.95 ms per frame on an ordinary processor, so a detector can be replaced or retrained without retuning the tracker.

- **Keywords:** multi-object tracking; tracking by detection; detector confidence calibration;
  online adaptation; Otsu thresholding; real-time image processing
- **Authors, in this order:**
  1. Ahmed Gouda Ismail (corresponding author), a7medgouda1@gmail.com,
     Computer Engineering and Artificial Intelligence Department, Military Technical College,
     Cairo, Egypt
  2. Tarek Ahmed Mahmoud, tarek.mohamed@eui.edu.eg,
     Computer Engineering Department, Egypt University of Informatics, Cairo, Egypt
  3. Mohamed S. Mohamed, mohamedms@mtc.edu.eg,
     Computer Engineering and Artificial Intelligence Department, Military Technical College,
     Cairo, Egypt
- **Declarations / questionnaire answers:**
  - Funding: none ("The authors did not receive support from any organization for the submitted work.")
  - Competing interests: none.
  - Ethics approval / human or animal subjects: not applicable (public benchmark datasets only).
  - Consent for publication: not applicable.
  - Data availability: public datasets MOT17, KITTI tracking and UAVDT; generated results
    available from the corresponding author on reasonable request.
  - Code availability: available from the corresponding author on reasonable request.
  - Previously published / under review elsewhere: No. (A different, related manuscript by the
    same authors on the AC-MOT controller is under review at the Journal of Aerospace Information
    Systems, ID 2026-10-I012138; this is stated in the cover letter.)
  - Preprint posted: No, unless I tell you otherwise.
- **Cover letter:** paste the full text of `cover_letter_TheVisualComputer.md`.

## 4. Which files to upload

- If the system says the review is **double-blind / anonymous** or asks for a "Title page" and a
  "Blinded manuscript": upload `Paper2_V71_title_page.pdf` as **Title Page**,
  `Paper2_V71_anonymous.pdf` as **Manuscript**, and, if LaTeX source is requested,
  `Paper2_V71_anonymous_overleaf.zip` as **LaTeX source / Supplementary source files**.
- Otherwise (single-blind): upload `Paper2_V71.pdf` as **Manuscript** and, if LaTeX source is
  requested, `Paper2_V71_overleaf.zip`.
- Figures are inside the PDF and the zip. If the system insists on separate figure files, stop and
  ask me.
- After uploading, open the PDF that the system builds and check that it has 16 pages, the right
  title, and (for the anonymous route) no author names.

## 5. Rules

- **Never pay anything** and never choose Open Access or any paid option. If a fee or an Open Access
  choice appears, choose the free / subscription option; if unclear, stop and ask me.
- Never invent data. If a required field is not covered above (for example ORCID, phone number,
  suggested or opposed reviewers, author biographies, classification codes, funder IDs,
  copyright or licence agreements), **stop and ask me**.
- Do not change the files or the text given above.
- **Before the final "Submit" / "Approve submission" / "Build PDF for approval → Approve" click,
  stop, show me a summary (journal, article type, title, authors, files uploaded, and the generated
  PDF), and wait for my explicit "yes, submit".**
- After submitting, tell me the manuscript number and copy the confirmation message.

## 6. When you are stuck

If anything fails or is unclear, stop and write one message in this exact format so I can forward
it to my other assistant:

```
SUBMISSION QUESTION
Step: <the page or step name>
What the page shows: <exact field names, options, error text>
What I tried: <short>
What I need: <the decision or information>
```
