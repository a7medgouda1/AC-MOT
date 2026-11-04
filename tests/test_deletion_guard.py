"""
Tests for the AC-MOT owner-only-delete policy (research/context/PRESERVATION_POLICY.md).

Nothing in the real repository is deleted, renamed or modified: the Claude tool guard
is only asked for its decision, and every git scenario runs in a disposable repository
created under pytest's temporary directory. Standard library + pytest (+ gpg for the
signed-approval tests, skipped when gpg is missing).
"""
from __future__ import annotations

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
import research_guard as RG  # noqa: E402

# Built by concatenation so that no agent-written file contains the literal trailer.
DEL = "Owner-Approved" + "-Delete"
CHG = "Owner-Approved" + "-Change"


def decide(tool: str, inp: dict, cwd: Path = ROOT) -> str | None:
    return CTG.decide({"tool_name": tool, "tool_input": inp, "cwd": str(cwd)})


def bash(cmd: str, cwd: Path = ROOT) -> str | None:
    return decide("Bash", {"command": cmd}, cwd)


# ---------------------------------------------------------------- Claude tool guard
BLOCKED = [
    "rm AGENTS.md", "rm -rf research/final", "rmdir research/context", "unlink AGENTS.md",
    "/bin/rm AGENTS.md", "sudo rm AGENTS.md", "env X=1 rm AGENTS.md", "echo ok; rm AGENTS.md",
    "true && rm -f AGENTS.md", "ls | xargs rm", "echo $(rm AGENTS.md)", 'echo "$(rm AGENTS.md)"',
    "cd research && rm context/NEXT_STEPS.md", "rm $TARGET", "rm ~/important.txt", "shred -u AGENTS.md",
    "find . -name '*.pyc' -delete", "find research -exec rm {} \\;", "rsync -a --delete src/ research/",
    "mv AGENTS.md /tmp/AGENTS.md", "mv research/context/NEXT_STEPS.md research/context/NEXT.md",
    "mv /tmp/x.md AGENTS.md", "truncate -s 0 AGENTS.md", ": > AGENTS.md", "> AGENTS.md",
    "cp /dev/null AGENTS.md", "echo x > AGENTS.md", "cat /dev/null > AGENTS.md",
    "git rm research/context/NEXT_STEPS.md", "git rm --cached AGENTS.md", "git rm -r research",
    "git clean -fdx", "git mv AGENTS.md A.md", "git reset --hard HEAD~1", "git checkout -- AGENTS.md",
    "git checkout -f main", "git restore AGENTS.md", "git stash drop", "git stash clear",
    "git branch -D old", "git branch -d old", "git branch -m old new", "git tag -d universal-acmot-v7-freeze",
    "git tag -f universal-acmot-v7-freeze HEAD", "git push origin --delete feature", "git push origin :feature",
    "git push --force", "git push -f origin x", "git push origin +x", "git push --force-with-lease",
    "git push --mirror origin", "git push --no-verify", "git commit -n -m x", "git commit --no-verify -m x",
    "git -c core.hooksPath=/dev/null commit -m x", "git config core.hooksPath ''",
    "git config --unset core.hooksPath", "git update-ref -d refs/heads/x", "git worktree remove ../w",
    "git reflog expire --all", "git filter-branch --tree-filter x", "git rebase main",
    "python3 -c \"import os; os.remove('AGENTS.md')\"", "python3 -c 'import shutil; shutil.rmtree(\"research\")'",
    "python3 - <<'EOF'\nfrom pathlib import Path\nPath('AGENTS.md').unlink()\nEOF",
    "python3 -c \"import os; os.rename('AGENTS.md', 'B.md')\"", "python3 -c \"import os; os.system('rm AGENTS.md')\"",
    "python3 -c \"import subprocess; subprocess.run(['git', 'rm', 'AGENTS.md'])\"",
    "node -e \"require('fs').unlinkSync('AGENTS.md')\"", "node -e \"require('fs').rmSync('research', {recursive: true})\"",
    "perl -e 'unlink \"AGENTS.md\"'", "ruby -e 'File.delete(\"AGENTS.md\")'",
    "bash -c 'rm AGENTS.md'", "sh -c \"git clean -fd\"", "eval rm AGENTS.md", "eval 'git rm AGENTS.md'",
    "ACMOT_OWNER_KEYS=x git push", "export ACMOT_OWNER_KEYS=abc", "env ACMOT_OWNER_KEYS=x git push",
    "python3 -c \"import os; os.environ['ACMOT_OWNER_KEYS'] = 'k'\"",
    "(rm AGENTS.md)", "\\rm AGENTS.md", "command rm AGENTS.md", "nohup rm AGENTS.md &", "timeout 5 rm AGENTS.md",
    "busybox rm AGENTS.md", "git -C . rm AGENTS.md", "find . -type f | xargs -I{} rm {}",
    "python3 -c \"import shutil; shutil.move('AGENTS.md', '/tmp/a')\"",
    "perl -MFile::Path -e 'rmtree(\"research\")'", "node -e 'require(\"fs\").promises.rm(\"x\")'",
    "ls; rm -r -- research/context", "rm -- -weird-name AGENTS.md",
    "echo '{}' > .claude/settings.local.json", "tee .claude/settings.local.json", "dd if=/dev/zero of=.git/config",
    "sed -i 's/a/b/' research/V7_POLICY_LOCK.json", "cp /tmp/x research/final/V7_MAIN_RESULTS.json",
    "cp /tmp/x research/context/DECISIONS.md",
    "python3 -c \"from pathlib import Path; Path('.claude/settings.json').write_text('{}')\"",
    "python3 -c \"open('.git/config', 'w').write('')\"", "git commit -m x -m '" + DEL + ": AGENTS.md'",
]

