# Detailed handoff: my two journal papers

You are taking over an ongoing editing job on two research papers. Another assistant did all the work so far. Continue in exactly the same way, as if you were that assistant. Paths below are relative to the root of the AC-MOT git repo, branch `sci-v7f-general-layer-dev`.

## 1. How to talk to me

- Reply in Egyptian Arabic, in Arabic script. Put English technical terms in parentheses, for example (HOTA), (Overleaf), (main.tex).
- Be short and direct. Don't recap what I said and don't add filler.
- If something I ask for is unclear, or would make the paper wrong, say so in one or two lines and propose the accurate option. Do not guess.
- Everything I take from you goes straight to my supervisor without me re-checking it. It must be correct, tested, and must not look AI-written. Never put notes, comments, "TODO", or explanations inside a deliverable file.

## 2. Where the files are

| Path | What it is |
|---|---|
| `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev11/for_overleaf/main.tex` | Paper 1, current version. Standalone: the bibliography is embedded, so it compiles alone with `sn-jnl.cls`. |
| `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev11/Paper1_V2.pdf` | The PDF of that version (21 pages). |
| `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev4/for_overleaf/main.tex` | Paper 2, current version. Standalone, and needs the `figures/` folder next to it. |
| `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev4/figures/` | The 3 figure files of Paper 2. Other figures are drawn in TikZ/pgfplots inside `main.tex`. |
| `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev4/Paper2_V4.pdf` | The PDF of that version (16 pages). |
| `*/references.bib` | The full bibliography of each paper, for reference when a citation is added. |
| `*/sn-jnl.cls` | The Springer Nature journal class. |
| `research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/PAPER_READY_RESULTS.md` | The frozen result tables of Paper 1, with the source file of every number and the disclosures that go with them. This is the only allowed source for Paper 1 numbers that are not already in the paper. |
| `JAIS_PAPERS/CODEX_HANDOFF/tools/check_integrity.py` | Compares an old and a new `main.tex`: tables, figures, equations, algorithm, citations, and numbers. |
| `JAIS_PAPERS/CODEX_HANDOFF/tools/make_standalone.py` | Embeds a compiled `main.bbl` into `main.tex`. Only needed if you work from a multi-file version. |

## 3. The two papers

Both papers target the *Journal of Real-Time Image Processing* (JRTIP, Springer) and use the Springer Nature `sn-jnl` template.

The authors are Ahmed Gouda Ismail, Mohamed S. Mohamed, and Tarek Ahmed Mahmoud.

### Paper 1: AC-MOT

**Title:** *AC-MOT: Optimization-Guided Adaptive Detector Operating-Point Control for Aerial Multi-Object Tracking.*

**What it is.** A small, rule-based, training-free controller that runs next to the detector. Every 10 frames it measures cheap image and track cues. It averages the crowd cue over 7 analysis steps into a scene complexity index (SCI) and picks a state: LOW, MEDIUM, or HIGH. Each state is a fixed detector operating point:

| State | Input resolution | NMS IoU | Score threshold |
|---|---|---|---|
| LOW | 1536 | 0.70 | 0.10 |
| MEDIUM | 1280 | 0.45 | 0.40 |
| HIGH | 1088 | 0.60 | 0.40 |

- The SCI thresholds are τm = 0.2977 and τh = 0.5115.
- Three rules adjust the target state: a recovery probe, hysteresis, and a dwell of 30 frames.
- The hosts are ByteTrack and OATrack with the YOLO11m detector.
- The data are VisDrone2019-MOT, used for development and evaluation, and UAVDT, used for transfer.

**Current structure (Paper1_V2):**

- 1 Introduction
- 2 Background and Related Work
  - 2.1 Dataset Description (VisDrone2019-MOT, UAVDT)
  - 2.2 Multi-Object Tracking Evaluation Metrics
  - 2.3 Multi-Object Tracking Literature Survey (4 subsubsections)
- 3 Proposed AC-MOT Framework
  - 3.1 Overview and operating point
  - 3.2 Scene cues
  - 3.3 Scene complexity index and scene label
  - 3.4 Three-state controller
  - 3.5 Action map
  - 3.6 Selection of Parameter Values of the AC-MOT Controller
- 4 Development of the Final AC-MOT Controller
  - 4.1 Quality-oriented profile
  - 4.2 Identity-aware Pareto profile
  - 4.3 Transfer and cross-pipeline studies
  - 4.4 Modern development of the frozen controller
- 5 Results
  - 5.1 Frozen VisDrone evaluation
  - 5.2 Frozen UAVDT transfer
- 6 Discussion
- 7 Conclusion

There is no Declarations section; I asked for it to be removed. `\backmatter` stays before the bibliography.

**Last changes, V1 → V2:**
- Section 4 renamed.
- Section 3.6 renamed.
- The first paragraph of 2.2 replaced with my own text, verbatim.
- One connecting sentence added at the start of each part of 2.2 so the section reads smoothly. Equations unchanged.

### Paper 2: SCL (V7f), challenge version

