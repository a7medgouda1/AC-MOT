"""
Claude Code PreToolUse hook (.claude/settings.json) for the AC-MOT owner-only-delete
policy (research/context/PRESERVATION_POLICY.md).

Agents may create, write and edit files normally. They may NOT delete, rename/move,
or empty an existing file or directory, nor delete or move a git branch or tag,
without the owner's explicit approval for that exact target. This hook cannot
receive that approval: it blocks every deletion route it recognises, and the owner
performs or approves the deletion through an owner-only action (their own terminal,
or a signed commit trailer checked by CI). There is no environment variable, flag
or file that lets an agent switch it off.

Reads the hook JSON on stdin; exit code 2 blocks the call and the reason on stderr
is shown to the agent. It never modifies anything.

Blocked (inside the repository, and anywhere outside the system temp directories):
- shell deletion: rm, rmdir, unlink, shred, srm, wipe, trash, gio trash/remove,
  truncate, find -delete / -exec rm, xargs rm, rsync --delete / --remove-source-files,
  mv/rename of an existing path or onto an existing file, emptying an existing file
  (`> f`, `: > f`, `cp /dev/null f`);
- git: rm, mv, clean, reset --hard, checkout/restore of paths, stash drop/clear,
  branch -d/-D/-m/-M/-f, tag -d/-f, push --delete / :ref / +ref / --force* / --mirror
  / --prune, update-ref -d, reflog expire/delete, worktree remove/prune, gc --prune,
  filter-branch/filter-repo, rebase, and every hook bypass (--no-verify, commit -n,
  core.hooksPath changes);
- code: python/node/perl/ruby/php snippets (-c / -e / heredoc) and new or changed
  scripts that call file-deletion or rename APIs or shell out to rm/git rm;
- bash -c / sh -c / eval / new or changed shell scripts are checked recursively;
- Edit/Write that empties an existing file (disguised deletion), that edits a
  frozen artifact or a tracked protection file, or that writes an owner-approval
  trailer; any write to Claude settings or .git internals;
- the GitHub MCP delete_file tool.
Files under the system temp directories (outside the repository) may be removed,
so disposable test clones can be cleaned up.
"""
from __future__ import annotations

import glob
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import research_guard as RG  # noqa: E402
import version_registry as VR  # noqa: E402

_REGS: list | None = None


def regs() -> list[dict]:
    """Registry at HEAD and in the working tree: an immutable status in either one wins,
    so editing the working copy cannot unprotect a completed version."""
    global _REGS
    if _REGS is None:
        _REGS = [VR.load("HEAD"), VR.load(None)]
    return _REGS


def completed(rel: str | None) -> tuple[str, dict] | None:
    if not rel:
        return None
    c = VR.classify(rel, regs())
    return c if c and c[0] in ("sealed", "existing", "lock") else None


def active_version(rel: str) -> bool:
    """Inside a registered ACTIVE/DRAFT version that was accepted before (in HEAD) or is new."""
    c = VR.classify(rel, [regs()[1]])
    if not c or c[0] != "active":
        return False
    head_ids = {e["id"] for e in regs()[0].get("entries", [])}
    return c[1]["id"] in head_ids or not VR.exists_at("HEAD", c[1]["path"])


READ_ONLY = {"ls", "cat", "head", "tail", "less", "more", "grep", "egrep", "fgrep", "rg", "ag", "wc", "diff",
             "cmp", "file", "stat", "du", "md5sum", "sha256sum", "shasum", "md5", "pdfinfo", "pdffonts",
             "readlink", "realpath", "basename", "dirname", "tree", "echo", "printf", "test", "[", "true",
             "false", "pwd", "sort", "uniq", "cut", "jq", "xxd", "hexdump", "strings", "git", "cp", "find",
             "sed", "awk", "column", "nl", "od", "comm", "zipinfo", "unzip"}
BUILD_TOOLS = {"pdflatex", "xelatex", "lualatex", "latex", "latexmk", "bibtex", "biber", "makeindex", "make",
               "cmake", "ninja", "pandoc", "convert", "magick", "gs", "pdftk", "qpdf", "inkscape", "soffice",
               "libreoffice", "tectonic", "dvipdfmx", "zip", "tar", "Rscript", "jupyter", "papermill"}

