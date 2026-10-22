# research/context — canonical project memory

FINAL TARGET = V7 (frozen V7f, Amendment 10). V4 = historical baseline / ablation only (HARD_CONSTRAINTS C0).

The chat history is NOT the project memory. This directory, git and the
machine-readable outputs are. A routine task reads only the files it needs (fast workflow in
AGENTS.md, D-038); a full state reconstruction (prompt: NEW_SESSION_PROMPT.md) is for an owner-requested
state review or when the session brief shows a contradiction.

## Start here (any agent: Codex, Claude Code, Copilot, MCP clients, humans)
1. PROJECT_STATE.md — current state, FINAL TARGET, papers.
2. HARD_CONSTRAINTS.md, PROTECTED_EVALUATIONS.md — what must never be done.
3. VERSION_HISTORY.md — every version, status labels, V7f vs V6-TF.
4. PAPERS.md — Paper 0/1/2, versions, submission state, claim and figure maps, open audit items.
5. NEXT_STEPS.md — the next exact action.
6. As needed: CODE_ARCHITECTURE.md (+ generated CODE_INVENTORY.md), EXPERIMENT_REGISTRY.md,
   REPRODUCIBILITY.md, RESULTS_CANONICAL.md (results index + conflict register), DATASETS_AND_SPLITS.md,
   DECISIONS.md, FAILED_EXPERIMENTS.md, CHANGELOG.md.
Everything canonical is plain Markdown/JSON in git. Graphify (`graphify-out/`, git-ignored) is an
optional navigation index built from these files; it is never the authority.

## Evidence hierarchy for scientific claims (highest first)
1. Verified raw experimental outputs and protocol metadata (result JSON/CSV, track archives, run
   environment and lock-check files, preregistrations written before the run).
2. Reproducible evaluation scripts and configurations at a recorded commit.
3. Frozen source-code tags and policy locks.
4. Verified result ledgers (`research/final/*LEDGER*.md`, `research/EXPERIMENT_REGISTRY.md`).
5. Submitted or finalized manuscript records (PAPERS.md, manuscript folders, SUBMISSION_HANDOFF.md).
6. research/context summaries (this directory).
7. Informal notes and conversation history (lowest; never cite alone).
The primary source depends on the claim type: submission status comes from submission records
(PAPERS.md, ScholarOne review copy), version identity from git tags and locks, numbers from result files.
When sources conflict: keep both records, add a row to the conflict register in RESULTS_CANONICAL.md
(CF-xx) with the evidence for each side, mark it OPEN unless the evidence settles it, never pick the
convenient one silently.

## Source-of-truth hierarchy for project state (highest first)
1. Git state / committed code (`git log`, `git show`, tags, working tree)
2. Frozen locks and machine-readable outputs (`research/*_LOCK*.json`,
   `research/TRAIN_SPLIT_V5.json`, `outputs/**/*.json|csv`)
3. research/context canonical files (this directory)
4. Detailed research logs (`research/OPTIMIZATION_PROTOCOL.md`,
   `research/EXPERIMENT_REGISTRY.md`, `research/PARAMETER_AUDIT.md`,
   `research/RESULTS_TESTDEV_V4.md`, legacy `README_ACMOT_*`)
5. Graphify graph (`graphify-out/`) — navigation aid built from 1–4
6. Chat history — LAST. If it conflicts with 1–4: verify the repo, fix context.

## Anti-hallucination rule
When uncertain about a project fact, do NOT infer it. Check, in order:
git/code → canonical result files → research/context → Graphify → detailed
logs. If still ambiguous, write UNKNOWN or NEEDS VERIFICATION. Never invent
metrics, experiment status, commit SHAs, dataset leakage status, parameter
justifications or frozen state.

## Files
| File | Purpose | Maintained |
|---|---|---|
| PROJECT_STATE.md | first file to read; status summary | manual + AUTO block |
| HARD_CONSTRAINTS.md | non-negotiable identity (training-free final AC …) | manual, via amendment only |
| ARCHITECTURE.md | original → V4 → V5-TF, component table | manual |
| DECISIONS.md | append-only decision log (D-xxx) | manual, append-only |
| EXPERIMENT_REGISTRY.md | index E01–E31 + authoritative E32+ | manual |
| RESULTS_CANONICAL.md | where authoritative numbers live | manual, health-checked |
| FAILED_EXPERIMENTS.md | negative results (FX-xx) | manual |
| DATASETS_AND_SPLITS.md | datasets, roles, fingerprints, leakage | manual |
| FROZEN_VERSIONS.md | tags, commits, meaning | manual, health-checked |
| PARAMETER_STATUS.md | constants with categories A–E | manual |
| VALIDATION_PROTOCOL.md | current vs historical protocol | manual |
| PROTECTED_EVALUATIONS.md | allowed/forbidden per protected test | manual |
| ENVIRONMENT_AND_PATHS.md | paths, packages (no secrets) | manual |
| GIT_STATE.md | branch, HEAD, tags, dirty files | AUTO (fully generated) |
| NEXT_STEPS.md | goal, blockers, next exact action | manual |
| PROJECT_COMPLETION.md | definition of done for the final system V5-TF | manual |
| SESSION_HANDOFF.md | one-file compact handoff | manual |
| VERSION_HISTORY.md | every research version and line, status vocabulary (latest / frozen / final target / validated / paper-specific), V7f vs V6-TF | manual, append rows |
| CODE_ARCHITECTURE.md | module roles, data flow, version and paper attribution, mechanism-to-code verification | manual |
| CODE_INVENTORY.md | generated list of modules, classes, functions, line numbers, last commit | AUTO (`tools/build_code_inventory.py`) |
| REPRODUCIBILITY.md | reproducibility labels, environments, experiment cards, matrix, missing artifacts | manual |
| CHANGELOG.md | dated log of knowledge-base changes | manual, append-only |
| PRESERVATION_POLICY.md | AI write access, owner-only delete: approval procedure, enforcement layers, owner setup, known gaps | owner (protection file) |
| RESTORE_AND_ROLLBACK.md | open, compare and recover any frozen version safely (no destructive commands) | manual |
| VERSION_REGISTRY.md | status (COMPLETED/FROZEN/SUPERSEDED/ACTIVE/DRAFT), Git hashes and next number of every version | AUTO (`tools/version_registry.py render`) from research/VERSION_REGISTRY.json |
| PAPERS.md | publication registry: Paper 0 (published survey), Paper 1 (JAIS, submitted), Paper 2 (JRTIP, in preparation), versions, submission and review state | manual |
| KNOWLEDGE_GRAPH.md | typed entities + relations fed to Graphify | manual |
| NEW_SESSION_PROMPT.md | copy-paste start prompt | manual |
| AUTONOMOUS_AGENT_PROMPT.md | safety contract for serialized non-interactive continuation | manual |
| AGENT_STATE.md | machine-readable autonomous stage, process and blocker state | supervisor + agent |

