# VERSION REGISTRY (generated from research/VERSION_REGISTRY.json — do not edit by hand)

Authoritative immutable status of completed versions (D-035). COMPLETED / FROZEN / SUPERSEDED
entries are read-only to AI agents; changes go into the next version created with
`python3 tools/version_registry.py new <family>`. Rules: PRESERVATION_POLICY.md section 6.

## Families and next version

| Family | Title | Kind | Pattern | Next |
|---|---|---|---|---|
| archives | completed results, evidence and frozen configuration files | fileset | `` | — (no sequence) |
| legacy-manuscripts | earlier manuscript drafts (no sequential number) | version_dir | `` | — (no sequence) |
| paper1 | Paper 1 AC-MOT operating-point controller (JAIS) | version_dir | `Paper1_V{n}_JAIS` | V14 |
| paper2 | Paper 2 SCL / frozen V7f (JRTIP) | version_dir | `PAPER2_V7F_JRTIP_challenge_rev{n}` | V65 |
| policy-locks | policy locks of frozen systems | lock | `` | — (no sequence) |
| tags | other frozen git tags | tag | `` | — (no sequence) |
| universal-acmot | Universal AC-MOT system (frozen tags) | tag | `universal-acmot-v{n}-freeze` | V8 |

## Entries

| ID | Status | Kind | Path / ref | Commit | Parent | Evidence |
|---|---|---|---|---|---|---|
| paper1/V1-jrtip | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev10` | cb1399591 |  | PAPERS.md 'Paper1_V1-V3 = manuscript_jrtip_supervisor_rev10-rev12' (order rev10->V1 assumed; NEEDS VERIFICATION) |
| paper1/V2-jrtip | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev11` | cb1399591 |  | PAPERS.md 'Paper1_V1-V3 = manuscript_jrtip_supervisor_rev10-rev12' (order rev10->V1 assumed; NEEDS VERIFICATION) |
| paper1/V3-jrtip | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev12` | 347577c66 |  | PAPERS.md 'Paper1_V1-V3 = manuscript_jrtip_supervisor_rev10-rev12' (order rev10->V1 assumed; NEEDS VERIFICATION) |
| paper1/V4-springer | SUPERSEDED | version_dir | `research/acmot_paper_v2/Paper1_Springer_Template/Paper1_V4` | 915175165 |  | PAPERS.md Paper 1 version history (Springer template) |
| paper1/V5-springer | SUPERSEDED | version_dir | `research/acmot_paper_v2/Paper1_Springer_Template/Paper1_V5` | 915175165 |  | PAPERS.md Paper 1 version history (Springer template) |
| paper1/V6-springer | SUPERSEDED | version_dir | `research/acmot_paper_v2/Paper1_Springer_Template/Paper1_V6` | b00ef64f5 |  | PAPERS.md Paper 1 version history (Springer template) |
| paper1/V6-jais | SUPERSEDED | version_dir | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V6_JAIS` | d916d78b5 |  | PAPERS.md Paper 1 version history |
| paper1/V7 | SUPERSEDED | version_dir | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V7_JAIS` | f9001aa68 |  | PAPERS.md Paper 1 version history |
| paper1/V8 | SUPERSEDED | version_dir | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V8_JAIS` | f9001aa68 |  | PAPERS.md Paper 1 version history |
| paper1/V9 | SUPERSEDED | version_dir | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V9_JAIS` | b00ef64f5 |  | PAPERS.md Paper 1 version history |
| paper1/V10 | SUPERSEDED | version_dir | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V10_JAIS` | f3832a917 |  | PAPERS.md Paper 1 version history |
| paper1/V11 | SUPERSEDED | version_dir | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V11_JAIS` | 67b543cf5 |  | PAPERS.md Paper 1 version history |
| paper1/V12 | COMPLETED | version_dir | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V12_JAIS` | 67b543cf5 |  | submitted to JAIS 18-Oct-2026, manuscript 2026-10-I012138 (PAPERS.md) |
| paper1/V13 | COMPLETED | version_dir | `research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS` | ffa3013d3 |  | delivered package for the revision (PDF + Overleaf zip), pushed e8428eb (PAPERS.md) |
| paper2/V1 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev1` | cb1399591 |  | PAPERS.md Paper 2 version history |
| paper2/V2 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev2` | cb1399591 |  | PAPERS.md Paper 2 version history |
| paper2/V3 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev3` | cb1399591 |  | PAPERS.md Paper 2 version history |
| paper2/V4 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev4` | cb1399591 |  | PAPERS.md Paper 2 version history |
| paper2/V5 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev5` | 347577c66 |  | PAPERS.md Paper 2 version history |
| paper2/V6 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev6` | 347577c66 |  | PAPERS.md Paper 2 version history |
| paper2/V7 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev7` | 347577c66 |  | PAPERS.md Paper 2 version history |
| paper2/V8 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev8` | 347577c66 |  | PAPERS.md Paper 2 version history |
| paper2/V9 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev9` | 347577c66 |  | PAPERS.md Paper 2 version history |
| paper2/V10 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev10` | 915175165 |  | PAPERS.md Paper 2 version history |
| paper2/V11 | COMPLETED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11` | dbf162ca3 |  | delivered Paper2_V11, internally reviewed (D-031), pushed dbf162c |
| legacy-manuscripts/PAPER1_SCENE_ADAPTIVE_JAIS | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER1_SCENE_ADAPTIVE_JAIS` | a1a2d5ecd |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/PAPER2_SIVP_SPRINGER | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_SIVP_SPRINGER` | e7071ee58 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/PAPER2_UNIVERSAL_ACMOT_JAIS | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_UNIVERSAL_ACMOT_JAIS` | 7252fa360 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/PAPER2_V7F_JRTIP_challenge_v1 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_v1` | a311a4654 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/PAPER2_V7F_JRTIP_full_v1 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_full_v1` | a311a4654 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/PAPER2_V7F_JRTIP_full_rev1 | SUPERSEDED | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_full_rev1` | cb1399591 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_blind_challenge_v1 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_blind_challenge_v1` | 25a55113f |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev1_single | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev1_single` | 05657b909 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev1 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev1` | 05657b909 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev2 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev2` | 05657b909 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev3 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev3` | 05657b909 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev4 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev4` | 05657b909 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev5 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev5` | 05657b909 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev6 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev6` | 05657b909 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev7 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev7` | 05657b909 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev8 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev8` | 05657b909 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| legacy-manuscripts/manuscript_jrtip_supervisor_rev9 | SUPERSEDED | version_dir | `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev9` | cb1399591 |  | earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20 |
| tags/acmot-v3-exp-2026-10-04-freeze | FROZEN | tag | `acmot-v3-exp-2026-10-04-freeze` | 280b4a2d2 |  | FROZEN_VERSIONS.md |
| tags/g2-s3-1 | FROZEN | tag | `g2-s3-1` | 6c88f5d69 |  | FROZEN_VERSIONS.md |
| tags/general-acmot-g1-freeze | FROZEN | tag | `general-acmot-g1-freeze` | 751c60221 |  | FROZEN_VERSIONS.md |
| tags/jais-overleaf-1 | FROZEN | tag | `jais-overleaf-1` | 8c50fc542 |  | FROZEN_VERSIONS.md |
| tags/jrtip-submission-v1 | FROZEN | tag | `jrtip-submission-v1` | c9aa32d33 |  | FROZEN_VERSIONS.md |
| tags/jrtip-submission-v2 | FROZEN | tag | `jrtip-submission-v2` | 2b466f3f8 |  | FROZEN_VERSIONS.md |
| tags/recent-assets-1 | FROZEN | tag | `recent-assets-1` | 70e5f7dc4 |  | FROZEN_VERSIONS.md |
| tags/sci-v7f-sweep-1 | FROZEN | tag | `sci-v7f-sweep-1` | e9c3bc0e0 |  | FROZEN_VERSIONS.md |
| tags/sci-v7f-unseen-1 | FROZEN | tag | `sci-v7f-unseen-1` | 3da0d1782 |  | FROZEN_VERSIONS.md |
| universal-acmot/V1 | SUPERSEDED | tag | `universal-acmot-v1-freeze` | e56c2f377 |  | FROZEN_VERSIONS.md |
| universal-acmot/V3 | SUPERSEDED | tag | `universal-acmot-v3-freeze` | c1e799d3b |  | FROZEN_VERSIONS.md |
| universal-acmot/V4 | SUPERSEDED | tag | `universal-acmot-v4-freeze` | fc003bf96 |  | FROZEN_VERSIONS.md |
| universal-acmot/V6 | SUPERSEDED | tag | `universal-acmot-v6-freeze` | 2cff95f8a |  | FROZEN_VERSIONS.md |
| universal-acmot/V7 | FROZEN | tag | `universal-acmot-v7-freeze` | 488df9a95 |  | FROZEN_VERSIONS.md (FINAL TARGET, Amendment 10) |
| tags/v1.0.0-acmot-frozen | FROZEN | tag | `v1.0.0-acmot-frozen` | a6c1fa49f |  | FROZEN_VERSIONS.md |
| tags/v3f-paper-first-journal | FROZEN | tag | `v3f-paper-first-journal` | 25a55113f |  | FROZEN_VERSIONS.md |
| tags/v7-dev-assets-1 | FROZEN | tag | `v7-dev-assets-1` | d56bba0d8 |  | FROZEN_VERSIONS.md |
| policy-locks/V7_POLICY_LOCK | FROZEN | lock | `research/V7_POLICY_LOCK.json` | 488df9a95 |  | active policy lock (R1); files may be run but not changed |
| policy-locks/V6TF_POLICY_LOCK | SUPERSEDED | lock | `research/V6TF_POLICY_LOCK.json` | 2cff95f8a |  | active policy lock (R1); files may be run but not changed |
| policy-locks/GENERAL_ACMOT_G1_LOCK | FROZEN | lock | `research/GENERAL_ACMOT_G1_LOCK.json` | 751c60221 |  | active policy lock (R1); files may be run but not changed |
| archives/research/final | COMPLETED | fileset | `research/final` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/acmot_paper_v2 | COMPLETED | fileset | `research/acmot_paper_v2` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/paper_split/evidence | COMPLETED | fileset | `research/paper_split/evidence` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/transfer_legacy | COMPLETED | fileset | `research/transfer_legacy` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/published_papers | COMPLETED | fileset | `research/published_papers` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/cue_audit | COMPLETED | fileset | `research/cue_audit` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/uavdt_protocol | COMPLETED | fileset | `research/uavdt_protocol` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/JAIS_PAPERS/overleaf | COMPLETED | fileset | `JAIS_PAPERS/overleaf` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/TRAIN_SPLIT_V5.json | COMPLETED | fileset | `research/TRAIN_SPLIT_V5.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/configs/g2_gsci_frozen.json | COMPLETED | fileset | `configs/g2_gsci_frozen.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/configs/general_acmot_g1.json | COMPLETED | fileset | `configs/general_acmot_g1.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/configs/universal_acmot_policy.json | COMPLETED | fileset | `configs/universal_acmot_policy.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/configs/universal_acmot_policy_v4.json | COMPLETED | fileset | `configs/universal_acmot_policy_v4.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/configs/universal_acmot_policy_v5tf.json | COMPLETED | fileset | `configs/universal_acmot_policy_v5tf.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/configs/universal_acmot_policy_v6tf.json | COMPLETED | fileset | `configs/universal_acmot_policy_v6tf.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/configs/universal_acmot_policy_v7.json | COMPLETED | fileset | `configs/universal_acmot_policy_v7.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/TESTDEV_LOCK.json | COMPLETED | fileset | `research/TESTDEV_LOCK.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/TESTDEV_LOCK_V4.json | COMPLETED | fileset | `research/TESTDEV_LOCK_V4.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/TRANSFER_LOCK_FASTERRCNN.json | COMPLETED | fileset | `research/TRANSFER_LOCK_FASTERRCNN.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/TRANSFER_LOCK_RETINANET_G1.json | COMPLETED | fileset | `research/TRANSFER_LOCK_RETINANET_G1.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/TRANSFER_LOCK_UAVDT.json | COMPLETED | fileset | `research/TRANSFER_LOCK_UAVDT.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/TRANSFER_LOCK_UAVDT_FRCNN.json | COMPLETED | fileset | `research/TRANSFER_LOCK_UAVDT_FRCNN.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/TRANSFER_LOCK_V6TF.json | COMPLETED | fileset | `research/TRANSFER_LOCK_V6TF.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/V5TF_POLICY_LOCK.json | COMPLETED | fileset | `research/V5TF_POLICY_LOCK.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| archives/research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/artifacts/research/TRANSFER_LOCK_UAVDT.json | COMPLETED | fileset | `research/acmot_paper_v2/experiments/ACMOT_EXP_V3_2026-10-04/artifacts/research/TRANSFER_LOCK_UAVDT.json` | 5a991405c |  | committed results/evidence/frozen config (immutable since R2, 2026-10-20); new files may be added, existing ones never change |
| paper2/V12 | ACTIVE | version_dir | `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev12` |  | paper2/V11 | copy of paper2/V11 (dbf162ca3) by tools/version_registry.py |

Not registered (completion status NOT decided; owner to classify): `THESIS/`, `notebooks/`,
presentations, root-level research scripts outside the locks.