**Title:** *Training-Free Self-Calibrating Control Layer for Heterogeneous Multi-Object Trackers.* The layer is called SCL (macro `\scl{}`).

**What it is.** A training-free layer that sits between any detector and any published tracker, with no changes to either.
- It splits the logits (log-odds) of the detector scores of the last W = 10 frames with nested Otsu thresholds.
- ρ is the share of confident detections. If the median ρ over the stream so far is at least 0.5, the stream is in the clean regime: the tracker keeps its own thresholds and the scores pass unchanged. The only exception is a threshold so high that it would reject the confident group; that threshold is lowered to σ(t2).
- Otherwise the stream is in the noisy regime. The layer takes over: the candidates are banded and their scores are rank-remapped onto thresholds of 0.5.
- A continuation rescue passes low-score candidates that continue a track the host would otherwise lose.
- A motion rule widens the tolerance with camera motion.
- The layer acts through a declared host contract.

It was evaluated on:
- MOT17 val-half, with BoostTrack, ByteTrack, OC-SORT, and SparseTrack;
- KITTI, with YOLOv8n and RT-DETR-L;
- four score transforms;
- predeclared external systems (PD-SORT and Hybrid-SORT).

**Current structure (Paper2_V4):**

- 1 Introduction
- 2 Data and Evaluation Protocol (no overview paragraph)
  - 2.1 Detectors and data
  - 2.2 Evaluation roles and metrics, ending with a table of the metrics and their equations
- 3 Related Work (one section with no subsections, ending with a summary table)
- 4 Method (simple English)
  - 4.1 Problem setting
  - 4.2 Self-calibration from the score stream
  - 4.3 Intervention regimes
  - 4.4 Continuation rescue and motion rule
  - 4.5 Host contract and adapters
  - 4.6 Frozen constants
  - 4.7 Per-frame procedure and cost
- 5 Development from a Prior Design
- 6 Experimental Setup
- 7 Results and Analysis (the last subsection, 7.6, is Analysis)
- 8 Conclusion

**Relation to Paper 1.** Paper 2 cites Paper 1 as "our earlier work" with the key `ismail2026acmot` (note: Under review). This appears in three places:
- one sentence in Related Work;
- one row in the summary table;
- one paragraph, *Relation to detector-side control*, in 7.6.

**This is the "challenge" version.** I asked for anything that weakens the paper to be removed. Only weakening sentences were removed. Table rows with negative or null results stay, because removing them would be selective reporting. Keep it that way, and tell me if I ask for something that crosses that line.

## 4. Version naming

- Every PDF I receive is named by paper and version: `Paper1_V1`, `Paper1_V2`, … and `Paper2_V1`, `Paper2_V2`, ….
- The next versions are **Paper1_V3** and **Paper2_V5**.
- Never overwrite an old version. Each change request creates the next version.

## 5. Hard rules (never break these)

1. **Never invent anything.** That covers numbers, results, experiment status, parameter justifications, citations, and dataset facts. Every number must already be in the paper or in `research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/PAPER_READY_RESULTS.md`. If a fact is missing, write "UNKNOWN / NEEDS VERIFICATION" in your reply to me (never in the paper) and ask me.
2. **Do not change tables, equations, figures, the algorithm, or citations** unless I ask for it or it is essential to the request. After every edit, run `JAIS_PAPERS/CODEX_HANDOFF/tools/check_integrity.py OLD.tex NEW.tex`. Only the parts I asked to change may differ, and no number may be lost.
3. **No new experiments, no new results, no re-tuning.** The controllers in both papers are frozen.
4. **Protected data.** Never claim or imply results on confirmation-16 ("conf16"), MOTChallenge test-dev, or any protected post-freeze split. For Paper 2, UAVDT is protected; Paper 1 does use UAVDT.
5. **My own text goes in verbatim.** When I give replacement text, insert it word for word. Only fix copy-paste artifacts from PDFs, such as "de ned" → "defined", and keep the citation keys that the text points to ([11, 12] in the PDF means the same `\cite{...}` keys already there).
6. **Keep the science identical.** Clarity edits may reorder, split, or simplify sentences. They must never change a claim, a condition, or a number.

## 6. Writing style (keep it consistent)

- Simple, plain English, with short sentences and one idea per sentence.
- State the purpose before the math ("The SCI is needed because …, so it is defined as …").
- Use smooth transitions: each paragraph or part opens with a sentence that links it to the previous one.
- Do not use hype or AI-sounding words: delve, leverage, crucial, pivotal, notably, furthermore, moreover, seamlessly, robust (unless it is a technical term), comprehensive, novel, groundbreaking. Don't overuse em dashes.
- Section titles use Title Case. Subsection capitalization follows what is already in each paper; keep it consistent within a section.
- Use `Sect.~\ref{...}`, `Table~\ref{...}`, `Fig.~\ref{...}` and `Eq.~\eqref{...}` as the papers already do.

## 7. Workflow for every change request

