"""
Research guard: enforce the AC-MOT owner-only-delete policy and the version-preserving
rules of the research record (research/context/PRESERVATION_POLICY.md).

It never edits files and never creates commits. It reads git and prints a report;
the exit code is 1 when a rule is violated. Used by the git hooks (.githooks/), by CI
(.github/workflows/research_guard.yml) and by the Claude Code hooks (.claude/settings.json).

  python3 tools/research_guard.py --staged                      # pre-commit (never accepts approvals)
  python3 tools/research_guard.py --range A B                   # CI: commits A..B
  python3 tools/research_guard.py --push-refs < refs            # pre-push (stdin from git)
  python3 tools/research_guard.py --worktree [--stop-hook]      # uncommitted tracked changes
  python3 tools/research_guard.py --session-brief               # Claude SessionStart

Rules
  R0 no deletion: a tracked file is never deleted, renamed/moved or emptied (disguised
     deletion) without the owner's approval for THAT path. Checked per commit in CI.
  R1 frozen code: every file in an active policy lock keeps its locked sha256.
  R2 immutable artifacts: committed results, evidence, locks, frozen configs and
     manuscripts are not modified (new files are allowed).
  R3 version folders: an existing manuscript version folder gets no new files;
     a revision is a NEW folder (for example Paper2_V12 next to Paper2_V11).
  R4 append-only records: no line is removed from the decision, failure, changelog,
     protocol and experiment-registry files.
  R5 documentation coupling: code/config/result/manuscript changes come with a
     CHANGELOG entry; a new manuscript version with PAPERS.md; new result files with
     EXPERIMENT_REGISTRY or RESULTS_CANONICAL; Python changes with a current CODE_INVENTORY.
  R6 untracked local files are never inspected or reported.
  R7 protection files (this guard, the hooks, the Claude settings, the CI workflow,
     the owner keys, the policy) are not changed without the owner's approval.
  R8 refs: no remote branch/tag deletion, no tag move, no non-fast-forward push.

Ordinary creation and editing need no approval. Owner approval = an authenticated,
path-specific statement: a git trailer naming the target (R0: "Owner-Approved-Delete:
<path or directory/> [| reason]"; R1/R2/R4/R7: the same with "-Change") inside a commit
that carries a VALID SIGNATURE by an owner key stored in .github/owner_keys/ (public GPG
keys *.asc and/or an SSH allowed_signers file) at the BASE of the checked range. The
trailer alone is never approval. Fail closed: with no owner key at the base, an unsigned
commit, a foreign key or an unverifiable signature, the trailer is ignored and the
deletion fails. Local hooks (--staged) see no signature and therefore never accept an
approval; CI and pre-push (--range / --push-refs) verify. One trailer approves one
target, in its own commit only. R8 has no trailer: the owner changes refs from their
own terminal or the GitHub web interface.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = "research/context/"

# Policy locks whose files must match exactly in the working tree (R1).
# Older locks (V1-V4 era) are verified against their own tags by the tests.
ACTIVE_LOCKS = ["research/V7_POLICY_LOCK.json", "research/V6TF_POLICY_LOCK.json",
                "research/GENERAL_ACMOT_G1_LOCK.json"]

# R2: existing files under these patterns are immutable.
IMMUTABLE = [
    "research/final/*", "research/acmot_paper_v2/*", "research/paper_split/evidence/*",
    "research/transfer_legacy/*", "research/published_papers/*", "research/cue_audit/*",
    "research/uavdt_protocol/*", "JAIS_PAPERS/PAPER*", "JAIS_PAPERS/overleaf/*",
    "research/*LOCK*.json", "research/TRAIN_SPLIT_V5.json",
    "configs/universal_acmot_policy*.json", "configs/general_acmot_g1.json",
    "configs/g2_gsci_frozen.json",
]

# R3: each direct child folder of these roots is one manuscript version.
VERSION_ROOTS = ["JAIS_PAPERS", "research/acmot_paper_v2/Paper1_JAIS",
                 "research/acmot_paper_v2/Paper1_Springer_Template", "research/acmot_paper_v2"]
VERSION_DIR_RE = re.compile(r"^(PAPER\d|Paper\d|manuscript_)")

# R7: protection mechanism files.
PROTECTION = ["tools/research_guard.py", "tools/claude_tool_guard.py", ".githooks/*",
              ".claude/settings.json", ".github/workflows/research_guard.yml",
              "tools/install_git_hooks.sh", "research/context/PRESERVATION_POLICY.md",
              "tools/version_registry.py",
              ".github/owner_keys/*", "tools/codex/*"]
DELETE_TRAILER = re.compile(r"^Owner-Approved-Delete:[ \t]*(.+)$", re.M | re.I)
CHANGE_TRAILER = re.compile(r"^Owner-Approved-Change:[ \t]*(.+)$", re.M | re.I)
# R9: a SEPARATE approval for changing a completed version (a delete approval never covers it).
COMPLETED_TRAILER = re.compile(r"^Owner-Approved-Completed-Change:[ \t]*(.+)$", re.M | re.I)
OWNER_KEYS = ".github/owner_keys"
ZERO = "0" * 40
SHRINK_MIN, SHRINK_RATIO = 200, 0.05  # emptying = >=200 bytes cut to <5%

# R4: append-only records.
APPEND_ONLY = [CTX + "DECISIONS.md", CTX + "FAILED_EXPERIMENTS.md", CTX + "CHANGELOG.md",
               CTX + "EXPERIMENT_REGISTRY.md", "research/OPTIMIZATION_PROTOCOL.md",
               "research/EXPERIMENT_REGISTRY.md"]

# R5: paths whose change needs a CHANGELOG entry.
RESEARCH_PATHS = ["*.py", "adapters/*", "tools/*", "configs/*", "research/final/*",
                  "research/acmot_paper_v2/*", "JAIS_PAPERS/*", "research/published_papers/*",
                  "THESIS/*", "notebooks/*", ".github/workflows/*", ".githooks/*",
                  ".claude/settings.json"]
RESULT_PATTERNS = ["research/final/*", "research/acmot_paper_v2/*_RESULT*.json"]


def git(*args: str, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def match(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, p) for p in patterns)


def version_folder(path: str) -> str | None:
    """Manuscript version folder that contains `path`, if any (deepest root wins)."""
    for root in sorted(VERSION_ROOTS, key=len, reverse=True):
        if path.startswith(root + "/"):
            child = path[len(root) + 1:].split("/", 1)
            if len(child) == 2 and VERSION_DIR_RE.match(child[0]):
                return f"{root}/{child[0]}"
            return None
    return None


# ---------------------------------------------------------------- pure core
def parse_approvals(text: str) -> dict[str, set[str]]:
    """Owner trailers -> {"delete": paths, "change": paths}. Value: path [| reason]."""
    def paths(rx):
        return {m.split("|", 1)[0].strip().strip("`'\"") for m in rx.findall(text or "")} - {""}
    return {"delete": paths(DELETE_TRAILER), "change": paths(CHANGE_TRAILER),
            "completed": paths(COMPLETED_TRAILER)}


def approved(path: str, targets: set[str]) -> bool:
    """Exact path, or a directory target written with a trailing slash."""
    return any(path == t or (t.endswith("/") and (path.startswith(t) or path + "/" == t)) for t in targets)


def evaluate(changes: list[tuple[str, str, str | None]], removed: dict[str, int],
             base_dirs: set[str], lock_failures: list[str], inventory_ok: bool | None,
             approvals: dict[str, set[str]] | None = None, shrunk: list[str] | None = None,
             check_r0: bool = True, reg: dict | None = None) -> list[tuple[str, str]]:
    """changes: (status letter, path, old path for renames). removed: lines removed per
    append-only file. base_dirs: version folders that already exist at the base.
    lock_failures: "path (LOCK)" strings. shrunk: modified paths emptied to <5%.
    reg: completed-version context (registry_context): rule(path) -> message for paths
    inside completed versions at the base, editable(path) for registered ACTIVE versions,
    violations of the registry change, and byte-for-byte verification failures.
    Returns (level, message) pairs; level is FAIL, WARN or PASS."""
    ap = {"delete": set(), "change": set(), "completed": set(), **(approvals or {})}
    out: list[tuple[str, str]] = []
    rule = (reg or {}).get("rule") or (lambda p: None)
    editable = (reg or {}).get("editable") or (lambda p: False)
    for path, msg in (reg or {}).get("violations", []):
        out.append(("FAIL", msg)) if not approved(path, ap["completed"]) else \
            out.append(("WARN", f"{msg} -- approved by the owner (completed: {path})"))
    for msg in (reg or {}).get("verify", []):
        out.append(("FAIL", f"R9 completed version not byte-for-byte identical to its record: {msg}"))
    for st, path, old in changes:
        for p in [x for x in (path, old) if x]:
            m = rule(p)
            if m:
                verb = {"A": "added inside", "M": "modified in", "T": "modified in", "D": "deleted from",
                        "R": "renamed/moved out of", "C": "copied into"}.get(st[0], "changed in")
                (out.append(("WARN", f"R9 {p} {verb} {m} -- approved by the owner (completed: {p})"))
                 if approved(p, ap["completed"]) else
                 out.append(("FAIL", f"R9 {p} {verb} {m}; completed versions are read-only — create the next "
                                     "version with: python3 tools/version_registry.py new <family>")))

    def gate(kind: str, path: str, msg: str) -> None:
        if editable(path) and kind == "change" and msg.startswith(("R2", "R3")):
            return  # registered ACTIVE version: normal editing
        if approved(path, ap[kind]):
            out.append(("WARN", f"{msg} -- approved by the owner ({kind}: {path})"))
        else:
            out.append(("FAIL", msg))

    if check_r0:
        for st, path, old in changes:
            if st[0] == "D":
                gate("delete", path, f"R0 deletion needs the owner's approval: {path}")
            elif st[0] == "R":
                gate("delete", old, f"R0 rename/move removes {old} (-> {path}); needs the owner's approval")
        for path in shrunk or []:
            gate("delete", path, f"R0 file emptied (disguised deletion) needs the owner's approval: {path}")
    for st, path, old in changes:
        if st[0] in "ACMT" and match(path, [OWNER_KEYS + "/*"]) and path.endswith((".asc", ".gpg", "allowed_signers")):
            gate("change", path, f"R7 trusted owner-key file added/changed: {path} (needs approval signed by an "
                                 "already trusted owner key; the first key is set up by the owner, see policy 4.3)")
        elif st[0] in "MT" and match(path, PROTECTION):
            gate("change", path, f"R7 protection file changed without the owner's approval: {path}")
    for f in lock_failures:
        gate("change", f.split(" (")[0], f"R1 frozen file differs from its policy lock: {f}")
    touched = {p for _, p, _ in changes} | {o for _, _, o in changes if o}
    for st, path, old in changes:
        if st[0] in "MT" and match(path, IMMUTABLE):
            gate("change", path, f"R2 immutable artifact modified (create a new version instead): {path}")
        vf = version_folder(path)
        if vf and vf in base_dirs and st[0] == "A" and not editable(path):
            out.append(("FAIL", f"R3 file added inside existing version folder {vf}: {path} "
                                "(create a new version folder instead)"))
    for f, n in removed.items():
        if n:
            gate("change", f, f"R4 append-only record lost {n} line(s): {f} (append a dated correction instead)")
    research = [p for st, p, _ in changes if match(p, RESEARCH_PATHS) and not p.startswith(CTX)]
    if research and CTX + "CHANGELOG.md" not in touched:
        out.append(("FAIL", f"R5 research change without a CHANGELOG.md entry: {research[:4]}"))
    new_versions = sorted({version_folder(p) for st, p, _ in changes
                           if st[0] == "A" and version_folder(p) and version_folder(p) not in base_dirs})
    if new_versions and not ({CTX + "PAPERS.md", "research/VERSION_REGISTRY.json"} & touched):
        out.append(("FAIL", f"R5 new manuscript version without a PAPERS.md update: {new_versions}"))
    new_results = [p for st, p, _ in changes if st[0] == "A" and match(p, RESULT_PATTERNS)]
    if new_results and not ({CTX + "EXPERIMENT_REGISTRY.md", CTX + "RESULTS_CANONICAL.md"} & touched):
        out.append(("FAIL", f"R5 new result files without a registry/results update: {new_results[:4]}"))
    if inventory_ok is False:
        out.append(("FAIL", "R5 Python code changed but research/context/CODE_INVENTORY.md is stale "
                            "(run python3 tools/build_code_inventory.py)"))
    if not [x for x in out if x[0] != "PASS"]:
        out.append(("PASS", f"{len(changes)} changed path(s) follow the preservation rules"))
    return out


def push_ref_report(lines: list[str], is_ancestor, exists) -> list[tuple[str, str]]:
    """R8 for pre-push stdin lines '<local ref> <local sha> <remote ref> <remote sha>'."""
    out = []
    for line in lines:
        parts = line.split()
        if len(parts) != 4:
            continue
        lref, lsha, rref, rsha = parts
        if lsha == ZERO:
            out.append(("FAIL", f"R8 deleting remote ref {rref} needs the owner (owner pushes it with --no-verify)"))
        elif rsha != ZERO and rref.startswith("refs/tags/") and rsha != lsha:
            out.append(("FAIL", f"R8 moving existing tag {rref} is not allowed"))
        elif rsha != ZERO and not rref.startswith("refs/tags/"):
            if not exists(rsha):
                out.append(("WARN", f"R8 remote {rref} is at an unknown commit {rsha[:9]}; fetch first"))
            elif not is_ancestor(rsha, lsha):
                out.append(("FAIL", f"R8 non-fast-forward (history-rewriting) push to {rref}"))
    return out


# ---------------------------------------------------------------- git readers
def parse_name_status(text: str) -> list[tuple[str, str, str | None]]:
    rows = []
    for line in text.splitlines():
        parts = line.split("\t")
        if not parts or not parts[0]:
            continue
        st = parts[0]
        if st[0] in "RC" and len(parts) == 3:
            rows.append((st, parts[2], parts[1]))
        elif len(parts) >= 2:
            rows.append((st, parts[1], None))
    return rows


def removed_lines(diff_args: list[str], files: list[str]) -> dict[str, int]:
    out = {}
    for f in files:
        d = git("diff", "-U0", *diff_args, "--", f, check=False)
        out[f] = sum(1 for l in d.splitlines() if l.startswith("-") and not l.startswith("---"))
    return out


def existing_version_dirs(ref: str | None) -> set[str]:
    dirs = set()
    for root in VERSION_ROOTS:
        if ref:
            listing = git("ls-tree", "-d", "--name-only", f"{ref}:{root}", check=False).split()
        else:
            p = ROOT / root
            listing = [x.name for x in p.iterdir() if x.is_dir()] if p.is_dir() else []
        dirs |= {f"{root}/{d}" for d in listing if VERSION_DIR_RE.match(d)}
    return dirs


def lock_check(ref: str | None) -> list[str]:
    fails = []
    for lock in ACTIVE_LOCKS:
        try:
            text = git("show", f"{ref}:{lock}") if ref else (ROOT / lock).read_text()
        except (RuntimeError, OSError):
            continue  # lock does not exist at this revision
        for path, sha in json.loads(text).get("file_sha256", {}).items():
            if ref:
                blob = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT,
                                      capture_output=True).stdout
            else:
                fp = ROOT / path
                blob = fp.read_bytes() if fp.exists() else b""
            if hashlib.sha256(blob).hexdigest() != sha:
                fails.append(f"{path} ({Path(lock).name})")
    return fails


def inventory_status(changes) -> bool | None:
    if not any(p.endswith(".py") for _, p, _ in changes):
        return None
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "build_code_inventory.py"), "--check"],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0


def owner_key_setup(ref: str, home: Path) -> list[str] | None:
    """git -c options that verify signatures against the owner keys stored at `ref`.
    None when no owner key is configured at that revision."""
    # Trust root 1 (preferred): the ACMOT_OWNER_KEYS value that CI takes from a GitHub
    # repository variable, which only a repository admin can set. When present, key files
    # in the repository are ignored. Trust root 2: key files at the base revision.
    env_keys = os.environ.get("ACMOT_OWNER_KEYS", "").strip()
    if env_keys:
        sources = [("env.asc" if "BEGIN PGP PUBLIC KEY" in env_keys else "allowed_signers",
                    env_keys.encode() + b"\n")]
    else:
        names = [n for n in git("ls-tree", "--name-only", f"{ref}:{OWNER_KEYS}", check=False).split()
                 if n.endswith((".asc", ".gpg")) or n == "allowed_signers"]
        sources = [(n, subprocess.run(["git", "show", f"{ref}:{OWNER_KEYS}/{n}"], cwd=ROOT,
                                      capture_output=True).stdout) for n in names]
    if not sources:
        return None
    opts: list[str] = []
    gnupg = home / "gnupg"
    gnupg.mkdir(mode=0o700, parents=True, exist_ok=True)
    for n, blob in sources:
        if n.endswith((".asc", ".gpg")):
            subprocess.run(["gpg", "--batch", "--quiet", "--homedir", str(gnupg), "--import"],
                           input=blob, capture_output=True)
        elif n == "allowed_signers":
            (home / "allowed_signers").write_bytes(blob)
            opts += ["-c", f"gpg.ssh.allowedSignersFile={home / 'allowed_signers'}"]
    os.environ["GNUPGHOME"] = str(gnupg)
    return opts


def commit_signed_by_owner(commit: str, opts: list[str]) -> bool:
    r = subprocess.run(["git", *opts, "log", "-1", "--format=%G?", commit], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout.strip() in ("G", "U")  # U: good signature, key not ultimately trusted


def range_commits(a: str, b: str) -> list[str]:
    return git("rev-list", "--reverse", "--no-merges", f"{a}..{b}", check=False).split()


def commit_message(c: str) -> str:
    return git("log", "-1", "--format=%B", c, check=False)


def range_approvals(a: str, b: str) -> tuple[dict[str, dict[str, set[str]]], list[tuple[str, str]]]:
    """Per-commit owner approvals in a..b. A trailer counts ONLY when its commit carries a
    valid signature by an owner key stored at the base `a`. Fail closed: no key configured,
    no signature, a foreign key or an unverifiable signature -> the trailer is ignored."""
    import tempfile
    notes: list[tuple[str, str]] = []
    per: dict[str, dict[str, set[str]]] = {}
    with tempfile.TemporaryDirectory(prefix="acmot_keys_") as tmp:
        opts = owner_key_setup(a, Path(tmp))
        for c in range_commits(a, b):
            ap = parse_approvals(commit_message(c))
            if not (ap["delete"] or ap["change"]):
                continue
            if opts is None:
                notes.append(("FAIL", f"approval trailer in {c[:9]} ignored: no owner key in {OWNER_KEYS}/ "
                                      "at the base, so owner approval cannot be verified"))
                continue
            if not commit_signed_by_owner(c, opts):
                notes.append(("FAIL", f"approval trailer in {c[:9]} ignored: commit not signed by an owner key"))
                continue
            per[c] = ap
    return per, notes


def union(per: dict[str, dict[str, set[str]]]) -> dict[str, set[str]]:
    u = {"delete": set(), "change": set(), "completed": set()}
    for ap in per.values():
        for k in u:
            u[k] |= ap.get(k, set())
    return u


def registry_context(base_ref: str, new_ref: str | None) -> dict:
    """Completed-version context for evaluate(). new_ref: a commit, ":" (the index) or
    None (the working tree). Protection comes from the registry at the BASE, so a change
    cannot unprotect the versions it touches."""
    import version_registry as VR
    verify_ref, worktree = new_ref, False
    if new_ref == ":":
        verify_ref = git("write-tree", check=False).strip() or "HEAD"  # tree of the index (no ref changes)
    elif new_ref is None:
        verify_ref, worktree = "HEAD", True
    base = VR.load(base_ref)
    new = VR.load(None) if new_ref is None else VR.load(verify_ref)
    base_ids = {e["id"] for e in base.get("entries", [])}

    def rule(p: str) -> str | None:
        c = VR.classify(p, [base])
        if c and c[0] in ("sealed", "existing", "lock"):
            e = c[1]
            return f"{e.get('status')} {e.get('kind')} {e['id']}"
        return None

    def editable(p: str) -> bool:
        c = VR.classify(p, [new])
        return bool(c and c[0] == "active" and (c[1]["id"] in base_ids or not VR.exists_at(base_ref, c[1]["path"])))

    violations = []
    if VR.dump(base) != VR.dump(new):
        violations = VR.check_change(base, new, lambda p: VR.exists_at(base_ref, p), base_ref)
    return {"rule": rule, "editable": editable, "violations": violations,
            "verify": VR.verify(new, verify_ref, worktree)}


def r0_per_commit(a: str, b: str, per: dict[str, dict[str, set[str]]]) -> list[tuple[str, str]]:
    """R0 for each non-merge commit with that commit's own approvals."""
    out = []
    for c in range_commits(a, b):
        ns = git("diff-tree", "-r", "--no-commit-id", "--name-status", "-M", f"{c}^", c, check=False)
        rows = [r for r in parse_name_status(ns) if r[0][0] in "DR"]
        shr = shrunk_paths(parse_name_status(ns), f"{c}^", c)
        if not rows and not shr:
            continue
        rep = evaluate(rows, {}, set(), [], None, per.get(c), shr)
        out += [(l, f"{c[:9]}: {m}") for l, m in rep if l != "PASS" and m.startswith("R0")]
    return out


