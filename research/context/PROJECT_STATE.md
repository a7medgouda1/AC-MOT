# PROJECT STATE — read this first

<!-- AUTO:BEGIN (tools/update_project_context.py — do not edit by hand) -->
LAST VERIFIED COMMIT: 26ffdada7f96ba23b25b196eb7e8a3d00d9a2e3e
CURRENT BRANCH: sci-v7f-general-layer-dev (upstream origin/sci-v7f-general-layer-dev, ahead 0, behind 0)
LAST CONTEXT UPDATE: 2026-10-24 23:22 UTC
LATEST FROZEN TAG (git): universal-acmot-v7-freeze → 488df9a
WORKING TREE: 8 uncommitted path(s) — see GIT_STATE.md
<!-- AUTO:END -->

FINAL TARGET: V7 — the approved final version and contribution, frozen policy V7f (Amendment 10, owner decision 2026-10-20). V6-TF = frozen history; V4 = historical baseline / ablation ONLY, never a fallback.
CURRENT RESEARCH VERSION: V7 (frozen V7f, tag universal-acmot-v7-freeze → 488df9a; the policy behind Paper 2)
CURRENT PHASE: publication — V7f frozen (2026-09-28) and approved (Amendment 10); post-freeze external evaluations done (research/final/V7_*.md); Paper 1 under review at JAIS; Paper 2: Paper2_V19 (UAVDT E56, VisDrone E55, journal references) ready for the supervisor and The Visual Computer (D-036); declarations to be confirmed by the owner. Previous phase text (V6-TF freeze → post-freeze evaluations) is history.

## Papers (registry: PAPERS.md)
- Paper 0, survey: PUBLISHED, IEEE ICMISI 2026, DOI 10.1109/ICMISI69868.2026.11583994.
- Paper 1, AC-MOT operating-point controller: SUBMITTED to JAIS (AIAA),
  manuscript ID 2026-10-I012138, 18-Oct-2026, file = Paper1_V12_JAIS;
  co-author confirmations pending; Paper1_V13_JAIS ready for the revision.
- Paper 2, SCL = frozen V7f: NOT SUBMITTED; target JRTIP (Springer);
  latest Paper2_V11; internal reviewer audit found 9 text items to fix in
  Paper2_V12 (PAPERS.md).

## What is the project?
Universal AC-MOT: an adaptive-control (AC) layer placed around a FROZEN
detector and a FROZEN tracker for multi-object tracking in drone video. It
controls which detector candidates reach the tracker and with which role
(birth/association vs extension-only), and the tracker's association
tolerance, from causal, online self-calibrated statistics of the stream. It
evolved from the original AC-MOT (YOLOv8n + ByteTrack + handcrafted Scene
Complexity Index, tag v1.0.0-acmot-frozen) into a detector/tracker-agnostic
plug-and-play layer.

## Final system (the contribution) = V7 (frozen V7f, Amendment 10)
training-free, online self-calibrating, causal, detector-agnostic, tracker-agnostic layer between a frozen detector and a frozen tracker: nested exact Otsu on the logits of frames t−10..t−1, whole-stream clean/noisy mode (median ρ ≥ ½) with a background check, host contract (a, b, ℓ, m0), host-anchored clean mode, crowd-safe duplicates and rank score remap in noisy frames, foreground continuation rescue, motion tolerance in noisy frames. Method: research/final/V7_METHOD.md; results:
research/final/V7_MAIN_RESULTS.md and V7_STATISTICS.md; paper: Paper 2 (SCL),
PAPERS.md. Earlier frozen V6-TF (nested-Otsu bands with IoU-0.5 duplicate
suppression) is history: it degraded strong published trackers (D-029),
which V7f's self-limiting clean mode fixes.

## Status by label
- FINAL TARGET: Version: V7 = frozen V7f (config configs/universal_acmot_policy_v7.json,
  lock research/V7_POLICY_LOCK.json, code acmot_v7.py; Amendment 10).
- FROZEN, SUPERSEDED (history): Version: V6-TF (tag universal-acmot-v6-freeze;
  negative external transfer, D-029).
- FROZEN, BASELINE/ABLATION ONLY: Version: V4 (tag universal-acmot-v4-freeze).
- SUPERSEDED DEVELOPMENT HISTORY: Version: V5-TF (F1–F5, E41; never frozen).
- FROZEN, SUPERSEDED (history): Version: V1, Version: V3, legacy AC-MOT
  (v1.0.0-acmot-frozen).
- SUPERSEDED, RESEARCH-ONLY: Version: V5 learned controller (S3 C1/C2/C3).

## Datasets seen / protected (details: DATASETS_AND_SPLITS.md, PROTECTED_EVALUATIONS.md)
- Development (seen): VisDrone2019-MOT-val (V1–V4 and the V6-TF iteration
  sandbox); VisDrone2019-MOT-train development-40 (V5-TF E36/E39/E41; V6-TF
  robustness check only, not iterated on).
- Seen once: VisDrone2019-MOT-test-dev (V4 held-out, E31) → post-hoc only.
- PROTECTED until tag universal-acmot-v6-freeze: train confirmation-16;
  Faster R-CNN quality; BoT-SORT quality; UAVDT quality.

## Exact next step
See NEXT_STEPS.md (NEXT EXACT ACTION) and research/final/.

## Must NOT be changed
HARD_CONSTRAINTS.md (C0 final target = V7 / V7f; training-free; causality; no
category-E constants; protected evaluations; immutable history); the frozen
V6-TF policy after the tag.