HOME = Path.home()
TEMP_ROOTS = [Path(p).resolve() for p in {"/tmp", "/private/tmp", "/var/folders", "/private/var/folders",
                                          tempfile.gettempdir(), os.environ.get("TMPDIR") or "/tmp"}
              if Path(p).exists()]
# Agent-writable files that could switch the guards off; never written by an agent.
CONFIG_FILES = [ROOT / ".claude" / "settings.json", ROOT / ".claude" / "settings.local.json",
                HOME / ".claude" / "settings.json", HOME / ".claude" / "settings.local.json"]
GUARD_NAMES = ["claude_tool_guard", "research_guard", ".githooks", ".claude/settings", ".claude\\settings",
               "research_guard.yml", "owner_keys", "PRESERVATION_POLICY", "install_git_hooks",
               "tools/codex", ".git/config", ".git/hooks", ".codex/rules"]
# Setting the trusted-key variable (mentioning it in text is fine).
SET_OWNER_KEYS = re.compile(r"ACMOT_OWNER_KEYS['\"]?\s*\]?\s*[:+]?=|\b(export|setenv|unset|declare|typeset|local)\b[^;&|\n]*"
                            r"ACMOT_OWNER_KEYS|putenv|environ\.(setdefault|update|pop)\([^)]*ACMOT_OWNER_KEYS")
TRAILER_ANY = re.compile(r"owner[\s_-]*approved[\s_-]*(completed[\s_-]*)?(delete|change)", re.I)
TRAILER_LINE = re.compile(r"^\s*owner[\s_-]*approved[\s_-]*(completed[\s_-]*)?(delete|change)\s*:", re.I | re.M)

DELETE_CMDS = {"rm", "rmdir", "unlink", "shred", "srm", "wipe", "trash", "trash-put", "trash-rm",
               "truncate"}
WRAPPERS = {"sudo", "env", "nohup", "time", "nice", "ionice", "command", "builtin", "exec", "stdbuf",
            "doas", "caffeinate", "chronic", "busybox", "toybox", "xcrun", "arch", "unbuffer"}
INTERPRETERS = re.compile(r"^(python[\d.]*|pypy[\d.]*|node|nodejs|deno|bun|perl|ruby|php|Rscript)$")
SHELLS = {"bash", "sh", "zsh", "dash", "ksh", "fish"}
DELETE_API = re.compile("|".join([
    r"\bos\.(remove|unlink|rmdir|removedirs|rename|renames|replace|truncate)\s*\(",
    r"\bshutil\.(rmtree|move)\s*\(", r"\bsend2trash\b",
    r"\.(unlink|rmdir)\s*\(", r"\.rename\s*\((?!\s*(columns|index|mapper|axis)\b)",
    r"\b(unlinkSync|rmSync|rmdirSync|renameSync|truncateSync)\b",
    r"\bfs\w*\.(unlink|rm|rmdir|rename|truncate)\b", r"\bpromises\.(unlink|rm|rmdir|rename|truncate)\b",
    r"[\"']fs(/promises)?[\"']\s*\)\s*\.\s*(unlink|rm|rmdir|rename|truncate)\w*\b",
    r"\b(rimraf|emptyDir|removeSync|remove_tree|rmtree)\b",
    r"\bFile\.(delete|unlink|rename)\b", r"\bFileUtils\.(rm|rm_r|rm_rf|rm_f|remove\w*|mv|rmdir)\b",
    r"\bDir\.(delete|rmdir|unlink)\b", r"\bunlink\s*\(?\s*['\"$@]",
    r"[\"'`](rm|rmdir|unlink|shred)(\s|[\"'`])", r"[\"'`]git[\"'`]\s*,\s*[\"'`](rm|clean|mv)[\"'`]",
    r"[\"'`]git\s+(rm|clean|mv)\b",
]))


class Block(Exception):
    pass


# ---------------------------------------------------------------- paths
def resolve(p: str, cwd: Path) -> Path:
    q = Path(os.path.expanduser(p))
    return (q if q.is_absolute() else cwd / q).resolve()


def inside(p: Path, root: Path) -> bool:
    try:
        p.relative_to(root)
        return True
    except ValueError:
        return False