ALLOWED = [
    "ls -la", "cat AGENTS.md", "grep -rn 'rm -rf' tools", "git status", "git log --oneline -5", "git diff",
    "git add -A", "git commit -m 'Remove stale wording from notes'", "git push -u origin sci-v7f-general-layer-dev",
    "git push origin HEAD:refs/heads/topic", "git checkout -b new-branch", "git switch main", "git stash",
    "git restore --staged AGENTS.md", "git fetch origin", "git tag new-tag-v1", "git merge origin/main",
    "python3 tools/build_code_inventory.py --check", "python3 -m pytest -q tests",
    "python3 -c \"import pandas as pd; df = pd.DataFrame(); df.rename(columns={'a': 'b'})\"",
    "python3 -c \"print('hello'.replace('h', 'j'))\"", "echo hello > research/context/new_note_x.md",
    "echo more >> research/context/NEXT_STEPS.md", "mkdir -p research/new_x && touch research/new_x/a.md",
    "cp AGENTS.md /tmp/acmot_copy.md", "rm /tmp/acmot_scratch_file.txt", "mv /tmp/acmot_a.txt /tmp/acmot_b.txt",
    "sed -i 's/a/b/' research/context/NEXT_STEPS.md", "python3 tools/research_guard.py --worktree 2>&1 | tail -3",
    "chmod +x .githooks/pre-push", "ls 2>/dev/null", "cat AGENTS.md >/dev/null 2>&1",
    "python3 tools/context_health_check.py --queries", "python3 tools/update_project_context.py",
    "python3 tools/build_code_inventory.py",
    "$(cat graphify-out/.graphify_python 2>/dev/null || echo python3) tools/build_context_graph.py",
    "graphify query 'what is V7f'", "git commit -F - <<'EOF'\nDrop old wording; rm is not used\n\nBody\nEOF",
    "cd research/context && ls && cd ../..", "pdflatex -interaction=nonstopmode main.tex",
    "git config --get core.hooksPath", "git config core.hooksPath", "git config --list --show-origin",
    "git config --get-all core.hooksPath", "graphify update .",
    "grep -n ACMOT_OWNER_KEYS research/context/PRESERVATION_POLICY.md",
    "python3 -c \"from pathlib import Path; p = Path('tools/context_health_check.py'); "
    "p.write_text(p.read_text().replace('.github/workflows/research_guard.yml', 'x'))\"",
    "cp /tmp/new_figure.pdf research/new_x/fig.pdf", "sed -i 's/x/y/' research/context/NEXT_STEPS.md",
    "grep -n research_guard tools/context_health_check.py", "chmod 644 research/context/NEXT_STEPS.md",
]


