"""
Tests for the AC-MOT research-memory and preservation system. Standard library +
pytest only (runs on Mac, Linux and in CI without the ML stack).
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "research" / "context"
sys.path.insert(0, str(ROOT / "tools"))
import build_code_inventory as INV  # noqa: E402
import research_guard as RG  # noqa: E402


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def blob_sha(ref: str, path: str) -> str:
    data = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True).stdout
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------- historical versions
def test_every_documented_tag_resolves_to_its_recorded_commit():
    rows = re.findall(r"\| ([\w.\-]+) \| ([0-9a-f]{40}) \|", (CTX / "FROZEN_VERSIONS.md").read_text())
    assert len(rows) >= 15
    for tag, sha in rows:
        assert git("rev-list", "-n1", tag).strip() == sha, tag


def test_version_history_commits_exist():
    text = (CTX / "VERSION_HISTORY.md").read_text()
    timeline = text.split("## Timeline", 1)[1].split("## V7f vs V6-TF", 1)[0]
    shas = set(re.findall(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{7}\b", timeline))
    assert len(shas) >= 12
    for s in shas:
        assert git("cat-file", "-t", s).strip() == "commit", s


def test_restore_document_covers_every_frozen_version():
    doc = (CTX / "RESTORE_AND_ROLLBACK.md").read_text()
    for tag in git("tag").split():
        if re.fullmatch(r"universal-acmot-v\w+-freeze|acmot-v3-exp-.*-freeze|general-acmot-g1-freeze|v1\.0\.0-acmot-frozen", tag):
            assert tag in doc, tag


# ---------------------------------------------------------------- frozen files
@pytest.mark.parametrize("lock", RG.ACTIVE_LOCKS)
def test_active_policy_locks_match_working_tree(lock):
    for path, sha in json.loads((ROOT / lock).read_text())["file_sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path


def test_every_lock_matches_the_commit_that_last_wrote_it():
    for lock in sorted((ROOT / "research").glob("*.json")):
        files = json.loads(lock.read_text()).get("file_sha256")
        if not isinstance(files, dict):
            continue
        rel = str(lock.relative_to(ROOT))
        # verified at the commit that last wrote the lock or at the code commit it names
        # (the superseded V3 TESTDEV_LOCK was last rewritten at the V4 commit; the V4 lock
        # was rehashed after its tag in 3ea7d69, CF-08)
        last = git("log", "-1", "--format=%H", "--", rel).strip()
        named = json.loads(lock.read_text()).get("code_commit")
        assert last, rel
        ok = [c for c in (last, named) if c and all(blob_sha(c, p) == s for p, s in files.items())]
        assert ok, f"{rel} matches neither {last[:7]} nor {str(named)[:7]}"


def test_frozen_v7f_tag_reproduces_the_v7_lock():
    lock = json.loads((ROOT / "research" / "V7_POLICY_LOCK.json").read_text())["file_sha256"]
    for path, sha in lock.items():
        assert blob_sha("universal-acmot-v7-freeze", path) == sha, path


# ---------------------------------------------------------------- guard rules
def _eval(changes, removed=None, base=None, approvals=None, inv=None):
    return RG.evaluate(changes, removed or {}, base or set(), [], inv, approvals)


def _levels(report):
    return {lvl for lvl, _ in report}


def test_guard_blocks_modified_results_and_frozen_configs():
    for p in ["research/final/V7_MAIN_RESULTS.json", "configs/universal_acmot_policy_v7.json",
              "research/V7_POLICY_LOCK.json", "research/acmot_paper_v2/SECOND_VAL_READ_V3_RESULT.json"]:
        r = _eval([("M", p, None), ("M", "research/context/CHANGELOG.md", None)])
        assert "FAIL" in _levels(r), p
        assert "FAIL" in _levels(_eval([("D", p, None), ("M", "research/context/CHANGELOG.md", None)])), p


def test_guard_requires_new_manuscript_folder_instead_of_editing_old_one():
    base = {"JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11"}
    edit = _eval([("A", "JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11/extra.tex", None),
                  ("M", "research/context/CHANGELOG.md", None), ("M", "research/context/PAPERS.md", None)], base=base)
    assert "FAIL" in _levels(edit)
    new = [("A", "JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev12/main.tex", None)]
    assert "FAIL" in _levels(_eval(new + [("M", "research/context/CHANGELOG.md", None)], base=base))
    ok = _eval(new + [("M", "research/context/CHANGELOG.md", None), ("M", "research/context/PAPERS.md", None)], base=base)
    assert _levels(ok) == {"PASS"}


def test_guard_keeps_append_only_records():
    r = _eval([("M", "research/context/DECISIONS.md", None)], removed={"research/context/DECISIONS.md": 2})
    assert "FAIL" in _levels(r)
    assert _levels(_eval([("M", "research/context/DECISIONS.md", None)],
                         removed={"research/context/DECISIONS.md": 0})) == {"PASS"}


def test_guard_requires_registry_for_new_results_and_changelog_for_code():
    res = [("A", "research/final/new_exp/results.json", None), ("M", "research/context/CHANGELOG.md", None)]
    assert "FAIL" in _levels(_eval(res))
    assert _levels(_eval(res + [("M", "research/context/EXPERIMENT_REGISTRY.md", None)])) == {"PASS"}
    assert "FAIL" in _levels(_eval([("M", "tools/v7/dev.py", None)]))
    assert "FAIL" in _levels(_eval([("M", "tools/v7/dev.py", None), ("M", "research/context/CHANGELOG.md", None)], inv=False))


def test_guard_owner_approval_is_path_specific():
    ch = [("M", "research/final/V7_MAIN_RESULTS.json", None), ("M", "research/context/CHANGELOG.md", None)]
    ok = _eval(ch, approvals={"delete": set(), "change": {"research/final/V7_MAIN_RESULTS.json"}})
    assert "FAIL" not in _levels(ok) and "WARN" in _levels(ok)
    other = _eval(ch, approvals={"delete": set(), "change": {"research/final/OTHER.json"}})
    assert "FAIL" in _levels(other)


def test_documentation_only_change_passes():
    assert _levels(_eval([("M", "research/context/NEXT_STEPS.md", None)])) == {"PASS"}


def test_guard_version_folder_detection():
    assert RG.version_folder("research/acmot_paper_v2/Paper1_JAIS/Paper1_V12_JAIS/main.tex") == \
        "research/acmot_paper_v2/Paper1_JAIS/Paper1_V12_JAIS"
    assert RG.version_folder("JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11/sections/a.tex") == \
        "JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11"
    assert RG.version_folder("research/acmot_paper_v2/run_v3_second_val_read.py") is None


def test_preserved_manuscript_versions_are_separate_tracked_folders():
    tracked = set(git("ls-files").splitlines())
    for folder in ["research/acmot_paper_v2/Paper1_JAIS/Paper1_V12_JAIS",
                   "research/acmot_paper_v2/Paper1_JAIS/Paper1_V13_JAIS",
                   "JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev11"]:
        assert any(t.startswith(folder + "/") for t in tracked), folder


# ---------------------------------------------------------------- generated docs
def test_inventory_lists_only_tracked_files_and_is_current():
    text = INV.build()
    tracked = set(git("ls-files").splitlines())
    listed = re.findall(r"^### `([^`]+)`", text, re.M)
    assert listed and all(p in tracked for p in listed)
    norm = lambda t: re.sub(r"last commit [^;\n]*", "last commit -", t)  # noqa: E731
    assert norm(text) == norm((CTX / "CODE_INVENTORY.md").read_text())
    assert INV.build() == text  # deterministic


def test_generated_docs_have_no_machine_specific_content():
    for name in ["CODE_INVENTORY.md", "GIT_STATE.md"]:
        text = (CTX / name).read_text()
        assert "/Users/" not in text and "/home/" not in text, name
    assert not re.search(r"^- `\?\? ", (CTX / "GIT_STATE.md").read_text(), re.M)


# ---------------------------------------------------------------- references
def test_knowledge_graph_relations_resolve():
    kg = (CTX / "KNOWLEDGE_GRAPH.md").read_text()
    ents = set(re.findall(r"^\| ([A-Z][\w-]*: [^|]+?) \| [^|]+ \| [^|]+ \| [^|]+ \|$",
                          kg.split("## Relations")[0], re.M))
    rel = kg.split("## Relations")[-1].split("## Code links")[0]
    pairs = re.findall(r"^\| ([^|]+?) \| ([A-Z_]+) \| ([^|]+?) \|$", rel, re.M)
    assert pairs
    for s, _, o in pairs:
        assert s in ents and o in ents, (s, o)
    for ent, _, code in re.findall(r"^\| ([^|]+?) \| ([A-Z_]+) \| ([^|]+?) \|$", kg.split("## Code links")[1], re.M):
        assert (ROOT / code).exists(), code


def test_reproducibility_records_point_to_existing_code_and_configs():
    text = (CTX / "REPRODUCIBILITY.md").read_text()
    refs = re.findall(r"`((?:tools|research|configs|adapters|tests)/[^`\s*<>]+?\.(?:py|md|json|sh|yml))`", text)
    assert len(refs) > 20
    missing = [r for r in refs if not (ROOT / r).exists()]
    assert not missing, missing
    assert "configs/universal_acmot_policy_v7.json" in text and "488df9a" in text


def test_rollback_tools_are_non_destructive():
    for f in ["tools/open_version.sh", "tools/install_git_hooks.sh", ".githooks/pre-commit",
              ".githooks/commit-msg", ".githooks/pre-push"]:
        body = (ROOT / f).read_text()
        for bad in ["reset --hard", "rm -rf", "push --force", "push -f", "clean -f", "tag -d"]:
            assert bad not in body, (f, bad)


# ---------------------------------------------------------------- fast workflow (D-038)
def test_sync_runs_only_the_tests_that_match_the_change():
    import sync_research_memory as SYNC
    assert SYNC.tests_for(["JAIS_PAPERS/PAPER2_X_rev1/main.tex", "research/context/PAPERS.md"], False) == []
    assert SYNC.tests_for(["tools/research_guard.py"], False) == SYNC.PROTECTION_TESTS
    assert SYNC.tests_for([".claude/settings.json"], False) == SYNC.PROTECTION_TESTS
    assert SYNC.tests_for(["tools/sync_research_memory.py"], False) == ["tests/test_research_memory.py"]
    assert SYNC.tests_for(["JAIS_PAPERS/PAPER2_X_rev1/main.tex"], True) == SYNC.PROTECTION_TESTS
    assert not SYNC.graph_relevant("JAIS_PAPERS/PAPER2_X_rev1/sections/01.tex")
    assert SYNC.graph_relevant("research/context/PAPERS.md") and SYNC.graph_relevant("AGENTS.md")


def test_sync_is_non_destructive_and_dry_run_writes_nothing():
    body = (ROOT / "tools" / "sync_research_memory.py").read_text()
    for bad in ["unlink", "rmtree", "os.remove", "git rm", "reset --hard", "push", "commit -", "cmd_complete",
                "cmd_new", "\"complete\"", "\"new\""]:
        assert bad not in body.split('"""', 2)[2], bad
    before = git("status", "--porcelain", "--untracked-files=all")
    stamp = (CTX / "GIT_STATE.md").stat().st_mtime
    out = subprocess.run([sys.executable, "tools/sync_research_memory.py", "--dry-run"], cwd=ROOT,
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert git("status", "--porcelain", "--untracked-files=all") == before
    assert (CTX / "GIT_STATE.md").stat().st_mtime == stamp