def disposable(p: Path) -> bool:
    """Only paths under the system temp directories and outside this repository."""
    return not inside(p, ROOT) and any(inside(p, t) and p != t for t in TEMP_ROOTS)


def expand(arg: str, cwd: Path) -> list[Path]:
    if "$" in arg or "`" in arg:
        return [ROOT]  # unresolvable here: treat as a repository path
    if any(c in arg for c in "*?["):
        hits = glob.glob(os.path.expanduser(arg) if os.path.isabs(os.path.expanduser(arg))
                         else str(cwd / arg))
        return [Path(h).resolve() for h in hits] or [resolve(arg, cwd)]
    return [resolve(arg, cwd)]


def require_disposable(args: list[str], cwd: Path, what: str) -> None:
    for a in args:
        for p in expand(a, cwd):
            if not disposable(p):
                raise Block(f"{what} of '{a}' ({p}) is a deletion")


def tracked(rel: str) -> bool:
    return subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=ROOT,
                          capture_output=True).returncode == 0


def rel_of(p: Path) -> str | None:
    return str(p.relative_to(ROOT)) if inside(p, ROOT) and p != ROOT else None


def frozen(rel: str) -> bool:
    if active_version(rel) and not completed(rel):
        return False  # registered ACTIVE version: normal editing
    if RG.match(rel, RG.IMMUTABLE) or RG.version_folder(rel):
        return True
    for lock in RG.ACTIVE_LOCKS:
        try:
            if rel in json.loads((ROOT / lock).read_text()).get("file_sha256", {}):
                return True
        except (OSError, ValueError):
            pass
    return False


def unreviewed(p: Path) -> bool:
    """True for code an agent may have written: outside the repo, untracked, or changed
    since the upstream branch. Committed-and-pushed project code runs freely."""
    rel = rel_of(p)
    if rel is None:
        return True
    if not tracked(rel):
        return True
    up = subprocess.run(["git", "diff", "--name-only", "@{upstream}", "--", rel], cwd=ROOT,
                        capture_output=True, text=True)
    if up.returncode != 0:
        up = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", rel], cwd=ROOT,
                            capture_output=True, text=True)
    return bool(up.stdout.strip())


# ---------------------------------------------------------------- shell parsing
HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][\w-]*)\1[^\n]*\n(.*?)\n\s*\2\s*(?:\n|$)", re.S)


def split_heredocs(cmd: str) -> tuple[str, list[str]]:
    bodies: list[str] = []

    def keep(m):
        bodies.append(m.group(3))
        return m.group(0).split("\n", 1)[0] + "\n"
    return HEREDOC.sub(keep, cmd), bodies


def segments(cmd: str) -> list[list[str]]:
    text = cmd.replace("`", " ; ").replace("$(", " ; (").replace("\\\n", " ")
    lex = shlex.shlex(text.replace("\n", " ; "), posix=True, punctuation_chars=";&|()<>")
    lex.whitespace_split = True
    lex.commenters = ""
    try:
        toks = list(lex)
    except ValueError:
        toks = text.replace("\n", " ; ").split()
    segs, cur = [], []
    for t in toks:
        if t and set(t) <= set(";&|()"):
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        segs.append(cur)
    return segs


def strip_prefix(seg: list[str]) -> list[str]:
    i = 0
    while i < len(seg):
        w = seg[i]
        if re.match(r"^[A-Za-z_]\w*=", w):
            i += 1
        elif os.path.basename(w) in WRAPPERS:
            i += 1
            while i < len(seg) and (seg[i].startswith("-") or re.match(r"^[A-Za-z_]\w*=", seg[i])):
                i += 1
        elif os.path.basename(w) == "timeout":
            i += 2
        else:
            break
    return seg[i:]


def redirects(seg: list[str]) -> tuple[list[str], list[tuple[str, str]]]:
    """Split '>' / '>>' / '<' redirections from the words."""
    words, reds, i = [], [], 0
    while i < len(seg):
        t = seg[i]
        if t in (">", ">>", "<", ">|", "&>", "<<", "<<<") and i + 1 < len(seg):
            reds.append((t, seg[i + 1]))
            i += 2
            continue
        if re.fullmatch(r"\d", t) and i + 1 < len(seg) and seg[i + 1] in (">", ">>", "<"):
            i += 1
            continue
        if t in (">&", "<&", ">&-") and i + 1 < len(seg):
            i += 2
            continue
        if t.startswith("&") and len(t) > 1 or re.fullmatch(r"&?\d?>&?\d", t):
            i += 1
            continue
        words.append(t)
        i += 1
    return words, reds


