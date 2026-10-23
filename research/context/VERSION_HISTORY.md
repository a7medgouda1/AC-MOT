# VERSION HISTORY — every AC-MOT version, why it existed, what replaced it

Purpose: one chronological record of every research version and research line,
with the problem it addressed, what changed, the evidence that kept or rejected
it, and the exact commit. Owns: version identities, version status labels,
lineage. Does not own: numbers (RESULTS_CANONICAL.md and the files it points
to), experiment detail (EXPERIMENT_REGISTRY.md), code symbols
(CODE_ARCHITECTURE.md, CODE_INVENTORY.md). Update it whenever a version is
created, frozen, superseded, or re-labelled; never rewrite an old row, add a
dated note instead. Freeze tags are verified by tools/context_health_check.py.

## Status vocabulary (four different questions)
| Label | Meaning | Who decides | Current holder |
|---|---|---|---|
| LATEST VERSION | newest research version of the Universal AC-MOT layer | git history | V7 (policy V7f) |
| OFFICIALLY FROZEN | a `universal-acmot-*-freeze` tag with a policy lock whose hashes match | tag + lock file | V7f (universal-acmot-v7-freeze → 488df9a, `research/V7_POLICY_LOCK.json`); earlier frozen: legacy, V1, V3, V4, V6-TF |
| FINAL TARGET (approved) | the version the owner declares as the contribution (HARD_CONSTRAINTS C0) | owner amendment | V7f since Amendment 10 (2026-10-20); V6-TF under Amendment 9; V5-TF under Amendment 7 |
| EXPERIMENTALLY VALIDATED | evaluated after freeze on predeclared external systems with paired bootstrap | evidence files | V7f: positive on PD-SORT, neutral on Hybrid-SORT, negative or neutral on C-TWiX / TrackTrack, TOPICTrack reproduction failed (see V7f row) |
| PAPER-SPECIFIC | the version a manuscript describes | PAPERS.md | Paper 1 = AC-MOT v3 operating-point controller (separate line, below); Paper 2 = V7f |

## Research lines
| Line | What it controls | Versions | Status |
|---|---|---|---|
| L — legacy thesis AC-MOT | detector resolution + confidence from a handcrafted SCI (YOLOv8n + ByteTrack) | legacy AC-MOT | frozen history |
| U — Universal AC-MOT | which detector candidates reach a frozen tracker, with which scores and thresholds | V1 → V7f | V7f latest, frozen, FINAL TARGET |
| C — compute layers on top of frozen V7f | detector compute (resolution, call rate, crops) upstream of V7f | C1 (SCI + V7f), G1, G2 | development candidates; none adopted beyond a constant compute point |
| P1 — Paper 1 operating-point controller | detector operating point (resolution, NMS IoU, confidence floor) from a scene index | AC-MOT v3 (Oct 2026) | frozen experiment archive; submitted as Paper 1 |

Lines U/C and P1 are different methods. Never mix their numbers: P1 uses the
YOLO11m VisDrone checkpoint with ByteTrack/OATrack and the official-compatible
VisDrone protocol; U/C use COCO detectors (YOLOv8n, RT-DETR-L, …) or published
detections on MOT17/KITTI with TrackEval.