def blob_size(spec: str) -> int | None:
    r = subprocess.run(["git", "cat-file", "-s", spec], cwd=ROOT, capture_output=True, text=True)
    return int(r.stdout) if r.returncode == 0 else None


def shrunk_paths(changes, old_ref: str, new_ref: str | None) -> list[str]:
    """Modified files emptied to <5% of a >=200-byte original. new_ref None = index,
    "WORKTREE" = working tree."""
    out = []
    for st, path, _ in changes:
        if st[0] != "M":
            continue
        old = blob_size(f"{old_ref}:{path}")
        if new_ref == "WORKTREE":
            fp = ROOT / path
            new = fp.stat().st_size if fp.is_file() else 0
        else:
            new = blob_size(f"{new_ref or ''}:{path}")
        if old is not None and new is not None and old >= SHRINK_MIN and new < old * SHRINK_RATIO:
            out.append(path)
    return out


def session_brief() -> int:
    ps = (ROOT / CTX / "PROJECT_STATE.md").read_text(encoding="utf-8")
    pick = [l for l in ps.splitlines() if l.startswith(("FINAL TARGET", "CURRENT RESEARCH VERSION",
                                                       "CURRENT PHASE"))]
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    dirty = [l for l in git("status", "--porcelain", "--untracked-files=no").splitlines()]
    print("AC-MOT research record (read research/context/README.md before substantive work).")
    print(f"Branch {branch}; {len(dirty)} uncommitted tracked change(s).")
    for l in pick:
        print(l[:220])
    print("Rules: create/edit normally; NEVER delete, rename, move or empty an existing file, dir, "
          "branch or tag without the owner's explicit approval for that exact target "
          "(research/context/PRESERVATION_POLICY.md); never modify frozen V7f code, results, locks or "
          "existing manuscript versions (new work = new version folder); update research/context + "
          "CHANGELOG; push only with the owner's approval.")
    fails = lock_check(None)
    print("Frozen-file locks: " + ("intact" if not fails else f"CHANGED {fails}"))
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if "--session-brief" in argv:
        return session_brief()
    quiet = "--quiet" in argv
    if "--push-refs" in argv:
        lines = [l for l in sys.stdin.read().splitlines() if l.strip()]
        anc = lambda x, y: subprocess.run(["git", "merge-base", "--is-ancestor", x, y], cwd=ROOT).returncode == 0  # noqa: E731
        has = lambda x: subprocess.run(["git", "cat-file", "-e", f"{x}^{{commit}}"], cwd=ROOT,  # noqa: E731
                                       capture_output=True).returncode == 0
        report = push_ref_report(lines, anc, has)
        for _, lsha, rref, rsha in [l.split() for l in lines if len(l.split()) == 4]:
            if lsha == ZERO or rref.startswith("refs/tags/"):
                continue
            if rsha == ZERO or not has(rsha):
                base = git("merge-base", lsha, "origin/HEAD", check=False).strip() or \
                    git("rev-list", "--max-parents=0", lsha).split()[-1]
            else:
                base = rsha
            report += range_report(base, lsha)
        return emit(report, quiet)
    if "--range" in argv:
        i = argv.index("--range")
        return emit(range_report(argv[i + 1], argv[i + 2]), quiet)
    if "--staged" in argv:
        ns = git("diff", "--cached", "--name-status", "-M")
        diff_args, shr_ref, new_ref = ["--cached"], None, ":"
    else:  # --worktree (default)
        ns = git("diff", "HEAD", "--name-status", "-M")
        diff_args, shr_ref, new_ref = ["HEAD"], "WORKTREE", None
    changes = parse_name_status(ns)
    aps = [p for _, p, _ in changes if p in APPEND_ONLY]
    # Uncommitted changes carry no signature, so no approval is ever accepted here.
    report = evaluate(changes, removed_lines(diff_args, aps), existing_version_dirs("HEAD"),
                      lock_check(None), inventory_status(changes), None,
                      shrunk_paths(changes, "HEAD", shr_ref), reg=registry_context("HEAD", new_ref))
    if any(l == "FAIL" and m[:2] in ("R0", "R1", "R2", "R4", "R7", "R9") for l, m in report):
        report.append(("WARN", "local hooks cannot verify owner signatures, so they never accept an approval. "
                               "An approved change is committed by the OWNER with a signed commit "
                               "(git commit -S --no-verify) and verified by CI / pre-push against "
                               f"{OWNER_KEYS}/ (research/context/PRESERVATION_POLICY.md)"))
    if "--stop-hook" in argv:
        # Claude Code Stop hook: never blocks; shows problems to the user only.
        probs = [f"[{l}] {m}" for l, m in report if l != "PASS"]
        if probs:
            print(json.dumps({"systemMessage": "Research guard (uncommitted changes): "
                              + " | ".join(probs)[:900]}))
        return 0
    return emit(report, quiet)