def opts_and_args(words: list[str]) -> tuple[list[str], list[str]]:
    opts, args, end = [], [], False
    for w in words:
        if not end and w == "--":
            end = True
        elif not end and w.startswith("-") and w != "-":
            opts.append(w)
        else:
            args.append(w)
    return opts, args


def check_emptying(name: str, words: list[str], reds, cwd: Path) -> None:
    trivial = name in ("", ":", "true", "false") or (name == "echo" and all(w in ("-n", "-e", '""', "''", "") for w in words[1:])) \
        or (name == "printf" and all(w in ("", '""', "''") for w in words[1:])) \
        or (name == "cat" and words[1:] == ["/dev/null"])
    literal = sum(len(w) for w in words[1:]) if name in ("echo", "printf") else None
    for op, target in reds:
        if op not in (">", ">|", "&>"):
            continue
        p = resolve(target, cwd)
        if not p.is_file() or disposable(p):
            continue
        size = p.stat().st_size
        if trivial and size > 0:
            raise Block(f"emptying existing file {target} is a disguised deletion")
        if literal is not None and size >= RG.SHRINK_MIN and literal < size * RG.SHRINK_RATIO:
            raise Block(f"overwriting {target} ({size} bytes) with a short literal is a disguised deletion")


def check_git(words: list[str], cwd: Path) -> None:
    gdir, i = cwd, 1
    while i < len(words) and words[i].startswith("-"):
        w = words[i]
        if w == "-C" and i + 1 < len(words):
            gdir = resolve(words[i + 1], cwd)
            i += 2
            continue
        if w == "-c" and i + 1 < len(words):
            if "hookspath" in words[i + 1].lower():
                raise Block("changing core.hooksPath disables the deletion guard")
            i += 2
            continue
        i += 1
    if i >= len(words):
        return
    sub, rest = words[i], words[i + 1:]
    if disposable(gdir):
        return  # a disposable clone under the temp directory
    joined = " " + " ".join(rest) + " "
    flags = set(rest)
    short = {c for w in rest if re.fullmatch(r"-[A-Za-z]+", w) for c in w[1:]}
    if "--no-verify" in flags:
        raise Block("--no-verify bypasses the git deletion guard")
    if sub == "config" and "hookspath" in joined.lower():
        reads = {"--get", "--get-all", "--get-regexp", "--list", "-l", "--show-origin", "--show-scope"}
        values = [a for a in rest if not a.startswith("-")]
        if not (flags & reads or (len(values) == 1 and not flags & {"--unset", "--unset-all",
                                                                   "--replace-all", "--add"})):
            raise Block("changing core.hooksPath disables the deletion guard")
    if sub in ("rm", "mv", "clean", "filter-branch", "filter-repo", "rebase"):
        raise Block(f"git {sub} deletes/moves files or rewrites history")
    if sub == "commit" and "n" in short:
        raise Block("git commit -n skips the deletion guard")
    if sub == "reset" and ({"--hard", "--merge", "--keep"} & flags):
        raise Block("git reset --hard discards work")
    if sub == "checkout" and ("--" in flags or "." in flags or "-f" in flags or "--force" in flags or "f" in short):
        raise Block("git checkout of paths / --force overwrites work")
    if sub == "restore" and not (flags <= {"--staged", "-S"} | {a for a in rest if not a.startswith("-")}
                                 and ("--staged" in flags or "-S" in flags) and "--worktree" not in flags and "-W" not in flags):
        raise Block("git restore overwrites working-tree content")
    if sub == "stash" and rest[:1] and rest[0] in ("drop", "clear"):
        raise Block("dropping stashed work")
    if sub == "branch" and (short & {"d", "D", "m", "M", "f", "c", "C"} or
                            flags & {"--delete", "--move", "--force", "--copy"}):
        raise Block("deleting, renaming or force-moving a branch")
    if sub == "tag" and (short & {"d", "f"} or flags & {"--delete", "--force"}):
        raise Block("deleting or moving a tag")
    if sub == "push":
        if (flags & {"--delete", "--force", "--force-with-lease", "--force-if-includes", "--mirror", "--prune"}
                or short & {"d", "f"} or any(w.startswith(("--force-with-lease=", "--delete=")) for w in rest)
                or any(re.match(r"^\+|^:", a) for a in rest if not a.startswith("-"))):
            raise Block("deleting a remote ref or force-pushing")
    if sub == "update-ref" and ("-d" in flags or "--stdin" in flags):
        raise Block("deleting a ref")
    if sub == "reflog" and rest[:1] and rest[0] in ("expire", "delete"):
        raise Block("deleting reflog history")
    if sub == "worktree" and rest[:1] and rest[0] in ("remove", "prune"):
        raise Block("removing a worktree directory")
    if sub == "gc" and any(w.startswith("--prune") for w in rest):
        raise Block("pruning unreachable history")
    if sub == "symbolic-ref" and ("-d" in flags or "--delete" in flags):
        raise Block("deleting a ref")


