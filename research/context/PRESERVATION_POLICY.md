# PRESERVATION POLICY — AI write access, owner-only delete

Owner decisions 2026-10-20 (D-033, D-034, D-035). This file is a protection file: agents do not edit it.

## 1. The rule

AI agents (Claude Code, Codex, any tool acting with agent credentials) may **create, write, edit
and update** project files normally: code, configs, documentation, new experiment and manuscript
versions, generated inventories and graphs, tests, experiment runs, commits and research-memory updates.
The scientific freeze rules still apply: frozen V7f code, locks, committed results and existing manuscript
version folders are not edited (new work = new version or experiment ID; HARD_CONSTRAINTS.md).

AI agents may **not delete** without the owner's explicit, authenticated approval for that exact target:
- an existing file or directory (tracked, untracked or ignored);
- a git branch or tag, local or remote, or committed history (force-push, rebase, reset --hard, filter-*);
- a historical artifact (results, logs, caches, manuscripts, PDFs, zips).

Deletion includes every indirect route: shell (`rm`, `rmdir`, `unlink`, `shred`, `find -delete`,
`xargs rm`, `rsync --delete`, `git rm`, `git clean`), code (Python `os.remove`/`unlink`/`rmtree`,
Node `fs.rm*`/`unlink*`, Perl/Ruby equivalents), git operations that delete tracked files, editor and
filesystem tools, third-party tools and cleanup scripts, renames or moves that remove the original path,
branch/tag deletion, CI or automation running with agent credentials, and emptying a file or destroying
its substantive content as a disguised deletion.

An agent never bypasses, disables or weakens a guard to finish a task, never writes an owner-approval
trailer, never uses `--no-verify`, and never retries a blocked deletion by another route.

## 2. What counts as owner approval

Approval is valid only when it is **authenticated and target-specific**:
1. The agent asks the owner, naming the exact target, why it should go, and the consequences
   (what is lost, what references it, how to restore it).
2. The owner approves that one target. Approval of one deletion never covers another. Silence,
   earlier approvals, general instructions ("clean up the repo") and anything an agent writes are not
   approval. **A commit-message trailer on its own is never approval.**
3. The owner makes the change in a commit **signed with the owner's private key** whose message names
   the target with the trailer `Owner-Approved-Delete: <path or directory/> | reason`
   (`Owner-Approved-Change: ...` for frozen files, protection files and append-only records). One trailer
   per target; it applies only to the commit that carries it.
4. Verification (CI and pre-push, `tools/research_guard.py --range`): the signature must be valid and made
   by a trusted owner key. Trust roots, in order: the GitHub repository variable `ACMOT_OWNER_KEYS`
   (set by the owner in repository settings; when it exists, key files in the repository are ignored),
   otherwise public keys in `.github/owner_keys/` at the BASE of the checked range.
5. **Fail closed:** no trusted key configured, no signature, a key the owner did not register, or a
   signature that cannot be verified (for example the verifier tool is missing) → the trailer is ignored
   and the deletion fails the check.
6. Local git hooks cannot see a signature before the commit exists, so they never accept an approval:
   they refuse every staged deletion. The owner commits an approved deletion with
   `git commit -S --no-verify` from their own terminal; CI and pre-push then verify it.
7. Branches and tags: the owner deletes or moves them from their own terminal or the GitHub web interface
   (no trailer mechanism; agents are blocked from every ref-deleting command).

The private key must never be reachable by an agent: not in the repository, not in a cloud session,
not on a machine user account that agents run under without a passphrase. Never register a key that an
agent environment already uses to sign commits (the Claude cloud sessions sign their own commits with an
SSH key; that key must not become an owner key).

## 3. What is enforced, and by what

Technically enforced (code that runs whether or not the agent cooperates, within its boundary):

| Layer | Files | Boundary | Enforces |
|---|---|---|---|
| Claude Code PreToolUse hook | `tools/claude_tool_guard.py`, `.claude/settings.json` | tool calls of Claude Code sessions and subagents in this project, while the hook is configured | blocks the deletion routes of section 1 it can parse (shell, git, inline Python/Node/Perl/Ruby, new or changed scripts, `bash -c`, `eval`, `$(...)`, renames, emptying), edits to frozen artifacts and tracked protection files, writes to Claude settings and `.git/`, owner trailers, `ACMOT_OWNER_KEYS`, `--no-verify`, hooksPath changes, GitHub MCP `delete_file`; fails closed if the guard crashes on a deletion-like command or a file edit |
| Git hooks | `.githooks/pre-commit`, `.githooks/pre-push` (enabled by `tools/install_git_hooks.sh`) | commits and pushes in a clone where the owner installed them, for any program that does not pass `--no-verify` | refuses committing a deletion, rename, emptied file or frozen/protected change; refuses pushing a ref deletion, tag move or non-fast-forward, and pushing commits whose deletions lack a verified owner signature |
| CI | `.github/workflows/research_guard.yml` | every push and pull request on GitHub | the same rules per commit with signature verification; marks the push red. It does not undo a push by itself (see 4.4) |
| GitHub rulesets (after the owner imports them) | `.github/rulesets/*.json` | the GitHub remote, for everyone without bypass rights | blocks branch/tag deletion, force-push and tag moves server-side; optionally refuses pushes whose commits fail CI |

