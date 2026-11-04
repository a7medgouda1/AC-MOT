"""
Completed-version registry for AC-MOT (owner rule D-035: every completed version is
permanently immutable to AI agents; changes go into the next independent version).

The registry research/VERSION_REGISTRY.json is authoritative for immutable status. Each
entry records family, version number, kind, path, status and Git evidence (commit + tree
or blob hashes), so "byte-for-byte unchanged" is checked against Git, not file names.

Statuses: COMPLETED, FROZEN, SUPERSEDED  -> immutable (read-only to AI tools)
          ACTIVE, DRAFT                  -> editable until explicitly completed
Kinds:    version_dir  sealed folder: nothing may be added, changed, renamed or removed
          fileset      archive folder: files present at `commit` are immutable; new files may be added
          lock         a policy lock and the files it hashes (frozen code; may be run, not changed)
          tag          a frozen git tag (must keep pointing at `commit`)

  python3 tools/version_registry.py list [FAMILY]
  python3 tools/version_registry.py next FAMILY            # next version number (registry + Git + filesystem)
  python3 tools/version_registry.py new FAMILY [--from ID] [--graph]
                                                           # exact copy of the latest completed version -> next number, ACTIVE
  python3 tools/version_registry.py complete ID --evidence "why it is final"
  python3 tools/version_registry.py verify [--ref REF] [--worktree]
  python3 tools/version_registry.py render                 # research/context/VERSION_REGISTRY.md

Rules enforced on every registry change (check_change, used by the hooks and CI):
existing entries are never removed; immutable entries never change (except COMPLETED <->
SUPERSEDED / FROZEN); an immutable entry never becomes ACTIVE/DRAFT; families never change;
a new version number is max+1 of everything ever used in that family (registry, Git tree,
filesystem), or carries a documented skip_reason; a new ACTIVE/DRAFT entry must be a NEW path.
"""
from __future__ import annotations

import datetime as _dt
import io
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG_REL = "research/VERSION_REGISTRY.json"
MD_REL = "research/context/VERSION_REGISTRY.md"
CHANGELOG_REL = "research/context/CHANGELOG.md"
IMMUTABLE = {"COMPLETED", "FROZEN", "SUPERSEDED"}
EDITABLE = {"ACTIVE", "DRAFT"}
STATUSES = IMMUTABLE | EDITABLE