@pytest.mark.parametrize("cmd", BLOCKED)
def test_claude_guard_blocks_deletion_routes(cmd):
    assert bash(cmd), cmd


@pytest.mark.parametrize("cmd", ALLOWED)
def test_claude_guard_allows_ordinary_work(cmd):
    assert bash(cmd) is None, (cmd, bash(cmd))


def test_claude_guard_allows_cleanup_of_disposable_clones(tmp_path):
    (tmp_path / "f.txt").write_text("x")
    assert bash(f"cd {tmp_path} && git rm f.txt && rm -rf {tmp_path}/sub") is None
    assert bash(f"rm -rf {tmp_path}") is None


def test_claude_guard_edit_tools(tmp_path):
    big = ROOT / "AGENTS.md"
    # normal creation and editing
    assert decide("Write", {"file_path": str(ROOT / "research/context/NEW_NOTE_X.md"), "content": "x"}) is None
    assert decide("Edit", {"file_path": str(big), "old_string": "Universal", "new_string": "Universal"}) is None
    assert decide("Write", {"file_path": str(big), "content": big.read_text() + "\nmore\n"}) is None
    # disguised deletion: emptying an existing file
    assert decide("Write", {"file_path": str(big), "content": ""})
    assert decide("Write", {"file_path": str(big), "content": "x\n"})
    body = big.read_text()
    assert decide("Edit", {"file_path": str(big), "old_string": body, "new_string": ""})
    assert decide("MultiEdit", {"file_path": str(big), "edits": [{"old_string": body, "new_string": "."}]})
    # frozen artifacts, protection/config files, approval trailers
    assert decide("Edit", {"file_path": str(ROOT / "research/V7_POLICY_LOCK.json"), "old_string": "a", "new_string": "b"})
    assert decide("Write", {"file_path": str(ROOT / ".claude/settings.local.json"), "content": "{}"})
    assert decide("Write", {"file_path": str(ROOT / ".claude/settings.json"), "content": "{}"})
    assert decide("Write", {"file_path": str(ROOT / ".git/config"), "content": "[core]"})
    assert decide("Write", {"file_path": str(tmp_path / "msg.txt"), "content": f"x\n\n{DEL}: AGENTS.md\n"})
    # the GitHub MCP delete tool
    assert decide("mcp__github__delete_file", {"path": "AGENTS.md"})
    # a disposable temp file may be emptied
    t = tmp_path / "scratch.txt"
    t.write_text("y" * 1000)
    assert decide("Write", {"file_path": str(t), "content": ""}) is None


def test_claude_guard_scans_new_scripts_but_runs_committed_ones(tmp_path):
    bad = tmp_path / "cleanup.py"
    bad.write_text("import shutil\nshutil.rmtree('research')\n")
    assert bash(f"python3 {bad}")
    good = tmp_path / "report.py"
    good.write_text("print('ok')\n")
    assert bash(f"python3 {good}") is None
    sh = tmp_path / "clean.sh"
    sh.write_text("#!/bin/sh\nrm -rf research\n")
    assert bash(f"bash {sh}") and bash(f"sh {sh}") and bash(f"source {sh}")


def test_guard_has_no_self_bypass():
    src = (ROOT / "tools" / "claude_tool_guard.py").read_text()
    assert "environ.get(\"ACMOT" not in src and "OVERRIDE" not in src
    assert "OVERRIDE" not in (ROOT / "tools" / "research_guard.py").read_text()