Stable names (use exactly): Version: V1/V3/V4/V5/V5-TF · Detector: YOLOv8n,
RT-DETR-L, Faster R-CNN ResNet50-FPN v2 · Tracker: ByteTrack, BoT-SORT ·
Dataset: VisDrone2019-MOT, UAVDT · Split: VisDrone2019-MOT-val,
VisDrone2019-MOT-test-dev, VisDrone2019-MOT-train development-40,
VisDrone2019-MOT-train confirmation-16, UAVDT test.

## Tools
- `tools/update_project_context.py` — refreshes FACTUAL metadata only
  (AUTO block in PROJECT_STATE.md, GIT_STATE.md). Never rewrites conclusions.
- `tools/build_context_graph.py` — rebuilds `graphify-out/` = Graphify AST
  extraction of code + deterministic extraction of KNOWLEDGE_GRAPH.md and the
  canonical Markdown (Graphify's documented extraction schema; no LLM).
  Run with Graphify's interpreter:
  `$(cat graphify-out/.graphify_python 2>/dev/null || echo /Users/ahmedgouda/.local/share/uv/tools/graphifyy/bin/python) tools/build_context_graph.py`
- `tools/context_health_check.py` — consistency checks (exit 1 on failure).
- `tools/research_guard.py` / `tools/claude_tool_guard.py` — owner-only-delete and preservation guards
  (git hooks via `tools/install_git_hooks.sh`, CI, Claude Code hook); `tools/open_version.sh` opens a
  version read-only. See PRESERVATION_POLICY.md and RESTORE_AND_ROLLBACK.md.
- `tools/version_registry.py` — completed-version registry: `next`, `new` (next version as exact copy),
  `complete`, `verify`, `render` (D-035).
- `graphify query "<question>"`, `graphify explain "<node>"`,
  `graphify path "<A>" "<B>"` — querying.

## Maintenance workflow (once per task, at the end; D-038 fast workflow)
Do the requested work first, without maintenance in between. Then, in one pass:
1. Update only the owning documents the task affected (one owner per fact, table above): PROJECT_STATE,
   VERSION_HISTORY, EXPERIMENT_REGISTRY (+ FAILED_EXPERIMENTS), RESULTS_CANONICAL, PAPERS, REPRODUCIBILITY,
   CODE_ARCHITECTURE, DATASETS_AND_SPLITS — whichever apply, usually one or two.
2. Register any new experiment (stable ID), result file or decision (append D-xxx; never edit old ones).
   New versions are registered by `python3 tools/version_registry.py new <family>` when they are created.
3. Link the change to code (path + symbol) and evidence (file + key); flag missing evidence as
   NEEDS VERIFICATION instead of filling it in.
4. Add one dated line to CHANGELOG.md.
5. `python3 tools/sync_research_memory.py --changed-only` does the deterministic rest and skips what is
   current: code inventory (only if code changed), VERSION_REGISTRY.md view, PROJECT_STATE auto block and
   GIT_STATE.md, graph rebuild (only if graph-relevant files are newer than the graph), then one validation
   pass (registry verify, research_guard --worktree, health check without graph queries, only the tests that
   match the change). It warns about an unregistered version folder or a missing CHANGELOG line. `--full` adds
   the graph queries and the three protection test suites: use it after guard, hook, permission or
   versioning changes. `--dry-run` prints the plan.
6. Report the documentation status in one or two lines in the final task report.
Never: create a version or call an experiment validated without evidence; edit frozen code, locks,
results or old decisions; commit secrets or large generated outputs. `graphify-out/` stays git-ignored.

## Autonomous continuation
`tools/autonomous_v5tf_supervisor.py` is the single-writer, artifact-gated
continuation loop. It does not restart cache queues or the current waiter. It
validates complete E36/E39 artifacts, runs context health, then serially invokes
one non-interactive Codex agent from `AUTONOMOUS_AGENT_PROMPT.md` plus
`NEW_SESSION_PROMPT.md`. Runtime status and logs are under
`outputs/autonomous_v5tf/`; canonical handoff state is `AGENT_STATE.md`.
Start/status/safe-stop commands are `tools/start_autonomous_v5tf.sh`,
`tools/status_autonomous_v5tf.sh`, and `tools/stop_autonomous_v5tf.sh`.
