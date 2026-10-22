"""
Tests for the completed-version rule (D-035): completed versions are immutable to AI agents;
changes go into the next sequential version. Every write scenario runs in a disposable
repository under pytest's temporary directory; the real repository is only read.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import claude_tool_guard as CTG  # noqa: E402
import version_registry as VR  # noqa: E402

DEL = "Owner-Approved" + "-Delete"
CMP = "Owner-Approved" + "-Completed-Change"
FAM_ROOT, PAT = "JAIS_PAPERS", "PAPER3_TEST_rev{n}"


def vdir(n: int) -> str:
    return f"{FAM_ROOT}/{PAT.replace('{n}', str(n))}"


def run(cmd, cwd, env, ok=True, inp=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, input=inp)
    if ok:
        assert r.returncode == 0, (cmd, r.stdout, r.stderr)
    return r


def snapshot(d: Path, versions=range(1, 8)) -> dict[str, str]:
    out = {}
    for n in versions:
        for p in sorted((d / vdir(n)).rglob("*")):
            if p.is_file():
                out[str(p.relative_to(d))] = hashlib.sha256(p.read_bytes()).hexdigest()
    out["research/final/r1.json"] = hashlib.sha256((d / "research/final/r1.json").read_bytes()).hexdigest()
    return out


@pytest.fixture()
def repo(tmp_path):
    d = tmp_path / "repo"
    (d / "tools").mkdir(parents=True)
    (d / ".githooks").mkdir()
    for f in ["research_guard.py", "claude_tool_guard.py", "version_registry.py"]:
        shutil.copy(ROOT / "tools" / f, d / "tools" / f)
    for f in ["pre-commit", "commit-msg", "pre-push"]:
        shutil.copy(ROOT / ".githooks" / f, d / ".githooks" / f)
        os.chmod(d / ".githooks" / f, 0o755)
    files = {".gitignore": "__pycache__/\n*.pyc\n", "research/context/CHANGELOG.md": "# CHANGELOG\n- start\n",
             "research/context/PAPERS.md": "# P\n", "research/context/EXPERIMENT_REGISTRY.md": "# E\n",
             "research/final/r1.json": '{"hota": 61.2}\n'}
    for n in range(1, 9):
        files[f"{vdir(n)}/main.tex"] = f"\\title{{Paper version {n}}}\n" + "text\n" * 50
        files[f"{vdir(n)}/fig.pdf"] = f"%PDF-1.4 figure {n}\n" * 20
    for rel, text in files.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(text)
    env = dict(os.environ, GIT_AUTHOR_NAME="Owner", GIT_AUTHOR_EMAIL="owner@example.com",
               GIT_COMMITTER_NAME="Owner", GIT_COMMITTER_EMAIL="owner@example.com",
               GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", PYTHONDONTWRITEBYTECODE="1")
    env.pop("ACMOT" + "_OWNER_KEYS", None)
    run(["git", "init", "-q", "-b", "main"], d, env)
    run(["git", "add", "-A"], d, env)
    run(["git", "commit", "-q", "-m", "content"], d, env)
    c = run(["git", "rev-parse", "HEAD"], d, env).stdout.strip()

    def tree(p):
        return run(["git", "rev-parse", f"HEAD:{p}"], d, env).stdout.strip()

    reg = {"schema": 1,
           "families": {"paper": {"title": "test paper", "kind": "version_dir", "root": FAM_ROOT, "pattern": PAT},
                        "archives": {"title": "results", "kind": "fileset"}},
           "entries": []}
    for n in range(1, 9):
        st = "SUPERSEDED" if n < 7 else ("COMPLETED" if n == 7 else "ACTIVE")
        e = {"id": f"paper/V{n}", "family": "paper", "version": n, "label": Path(vdir(n)).name,
             "kind": "version_dir", "path": vdir(n), "status": st, "evidence": "test"}
        if n < 8:
            e.update(commit=c, tree=tree(vdir(n)))
        reg["entries"].append(e)
    reg["entries"].append({"id": "archives/research/final", "family": "archives", "version": None, "label": "final",
                           "kind": "fileset", "path": "research/final", "status": "COMPLETED", "commit": c,
                           "tree": tree("research/final"), "evidence": "test"})
    (d / VR.REG_REL).write_text(json.dumps(reg, indent=2) + "\n")
    run([sys.executable, "tools/version_registry.py", "render"], d, env)
    run(["git", "add", "-A"], d, env)
    run(["git", "commit", "-q", "--no-verify", "-m", "registry (owner bootstrap)"], d, env)
    run(["git", "config", "core.hooksPath", ".githooks"], d, env)
    return d, env


def hook(d, env, tool, inp):
    r = run([sys.executable, "tools/claude_tool_guard.py"], d, env, ok=False,
            inp=json.dumps({"tool_name": tool, "tool_input": inp, "cwd": str(d)}))
    return r.returncode


def bash(d, env, cmd):
    return hook(d, env, "Bash", {"command": cmd})


def tool(d, env, *args, ok=True):
    return run([sys.executable, "tools/version_registry.py", *args], d, env, ok=ok)


def changelog(d, line):
    p = d / "research/context/CHANGELOG.md"
    p.write_text(p.read_text() + f"- {line}\n")


def commit(d, env, msg, ok=True):
    run(["git", "add", "-A"], d, env)
    return run(["git", "commit", "-q", "-m", msg], d, env, ok=ok)


def restore(d, env):
    """Test-only cleanup of a refused attempt inside the disposable repository."""
    run(["git", "reset", "-q", "--hard", "HEAD"], d, env)
    run(["git", "clean", "-qfd"], d, env)


# ---------------------------------------------------------------- 1, 2, 8, 10
def test_active_edit_new_version_and_memory_update(repo):
    d, env = repo
    before = snapshot(d)
    v8, v9 = vdir(8), vdir(9)
    # 1 editing the ACTIVE V8 is normal work
    assert hook(d, env, "Edit", {"file_path": str(d / v8 / "main.tex"), "old_string": "text", "new_string": "Text"}) == 0
    assert hook(d, env, "Write", {"file_path": str(d / v8 / "extra.tex"), "content": "new section\n"}) == 0
    assert bash(d, env, f"sed -i 's/text/TEXT/' {v8}/main.tex") == 0
    assert bash(d, env, f"cd {v8} && pdflatex main.tex") == 0
    (d / v8 / "main.tex").write_text((d / v8 / "main.tex").read_text() + "edited\n")
    (d / v8 / "extra.tex").write_text("new section\n")
    changelog(d, "edit active V8")
    commit(d, env, "edit V8")
    # numbering comes from the registry + Git + filesystem
    assert tool(d, env, "next", "paper").stdout.strip() == "V9"
    r = tool(d, env, "new", "paper", ok=False)
    assert r.returncode != 0 and "ACTIVE" in r.stdout + r.stderr  # edit the active one or complete it first
    tool(d, env, "complete", "paper/V8", "--evidence", "delivered to the supervisor")
    commit(d, env, "complete V8")
    # 2 + 10 creating V9: exact copy of V8, registered with provenance, memory updated
    tool(d, env, "new", "paper")
    for f in ["main.tex", "fig.pdf", "extra.tex"]:
        assert (d / v9 / f).read_bytes() == (d / v8 / f).read_bytes()
    reg = json.loads((d / VR.REG_REL).read_text())
    e9 = next(e for e in reg["entries"] if e["id"] == "paper/V9")
    e8 = next(e for e in reg["entries"] if e["id"] == "paper/V8")
    assert e9["status"] == "ACTIVE" and e9["parent"] == "paper/V8" and e9["parent_commit"] == e8["commit"]
    assert e9["parent_tree"] == e8["tree"] and e9["path"] == v9
    assert "paper/V9" in (d / VR.MD_REL).read_text()
    assert "new version paper/V9" in (d / "research/context/CHANGELOG.md").read_text()
    commit(d, env, "start V9")
    # the new version is editable; V8 is now read-only
    (d / v9 / "main.tex").write_text((d / v9 / "main.tex").read_text() + "V9 change\n")
    changelog(d, "edit V9")
    commit(d, env, "edit V9")
    assert hook(d, env, "Edit", {"file_path": str(d / v8 / "main.tex"), "old_string": "Paper", "new_string": "X"}) == 2
    # 8 V1-V7 byte-for-byte unchanged, and every completed record verifies
    assert snapshot(d) == before
    assert tool(d, env, "verify", "--worktree").returncode == 0
    head = run(["git", "rev-parse", "HEAD"], d, env).stdout.strip()
    base = run(["git", "rev-list", "--max-parents=0", "HEAD"], d, env).stdout.split()[0]
    r = run([sys.executable, "tools/research_guard.py", "--range", f"{base}", head], d, env, ok=False)
    assert "R9" not in r.stdout, r.stdout


# ---------------------------------------------------------------- 3, 4, 5, 6, 8
def test_completed_v7_and_results_are_read_only(repo):
    d, env = repo
    before = snapshot(d)
    v7, v8 = vdir(7), vdir(8)
    blocked = [
        ("Edit", {"file_path": str(d / v7 / "main.tex"), "old_string": "text", "new_string": "Text"}),
        ("Write", {"file_path": str(d / v7 / "main.tex"), "content": "rewritten\n"}),
        ("Write", {"file_path": str(d / v7 / "new_section.tex"), "content": "added\n"}),
        ("Write", {"file_path": str(d / "research/final/r1.json"), "content": '{"hota": 99}\n'}),
        ("Bash", {"command": f"sed -i 's/text/TEXT/' {v7}/main.tex"}),
        ("Bash", {"command": f"echo more >> {v7}/main.tex"}),
        ("Bash", {"command": f"cp {v8}/main.tex {v7}/"}),
        ("Bash", {"command": f"cp /tmp/x.json research/final/r1.json"}),
        ("Bash", {"command": f"touch {v7}/x.tex && echo"}),
        ("Bash", {"command": f"mv {v7} {FAM_ROOT}/old"}),
        ("Bash", {"command": f"rm -rf {v7}"}),
        ("Bash", {"command": f"git rm -r {v7}"}),
        ("Bash", {"command": f"python3 -c \"open('{v7}/main.tex', 'w').write('')\""}),
        ("Bash", {"command": f"cd {v7} && pdflatex main.tex"}),
        ("Bash", {"command": f"latexmk -cd {v7}/main.tex"}),
        ("Bash", {"command": f"pdflatex -output-directory={v7} {v8}/main.tex"}),
        ("Bash", {"command": f"cd {v7} && python3 make_figures.py"}),
        ("Bash", {"command": f"python3 {v7}/make_figures.py"}),
    ]
    (d / v7 / "make_figures.py").parent.mkdir(exist_ok=True)
    for t, inp in blocked:
        if t == "Bash" and "touch" in inp["command"]:
            continue  # touch only changes times; covered by git below
        assert hook(d, env, t, inp) == 2, inp
    # new results in new files are normal work
    assert hook(d, env, "Write", {"file_path": str(d / "research/final/r2.json"), "content": "{}\n"}) == 0
    # git: every route that changes V7 or the completed result is refused at commit
    attempts = [
        lambda: (d / v7 / "main.tex").write_text("rewritten\n"),
        lambda: (d / v7 / "added.tex").write_text("added\n"),
        lambda: run(["git", "rm", "-q", "-r", v7], d, env),
        lambda: run(["git", "mv", v7, f"{FAM_ROOT}/moved"], d, env),
        lambda: (d / "research/final/r1.json").write_text('{"hota": 99}\n'),
    ]
    for act in attempts:
        act()
        changelog(d, "attempt")
        r = commit(d, env, "attempt", ok=False)
        assert r.returncode != 0 and "R9" in r.stdout + r.stderr, r.stdout + r.stderr
        restore(d, env)
    (d / "research/final/r2.json").write_text("{}\n")
    changelog(d, "new result")
    p = d / "research/context/EXPERIMENT_REGISTRY.md"
    p.write_text(p.read_text() + "- r2\n")
    commit(d, env, "add new result")
    assert snapshot(d) == before
    assert tool(d, env, "verify", "--worktree").returncode == 0


# ---------------------------------------------------------------- 9
def test_numbering_and_status_cannot_be_manipulated(repo):
    d, env = repo
    reg_path = d / VR.REG_REL
    reg = json.loads(reg_path.read_text())

    def write_reg(r):
        return hook(d, env, "Write", {"file_path": str(reg_path), "content": json.dumps(r, indent=2)})

    def mutated(fn):
        r = json.loads(json.dumps(reg))
        fn(r)
        return r

    def add(r, **kw):
        e = {"family": "paper", "kind": "version_dir", "status": "ACTIVE", "evidence": "x"}
        e.update(kw)
        r["entries"].append(e)

    bad = {
        "V7 back to ACTIVE": lambda r: r["entries"][6].update(status="ACTIVE"),
        "V7 tree rewritten": lambda r: r["entries"][6].update(tree="0" * 40),
        "entry removed": lambda r: r["entries"].pop(5),
        "family pattern changed": lambda r: r["families"]["paper"].update(pattern="X{n}"),
        "skip to V11": lambda r: add(r, id="paper/V11", version=11, label="x", path=vdir(11)),
        "reuse V7": lambda r: add(r, id="paper/V7b", version=7, label="x", path=vdir(70)),
        "existing V6 as ACTIVE": lambda r: add(r, id="paper/V9", version=9, label="x", path=vdir(6)),
        "wrong path": lambda r: add(r, id="paper/V9", version=9, label="x", path="elsewhere/V9"),
    }
    for name, fn in bad.items():
        assert write_reg(mutated(fn)) == 2, name
    good = mutated(lambda r: add(r, id="paper/V9", version=9, label=Path(vdir(9)).name, path=vdir(9)))
    assert write_reg(good) == 0
    for cmd in [f"sed -i 's/COMPLETED/ACTIVE/' {VR.REG_REL}", f"echo '{{}}' > {VR.REG_REL}",
                f"python3 -c \"open('{VR.REG_REL}', 'w').write('{{}}')\"", f"cp /tmp/r.json {VR.REG_REL}"]:
        assert bash(d, env, cmd) == 2, cmd
    # a registry edit that the hook never saw is still refused at commit
    reg_path.write_text(json.dumps(mutated(bad["V7 back to ACTIVE"]), indent=2))
    (d / vdir(7) / "main.tex").write_text("rewritten after unlocking\n")
    changelog(d, "attempt")
    r = commit(d, env, "unlock V7", ok=False)
    assert r.returncode != 0 and "R9" in r.stdout + r.stderr
    restore(d, env)
    reg_path.write_text(json.dumps(mutated(bad["skip to V11"]), indent=2))
    (d / vdir(11)).mkdir()
    (d / vdir(11) / "main.tex").write_text("x\n")
    changelog(d, "attempt")
    r = commit(d, env, "skip", ok=False)
    assert r.returncode != 0 and "next paper version is 9" in r.stdout + r.stderr
    restore(d, env)
    # the tool refuses reuse and re-completion
    assert tool(d, env, "complete", "paper/V7", "--evidence", "x", ok=False).returncode != 0
    assert tool(d, env, "next", "paper").stdout.strip() == "V9"


@pytest.mark.skipif(shutil.which("gpg") is None, reason="gpg not installed")
def test_delete_approval_does_not_authorise_changing_a_completed_version(repo, tmp_path):
    d, env = repo
    home = tmp_path / "g"
    home.mkdir(mode=0o700)
    e = dict(env, GNUPGHOME=str(home))
    run(["gpg", "--batch", "--pinentry-mode", "loopback", "--passphrase", "", "--quick-gen-key",
         "Owner <owner@example.com>", "ed25519", "sign", "never"], home, e)
    fpr = [l.split(":")[9] for l in run(["gpg", "--list-secret-keys", "--with-colons"], home, e).stdout.splitlines()
           if l.startswith("fpr")][0]
    pub = run(["gpg", "--armor", "--export", fpr], home, e).stdout
    base = run(["git", "rev-parse", "HEAD"], d, env).stdout.strip()
    target = f"{vdir(7)}/fig.pdf"

    def owner_commit(msg, update_registry):
        run(["git", "checkout", "-q", "-B", f"t{len(msg)}{update_registry}", base], d, env)
        run(["git", "rm", "-q", target], d, env)
        changelog(d, "owner removes a figure from V7")
        run(["git", "add", "research/context/CHANGELOG.md"], d, env)
        if update_registry:  # the owner also records the new tree of V7
            tree = run(["git", "write-tree"], d, env).stdout.strip()
            sub = run(["git", "rev-parse", f"{tree}:{vdir(7)}"], d, env).stdout.strip()
            reg = json.loads((d / VR.REG_REL).read_text())
            next(x for x in reg["entries"] if x["id"] == "paper/V7").update(tree=sub)
            (d / VR.REG_REL).write_text(json.dumps(reg, indent=2) + "\n")
            run(["git", "add", VR.REG_REL], d, env)
        run(["git", "-c", f"user.signingkey={fpr}", "commit", "-q", "--no-verify", "-S", "-m", msg], d, e)
        return run([sys.executable, "tools/research_guard.py", "--range", base, "HEAD"], d,
                   dict(env, ACMOT_OWNER_KEYS=pub), ok=False)

    r = owner_commit(f"remove fig\n\n{DEL}: {target}", True)
    assert r.returncode == 1 and "R9" in r.stdout          # a delete approval alone is not enough
    r = owner_commit(f"remove fig\n\n{DEL}: {target}\n{CMP}: {vdir(7)}/", True)
    assert r.returncode == 0, r.stdout                       # separate signed approval for the completed version
    r = owner_commit(f"remove fig\n\n{DEL}: {target}\n{CMP}: {vdir(7)}/", False)
    assert r.returncode == 1 and "byte-for-byte" in r.stdout  # and the record must match the content


# ---------------------------------------------------------------- 7
@pytest.mark.skipif(shutil.which("graphify") is None, reason="graphify not installed")
def test_graph_rebuild_leaves_completed_versions_unchanged(repo):
    d, env = repo
    before = snapshot(d)
    assert bash(d, env, "graphify update .") == 0
    run(["graphify", "update", "."], d, env, ok=False)
    assert snapshot(d) == before
    assert not run(["git", "status", "--porcelain", "--", FAM_ROOT, "research"], d, env).stdout.strip()
    assert tool(d, env, "verify", "--worktree").returncode == 0


# ---------------------------------------------------------------- real registry (read only)
def test_real_registry_verifies_and_numbers():
    reg = VR.load("HEAD") if VR.exists_at("HEAD", VR.REG_REL) else VR.load(None)
    assert not VR.verify(reg, "HEAD")
    # the next number is always one above every number already used (registry, Git, disk)
    for fam, floor in (("paper1", 14), ("paper2", 12), ("universal-acmot", 8)):
        used = VR.family_numbers(reg["families"][fam], reg, fam, "HEAD") | \
            VR.family_numbers(reg["families"][fam], reg, fam, None)
        assert VR.next_number(fam, reg) == max(used) + 1 >= floor, fam
    ids = {e["id"]: e["status"] for e in reg["entries"]}
    assert ids["paper1/V12"] == ids["paper1/V13"] == ids["paper2/V11"] == "COMPLETED"
    assert ids["universal-acmot/V7"] == "FROZEN"


def test_real_repo_hook_protects_completed_versions():
    def decide(tool_name, inp):
        return CTG.decide({"tool_name": tool_name, "tool_input": inp, "cwd": str(ROOT)})
    v13 = ROOT / "research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS"
    assert decide("Edit", {"file_path": str(v13 / "main.tex"), "old_string": "a", "new_string": "b"})
    assert decide("Write", {"file_path": str(v13 / "new.tex"), "content": "x"})
    assert decide("Bash", {"command": "cd research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS && pdflatex main.tex"})
    assert decide("Write", {"file_path": str(ROOT / "JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11/x.tex"), "content": "x"})
    assert decide("Write", {"file_path": str(ROOT / "research/final/V7_MAIN_RESULTS.json"), "content": "{}"})
    assert decide("Edit", {"file_path": str(ROOT / "acmot_v7.py"), "old_string": "a", "new_string": "b"})
    assert decide("Bash", {"command": "python3 research/acmot_paper_v2/run_v3_second_val_read.py"})
    # normal work stays allowed
    assert decide("Write", {"file_path": str(ROOT / "research/final/NEW_RESULT_X.json"), "content": "{}"}) is None
    assert decide("Bash", {"command": "python3 tools/version_registry.py next paper1"}) is None
    assert decide("Bash", {"command": "cat research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS/main.tex"}) is None
    assert decide("Bash", {"command": "graphify update ."}) is None
