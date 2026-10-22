## Universal AC-MOT Context Protocol

The repository — not chat history — is the project memory. Canonical files:
`research/context/` (start with `research/context/README.md`).

Fast workflow (owner decision D-038; Claude Code, Codex and any other agent). For every task:
1. Read only what the task needs. The session brief (SessionStart hook / `python3 tools/research_guard.py
   --session-brief`) gives branch, phase and rules; read a context file only when the task touches it
   (experiments/evaluation → `HARD_CONSTRAINTS.md` + `PROTECTED_EVALUATIONS.md` first; a paper →
   its `PAPERS.md` row; code → `CODE_ARCHITECTURE.md` section). No full-repository survey.
2. Find the latest relevant version (`python3 tools/version_registry.py list <family>`). If it is COMPLETED,
   FROZEN or SUPERSEDED, run `python3 tools/version_registry.py new <family> [--from <id>]` (one quick
   command) and work in the new ACTIVE folder; an ACTIVE version is edited directly.
3. Do the requested work directly. During the work do NOT rebuild Graphify, rerun the health check, regenerate
   inventories or rewrite research documentation, and do not stop for routine confirmations.
4. Once, at the end: update only the affected hand-written records (the paper's `PAPERS.md` row, a new
   `DECISIONS.md` / `EXPERIMENT_REGISTRY.md` entry when one is made, one `CHANGELOG.md` line), then run
   `python3 tools/sync_research_memory.py --changed-only`. It regenerates what is stale (inventory, registry
   view, context facts, graph), skips what is not, validates once (registry, preservation guard, health check,
   only the tests that match the change) and warns about an unregistered version or a missing CHANGELOG line.
   Add `--full` only for changes to guards, hooks, permissions or versioning, or when CI requires it.
5. Report briefly: what was done, the new version, what changed, memory updated (yes/no), validation result,
   and anything that needs the owner (deletion, completing/freezing a version, push).
Never complete or freeze a version, commit or push without the owner's explicit instruction.

Single writer (applies to Claude AND Codex, interactive or not): if
`outputs/autonomous_v5tf/repo_writer.lock/pid` names a live process, do NOT
modify tracked files. Stop the supervisor with `tools/stop_autonomous_v5tf.sh`
(never touch the waiter or cache queues), verify no `codex exec` child runs,
hold the lock, make and commit the change, release the lock, then restart the
supervisor with `tools/start_autonomous_v5tf.sh`.

Deletion (owner decisions D-033, D-034; `research/context/PRESERVATION_POLICY.md`): create, write and
edit files normally, but NEVER delete, rename/move or empty an existing file or directory, delete or move
a branch or tag, or rewrite history without the owner's explicit, authenticated approval for that exact
target. Ask first, naming the target, the reason and the consequences. A commit-message trailer alone is
not approval; never write owner-approval trailers, never use `--no-verify`, never edit the guards, hooks,
Claude settings or owner keys, and never retry a blocked deletion by another route.

Completed versions (D-035): every COMPLETED / FROZEN / SUPERSEDED version in
`research/VERSION_REGISTRY.json` is read-only. To change a completed artifact, run
`python3 tools/version_registry.py new <family>` (exact copy, next number, provenance recorded) and edit only
the new ACTIVE version; never edit, add to, rename, regenerate or delete a completed one, and never mark a
completed version ACTIVE. Determine numbers with `version_registry.py next`, never by assumption.

Task-dependent reading:
- architecture → `ARCHITECTURE.md`, `DECISIONS.md`
- evaluation → `VALIDATION_PROTOCOL.md`, `DATASETS_AND_SPLITS.md` (and PROTECTED_EVALUATIONS.md first)
- results → `RESULTS_CANONICAL.md` + the machine-readable files it points to

Non-negotiable (details in HARD_CONSTRAINTS.md): the final AC layer is
TRAINING-FREE, online self-calibrating, causal, detector-/tracker-agnostic;
the FINAL TARGET is V7 = frozen V7f (Amendment 10); Optuna/S1–S3 are discovery
tools only; protected evaluations stay closed (PROTECTED_EVALUATIONS.md);
frozen versions, tags, locks, results and old decisions are immutable.

When uncertain about a project fact, DO NOT infer it. Check, in order:
1. git/code  2. canonical result files  3. research/context  4. Graphify  5. detailed logs.
If evidence remains ambiguous, mark the fact UNKNOWN or NEEDS VERIFICATION.
Never invent metrics, experiment status, commit SHAs, dataset leakage status,
parameter justification or frozen state.

Research-memory maintenance happens once per task, at the end (step 4 above); the full checklist in
`research/context/README.md` ("Maintenance workflow") is the reference for what each record owns. Evidence
ranking and conflict handling: same README.

Graph rebuild by hand (normally done by the sync command; deterministic, no LLM):
`$(cat graphify-out/.graphify_python 2>/dev/null || echo ~/.local/share/uv/tools/graphifyy/bin/python) tools/build_context_graph.py`

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For architecture questions you cannot answer with one targeted file read, run `graphify query "<question>"` (small `--budget`) when graphify-out/graph.json exists; never load the full graph or GRAPH_REPORT.md into the conversation for a routine task. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- Do not update the graph during a task: `tools/sync_research_memory.py` rebuilds it once at the end, only when graph-relevant files changed.