## Timeline
| Date | Version | Commit / tag | Problem addressed | Change | Evidence | Outcome | Kept later |
|---|---|---|---|---|---|---|---|
| 2026-09-11 | Legacy AC-MOT | a6c1fa4, tag v1.0.0-acmot-frozen | drone MOT under changing scenes (thesis) | SCI = weighted sum of crowd/tiny/edge/darkness/blur cues every 10 frames → resolution {640,736,832} + confidence sensitivity, hysteresis, recovery probe | ARCHITECTURE.md §A; research/PARAMETER_AUDIT.md | heuristic, detector-/tracker-specific constants; later shown ≤ random allocation (E24–E26) | SCI idea reused by P1 (cue formulas in acmot_sci.py) |
| 2026-09-27 | V1 | e56c2f3, universal-acmot-v1-freeze | make the layer detector-/tracker-agnostic | adapters + online histogram percentile normaliser + leader-relative ratio gate ρ 0.6 + legacy SCI | research/EXPERIMENT_REGISTRY.md E01–E19 | not invariant to score temperature (E20); candidate explosion (FX) | adapter interfaces |
| 2026-09-27 | V2b–V2f | never frozen | candidate explosion, reliability | density budgets / Top-K, proportional thresholds, reliability feedback, closed-loop trust | E02, E03, E06–E14 | all failed (FAILED_EXPERIMENTS.md) | leader-relative score (E15–E17) |
| 2026-09-27 | V3 | c1e799d, universal-acmot-v3-freeze | score-scale invariance | order-only causal ECDF + z-logit leader gate τ 0.75; SCI still in path | E20–E23 | exact Platt/temperature invariance; SCI unjustified (E24–E26) | ECDF rank (later the noisy-mode remap) |
| 2026-09-27 | V4 | fc003bf, universal-acmot-v4-freeze | remove unjustified SCI | V3 core, SCI removed, resolution = compute budget, global τ/s/offsets by nested LOSO | E27–E31 (test-dev once) | baseline / ablation ONLY; category-E constants | comparison baseline |
| 2026-09-27 | V5 learned | 62111e8 … e6d48b7 | scene-state control | scene-state vector + learned per-target controllers (stump/tree/Optuna) | E32–E35 | learned controllers lose to V4 held-out; forbidden as deployed method (Amendment 6) | cue candidates (E33) |
| 2026-09-27 | V5-TF (F1–F5, E41) | 3684684, 71faf44, 240eba9 (never frozen) | training-free self-calibration (Amendment 6) | Otsu bands on causal windows, ECDF in band, F3 motion-scaled association tolerance, F5 scene-adaptive resolution | E36, E39, E40, E41 | F5 resolution control ≤ random (FX-17); E41 rejected by audit (FX-18) | F3 motion rule; Otsu bands |
| 2026-09-28 | V6-TF | 2cff95f, universal-acmot-v6-freeze | E41 failures (duplicates, ghost births) | IoU-0.5 duplicate suppression + nested exact Otsu on logits of frames t−10..t−1 + ECDF within band + motion tolerance | E42–E54, research/final/FREEZE_RECORD_V6TF.md | strong on noisy/miscalibrated VisDrone streams; external transfer NEGATIVE: SparseTrack −4.15, BoostTrack −5.89 HOTA (D-029) | nested Otsu, motion rule, ECDF remap |
| 2026-09-28 | V7a–V7d | tag v7-dev-assets-1 → d56bba0 (not frozen) | V6-TF harms strong trackers on clean crowded streams | ρ regime, host-anchored clean mode, crowd-safe track-context duplicates, cross-class duplicates in clean frames, motion only in noisy frames | research/final/V7_EXPERIMENT_LEDGER.md E0–E10 | SparseTrack/BoostTrack restored to host level | all kept in V7f |
| 2026-09-28 | **V7f** | **488df9a, universal-acmot-v7-freeze**; config `configs/universal_acmot_policy_v7.json`; lock `research/V7_POLICY_LOCK.json`; code acmot_v7.py | mode flips, missing continuation for single-stage trackers, wrong noisy decisions without a background mode | + whole-stream mode (rho_frames 0), + foreground continuation rescue, + background (interpretability) check | V7 ledger E15–E20; `research/final/V7_MAIN_RESULTS.md`; `research/final/V7_STATISTICS.md`; post-freeze `research/final/V7_EXTERNAL_TRANSFER.md`, `research/final/V7_RECENT_EXTERNAL_SYSTEMS.md` | dev: two-stage clean hosts unchanged, OC-SORT +0.61 HOTA, score-shift recovery; known regression KITTI YOLOv8n two-stage MOTA −1.9/−2.4; external: PD-SORT +0.61 HOTA, Hybrid-SORT identical, C-TWiX KITTIMOT car −1.52 HOTA (CI < 0), TrackTrack DanceTrack −0.012 HOTA (CI < 0), TOPICTrack reproduction FAILED | LATEST, FROZEN, FINAL TARGET (Amendment 10) |
| 2026-10-02 | C1 SCI + V7f | 5a8502f (candidate) | does scene-driven compute help on top of V7f? | historical SCI resolution rule (acmot_sci.py) upstream of frozen V7f (acmot_sci_v7.py) | `research/final/SCI_V7F_EXPERIMENT_LEDGER.md` E-SCI-1, D-SCI-1 | SCI + V7f − V7f only: −0.17 HOTA [−0.56, +0.21]; not adopted | — |
| 2026-10-02 | G1 | 751c602, general-acmot-g1-freeze; lock `research/GENERAL_ACMOT_G1_LOCK.json` | general compute layer | constant compute request (no cue passed the pre-registered rule) + V7f; behaviourally V7f at 736 px | SCI ledger §3–4 (T-G1-OCSORT, T-G1-RETINANET, T-G1-BOTSORT) | development candidate; transfer tests recorded | constant compute point |
| 2026-10-02 | G2 | tags g2-s3-1 (workflow); acmot_g2.py | compute adaptation spaces S1 resolution, S2 call rate, S3 crops | pre-registered GT-oracle gate before any controller | `research/final/G2_EXPERIMENT_LEDGER.md` | all spaces FAIL the gate → static compute point + frozen V7f; no controller designed | — |
| 2026-10-04/05 | P1 AC-MOT v3 | bfa5caf (static no-op first val read), 280b4a2 tag acmot-v3-exp-2026-10-04-freeze | adaptive detector operating point for UAV MOT | frozen acmot_sci.SceneLayer (crowd cue only) → LOW/MEDIUM/HIGH → (1536, 0.70, 0.10) / (1280, 0.45, 0.40) / (1088, 0.60, 0.40); τm 0.297, τh 0.511 | research/acmot_paper_v2/FINAL_REPORT.md; `research/acmot_paper_v2/SECOND_VAL_READ_V3_RESULT.json`; `research/acmot_paper_v2/UAVDT_TRANSFER_RESULT.json` | VisDrone val (second read) ByteTrack HOTA 41.586 → 44.523; UAVDT transfer without retuning | described in Paper 1 |

