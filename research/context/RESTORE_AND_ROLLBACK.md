# RESTORE AND ROLLBACK — opening, restoring and recovering any version safely

Nothing here deletes or rewrites anything. Every procedure reads from git history into a NEW
location; the current branch, its uncommitted work and all tags stay as they are. Commands that
destroy work (`git reset --hard`, `git checkout -- <path>` over uncommitted edits, `git clean`,
force-push, tag/branch deletion) are never part of a restore; agents are blocked from them
(PRESERVATION_POLICY.md).

## 1. Frozen versions (every freeze tag)

Commits are full SHAs in FROZEN_VERSIONS.md; details per version in VERSION_HISTORY.md;
reproduction cards in REPRODUCIBILITY.md.

| ID | Tag | Commit | Status | Paper | Config / code | Results | Limitations |
|---|---|---|---|---|---|---|---|
| Legacy AC-MOT | v1.0.0-acmot-frozen | a6c1fa4 | historical (original thesis method) | thesis | handcrafted SCI controller at that commit | legacy runs listed in FROZEN_VERSIONS.md | exploratory test-dev runs; superseded research line |
| V1 | universal-acmot-v1-freeze | e56c2f3 | superseded → V3 | — | `configs/universal_acmot_policy.json` at the tag | val only | baseline row only |
| V3 | universal-acmot-v3-freeze | c1e799d | superseded → V4 | — | policy + pipeline hashes in `research/TESTDEV_LOCK.json` (lock superseded before any test-dev metric) | val | baseline row only |
| V4 | universal-acmot-v4-freeze | fc003bf | BASELINE / ABLATION ONLY (Amendment 7) | — | `configs/universal_acmot_policy_v4.json`, `research/TESTDEV_LOCK_V4.json` | E31 (`research/EXPERIMENT_REGISTRY.md`) | lock rehashed after the tag in 3ea7d69, "no behaviour change" (RESULTS_CANONICAL.md CF-08) |
| V6-TF | universal-acmot-v6-freeze | 2cff95f | frozen history (superseded by V7, Amendment 10) | — | `configs/universal_acmot_policy_v6tf.json`, `research/V6TF_POLICY_LOCK.json` | `research/final/FINAL_RESULTS.md`, `research/final/FREEZE_RECORD_V6TF.md` | — |
| **V7 (V7f)** | universal-acmot-v7-freeze | 488df9a | **FINAL TARGET** (Amendment 10) | Paper 2 | `configs/universal_acmot_policy_v7.json`, `acmot_v7.py`, `research/V7_POLICY_LOCK.json` | `research/final/V7_MAIN_RESULTS.md` / `.json`, `research/final/V7_RECENT_EXTERNAL_RESULTS.json` | Paper2_V11 audit gaps CF-02–CF-04 |
| G1 | general-acmot-g1-freeze | 751c602 | development candidate | — | `configs/general_acmot_g1.json`, `research/GENERAL_ACMOT_G1_LOCK.json` | `research/final/SCI_V7F_RESULTS.md` | not a final system |
| AC-MOT V3 experiment archive | acmot-v3-exp-2026-10-04-freeze | 280b4a2 | frozen evidence behind Paper 1 | Paper 1 | `research/acmot_paper_v2/` scripts at the tag | `research/acmot_paper_v2/FINAL_ACMOT_SYSTEMS_RESULT.json`, `BOOTSTRAP_V3_RESULT.json`, `UAVDT_TRANSFER_RESULT.json` | second val read CF-07 |

Other tags (assets, workflow releases, manuscript snapshots: recent-assets-1, v7-dev-assets-1,
jais-overleaf-1, g2-s3-1, sci-v7f-sweep-1, sci-v7f-unseen-1, jrtip-submission-v1, jrtip-submission-v2,
v3f-paper-first-journal) are listed with their meaning in FROZEN_VERSIONS.md and open the same way.
Manuscript versions are separate folders, never overwritten; the full list (folder, template, change,
commit) is in PAPERS.md.

## 2. Safe procedures

Read one file from any version (prints to the terminal or to a NEW file):

    git show universal-acmot-v7-freeze:configs/universal_acmot_policy_v7.json
    git show 488df9a:acmot_v7.py > /tmp/acmot_v7_at_freeze.py

Open a whole version read-only next to the current work (no effect on the current checkout):

    sh tools/open_version.sh universal-acmot-v7-freeze
    # -> ../AC-MOT-versions/universal-acmot-v7-freeze (detached worktree, write-protected)

Compare a version with today:

    git diff universal-acmot-v7-freeze -- configs/ acmot_v7.py

Verify a frozen version is intact (locks and tags):

    python3 -m pytest -q tests/test_research_memory.py

Recover a file that was deleted or overwritten in the working tree (creates it again; nothing else
changes):

    git log --oneline -- <path>                    # find the last commit that had it
    git show <commit>:<path> > <path>              # write it back as a new file

Recover a whole folder from a version into a NEW folder (never on top of the current one):

    git archive <tag-or-commit> <folder> | tar -x -C /tmp/acmot_restore/

Undo a bad commit on a shared branch: `git revert <commit>` (adds a new commit; history is kept).

A rollback of the current branch to an old version is done by the owner only, as a new commit or a new
branch (`git switch -c restore-<tag> <tag>`), never by moving or deleting existing refs.

## 3. What git cannot restore

Untracked and ignored data (`outputs/`, caches, datasets, model weights) exists only on disk. Keep a
backup (Time Machine on the Mac, Drive copies) — see PRESERVATION_POLICY.md section 5.
