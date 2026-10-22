> **Amendment 10 (2026-10-20): V7 / frozen V7f is the approved FINAL version. The PAPERS section is current; the V6-TF sections below are history.**

# NEXT STEPS (operational; keep short; move finished items to DECISIONS/EXPERIMENT_REGISTRY)

## PAPERS (current work, 2026-10-20; details PAPERS.md)
1. Paper 1 (JAIS 2026-10-I012138): confirm both co-authors completed the
   ScholarOne confirmation; record the declarations as entered; wait for
   reviews; revise from Paper1_V13_JAIS in a new version folder.
2. Paper 2 (D-036, D-037, D-039): Paper2_V23 (challenge copy without VisDrone, journal submission layout, with the E57/E58 positive cells) and Paper2_V24 (same content, two columns), now Paper2_V36 (V35 without the declarations section, which must be added back for submission; 15 pages, track paths in the KITTI figure; condensed from Paper2_V34/V33, 25 pages; positives-only challenge copy of Paper2_V31, which holds the review wording fixes; V29 content in Paper 1's section structure and style: two columns, ACT comparison E59/E60, IDS in every table and in the text, plain-English terms table, metric equations in the text, figures to the journal artwork rules, score-groups figure and KITTI example frame, short discussion) go to the supervisor; Paper2_V19 (all results) is the submission candidate, then to The
   Visual Computer. Declarations confirmed (no funding, code on request); owner adds the author photos
   (black and white, passport size). On push: commit V12 and its registry entry first, then register V13,
   V14 to V21 in separate commits (checked registry edit; one new version per family per change).
3. Paper2_V11 (JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11) is not pushed yet.
4. Knowledge base (2026-10-20): resolve the OPEN conflicts CF-02, CF-03, CF-04, CF-07
   (RESULTS_CANONICAL.md) in the next manuscript versions; restore the missing artifacts listed in
   REPRODUCIBILITY.md (Paper 1 detection cache release, VisDrone zip hash, Paper 2 fig3 script).
5. Optional: HTML presentation of Paper 2 (prompt prepared; new folder
   presentations/Paper2_SCL_V11/, never edit older presentations).

## CURRENT GOAL
Complete V6-TF, the FINAL system (Amendment 9; V4 = baseline/ablation only;
E41/V5-TF = rejected development history). Freeze → one-way post-freeze
evaluations → external published-system transfer → paper package in
`research/final/`. Full checklist: PROJECT_COMPLETION.md.

## BLOCKERS
- T4 fidelity gate (Amendment 5f) and official T4 timing: deferred by the
  owner to the final pre-paper step (Amendment 9 §5). Harness:
  notebooks/Colab_T4_gate_and_benchmark.ipynb must be retargeted to the V6-TF
  freeze commit and configs/universal_acmot_policy_v6tf.json first.
- Single-writer rule (AGENTS.md): hold outputs/autonomous_v5tf/repo_writer.lock
  before editing tracked files; the old V5-TF supervisor must NOT be restarted
  (its stage machine targets the rejected E41 path).
- Unknown-provenance WIP preserved in git stash (D-028); do not pop it into a
  freeze or evaluation commit.

## NEXT EXACT ACTION
All post-freeze evaluations are done: confirmation-16, BoT-SORT, Faster R-CNN
(val-7, test-dev, UAVDT), UAVDT, test-dev post-hoc, and the external
SparseTrack/BoostTrack transfers (negative). Remaining:
1. The owner's pre-paper step: the Amendment-5f T4 fidelity gate and
   official GPU timing. Retarget notebooks/Colab_T4_gate_and_benchmark.ipynb
   to 2cff95f and configs/universal_acmot_policy_v6tf.json.
2. Optional: TOPICTrack (IEEE TIP 2025) external run. The environment and
   weights are in acmot_external/TOPICTrack. The same detector checkpoint is
   used, and the result is expected but not tested.
3. Write the paper from research/final/ (claims restricted per
   PAPER_CLAIMS.md).

## DO NOT DO
- No retuning of V6-TF after the tag; no second confirmation run.
- Do not treat V4 as a fallback final system.
- Do not restart tools/autonomous_v5tf_supervisor.py (targets E41).
- Do not run `tools/v5_train.py final` (Amendment 6).
- Do not change V1/V3/V4/V5-TF policy files, tags or locks.