WRITE_TARGET = re.compile(r"(?:Path|open|writeFileSync|writeFile|appendFileSync|appendFile|copyFileSync|"
                          r"copyFile|copy|copy2|copyfile|File\.write|File\.open)\(\s*[rbuf]*['\"]([^'\"\n]+)['\"]")


def scan_code(code: str, origin: str, inline: bool = True, cwd: Path | None = None) -> None:
    m = DELETE_API.search(code)
    if m:
        raise Block(f"{origin} calls a file-deletion/rename API ({m.group(0).strip()[:40]})")
    if WRITE_API.search(code):
        # literal paths opened/wrapped for writing; dynamic paths are a documented gap
        for lit in WRITE_TARGET.findall(code):
            try:
                guard_write_target(resolve(lit, cwd or ROOT))
            except Block as b:
                raise Block(f"{origin}: {b}")
    if inline and TRAILER_ANY.search(code):
        raise Block(f"{origin} writes an owner-approval trailer")


def script_text(arg: str, cwd: Path) -> str | None:
    p = resolve(arg, cwd)
    if p.is_file() and unreviewed(p):
        try:
            return p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return None
    return None


def check_completed_use(name: str, words: list[str], cwd: Path) -> None:
    """Commands that would regenerate or rewrite a completed version in place: anything that
    is not read-only run from inside a sealed version folder, build tools pointed at a
    completed version, and scripts that live inside a completed version or archive."""
    c = completed(rel_of(cwd))
    if c and c[0] == "sealed" and name not in READ_ONLY and name not in ("cd", "pushd", "popd"):
        raise Block(f"'{name}' run inside completed version {c[1]['id']} can rewrite it; work in the next "
                    "version (python3 tools/version_registry.py new <family>)")
    if name in BUILD_TOOLS:
        for w in words[1:]:
            val = w.split("=", 1)[1] if w.startswith("-") and "=" in w else w
            if val.startswith("-") or not val:
                continue
            c = completed(rel_of(resolve(val, cwd)))
            if c:
                raise Block(f"{name} on completed version {c[1]['id']} would regenerate its outputs; build the next "
                            "version, or reproduce in a read-only worktree (tools/open_version.sh)")
    script = None
    if INTERPRETERS.match(name) or name in SHELLS or name in ("source", "."):
        _, args = opts_and_args(words[1:])
        if not any(w in ("-c", "-e", "-m", "--eval") for w in words):
            script = args[0] if args else None
    elif words[0].startswith(("./", "/", "~")) or "/" in words[0]:
        script = words[0]
    if script:
        c = completed(rel_of(resolve(script, cwd)))
        if c and c[0] in ("sealed", "existing"):
            raise Block(f"{script} belongs to completed {c[1]['id']}; running it in place can overwrite completed "
                        "outputs. Reproduce in a read-only worktree: sh tools/open_version.sh <tag-or-commit>")