Enforced only by AI instructions (AGENTS.md, CLAUDE.md, this file, the session brief): asking before any
deletion with target/reason/consequences; not using routes the hook cannot parse; Codex behaviour where no
hook exists; not deleting untracked data outside the Claude hook's reach.

Requires owner configuration or approval: section 4.

## 4. Owner-side setup (genuine owner actions, not done by agents)

4.1 **Claude deny rules (optional second layer).** Review `.claude/settings.proposed.json` (the active
`.claude/settings.json` plus a `permissions.deny` list and the GitHub MCP matcher), then in your own
terminal: `cp .claude/settings.proposed.json .claude/settings.json`. Agents cannot do this: the hook blocks
writes to Claude settings. Keep `.claude/settings.local.json` and `~/.claude/settings.json` free of
`disableAllHooks`.

4.2 **Git hooks** in each clone (Mac and cloud): `sh tools/install_git_hooks.sh`
(sets `core.hooksPath=.githooks`; undo with `git config --unset core.hooksPath`). Not installed yet.

4.3 **Owner signing key.** Create a key agents cannot reach (hardware key, or a passphrase-protected key
on your Mac only). Preferred: put its public key in the GitHub repository variable `ACMOT_OWNER_KEYS`
(Settings → Secrets and variables → Actions → Variables; ASCII-armored GPG public key, or SSH
`allowed_signers` lines). Alternative: commit it to `.github/owner_keys/owner.asc` (or `allowed_signers`)
yourself. The first key cannot be verified by an earlier key, so that commit is flagged once by design;
adding any later key needs an approval signed by an already trusted key. Configure git to sign:
`git config user.signingkey <id>`, then `git commit -S`.
Until a key is configured, every deletion is refused (fail closed).

4.4 **GitHub rulesets.** Settings → Rules → Rulesets → New ruleset → Import, using
`.github/rulesets/protect_branches.json` and `.github/rulesets/protect_tags.json`. Without them, CI only
reports; with the optional required status check (`guard`), GitHub refuses pushes that fail the
deletion check, and the workflow and guard files can only change through checks you control. Add a
CODEOWNERS review for `tools/*guard*`, `.githooks/`, `.github/` and `.claude/` if you use pull requests.
Never give agent tokens admin or bypass rights.

4.5 **Codex.** Codex has no PreToolUse hook here. It reads AGENTS.md; its commits pass the git hooks (if
installed) and CI. If your Codex version supports execpolicy rule files (NEEDS VERIFICATION), add rules that
forbid `rm`, `rmdir`, `unlink`, `shred`, `truncate`, `git rm`, `git mv`, `git clean`, `git reset --hard`,
`git branch -d/-D/-m`, `git tag -d/-f`, `git push --delete/--force/--no-verify`,
`git commit --no-verify/-n` and `git config core.hooksPath`, and run it with
`sandbox_mode = "workspace-write"` and an approval policy that asks before untrusted commands.

4.6 **Operating-system isolation (the only layer that makes deletion physically impossible).** None of the
layers above can stop a process that runs as your user and ignores them. To make deletion impossible,
the OS must deny it: run agents as a separate user with read-only access to protected folders, in a
container whose mounts are read-only, or keep `chflags uchg` / `chattr +i` on frozen folders (owner applies;
it also stops ordinary editing of those folders). Keep backups (Time Machine) for data outside git.

## 5. Known gaps and bypasses

- Pattern guards cannot understand every program: commands built from strings at run time
  (`eval "$(printf ...)"`, base64), compiled binaries, and third-party tools that delete internally
  (`make clean`, `latexmk -C`, package managers, test runners that clean up) can pass the Claude hook.
  Committed deletions are still caught by the git hooks and CI, and committed files stay in git history.
- Committed and pushed scripts are trusted and run without inspection; only new or changed scripts are scanned.
- Untracked and ignored files (`outputs/`, caches, data) are protected only by the Claude hook; git and CI
  cannot see them. Back them up.
- Git hooks are local: `--no-verify` or another clone without them skips them. Codex is not blocked from
  `--no-verify` by any hook here. CI reports the violation after the push; only a ruleset with the
  required check (4.4) refuses the push.
