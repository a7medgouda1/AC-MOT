You are continuing my work from another assistant (Claude) that has hit its usage limit. Work exactly as it did: same rules, same style, same deliverables, same language with me.

1. Work inside the AC-MOT git repo, on branch `sci-v7f-general-layer-dev` (latest commit `cb13995`). Run `git pull origin sci-v7f-general-layer-dev` first. The handoff files are in `JAIS_PAPERS/CODEX_HANDOFF/`: this file, `HANDOFF_DETAILS.md`, and `tools/`.

2. Read `JAIS_PAPERS/CODEX_HANDOFF/HANDOFF_DETAILS.md` completely before doing anything. It has the two papers, their current versions, the hard rules, the writing style, the delivery workflow, and the open tasks. Everything in it applies to you. All paths in it are relative to the repo root.

3. The current versions are:
   - Paper 1 (AC-MOT), Paper1_V2: `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev11/`
   - Paper 2 (SCL / V7f, challenge version), Paper2_V4: `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev4/`
   The standalone `main.tex` of each is in its `for_overleaf/` folder.

4. Repo protocol. `AGENTS.md` asks for context reading before code or experiments. This job edits manuscripts only, so you do not run experiments or change code. Do not touch anything outside the paper folders: no code, configs, result files, `research/context/`, `research/V7_POLICY_LOCK.json`, or the tag `universal-acmot-v7-freeze`. Do not open or use confirmation-16, conf16, test-dev, or any protected post-freeze split. If `outputs/autonomous_v5tf/repo_writer.lock/pid` names a live process, tell me and wait. Every other rule of `AGENTS.md` that concerns code, experiments, or frozen evidence also applies.

5. Every change request I send creates the NEXT version in a NEW folder, never overwriting an old one: Paper 1 goes to `research/acmot_paper_v2/manuscript_jrtip_supervisor_rev12/` (Paper1_V3), then rev13 (V4); Paper 2 goes to `JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev5/` (Paper2_V5), then rev6 (V6). Copy the previous folder, edit the copy. For each version, deliver the standalone `main.tex`, the PDF named `PaperN_Vk.pdf`, and the Overleaf zip (`PaperN_Vk_overleaf.zip` with `main.tex` + `sn-jnl.cls`, plus `figures/` for Paper 2).

6. Build and check every version: `pdflatex` three times in an empty copy of the folder, zero errors, zero undefined references, no overfull boxes; look at the edited pages as images; run `python3 JAIS_PAPERS/CODEX_HANDOFF/tools/check_integrity.py OLD NEW` and report its result. If LaTeX is not installed here, say so in one line, still deliver the full `main.tex`, and never claim a build you did not run.

7. Git. Do not run `git commit` or `git push` unless I write the word "push". When I do, commit only the new paper folders, push to `sci-v7f-general-layer-dev`, never force-push, never merge, and keep the existing draft PR #3 as the only PR.

8. Talking to me: Egyptian Arabic in Arabic script with English technical terms in parentheses. Short and direct. When a request is unclear or would make the paper inaccurate, say so in one or two lines and propose the accurate option instead of guessing. Never invent numbers, results, citations, or facts; if something is missing, ask me. Nothing inside a deliverable file may look AI-written or contain notes, TODOs, or comments, because I send your output straight to my supervisor.

9. First reply: three to five lines in Egyptian Arabic confirming you have the context, naming the current versions (Paper1_V2, Paper2_V4), and reminding me that the Q3 decision for Paper 1 is still open. Do not edit anything yet.