def range_report(a: str, b: str) -> list[tuple[str, str]]:
    ns = git("diff", "--name-status", "-M", a, b)
    changes = parse_name_status(ns)
    aps = [p for _, p, _ in changes if p in APPEND_ONLY]
    per, notes = range_approvals(a, b)
    # The inventory can only be regenerated from a checkout of b (CI, or pre-push at HEAD).
    at_b = (git("rev-parse", "HEAD").strip() == git("rev-parse", b).strip()
            and not git("status", "--porcelain", "--untracked-files=no").strip())
    report = evaluate(changes, removed_lines([a, b], aps), existing_version_dirs(a), lock_check(b),
                      inventory_status(changes) if at_b else None, union(per), None, check_r0=False,
                      reg=registry_context(a, b))
    report = [x for x in report if x[0] != "PASS"] + r0_per_commit(a, b, per) + notes
    if not [x for x in report if x[0] == "FAIL"]:
        report.append(("PASS", f"{a[:9]}..{b[:9]}: {len(changes)} changed path(s) follow the preservation rules"))
    return report


def emit(report: list[tuple[str, str]], quiet: bool) -> int:
    for level, msg in report:
        if not (quiet and level == "PASS"):
            print(f"[{level}] {msg}")
    return 1 if any(l == "FAIL" for l, _ in report) else 0


if __name__ == "__main__":
    sys.exit(main())