## V7f vs V6-TF (what changed and why)
| Aspect | V6-TF | V7f | Reason (evidence) |
|---|---|---|---|
| When to act | every frame (always noisy bands) | only on noisy streams; clean streams keep the host's thresholds and raw scores | V6-TF cost SparseTrack −4.15 and BoostTrack −5.89 HOTA (D-029, V7 ledger E1–E8) |
| Mode decision | none | median of the confident share ρ over all past non-cold frames ≥ ½ | per-frame regime flipped on transient dips (E16) |
| Duplicates | IoU 0.5 greedy, class-agnostic | cross-class only in clean frames; track-context crowd-safe rule in noisy frames | duplicate removal deleted occluded people in crowds (E1–E5) |
| Thresholds | tracker defaults 0.5/0.1 | host contract (a, b, ℓ, m0); clean: min(host, σ(t2)); noisy: 0.5/0.5 | host-anchored behaviour (E8) |
| Continuation | none | foreground rescue for candidates the host cannot see (single-stage hosts) | OC-SORT lost tracks (E17) |
| Interpretability | none | background check: ρ = 1 when fewer candidates lie below t1 than above | wrong noisy decisions at sequence starts (E18) |
| Shared | nested exact Otsu on logits of t−10..t−1, ECDF rank, motion tolerance min(0.95, 1 − (1 − m0)/max(1, r)) | same, motion only in noisy frames | kept |

## Open version questions
- G1 is tagged `general-acmot-g1-freeze` but labelled "development candidate" in its lock; it is not a Universal AC-MOT freeze and not the FINAL TARGET.
- The P1 controller archive is frozen as an experiment snapshot (280b4a2), not as a `universal-acmot-*` version; Paper 1 reports it as "AC-MOT".

## Completed-version registry (D-035)
Immutable status (COMPLETED / FROZEN / SUPERSEDED / ACTIVE / DRAFT) and the next number of each family are
kept in `research/VERSION_REGISTRY.json` (view: VERSION_REGISTRY.md). Universal AC-MOT numbering continues at
V8 (V2 and V5 were never frozen; documented skip reasons). This file keeps the narrative history.