def test_hook_exit_code_blocks(tmp_path):
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "claude_tool_guard.py")],
                       input=json.dumps({"tool_name": "Bash", "tool_input": {"command": "rm AGENTS.md"},
                                         "cwd": str(ROOT)}), capture_output=True, text=True)
    assert r.returncode == 2 and "owner" in r.stderr
    assert (ROOT / "AGENTS.md").exists()


# ---------------------------------------------------------------- research guard (pure)
def test_r0_needs_path_specific_approval():
    ch = [("D", "data/b.txt", None), ("D", "docs/keep.md", None)]
    lv = lambda rep: {l for l, _ in rep}  # noqa: E731
    assert "FAIL" in lv(RG.evaluate(ch, {}, set(), [], None))
    one = RG.parse_approvals(f"msg\n\n{DEL}: data/b.txt | obsolete copy\n")
    rep = RG.evaluate(ch, {}, set(), [], None, one)
    assert ("FAIL", "R0 deletion needs the owner's approval: docs/keep.md") in rep
    assert any(l == "WARN" and "data/b.txt" in m for l, m in rep)
    both = RG.parse_approvals(f"{DEL}: data/b.txt\n{DEL}: docs/\n")
    assert "FAIL" not in lv(RG.evaluate(ch, {}, set(), [], None, both))
    ren = [("R100", "data/z.txt", "data/a.txt")]
    assert "FAIL" in lv(RG.evaluate(ren, {}, set(), [], None))
    assert "FAIL" in lv(RG.evaluate([("M", "data/a.txt", None)], {}, set(), [], None, None, ["data/a.txt"]))
    # a change approval does not approve a deletion
    assert "FAIL" in lv(RG.evaluate(ch[:1], {}, set(), [], None, RG.parse_approvals(f"{CHG}: data/b.txt")))


def test_push_ref_rules():
    z = RG.ZERO
    rep = RG.push_ref_report([f"(delete) {z} refs/heads/x {'a' * 40}",
                              f"refs/tags/t {'b' * 40} refs/tags/t {'c' * 40}",
                              f"refs/heads/m {'d' * 40} refs/heads/m {'e' * 40}",
                              f"refs/heads/n {'f' * 40} refs/heads/n {z}"],
                             is_ancestor=lambda a, b: False, exists=lambda s: True)
    assert [l for l, _ in rep] == ["FAIL", "FAIL", "FAIL"]