# ---------------------------------------------------------------- git helpers
def git(*args: str, check: bool = False, root: Path | None = None) -> str:
    r = subprocess.run(["git", *args], cwd=root or ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def obj(ref: str, path: str) -> str | None:
    """Object id of path at ref (tree or blob), None when absent."""
    r = subprocess.run(["git", "rev-parse", "--verify", "-q", f"{ref}:{path}"], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout.strip() or None


def exists_at(ref: str, path: str) -> bool:
    return obj(ref, path) is not None


def blobs(ref: str, path: str) -> dict[str, str]:
    out = git("ls-tree", "-r", ref, "--", path)
    res = {}
    for line in out.splitlines():
        meta, name = line.split("\t", 1)
        res[name] = meta.split()[2]
    return res


# ---------------------------------------------------------------- registry
def empty() -> dict:
    return {"schema": 1, "families": {}, "entries": []}


def load_text(text: str | None) -> dict:
    if not text:
        return empty()
    try:
        data = json.loads(text)
    except ValueError:
        return {"schema": 1, "families": {}, "entries": [], "_invalid": True}
    data.setdefault("families", {})
    data.setdefault("entries", [])
    return data


def load(ref: str | None = None) -> dict:
    """ref None = working tree, ':' = index, otherwise a commit."""
    if ref is None:
        p = ROOT / REG_REL
        return load_text(p.read_text(encoding="utf-8") if p.exists() else None)
    r = subprocess.run(["git", "show", f"{ref}:{REG_REL}"], cwd=ROOT, capture_output=True, text=True)
    return load_text(r.stdout if r.returncode == 0 else None)


def dump(reg: dict) -> str:
    return json.dumps(reg, indent=2, ensure_ascii=False) + "\n"


def by_id(reg: dict) -> dict[str, dict]:
    return {e["id"]: e for e in reg.get("entries", [])}


def lock_files(entry: dict, ref: str = "HEAD") -> list[str]:
    try:
        text = git("show", f"{entry.get('commit') or ref}:{entry['path']}")
        return [entry["path"]] + list(json.loads(text).get("file_sha256", {}))
    except ValueError:
        return [entry["path"]]


def inside(rel: str, path: str) -> bool:
    return rel == path or rel.startswith(path.rstrip("/") + "/")


def classify(rel: str, regs: list[dict]) -> tuple[str, dict] | None:
    """How `rel` is protected by any of the given registries (HEAD and working copy are
    both passed by the guards, so an immutable status in either one wins).
    Returns ("sealed" | "existing" | "lock", entry) or ("active", entry) or None."""
    active = None
    for reg in regs:
        for e in reg.get("entries", []):
            path, kind, st = e.get("path"), e.get("kind"), e.get("status")
            if not path or kind == "tag":
                continue
            if st in IMMUTABLE:
                if kind == "version_dir" and inside(rel, path):
                    return "sealed", e
                if kind == "fileset" and inside(rel, path):
                    if rel == path or exists_at(e.get("commit") or "HEAD", rel):
                        return "existing", e
                if kind == "lock" and rel in lock_files(e):
                    return "lock", e
            elif st in EDITABLE and kind == "version_dir" and inside(rel, path):
                active = ("active", e)
    return active


# ---------------------------------------------------------------- numbering
def family_numbers(fam: dict, reg: dict, name: str, ref: str | None) -> set[int]:
    """Every version number ever used by the family: registry entries, plus folder or tag
    names matching the family pattern in the Git tree at ref (or the filesystem)."""
    nums = {int(e["version"]) for e in reg.get("entries", [])
            if e.get("family") == name and isinstance(e.get("version"), int)}
    pats = [fam.get("pattern")] + list(fam.get("legacy_patterns", []))
    rx = [re.compile("^" + re.escape(p).replace(r"\{n\}", r"(\d+)") + "$") for p in pats if p]
    names: list[str] = []
    if fam.get("kind") == "tag":
        names = git("tag").split()
    else:
        for root in [fam.get("root")] + list(fam.get("legacy_roots", [])):
            if not root:
                continue
            if ref:
                names += git("ls-tree", "-d", "--name-only", f"{ref}:{root}").split()
            elif (ROOT / root).is_dir():
                names += [p.name for p in (ROOT / root).iterdir() if p.is_dir()]
    for n in names:
        for r in rx:
            m = r.match(n)
            if m:
                nums.add(int(m.group(1)))
    return nums


def next_number(name: str, reg: dict, ref: str | None = "HEAD") -> int:
    fam = reg["families"][name]
    used = family_numbers(fam, reg, name, ref) | family_numbers(fam, reg, name, None)
    return (max(used) + 1) if used else 1


# ---------------------------------------------------------------- change rules
def check_change(old: dict, new: dict, exists_base, base_ref: str = "HEAD") -> list[tuple[str, str]]:
    """Violations (path, message) of a registry change old -> new. exists_base(path) tells
    whether a path existed in the base revision base_ref."""
    out: list[tuple[str, str]] = []
    if new.get("_invalid"):
        return [(REG_REL, "R9 version registry is not valid JSON")]
    for name, fam in old.get("families", {}).items():
        if new.get("families", {}).get(name) != fam:
            out.append((REG_REL, f"R9 version family '{name}' changed or removed (families are fixed)"))
    o, n = by_id(old), by_id(new)
    for eid, e in o.items():
        ne = n.get(eid)
        where = e.get("path") or REG_REL
        if ne is None:
            out.append((where, f"R9 registry entry {eid} removed"))
            continue
        if e.get("status") in IMMUTABLE:
            a = {k: v for k, v in e.items() if k != "status"}
            b = {k: v for k, v in ne.items() if k != "status"}
            if a != b:
                out.append((where, f"R9 completed registry entry {eid} changed"))
            if ne.get("status") not in IMMUTABLE:
                out.append((where, f"R9 completed version {eid} cannot become {ne.get('status')}"))
        else:
            for k in ("family", "version", "kind", "path", "parent", "label"):
                if e.get(k) != ne.get(k):
                    out.append((where, f"R9 registry entry {eid}: field '{k}' changed"))
            if ne.get("status") in IMMUTABLE and not (ne.get("commit") and (ne.get("tree") or ne.get("kind") == "tag")):
                out.append((where, f"R9 {eid} marked {ne.get('status')} without commit/tree evidence"))
    fams = new.get("families", {})
    seen: dict[tuple, str] = {}
    for e in new.get("entries", []):
        key = (e.get("family"), e.get("version"), e.get("variant"))
        if e.get("version") is not None and key in seen:
            out.append((e.get("path") or REG_REL, f"R9 version number reused: {e['id']} and {seen[key]}"))
        seen[key] = e["id"]
    for eid, e in n.items():
        if eid in o:
            continue
        where = e.get("path") or REG_REL
        if e.get("status") not in STATUSES:
            out.append((where, f"R9 {eid}: unknown status {e.get('status')}"))
        fam_name = e.get("family")
        if fam_name not in fams:
            out.append((where, f"R9 {eid}: unknown family {fam_name}"))
            continue
        fam = fams[fam_name]
        if e.get("status") in EDITABLE:
            if not e.get("path") or exists_base(e["path"]):
                out.append((where, f"R9 {eid}: an ACTIVE/DRAFT entry must be a new path, not existing work"))
            if not isinstance(e.get("version"), int):
                out.append((where, f"R9 {eid}: new versions need an integer version number"))
                continue
            used = family_numbers(fam, old, fam_name, base_ref) | {
                int(x["version"]) for x in old.get("entries", [])
                if x.get("family") == fam_name and isinstance(x.get("version"), int)}
            want = (max(used) + 1) if used else 1
            if e["version"] in used:
                out.append((where, f"R9 {eid}: version number {e['version']} already used in {fam_name}"))
            elif e["version"] != want and not str(e.get("skip_reason", "")).strip():
                out.append((where, f"R9 {eid}: next {fam_name} version is {want}, not {e['version']} "
                                   "(a skipped number needs a documented skip_reason)"))
            if fam.get("pattern") and fam.get("root") and e.get("kind") == "version_dir":
                expect = f"{fam['root']}/{fam['pattern'].replace('{n}', str(e['version']))}"
                if e.get("path") != expect:
                    out.append((where, f"R9 {eid}: path must be {expect}"))
        elif e.get("status") in IMMUTABLE and not e.get("commit"):
            out.append((where, f"R9 {eid}: completed entry without commit evidence"))
    return out


# ---------------------------------------------------------------- verification
def verify(reg: dict, ref: str = "HEAD", worktree: bool = False) -> list[str]:
    """Byte-for-byte check of every immutable entry against its recorded Git evidence."""
    fails = []
    for e in reg.get("entries", []):
        if e.get("status") not in IMMUTABLE:
            continue
        kind, path, eid = e.get("kind"), e.get("path"), e["id"]
        if kind == "tag":
            got = git("rev-list", "-n1", e.get("ref", ""), "--").strip()
            if got != e.get("commit"):
                fails.append(f"{eid}: tag {e.get('ref')} -> {got[:9] or 'missing'}, recorded {e.get('commit', '')[:9]}")
            continue
        if kind == "version_dir":
            if obj(ref, path) != e.get("tree"):
                fails.append(f"{eid}: {path} differs from recorded tree {e.get('tree', '')[:9]} at {ref}")
        elif kind == "fileset":
            before, now = blobs(e["commit"], path), blobs(ref, path)
            changed = [p for p, b in before.items() if now.get(p) != b]
            if changed:
                fails.append(f"{eid}: {len(changed)} completed file(s) changed or missing, e.g. {changed[:3]}")
        elif kind == "lock":
            for p in lock_files(e):
                if obj(ref, p) != obj(e["commit"], p):
                    fails.append(f"{eid}: {p} differs from {e['commit'][:9]}")
        if worktree and path and kind in ("version_dir", "fileset", "lock"):
            st = git("status", "--porcelain", "--untracked-files=all", "--", path).splitlines()
            if kind == "fileset":
                st = [l for l in st if exists_at(e["commit"], l[3:].split(" -> ")[0])]
            if kind == "lock":
                files = set(lock_files(e))
                st = [l for l in git("status", "--porcelain", "--", *files).splitlines()]
            if st:
                fails.append(f"{eid}: working tree differs: {st[:3]}")
    return fails


# ---------------------------------------------------------------- outputs
def render(reg: dict) -> str:
    lines = ["# VERSION REGISTRY (generated from research/VERSION_REGISTRY.json — do not edit by hand)", "",
             "Authoritative immutable status of completed versions (D-035). COMPLETED / FROZEN / SUPERSEDED",
             "entries are read-only to AI agents; changes go into the next version created with",
             "`python3 tools/version_registry.py new <family>`. Rules: PRESERVATION_POLICY.md section 6.", ""]
    lines += ["## Families and next version", "", "| Family | Title | Kind | Pattern | Next |", "|---|---|---|---|---|"]
    for name, fam in sorted(reg.get("families", {}).items()):
        try:
            nxt = f"V{next_number(name, reg)}" if fam.get("pattern") else "— (no sequence)"
        except Exception:  # noqa: BLE001 - informative only
            nxt = "?"
        lines.append(f"| {name} | {fam.get('title', '')} | {fam.get('kind', 'version_dir')} | "
                     f"`{fam.get('pattern', '')}` | {nxt} |")
    lines += ["", "## Entries", "", "| ID | Status | Kind | Path / ref | Commit | Parent | Evidence |",
              "|---|---|---|---|---|---|---|"]
    for e in reg.get("entries", []):
        lines.append(f"| {e['id']} | {e.get('status')} | {e.get('kind')} | `{e.get('path') or e.get('ref')}` | "
                     f"{(e.get('commit') or '')[:9]} | {e.get('parent') or ''} | "
                     f"{str(e.get('evidence', '')).replace('|', '/')} |")
    lines += ["", "Not registered (completion status NOT decided; owner to classify): `THESIS/`, `notebooks/`,",
              "presentations, root-level research scripts outside the locks.", ""]
    return "\n".join(lines)


def save(reg: dict) -> None:
    errs = check_change(load("HEAD"), reg, lambda p: exists_at("HEAD", p))
    if errs:
        raise SystemExit("refused: " + "; ".join(m for _, m in errs))
    (ROOT / REG_REL).write_text(dump(reg), encoding="utf-8")
    (ROOT / MD_REL).write_text(render(reg), encoding="utf-8")


def changelog(line: str) -> None:
    p = ROOT / CHANGELOG_REL
    text = p.read_text(encoding="utf-8").rstrip("\n")
    p.write_text(text + "\n" + line + "\n", encoding="utf-8")


# ---------------------------------------------------------------- commands
def cmd_new(argv: list[str]) -> int:
    reg = load()
    name = argv[0]
    if name not in reg["families"]:
        raise SystemExit(f"unknown family {name}")
    fam = reg["families"][name]
    if fam.get("kind") == "tag":
        raise SystemExit("tag families get new versions by freezing a new tag (owner action)")
    members = sorted((e for e in reg["entries"] if e.get("family") == name and e.get("kind") == "version_dir"
                      and isinstance(e.get("version"), int)), key=lambda e: e["version"])
    src = by_id(reg).get(argv[argv.index("--from") + 1]) if "--from" in argv else (members[-1] if members else None)
    if src is None:
        raise SystemExit("no source version found")
    if src.get("status") in EDITABLE:
        raise SystemExit(f"{src['id']} is {src['status']}: edit it directly, or complete it before starting a new version")
    n = next_number(name, reg)
    dest = f"{fam['root']}/{fam['pattern'].replace('{n}', str(n))}"
    if (ROOT / dest).exists() or exists_at("HEAD", dest):
        raise SystemExit(f"refused: {dest} already exists")
    # exact copy of the completed version from Git (byte-for-byte, recorded tree)
    data = subprocess.run(["git", "archive", "--format=tar", f"{src['commit']}:{src['path']}"], cwd=ROOT,
                          capture_output=True, check=True).stdout
    (ROOT / dest).mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        tf.extractall(ROOT / dest, filter="tar") if hasattr(tarfile, "data_filter") else tf.extractall(ROOT / dest)
    head = git("rev-parse", "HEAD").strip()
    entry = {"id": f"{name}/V{n}", "family": name, "version": n, "label": Path(dest).name, "kind": "version_dir",
             "path": dest, "status": "ACTIVE", "parent": src["id"], "parent_commit": src["commit"],
             "parent_tree": src.get("tree"), "created": _dt.date.today().isoformat(), "created_at_head": head,
             "evidence": f"copy of {src['id']} ({src['commit'][:9]}) by tools/version_registry.py"}
    reg["entries"].append(entry)
    save(reg)
    changelog(f"- {entry['created']}: new version {entry['id']} at `{dest}` (ACTIVE), exact copy of "
              f"{src['id']} (commit {src['commit'][:9]}, tree {str(src.get('tree'))[:9]}); registry updated.")
    print(f"created {dest} as {entry['id']} (ACTIVE) from {src['id']}")
    if "--graph" in argv:
        gp = ROOT / "graphify-out" / ".graphify_python"
        py = gp.read_text().strip() if gp.exists() else sys.executable
        subprocess.run([py, str(ROOT / "tools" / "build_context_graph.py")], cwd=ROOT)
    return 0


def cmd_complete(argv: list[str]) -> int:
    reg = load()
    eid = argv[0]
    if "--evidence" not in argv:
        raise SystemExit("--evidence is required (why this version is final)")
    ev = argv[argv.index("--evidence") + 1]
    e = by_id(reg).get(eid)
    if not e or e.get("status") not in EDITABLE:
        raise SystemExit(f"{eid} is not an ACTIVE/DRAFT entry")
    if git("status", "--porcelain", "--untracked-files=all", "--", e["path"]).strip():
        raise SystemExit(f"commit {e['path']} first: completion records the committed tree")
    tree = obj("HEAD", e["path"])
    if not tree:
        raise SystemExit(f"{e['path']} is not in HEAD")
    e.update(status="COMPLETED", commit=git("log", "-1", "--format=%H", "--", e["path"]).strip(), tree=tree,
             evidence=ev, completed=_dt.date.today().isoformat())
    save(reg)
    changelog(f"- {e['completed']}: {eid} COMPLETED at {e['commit'][:9]} (tree {tree[:9]}): {ev}")
    print(f"{eid} COMPLETED")
    return 0


def bootstrap_acmot() -> dict:
    """Initial AC-MOT registry (2026-10-20). Classification evidence is written into each
    entry; nothing is marked completed only because a folder exists."""
    head = git("rev-parse", "HEAD", check=True).strip()

    def last(path: str) -> str:
        return git("log", "-1", "--format=%H", "--", path).strip() or head

    reg = empty()
    reg["families"] = {
        "paper1": {"title": "Paper 1 AC-MOT operating-point controller (JAIS)", "kind": "version_dir",
                   "root": "research/acmot_paper_v2/Paper1_JAIS", "pattern": "Paper1_V{n}_JAIS",
                   "legacy_roots": ["research/acmot_paper_v2/Paper1_Springer_Template"],
                   "legacy_patterns": ["Paper1_V{n}"]},
        "paper2": {"title": "Paper 2 SCL / frozen V7f (JRTIP)", "kind": "version_dir",
                   "root": "JAIS_PAPERS", "pattern": "PAPER2_V7F_JRTIP_challenge_rev{n}"},
        "universal-acmot": {"title": "Universal AC-MOT system (frozen tags)", "kind": "tag",
                            "pattern": "universal-acmot-v{n}-freeze",
                            "skips": {"2": "V2b/V2cA were development policies, never frozen (FROZEN_VERSIONS.md)",
                                      "5": "V5-TF was never frozen; its lock was rejected by audit (FX-18)"}},
        "legacy-manuscripts": {"title": "earlier manuscript drafts (no sequential number)", "kind": "version_dir"},
        "archives": {"title": "completed results, evidence and frozen configuration files", "kind": "fileset"},
        "policy-locks": {"title": "policy locks of frozen systems", "kind": "lock"},
        "tags": {"title": "other frozen git tags", "kind": "tag"},
    }
    E = reg["entries"]

    def vdir(fam, ver, path, status, evidence, variant=None, label=None):
        e = {"id": f"{fam}/V{ver}" + (f"-{variant}" if variant else "") if ver is not None else f"{fam}/{Path(path).name}",
             "family": fam, "version": ver, "label": label or Path(path).name, "kind": "version_dir", "path": path,
             "status": status, "commit": last(path), "tree": obj("HEAD", path), "evidence": evidence}
        if variant:
            e["variant"] = variant
        E.append(e)

    p1 = "research/acmot_paper_v2"
    for v, rev in [(1, 10), (2, 11), (3, 12)]:
        vdir("paper1", v, f"{p1}/manuscript_jrtip_supervisor_rev{rev}", "SUPERSEDED",
             "PAPERS.md 'Paper1_V1-V3 = manuscript_jrtip_supervisor_rev10-rev12' (order rev10->V1 assumed; "
             "NEEDS VERIFICATION)", variant="jrtip")
    for v in (4, 5, 6):
        vdir("paper1", v, f"{p1}/Paper1_Springer_Template/Paper1_V{v}", "SUPERSEDED",
             "PAPERS.md Paper 1 version history (Springer template)", variant="springer")
    for v in range(6, 14):
        st, ev = "SUPERSEDED", "PAPERS.md Paper 1 version history"
        if v == 12:
            st, ev = "COMPLETED", "submitted to JAIS 18-Oct-2026, manuscript 2026-10-I012138 (PAPERS.md)"
        if v == 13:
            st, ev = "COMPLETED", "delivered package for the revision (PDF + Overleaf zip), pushed e8428eb (PAPERS.md)"
        vdir("paper1", v, f"{p1}/Paper1_JAIS/Paper1_V{v}_JAIS", st, ev, variant="jais" if v == 6 else None)
    for v in range(1, 12):
        vdir("paper2", v, f"JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_rev{v}",
             "COMPLETED" if v == 11 else "SUPERSEDED",
             "delivered Paper2_V11, internally reviewed (D-031), pushed dbf162c" if v == 11
             else "PAPERS.md Paper 2 version history")
    for path in ["JAIS_PAPERS/PAPER1_SCENE_ADAPTIVE_JAIS", "JAIS_PAPERS/PAPER2_SIVP_SPRINGER",
                 "JAIS_PAPERS/PAPER2_UNIVERSAL_ACMOT_JAIS", "JAIS_PAPERS/PAPER2_V7F_JRTIP_challenge_v1",
                 "JAIS_PAPERS/PAPER2_V7F_JRTIP_full_v1", "JAIS_PAPERS/PAPER2_V7F_JRTIP_full_rev1",
                 f"{p1}/manuscript_jrtip_supervisor_blind_challenge_v1", f"{p1}/manuscript_jrtip_supervisor_rev1_single"] + \
            [f"{p1}/manuscript_jrtip_supervisor_rev{r}" for r in range(1, 10)]:
        vdir("legacy-manuscripts", None, path, "SUPERSEDED",
             "earlier committed draft, superseded by the numbered versions (PAPERS.md); protected by R3 since 2026-10-20")
    tag_status = {"universal-acmot-v7-freeze": "FROZEN"}
    for t in git("tag").split():
        sha = git("rev-list", "-n1", t, "--").strip()
        m = re.match(r"^universal-acmot-v(\d+)-freeze$", t)
        E.append({"id": f"universal-acmot/V{m.group(1)}" if m else f"tags/{t}",
                  "family": "universal-acmot" if m else "tags", "version": int(m.group(1)) if m else None,
                  "label": t, "kind": "tag", "ref": t, "path": None,
                  "status": tag_status.get(t, "SUPERSEDED" if m else "FROZEN"), "commit": sha,
                  "evidence": "FROZEN_VERSIONS.md" + (" (FINAL TARGET, Amendment 10)" if t in tag_status else "")})
    for lock, st in [("research/V7_POLICY_LOCK.json", "FROZEN"), ("research/V6TF_POLICY_LOCK.json", "SUPERSEDED"),
                     ("research/GENERAL_ACMOT_G1_LOCK.json", "FROZEN")]:
        E.append({"id": f"policy-locks/{Path(lock).stem}", "family": "policy-locks", "version": None,
                  "label": Path(lock).name, "kind": "lock", "path": lock, "status": st, "commit": last(lock),
                  "evidence": "active policy lock (R1); files may be run but not changed"})
    archives = ["research/final", "research/acmot_paper_v2", "research/paper_split/evidence",
                "research/transfer_legacy", "research/published_papers", "research/cue_audit",
                "research/uavdt_protocol", "JAIS_PAPERS/overleaf", "research/TRAIN_SPLIT_V5.json",
                "configs/g2_gsci_frozen.json", "configs/general_acmot_g1.json"]
    archives += sorted(git("ls-files", "configs/universal_acmot_policy*.json").split())
    archives += sorted(p for p in git("ls-files", "research/*LOCK*.json").split()
                       if p not in ("research/V7_POLICY_LOCK.json", "research/V6TF_POLICY_LOCK.json",
                                    "research/GENERAL_ACMOT_G1_LOCK.json"))
    for path in archives:
        E.append({"id": f"archives/{path}", "family": "archives", "version": None, "label": Path(path).name,
                  "kind": "fileset", "path": path, "status": "COMPLETED", "commit": head, "tree": obj("HEAD", path),
                  "evidence": "committed results/evidence/frozen config (immutable since R2, 2026-10-20); "
                              "new files may be added, existing ones never change"})
    return reg


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "list":
        for e in load()["entries"]:
            if not rest or e.get("family") == rest[0]:
                print(f"{e['id']:<34} {e.get('status'):<10} {e.get('kind'):<11} {e.get('path') or e.get('ref')}")
        return 0
    if cmd == "next":
        print(f"V{next_number(rest[0], load())}")
        return 0
    if cmd == "new":
        return cmd_new(rest)
    if cmd == "complete":
        return cmd_complete(rest)
    if cmd == "bootstrap-acmot":
        if (ROOT / REG_REL).exists():
            raise SystemExit("refused: the registry already exists (it is append-only)")
        reg = bootstrap_acmot()
        (ROOT / REG_REL).write_text(dump(reg), encoding="utf-8")
        (ROOT / MD_REL).write_text(render(reg), encoding="utf-8")
        print(f"wrote {REG_REL} ({len(reg['entries'])} entries) and {MD_REL}")
        return 0
    if cmd == "render":
        (ROOT / MD_REL).write_text(render(load()), encoding="utf-8")
        print(f"wrote {MD_REL}")
        return 0
    if cmd == "verify":
        ref = rest[rest.index("--ref") + 1] if "--ref" in rest else "HEAD"
        fails = verify(load(None if "--worktree" in rest else ref), ref, "--worktree" in rest)
        for f in fails:
            print(f"[FAIL] {f}")
        n = sum(1 for e in load()["entries"] if e.get("status") in IMMUTABLE)
        print(f"{'FAIL' if fails else 'PASS'}: {n} immutable entries checked against Git evidence")
        return 1 if fails else 0
    raise SystemExit(f"unknown command {cmd}")


if __name__ == "__main__":
    sys.exit(main())