def check_segment(seg: list[str], bodies: list[str], cwd: Path, depth: int) -> Path:
    seg = strip_prefix(seg)
    words, reds = redirects(seg)
    name = os.path.basename(words[0]) if words else ""
    check_emptying(name, words, reds, cwd)
    for op, target in reds:
        if op in (">", ">>", ">|", "&>"):
            guard_write_target(resolve(target, cwd))
    if not words:
        return cwd
    if name == "cd":
        return resolve(words[1], cwd) if len(words) > 1 and not words[1].startswith("-") else HOME
    check_completed_use(name, words, cwd)
    if name in ("pushd",) and len(words) > 1:
        return resolve(words[1], cwd)
    if name == "xargs":
        inner = [w for w in words[1:] if not w.startswith("-")]
        if inner:
            check_segment(inner + ["$XARGS_INPUT"], [], cwd, depth)
        return cwd
    opts, args = opts_and_args(words[1:])
    if name in DELETE_CMDS:
        targets = args if name != "truncate" else [a for a in args]
        if not targets and name != "truncate":
            return cwd
        require_disposable(targets or ["$UNKNOWN"], cwd, name)
    elif name == "gio" and args[:1] and args[0] in ("trash", "remove", "rename", "move"):
        require_disposable(args[1:] or ["$UNKNOWN"], cwd, f"gio {args[0]}")
    elif name in ("mv", "rename", "prename", "mmv"):
        if len(args) >= 2:
            require_disposable(args[:-1] if name == "mv" else args, cwd, name)
            dest = resolve(args[-1], cwd)
            if name == "mv" and dest.exists() and not dest.is_dir() and not disposable(dest):
                raise Block(f"mv onto existing file {args[-1]} destroys it")
    elif name == "cp" and args[:1] == ["/dev/null"] and len(args) >= 2:
        p = resolve(args[-1], cwd)
        if p.exists() and not disposable(p):
            raise Block(f"cp /dev/null {args[-1]} empties an existing file")
    elif name in ("cp", "install", "ln", "rsync", "scp") and len(args) >= 2 and not (
            name == "rsync" and any(w.startswith(("--del", "--remove-source-files")) for w in words)):
        guard_copy_dest(args, cwd)
    elif name in ("sed", "gsed") and any(o.startswith(("-i", "--in-place")) or re.fullmatch(r"-[nrEs]*i\S*", o)
                                         for o in opts):
        for a in args:
            guard_write_target(resolve(a, cwd))
    elif name == "tee":
        for a in args:
            guard_write_target(resolve(a, cwd))
    elif name == "dd":
        for w in words[1:]:
            if w.startswith("of="):
                guard_write_target(resolve(w[3:], cwd))
    elif name in ("chmod", "chown", "chgrp", "chattr", "chflags", "setfacl"):
        plain = {"-R", "-v", "-f", "-c", "-h", "-H", "-L", "-P", "-V"}
        toks = [w for w in words[1:] if w not in plain and not w.startswith("--")]
        mode, targets = (toks[0], toks[1:]) if toks else ("", [])
        if not (name == "chmod" and re.fullmatch(r"[ugoa]*\+x", mode)):
            for a in targets:
                guard_write_target(resolve(a, cwd))
    elif name == "find":
        if any(w in ("-delete",) for w in words) or any(
                w in ("-exec", "-execdir", "-ok", "-okdir") and i + 1 < len(words)
                and os.path.basename(words[i + 1]) in DELETE_CMDS | {"mv"}
                for i, w in enumerate(words)):
            roots = [a for a in words[1:] if not a.startswith("-")][:1] or ["."]
            require_disposable(roots, cwd, "find -delete/-exec rm")
    elif name == "rsync" and any(w.startswith(("--delete", "--remove-source-files", "--del")) for w in words):
        require_disposable(args[-1:], cwd, "rsync --delete")
        if any(w == "--remove-source-files" for w in words):
            require_disposable(args[:-1], cwd, "rsync --remove-source-files")
    elif name == "git":
        check_git(words, cwd)
    elif name in SHELLS:
        if "-c" in opts or any(re.fullmatch(r"-\w*c\w*", o) for o in opts):
            code = args[0] if args else ""
            if depth < 4:
                check_bash(code, cwd, depth + 1)
        else:
            src = [b for b in bodies] + [t for t in (script_text(a, cwd) for a in args[:1]) if t]
            for b in src:
                if depth < 4:
                    check_bash(b, cwd, depth + 1)
    elif name in ("source", ".") and args:
        t = script_text(args[0], cwd)
        if t and depth < 4:
            check_bash(t, cwd, depth + 1)
    elif name == "eval":
        if depth < 4:
            check_bash(" ".join(words[1:]), cwd, depth + 1)
    elif INTERPRETERS.match(name):
        if name == "perl" and any(re.fullmatch(r"-[pnlaw0-9]*i(\.\w+)?[pnlaw]*", o) for o in opts):
            for a in args[1:] if "-e" not in words else args:
                guard_write_target(resolve(a, cwd))  # perl -pi -e '...' files (in-place edit)
        code_parts = [(b, True) for b in bodies]
        for i, w in enumerate(words):
            if w in ("-c", "-e", "-E", "--eval", "-p", "--print", "-r") and i + 1 < len(words):
                code_parts.append((words[i + 1], True))
        if "-m" not in words and "-c" not in words and "-e" not in words and "--eval" not in words:
            for a in args[:1]:
                t = script_text(a, cwd)
                if t:
                    code_parts.append((t, False))
        for c, inline in code_parts:
            scan_code(c, f"{name} code", inline, cwd)
    elif words[0].startswith(("./", "/", "~")) or "/" in words[0]:
        t = script_text(words[0], cwd)
        if t:
            first = t.splitlines()[0] if t else ""
            if re.search(r"python|node|perl|ruby|php", first):
                scan_code(t, words[0], inline=False, cwd=cwd)
            elif depth < 4:
                check_bash(t, cwd, depth + 1)
    return cwd