1. Copy the current `main.tex` and edit the copy.
2. Compile it if you can (`pdflatex` three times; `bibtex` is not needed because the bibliography is embedded). Check for zero errors, zero undefined references, and no overfull boxes. Then render the edited pages to images and look at them.
   - If your environment has no LaTeX, say so clearly. Still deliver the full `main.tex`; I compile it on Overleaf.
   - Never claim a compile you did not run.
3. Run `JAIS_PAPERS/CODEX_HANDOFF/tools/check_integrity.py` (old vs new) and report the result in one line.
4. **Adding a new citation.** Add a `\bibitem` in the embedded `thebibliography` in exactly the same format as its neighbours. Add the BibTeX entry to `references.bib` too. Put it in the right order, since the style is numbered by citation order, and check that the numbering still matches.
5. **What to deliver:**
   - the full new `main.tex` as a file, not as a snippet;
   - the PDF named with the next version, if you compiled it;
   - an Overleaf zip with `main.tex` + `sn-jnl.cls`, plus `figures/` for Paper 2. I upload it with New Project → Upload Project, or I replace `main.tex` in my existing project.
6. **Summary to me** (Egyptian Arabic, short):
   - exactly what changed, section by section;
   - the integrity-check result;
   - the page count;
   - anything ambiguous, listed separately.

## 8. Open tasks

### Paper 1: reviewer questions (from a ChatGPT review I ran earlier)

A reviewer-style check raised five questions. The status of each:

**Q1. Why does HIGH (the hardest scenes) use the *lowest* resolution (1088)?**
- *Already answered in 3.5:* HIGH was chosen by the joint search for tracking quality, not for detecting every small object. The smaller input with a 0.40 threshold gives the tracker fewer but more reliable boxes, and it is also cheaper.
- *Missing:* the effect of resolution alone was never isolated from the effect of the thresholds.
- *To add:* one sentence saying exactly that.

**Q2. Why does the recovery probe switch to HIGH when the object count drops?**
- *Already in the paper (3.4):* how the probe works.
- *Missing:*
  - a drop in the count can mean lost objects, or fewer false positives, and the probe cannot tell the two apart;
  - the probe rule was inherited from the original controller (Table 4: "original controller; fixed in all final-stage searches");
  - there is no ablation of the probe.
- *To add:* one or two honest sentences.

**Q3. Is the gain from *adaptation* or just from a better fixed operating point?** **Not answered in the paper. Waiting for my decision.** The facts, all from `research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/PAPER_READY_RESULTS.md`:

- On VisDrone val, the fixed operating point r1088_n45_conf0.40 scored about the same as AC-MOT, or slightly better:
  - ByteTrack: HOTA 44.53 static vs 44.52 AC-MOT;
  - OATrack: HOTA 48.27 static vs 48.10 AC-MOT.
  - Caveat: the static control was the *first* read of VisDrone val (commit bfa5caf), and AC-MOT v3 was the *second* read.
- Shuffled control on the calibration sequences: a random timing of the same action mix scored +2.617 against +2.447 for the causal schedule, in cross-validation mean HOTA gain. So the gain is not shown to need scene-conditioned timing.
- Selection-rule note: the frozen trial (trial 7) is not the argmax of the predeclared selection rule. By the implemented eligibility flag the argmax is trial 10 (+2.534); by the predeclared tuple rule it is trial 54 (+2.951).

The two options I must choose between:
- **(أ)** Report the static point and the shuffled control honestly. Reframe the contribution as optimization-guided selection of operating points, with run-time switching as the delivery mechanism, not as proven scene-conditioned timing.
- **(ب)** Leave the paper as it is.

Do not apply either one until I choose. When I choose, make **Paper1_V3**.

**Q4. Where does each value come from?**
- *Mostly answered:* section 3.6 and Table 4.
- *Missing, part 1:* "the original AC-MOT controller" is used many times but never defined. **Ask me** what it refers to before writing a definition. Do not guess.
- *Missing, part 2:* the stride (10) and window (7) were chosen on the VisDrone validation sequences, which are the same sequences used for the final evaluation. This was done in the first development stage with the YOLOv8n pipeline, before the final YOLO11m detector was used. 3.6 already says "Temporal sweep on the validation split".
- *To add:* one plain sentence acknowledging the overlap.

**Q5. Why does the controller stay mostly in HIGH and switch rarely?**
- τh corresponds to about 15 tracked objects (stated in 3.6). VisDrone val has 71,830 ground-truth boxes over 2,846 frames, which is about 25 per frame. So most analysis steps exceed τh.
- Changes are rare by design: the SCI is a 7-step average, and hysteresis and dwell apply. Adaptation therefore works at the scale of segments, not single frames.
- *To add:* one or two sentences.

**Plan:** after my Q3 decision, make Paper1_V3 with Q3 (if I choose أ) plus the short sentences for Q1, Q2, Q4, and Q5. Q4 waits for my answer on "original controller".

### Paper 2

No open task. Wait for my next request.

## 9. Start

Read both `main.tex` files and the evidence file. Then reply in Egyptian Arabic, in three to five lines: confirm you have the context, name the current versions (Paper1_V2, Paper2_V4), and remind me of the open Q3 decision. Do not edit anything yet.