# ---------------------------------------------------------------- disposable git repository
def run(cmd, cwd, env=None, ok=True, inp=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, input=inp)
    if ok:
        assert r.returncode == 0, (cmd, r.stdout, r.stderr)
    return r


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
    files = {".gitignore": "__pycache__/\n*.pyc\n",
             "research/context/CHANGELOG.md": "# CHANGELOG\n- start\n", "research/context/PAPERS.md": "# P\n",
             "data/a.txt": "a" * 400, "data/b.txt": "b" * 400, "data/c.txt": "c" * 400,
             "docs/keep.md": "keep\n" * 60, "research/final/R.json": '{"x": 1}\n'}
    for rel, text in files.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(text)
    # Ignore the machine's git config (it may sign every commit or set hooks).
    env = dict(os.environ, GIT_AUTHOR_NAME="Owner", GIT_AUTHOR_EMAIL="owner@example.com",
               GIT_COMMITTER_NAME="Owner", GIT_COMMITTER_EMAIL="owner@example.com",
               GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    env.pop("ACMOT" + "_OWNER_KEYS", None)
    run(["git", "init", "-q", "-b", "main"], d, env)
    run(["git", "add", "-A"], d, env)
    run(["git", "commit", "-q", "-m", "base"], d, env)
    run(["git", "config", "core.hooksPath", ".githooks"], d, env)
    return d, env


def commit(d, env, msg, ok=True):
    return run(["git", "commit", "-q", "-m", msg], d, env, ok=ok)


def test_git_hooks_scenarios(repo):
    d, env = repo
    # 1 create allowed
    (d / "data/new.txt").write_text("new\n")
    run(["git", "add", "-A"], d, env)
    commit(d, env, "add new file")
    # 2 edit allowed
    (d / "data/a.txt").write_text("a" * 380 + "edited\n")
    run(["git", "add", "-A"], d, env)
    commit(d, env, "edit a")
    head = run(["git", "rev-parse", "HEAD"], d, env).stdout
    # 3 delete file blocked
    run(["git", "rm", "-q", "data/b.txt"], d, env)
    r = commit(d, env, "remove b", ok=False)
    assert r.returncode != 0 and "R0 deletion" in r.stdout + r.stderr
    # a commit-message trailer alone is never approval (local hooks cannot verify a signature)
    r = commit(d, env, f"remove b\n\n{DEL}: data/b.txt | duplicate of a", ok=False)
    assert r.returncode != 0 and "R0 deletion" in r.stdout + r.stderr
    run(["git", "reset", "-q", "HEAD", "--", "data/b.txt"], d, env)
    run(["git", "checkout", "-q", "--", "data/b.txt"], d, env)
    assert (d / "data/b.txt").exists()
    # 4 delete directory blocked
    run(["git", "rm", "-q", "-r", "docs"], d, env)
    assert commit(d, env, "remove docs", ok=False).returncode != 0
    run(["git", "reset", "-q", "HEAD", "--", "docs"], d, env)
    run(["git", "checkout", "-q", "--", "docs"], d, env)
    # 5 rename/move blocked
    run(["git", "mv", "data/a.txt", "data/z.txt"], d, env)
    r = commit(d, env, "rename a", ok=False)
    assert r.returncode != 0 and "rename" in r.stdout + r.stderr
    run(["git", "mv", "data/z.txt", "data/a.txt"], d, env)
    # 6 emptying blocked
    (d / "docs/keep.md").write_text("")
    run(["git", "add", "-A"], d, env)
    r = commit(d, env, "empty keep", ok=False)
    assert r.returncode != 0 and "emptied" in r.stdout + r.stderr
    run(["git", "reset", "-q", "HEAD", "--", "docs/keep.md"], d, env)
    run(["git", "checkout", "-q", "--", "docs/keep.md"], d, env)
    # frozen artifact edit blocked, protection file edit blocked
    (d / "research/final/R.json").write_text('{"x": 2}\n')
    (d / "research/context/CHANGELOG.md").write_text("# CHANGELOG\n- start\n- edit R\n")
    run(["git", "add", "-A"], d, env)
    assert commit(d, env, "edit frozen", ok=False).returncode != 0
    run(["git", "reset", "-q", "HEAD", "--", "."], d, env)
    run(["git", "checkout", "-q", "--", "."], d, env)
    # untracked files are never touched or reported
    (d / "local_notes.txt").write_text("mine\n")
    out = run([sys.executable, "tools/research_guard.py", "--worktree"], d, env).stdout
    assert "local_notes" not in out and (d / "local_notes.txt").exists()
    # the Claude tool guard inside this repository blocks the same deletions
    for cmd in ["rm data/a.txt", "git rm data/a.txt", "rm -rf docs", "mv data/a.txt data/q.txt",
                "python3 -c \"import os; os.remove('data/a.txt')\""]:
        r = run([sys.executable, "tools/claude_tool_guard.py"], d, env, ok=False,
                inp=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(d)}))
        assert r.returncode == 2, cmd
    # ... and edits of its own (committed) guard files by any route
    for cmd in ["sed -i 's/exit 2/exit 0/' tools/claude_tool_guard.py", "cp /tmp/x tools/research_guard.py",
                "echo x >> .githooks/pre-commit", "chmod -x .githooks/pre-commit",
                "python3 -c \"open('tools/claude_tool_guard.py', 'w').write('')\"",
                "git apply /tmp/p.diff && echo tools/research_guard.py"]:
        r = run([sys.executable, "tools/claude_tool_guard.py"], d, env, ok=False,
                inp=json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(d)}))
        assert r.returncode == 2, cmd
    for tool, inp in [("Edit", {"file_path": str(d / "tools/claude_tool_guard.py"), "old_string": "2", "new_string": "0"}),
                      ("Write", {"file_path": str(d / ".githooks/pre-commit"), "content": "exit 0\n"})]:
        r = run([sys.executable, "tools/claude_tool_guard.py"], d, env, ok=False,
                inp=json.dumps({"tool_name": tool, "tool_input": inp, "cwd": str(d)}))
        assert r.returncode == 2, tool
    assert (d / "data/a.txt").exists() and (d / "docs/keep.md").exists()
    assert run(["git", "rev-parse", "HEAD"], d, env).stdout == head