def guard_copy_dest(args: list[str], cwd: Path) -> None:
    dest = resolve(args[-1], cwd)
    targets = [dest] + ([dest / Path(a).name for a in args[:-1]] if dest.is_dir() else [])
    for t in targets:
        guard_write_target(t)
        if t.is_file() and not disposable(t) and RG.match(rel_of(t) or "", RG.APPEND_ONLY):
            raise Block(f"overwriting append-only record {rel_of(t)}")


WRITE_API = re.compile(r"write_text|write_bytes|open\([^)]*['\"][wax+]|\.write\(|writeFileSync|"
                       r"writeFile|appendFile|copyFile|shutil\.copy|os\.chmod|createWriteStream")


def guard_write_target(p: Path) -> None:
    if any(p == c for c in CONFIG_FILES) or inside(p, ROOT / ".git"):
        raise Block(f"agents may not write {p} (it can switch the guards off)")
    rel = rel_of(p)
    c = completed(rel)
    if c:
        raise Block(f"{rel} belongs to completed version {c[1]['id']} ({c[1]['status']}), which is read-only; "
                    "create the next version with: python3 tools/version_registry.py new <family>")
    if rel == VR.REG_REL:
        raise Block("the version registry changes only through tools/version_registry.py (or a checked Edit)")
    if rel and tracked(rel) and (RG.match(rel, RG.PROTECTION) or frozen(rel)):
        raise Block(f"{rel} is a protected file (frozen artifact or deletion guard)")


def check_registry_edit(tool: str, inp: dict, p: Path) -> None:
    """Edit/Write of the registry: the resulting file must satisfy the registry rules."""
    try:
        text = p.read_text(encoding="utf-8") if p.exists() else ""
    except OSError:
        text = ""
    if tool == "Write":
        text = inp.get("content", "")
    else:
        for e in ([inp] if tool == "Edit" else inp.get("edits", [])):
            o, n = e.get("old_string", ""), e.get("new_string", "")
            text = text.replace(o, n) if e.get("replace_all") else text.replace(o, n, 1)
    errs = VR.check_change(regs()[0], VR.load_text(text), lambda q: VR.exists_at("HEAD", q))
    if errs:
        raise Block("version registry change refused: " + "; ".join(m for _, m in errs[:3]))


