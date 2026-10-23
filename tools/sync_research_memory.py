"""
One fast, deterministic maintenance pass for AC-MOT, shared by Claude Code, Codex and any
other agent. Run it ONCE, at the end of a task, after the requested work is finished:

  python3 tools/sync_research_memory.py --changed-only   # default: act only on what changed
  python3 tools/sync_research_memory.py --dry-run        # print the plan, write nothing
  python3 tools/sync_research_memory.py --full           # every step, all protection tests, graph queries
  python3 tools/sync_research_memory.py --base REF       # also count changes committed since REF

Steps (each one is skipped when nothing relevant changed):
  1. code inventory   tools/build_code_inventory.py      only if a .py changed and the inventory is stale
  2. registry view    research/context/VERSION_REGISTRY.md, only if it no longer matches the registry
  3. context facts    tools/update_project_context.py    only if tracked project files changed
  4. graph            tools/build_context_graph.py       only if graph-relevant files are newer than the graph
  5. validation       registry verify, research_guard --worktree, context_health_check, and only the
                      tests that match the change (the three protection suites run only when guards,
                      hooks, settings, versioning or the maintenance tools themselves changed)

A state that already passed is remembered (outputs/.sync_research_memory.json, git-ignored), so a
second run with no new change does nothing. The command never creates, completes or freezes a
version, never commits or pushes, never removes anything, and never edits hand-written records
(DECISIONS, PAPERS, RESULTS_CANONICAL, CHANGELOG ...); it only warns when one looks missing.
Exit code 0 = PASS, 1 = a validation step failed.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import research_guard as RG  # noqa: E402  (path patterns only; nothing runs on import)
import version_registry as VR  # noqa: E402

STATE = ROOT / "outputs" / ".sync_research_memory.json"
GRAPH = ROOT / "graphify-out" / "graph.json"
CHANGELOG = "research/context/CHANGELOG.md"
# Written by the maintenance tools themselves; a change here alone is not new work.
GENERATED = {"research/context/GIT_STATE.md", "research/context/CODE_INVENTORY.md",
             "research/context/VERSION_REGISTRY.md"}
# Owner-held paths agents never touch (D-034 trust root, Codex rules); never "work".
OWNER_HELD = (".github/owner_keys/", "tools/codex/")
# Manuscript/thesis folders: wording and builds, not graph or inventory input.
MANUSCRIPT_ROOTS = ("JAIS_PAPERS/", "THESIS/")
NOT_GRAPH = ("outputs/", "weights/", "legacy/", "versions/", "notebooks/", "figures/", "scripts/",
             "graphify-out/")
GRAPH_EXT = {".py", ".sh", ".json", ".md", ".yml", ".yaml", ".txt"}
PROTECTION_TESTS = ["tests/test_deletion_guard.py", "tests/test_completed_versions.py",
                    "tests/test_research_memory.py"]
# Changes that justify the protection suites (guards, hooks, permissions, versioning, CI).
PROTECTION_PATHS = RG.PROTECTION + [".claude/*", ".github/rulesets/*", ".github/workflows/*",
                                    "tools/open_version.sh", "tools/owner_lock_completed.sh"]
# Changes to the memory tooling: test_research_memory.py covers them.
MEMORY_TOOLS = ["tools/sync_research_memory.py", "tools/build_code_inventory.py",
                "tools/update_project_context.py", "tools/context_health_check.py",
                "tools/build_context_graph.py"]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def changed_paths(base: str | None) -> dict[str, str]:
    """{path: status} for uncommitted changes (tracked + untracked, not ignored) and, with base,
    for changes committed since base."""
    out: dict[str, str] = {}
    raw = git("status", "--porcelain=v1", "-z", "--untracked-files=all").split("\0")
    i = 0
    while i < len(raw):
        rec = raw[i]
        i += 1
        if len(rec) < 4:
            continue
        status, path = rec[:2], rec[3:]
        if "R" in status or "C" in status:
            i += 1  # the original path follows a rename/copy record
        out[path] = "??" if status == "??" else status.strip() or "M"
    if base:
        for path in git("diff", "--name-only", f"{base}", "HEAD").splitlines():
            out.setdefault(path, "C")  # committed since base
    return out


def fingerprint(paths: dict[str, str]) -> str:
    h = hashlib.sha256(git("rev-parse", "HEAD").strip().encode())
    for p in sorted(paths):
        f = ROOT / p
        h.update(f"{p}\0{paths[p]}\0".encode())
        if f.is_file():
            h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest()


def run(cmd: list[str], timeout: int = 900) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip()


def line(tag: str, step: str, msg: str) -> None:
    print(f"[{tag:<4}] {step:<14} {msg}")


def tail(text: str, n: int = 15) -> None:
    for t in text.splitlines()[-n:]:
        print(f"         {t}")


def graph_python() -> str | None:
    p = ROOT / "graphify-out" / ".graphify_python"
    if p.exists() and Path(p.read_text().strip()).exists():
        return p.read_text().strip()
    alt = Path.home() / ".local/share/uv/tools/graphifyy/bin/python"
    return str(alt) if alt.exists() else None


def graph_relevant(path: str) -> bool:
    if path.startswith(MANUSCRIPT_ROOTS) or path.startswith(NOT_GRAPH):
        return False
    return Path(path).suffix in GRAPH_EXT or path in ("AGENTS.md", "CLAUDE.md")


def unregistered_versions(reg: dict) -> list[str]:
    """Version folders on disk that match a registry family pattern but have no entry."""
    missing = []
    for name, fam in reg.get("families", {}).items():
        if fam.get("kind") != "version_dir" or not fam.get("root") or not fam.get("pattern"):
            continue
        rx = re.compile("^" + re.escape(fam["pattern"]).replace(r"\{n\}", r"(\d+)") + "$")
        known = {e.get("version") for e in reg["entries"] if e.get("family") == name}
        root = ROOT / fam["root"]
        if not root.is_dir():
            continue
        for d in sorted(root.iterdir()):
            m = rx.match(d.name)
            if d.is_dir() and m and int(m.group(1)) not in known:
                missing.append(f"{fam['root']}/{d.name} ({name}/V{m.group(1)})")
    return missing


def tests_for(paths: list[str], full: bool) -> list[str]:
    if full:
        return list(PROTECTION_TESTS)
    sel: list[str] = []
    if any(RG.match(p, PROTECTION_PATHS) for p in paths):
        sel += PROTECTION_TESTS
    elif any(p in MEMORY_TOOLS for p in paths):
        sel.append("tests/test_research_memory.py")
    tests_dir = ROOT / "tests"
    for p in paths:
        if p.startswith("tests/") and p.endswith(".py") and (ROOT / p).is_file():
            sel.append(p)
        elif p.endswith(".py") and not p.startswith(MANUSCRIPT_ROOTS) and (ROOT / p).is_file():
            stem = Path(p).stem
            own = tests_dir / f"test_{stem}.py"
            if own.is_file():
                sel.append(f"tests/{own.name}")
            rx = re.compile(rf"(^|\n)\s*(from|import)\s+[\w.]*\b{re.escape(stem)}\b")
            for t in sorted(tests_dir.glob("test_*.py")):
                if rx.search(t.read_text(encoding="utf-8", errors="ignore")):
                    sel.append(f"tests/{t.name}")
    return list(dict.fromkeys(sel))


def main() -> int:
    argv = sys.argv[1:]
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    full, dry = "--full" in argv, "--dry-run" in argv
    base = argv[argv.index("--base") + 1] if "--base" in argv else None
    t0 = time.time()

    paths = {p: s for p, s in changed_paths(base).items() if not p.startswith(OWNER_HELD)}
    work = {p: s for p, s in paths.items() if p not in GENERATED}
    fp = fingerprint(paths)
    try:
        last = json.loads(STATE.read_text()) if STATE.exists() else {}
    except (OSError, ValueError):
        last = {}
    if not full and last.get("fingerprint") == fp:
        print(f"sync: nothing changed since the last passing sync ({last.get('when', '?')}); nothing to do")
        return 0
    py = [p for p in work if p.endswith(".py") and not p.startswith(MANUSCRIPT_ROOTS)]
    manus = sorted({p.split("/")[0] + "/" + p.split("/")[1] for p in work
                    if p.startswith(MANUSCRIPT_ROOTS) and p.count("/") >= 1})
    print(f"sync: {len(work)} changed path(s): {len(py)} code, "
          f"{sum(p.startswith('research/') for p in work)} research, {len(manus)} manuscript folder(s)"
          + (" [dry run]" if dry else ""))
    if not work and not full:
        print("sync: no changes; nothing to do")
        return 0

    # 1. code inventory
    if py or full:
        rc, out = run([sys.executable, "tools/build_code_inventory.py", "--check"])
        if rc == 0:
            line("ok", "inventory", "up to date")
        elif dry:
            line("plan", "inventory", "would regenerate")
        else:
            rc, out = run([sys.executable, "tools/build_code_inventory.py"])
            line("done" if rc == 0 else "FAIL", "inventory", "regenerated" if rc == 0 else "failed")
            if rc:
                tail(out)
        untracked = [p for p in py if paths[p] == "??"]
        if untracked:
            line("note", "inventory", f"{len(untracked)} new untracked .py file(s) enter it after `git add`")
    else:
        line("skip", "inventory", "no code change")

    # 2. registry view
    reg = VR.load(None)
    md = ROOT / VR.MD_REL
    if md.exists() and md.read_text(encoding="utf-8") == VR.render(reg):
        line("ok", "registry view", "up to date")
    elif dry:
        line("plan", "registry view", "would re-render VERSION_REGISTRY.md")
    else:
        md.write_text(VR.render(reg), encoding="utf-8")
        line("done", "registry view", "re-rendered VERSION_REGISTRY.md")

    # 3. context facts (PROJECT_STATE auto block + GIT_STATE.md)
    if dry:
        line("plan", "context facts", "would refresh PROJECT_STATE auto block and GIT_STATE.md")
    else:
        rc, out = run([sys.executable, "tools/update_project_context.py"])
        line("done" if rc == 0 else "FAIL", "context facts", "refreshed" if rc == 0 else "failed")
        if rc:
            tail(out)

    # 4. graph (local, git-ignored; deterministic, no LLM)
    gpy = graph_python()
    rel = [p for p in work if graph_relevant(p)]
    stamp = GRAPH.stat().st_mtime if GRAPH.exists() else 0.0
    newer = [p for p in rel if not (ROOT / p).exists() or (ROOT / p).stat().st_mtime > stamp]
    if not gpy:
        line("skip", "graph", "Graphify not installed here")
    elif not (full or newer or not GRAPH.exists()):
        line("skip", "graph", "up to date" if rel else "no graph-relevant change")
    elif dry:
        line("plan", "graph", f"would rebuild ({len(newer)} newer file(s))")
    else:
        rc, out = run([gpy, "tools/build_context_graph.py"])
        line("done" if rc == 0 else "FAIL", "graph", "rebuilt" if rc == 0 else "rebuild failed")
        if rc:
            tail(out)

    if dry:
        tests = tests_for(list(work), full)
        line("plan", "tests", ", ".join(Path(t).stem for t in tests) or "none needed")
        return 0

    # 5. validation, once
    fails = 0
    rc, out = run([sys.executable, "tools/version_registry.py", "verify", "--worktree"])
    line("pass" if rc == 0 else "FAIL", "registry", out.splitlines()[-1] if out else "")
    if rc:
        fails += 1
        tail(out)
    rc, out = run([sys.executable, "tools/research_guard.py", "--worktree"])
    bad = [t for t in out.splitlines() if t.startswith("[FAIL")]
    line("pass" if rc == 0 else "FAIL", "guard", "preservation rules hold" if rc == 0 else f"{len(bad)} violation(s)")
    if rc:
        fails += 1
        tail("\n".join(bad) or out)
    hc = [sys.executable, "tools/context_health_check.py"] + ([] if full else ["--no-graphify"])
    rc, out = run(hc)
    summary = next((t for t in reversed(out.splitlines()) if t.startswith("SUMMARY")), out[-200:])
    line("pass" if rc == 0 else "FAIL", "health", summary.replace("SUMMARY: ", ""))
    for t in out.splitlines():
        if t.startswith("[FAIL]") or (rc and t.startswith("[WARN]")):
            print(f"         {t}")
    fails += rc != 0
    tests = tests_for(list(work), full)
    if tests:
        rc, out = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *tests], timeout=3600)
        last_line = out.splitlines()[-1] if out else ""
        line("pass" if rc == 0 else "FAIL", "tests", f"{len(tests)} file(s): {last_line}")
        if rc:
            fails += 1
            tail(out, 25)
    else:
        line("skip", "tests", "no code, guard or versioning change")

    # reminders (never written automatically)
    for m in unregistered_versions(reg):
        line("warn", "version", f"not in the registry: {m}")
    if any(RG.match(p, RG.RESEARCH_PATHS) for p in work) and CHANGELOG not in paths:
        line("warn", "changelog", f"research files changed but {CHANGELOG} has no new line")
    head = {e["id"] for e in VR.load("HEAD").get("entries", [])}
    new = [f"{e['id']} {e.get('status')}" for e in reg["entries"] if e["id"] not in head]
    if new:
        print(f"new versions (uncommitted): {', '.join(new)}")

    ok = fails == 0
    if ok:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps({"fingerprint": fingerprint(
                                         {p: s for p, s in changed_paths(base).items() if not p.startswith(OWNER_HELD)}),
                                     "when": time.strftime("%Y-%m-%d %H:%M")}), encoding="utf-8")
    print(f"SYNC: {'PASS' if ok else 'FAIL'} ({time.time() - t0:.0f}s)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