def test_ci_range_checks_each_commit(repo):
    d, env = repo
    base = run(["git", "rev-parse", "HEAD"], d, env).stdout.strip()
    # approval sits in a commit that deletes nothing; the deletion comes later without one
    (d / "data/new.txt").write_text("n\n")
    run(["git", "add", "-A"], d, env)
    run(["git", "commit", "-q", "--no-verify", "-m", f"note\n\n{DEL}: data/c.txt"], d, env)
    run(["git", "rm", "-q", "data/c.txt"], d, env)
    run(["git", "commit", "-q", "--no-verify", "-m", "remove c"], d, env)
    r = run([sys.executable, "tools/research_guard.py", "--range", base, "HEAD"], d, env, ok=False)
    assert r.returncode == 1 and "R0 deletion" in r.stdout


def test_ci_fails_closed_without_owner_key(repo):
    d, env = repo
    base = run(["git", "rev-parse", "HEAD"], d, env).stdout.strip()
    run(["git", "rm", "-q", "data/b.txt"], d, env)
    run(["git", "commit", "-q", "--no-verify", "-m", f"remove b\n\n{DEL}: data/b.txt"], d, env)
    r = run([sys.executable, "tools/research_guard.py", "--range", base, "HEAD"], d, env, ok=False)
    assert r.returncode == 1 and "cannot be verified" in r.stdout and "R0 deletion" in r.stdout


def _gpg_key(home: Path, name: str, env: dict) -> str:
    home.mkdir(mode=0o700)
    e = dict(env, GNUPGHOME=str(home))
    run(["gpg", "--batch", "--pinentry-mode", "loopback", "--passphrase", "", "--quick-gen-key",
         f"{name} <{name.lower()}@example.com>", "ed25519", "sign", "never"], home, e)
    out = run(["gpg", "--list-secret-keys", "--with-colons"], home, e).stdout
    return [l.split(":")[9] for l in out.splitlines() if l.startswith("fpr")][0]