def check_bash(cmd: str, cwd: Path, depth: int = 0) -> None:
    if TRAILER_ANY.search(cmd):
        raise Block("only the owner writes owner-approval trailers")
    if SET_OWNER_KEYS.search(cmd):
        raise Block("agents may not set or create the trusted owner approval keys")
    low = cmd.replace("\\", "/").lower()
    if any(n.lower() in low for n in GUARD_NAMES) and re.search(
            r"\bgit\s+(apply|am|update-index)\b|\bpatch\b", cmd):
        raise Block("agents may not patch the deletion guard, the hooks or the Claude settings")
    stripped, bodies = split_heredocs(cmd)
    if depth < 4:  # command substitutions run even inside double quotes
        for m in re.finditer(r"\$\(([^()]*)\)|`([^`]*)`", stripped):
            check_bash(m.group(1) or m.group(2) or "", cwd, depth + 1)
    segs = segments(stripped)
    for k, seg in enumerate(segs):
        # heredoc bodies belong to the segment that opened them
        mine = bodies if any(t in ("<<", "<<-") or t.startswith("<<") for t in seg) else []
        if mine:
            bodies = []
        cwd = check_segment(seg, mine, cwd, depth)
    for b in bodies:  # unattached bodies (parser edge cases): still checked
        if TRAILER_ANY.search(b):
            raise Block("only the owner writes owner-approval trailers")


# ---------------------------------------------------------------- edit tools
def new_texts(tool: str, inp: dict) -> list[str]:
    if tool == "Write":
        return [inp.get("content", "")]
    if tool == "Edit":
        return [inp.get("new_string", "")]
    if tool == "MultiEdit":
        return [e.get("new_string", "") for e in inp.get("edits", [])]
    if tool == "NotebookEdit":
        return [inp.get("new_source", "")]
    return []


def resulting_size(tool: str, inp: dict, p: Path) -> int | None:
    try:
        old = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    if tool == "Write":
        return len(inp.get("content", "").strip())
    edits = [inp] if tool == "Edit" else inp.get("edits", []) if tool == "MultiEdit" else []
    text = old
    for e in edits:
        o, n = e.get("old_string", ""), e.get("new_string", "")
        text = text.replace(o, n) if e.get("replace_all") else text.replace(o, n, 1)
    return len(text.strip()) if edits else None


def check_edit(tool: str, inp: dict, cwd: Path) -> None:
    raw = inp.get("file_path") or inp.get("notebook_path") or ""
    if not raw:
        return
    p = resolve(raw, cwd)
    if rel_of(p) == VR.REG_REL:
        check_registry_edit(tool, inp, p)
    else:
        guard_write_target(p)
    rel = rel_of(p)
    if rel and tracked(rel) and frozen(rel):
        raise Block(f"{rel} is a frozen/immutable research artifact; create a new version instead")
    if any(TRAILER_LINE.search(t or "") for t in new_texts(tool, inp)):
        raise Block("only the owner writes owner-approval trailers")
    if p.is_file() and not disposable(p):
        old = p.stat().st_size
        new = resulting_size(tool, inp, p)
        if new is not None and old >= RG.SHRINK_MIN and new < old * RG.SHRINK_RATIO:
            raise Block(f"emptying {raw} ({old} -> ~{new} bytes) is a disguised deletion")


# ---------------------------------------------------------------- entry point
def decide(data: dict) -> str | None:
    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {}) or {}
    cwd = Path(data.get("cwd") or os.getcwd())
    try:
        if tool == "Bash":
            check_bash(inp.get("command", ""), cwd)
        elif tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
            check_edit(tool, inp, cwd)
        elif re.search(r"delete_file|delete_branch|delete_ref|delete_tag|delete_repo", tool) and "github" in tool:
            raise Block(f"{tool} deletes repository content")
    except Block as b:
        return str(b)
    return None


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    try:
        msg = decide(data)
    except Exception as exc:  # fail closed for anything that looks like a deletion
        cmd = json.dumps(data.get("tool_input", {}))
        risky = re.search(r"\b(rm|rmdir|unlink|shred|truncate|mv|find|xargs|git|rsync|eval|python\S*|node|perl|ruby)\b", cmd)
        if data.get("tool_name") == "Bash" and not risky:
            return 0
        if data.get("tool_name") != "Bash" and data.get("tool_name") not in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
            return 0
        msg = f"the deletion guard could not analyse this call ({type(exc).__name__}: {exc})"
    if msg:
        print(f"BLOCKED by the AC-MOT owner-only-delete policy: {msg}. "
              "Do not retry by another route. Stop and ask the owner for explicit approval, naming "
              "the exact target, why it should be removed and the consequences; the owner performs "
              "or approves it themselves (research/context/PRESERVATION_POLICY.md).", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