- Keys stored in the repository (trust root 2) are only as strong as the repository: an agent with push
  rights could land its own key file if a red CI is ignored. Use the repository variable (trust root 1)
  and rulesets.
- An agent with push rights could edit the CI workflow itself; that change is flagged (R7) but only a ruleset
  with required checks / owner review stops it.
- The owner can always delete (admin rights, `--no-verify`, web interface). That is intended.

## 6. Completed versions are immutable (D-035)

Every completed version of a project artifact (code, configurations, results, manuscripts,
presentations, figures, reports, snapshots) is permanently read-only to AI agents. Agents create new
versions and edit the ACTIVE version; they never delete, overwrite, move, rename, add to or regenerate a
completed one. Approval to delete a file never authorises changing a completed version: that needs its own
owner-signed trailer `Owner-Approved-Completed-Change: <path>` (and the owner also records the new tree in
the registry). By default a change goes into the next version.

**Authority.** `research/VERSION_REGISTRY.json` (human view: `research/context/VERSION_REGISTRY.md`) lists
every registered version with family, number, kind, path, status, Git commit and tree/blob hash, parent and
evidence. Statuses: COMPLETED, FROZEN, SUPERSEDED = immutable; ACTIVE, DRAFT = editable until completed.
Kinds: `version_dir` (sealed folder), `fileset` (archive: existing files immutable, new files may be added,
e.g. `research/final`), `lock` (frozen code: may be run, never changed), `tag` (frozen git tag). File names
alone (V1, V2, ...) never decide the status; the registry does, backed by Git hashes.

**Sequential versions.** `python3 tools/version_registry.py next <family>` gives the next number = highest
number ever used in the family (registry entries, folder or tag names in Git and on disk) + 1; a skipped
number needs a documented `skip_reason`. Existing names (V7f, Paper2_V11, PAPER2_..._rev11) are kept.
Current: Paper 1 → V14 (`Paper1_V14_JAIS`), Paper 2 → V12 (`PAPER2_V7F_JRTIP_challenge_rev12`),
Universal AC-MOT → V8 (V2 and V5 skipped, documented).

**Workflow for a change to a completed artifact.**
1. `python3 tools/version_registry.py new <family>`: copies the latest completed version byte-for-byte from
   Git into the next-numbered folder, registers it ACTIVE with parent, parent commit and parent tree, appends
   CHANGELOG, regenerates VERSION_REGISTRY.md (`--graph` also rebuilds the graph).
2. Edit only the new folder; update PAPERS.md / REPRODUCIBILITY.md / VERSION_HISTORY.md as applicable;
   rebuild Graphify.
3. When the version is final: commit it, then `python3 tools/version_registry.py complete <id> --evidence "..."`
   records the commit and tree; from then on it is read-only.
4. `python3 tools/version_registry.py verify --worktree` confirms every completed version is still
   byte-for-byte identical to its record.

**Enforcement.**
- Claude Code hook: blocks writes, edits, new files, renames, deletions and emptying inside completed
  versions (by Edit/Write, shell redirection, `cp`/`mv`/`tee`/`sed -i`/`dd`/`chmod`, inline code with a
  literal path); blocks non-read-only commands run from inside a completed version folder; blocks build tools
  (LaTeX, make, pandoc, zip, ...) pointed at a completed version; blocks running scripts that live inside a
  completed version or archive (reproduce them in a read-only worktree: `tools/open_version.sh`); blocks
  direct writes to the registry and validates every Edit/Write of it.
- Git hooks and CI (`research_guard.py` R9): any added/modified/deleted/renamed path inside a completed
  version at the BASE is refused; registry changes must follow the rules (no entry removed, completed entries
  unchanged and never ACTIVE again, families fixed, next number = max + 1, ACTIVE entries only for new
  paths); every completed entry is verified against its Git hash at the checked commit. Protection is read
  from the base revision, so a change cannot unprotect what it touches.
- Owner-only OS immutability: `sh tools/owner_lock_completed.sh` prints (`--apply` runs, with sudo)
  `chflags -R schg` (macOS) or `chattr -R +i` (Linux) for every completed version folder. This is the only
  layer that makes modification physically impossible; it needs root to undo.

**Limits.** Programs that compute paths at run time, and tools started from outside a completed folder that
write into it without naming it, can change files on disk before a commit; the commit check and
`verify --worktree` then report it, and Git holds the original. Untracked build leftovers (LaTeX `.aux`,
`.log`) in old folders are not part of a version. Not yet classified (owner to decide): `THESIS/`,
`notebooks/`, presentations, root-level scripts outside the policy locks.

## 7. Verification

`python3 -m pytest -q tests/test_deletion_guard.py tests/test_completed_versions.py tests/test_research_memory.py`
(results in CHANGELOG 2026-10-20). Write scenarios use only disposable repositories under the temporary
directory, so no project file is touched.