@pytest.mark.skipif(shutil.which("gpg") is None, reason="gpg not installed")
def test_ci_accepts_only_owner_signed_approvals(repo, tmp_path):
    d, env = repo
    owner_home, other_home = tmp_path / "g1", tmp_path / "g2"
    owner = _gpg_key(owner_home, "Owner", env)
    other = _gpg_key(other_home, "Agent", env)
    pub = run(["gpg", "--armor", "--export", owner], d, dict(env, GNUPGHOME=str(owner_home))).stdout
    (d / ".github/owner_keys").mkdir(parents=True)
    (d / ".github/owner_keys/owner.asc").write_text(pub)
    run(["git", "add", "-A"], d, env)
    run(["git", "commit", "-q", "--no-verify", "-m", "owner key"], d, env)
    base = run(["git", "rev-parse", "HEAD"], d, env).stdout.strip()

    def check(start, extra_env=None):
        return run([sys.executable, "tools/research_guard.py", "--range", start, "HEAD"], d,
                   dict(env, **(extra_env or {})), ok=False)

    def delete(home, key, signed, paths=("data/b.txt",), approve=("data/b.txt",), start=None):
        run(["git", "checkout", "-q", "-B", f"t{key[:6]}{signed}{len(paths)}", start or base], d, env)
        run(["git", "rm", "-q", *paths], d, env)
        msg = "remove\n\n" + "\n".join(f"{DEL}: {p}" for p in approve)
        cmd = ["git", "-c", f"user.signingkey={key}", "commit", "-q", "--no-verify", "-m", msg] + (["-S"] if signed else [])
        run(cmd, d, dict(env, GNUPGHOME=str(home)))
        return check(start or base)

    # owner-signed approval for exactly that target: accepted
    assert delete(owner_home, owner, True).returncode == 0
    # the same approval does not cover a second target
    r = delete(owner_home, owner, True, paths=("data/b.txt", "data/c.txt"))
    assert r.returncode == 1 and "data/c.txt" in r.stdout
    # unsigned trailer, or signed with a key the owner did not register: refused
    r = delete(owner_home, owner, False)
    assert r.returncode == 1 and "not signed by an owner key" in r.stdout
    r = delete(other_home, other, True)
    assert r.returncode == 1 and "not signed by an owner key" in r.stdout
    # an agent adding its own key is refused, and once its key has landed in the repository
    # the repository-variable trust root (ACMOT_OWNER_KEYS) still does not trust it
    run(["git", "checkout", "-q", "-B", "agentkey", base], d, env)
    other_pub = run(["gpg", "--armor", "--export", other], d, dict(env, GNUPGHOME=str(other_home))).stdout
    (d / ".github/owner_keys/agent.asc").write_text(other_pub)
    run(["git", "add", "-A"], d, env)
    run(["git", "-c", f"user.signingkey={other}", "commit", "-q", "--no-verify", "-S", "-m",
         f"add key\n\n{CHG}: .github/owner_keys/agent.asc"], d, dict(env, GNUPGHOME=str(other_home)))
    r = check(base)
    assert r.returncode == 1 and "R7 trusted owner-key file" in r.stdout
    landed = run(["git", "rev-parse", "HEAD"], d, env).stdout.strip()
    assert delete(other_home, other, True, start=landed).returncode == 0  # repo keys alone: weak
    r = check(landed, {"ACMOT_OWNER_KEYS": pub})
    assert r.returncode == 1 and "not signed by an owner key" in r.stdout
    assert delete(owner_home, owner, True, start=landed).returncode == 0
    assert check(landed, {"ACMOT_OWNER_KEYS": pub}).returncode == 0


def test_pre_push_blocks_ref_deletion_tag_move_and_force(repo, tmp_path):
    d, env = repo
    remote = tmp_path / "remote.git"
    run(["git", "init", "-q", "--bare", str(remote)], tmp_path, env)
    run(["git", "remote", "add", "origin", str(remote)], d, env)
    run(["git", "tag", "v1"], d, env)
    run(["git", "push", "-q", "origin", "main", "v1"], d, env)
    run(["git", "push", "-q", "origin", "main:feature"], d, env)
    assert run(["git", "push", "-q", "origin", "--delete", "feature"], d, env, ok=False).returncode != 0
    (d / "data/new.txt").write_text("n\n")
    run(["git", "add", "-A"], d, env)
    commit(d, env, "more")
    run(["git", "tag", "-f", "v1"], d, env)
    assert run(["git", "push", "-q", "-f", "origin", "v1"], d, env, ok=False).returncode != 0
    run(["git", "push", "-q", "origin", "main"], d, env)  # fast-forward is fine
    run(["git", "reset", "-q", "--hard", "HEAD~1"], d, env)
    assert run(["git", "push", "-q", "-f", "origin", "main"], d, env, ok=False).returncode != 0
    heads = run(["git", "ls-remote", str(remote)], d, env).stdout
    assert "refs/heads/feature" in heads
