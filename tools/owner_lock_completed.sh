#!/bin/sh
# OWNER-ONLY: operating-system immutability for completed versions (D-035).
#
# The git hooks, CI and the Claude Code hook block AI changes to completed versions, but a
# program running as your user can still change files on disk. Only flags that your user
# cannot clear make that physically impossible:
#   macOS: system-immutable flag  `sudo chflags -R schg <dir>`  (clearing it needs single-user
#          mode / recovery; `uchg` is weaker: the same user can clear it with `chflags nouchg`)
#   Linux: `sudo chattr -R +i <dir>` (clearing needs root: `sudo chattr -R -i <dir>`)
# Agents must never run with sudo. A locked folder also stops YOU from editing it; new
# versions are new sibling folders and are not affected.
#
#   sh tools/owner_lock_completed.sh            # dry run: print the commands for every completed folder
#   sh tools/owner_lock_completed.sh --apply    # run them (asks for your password via sudo)
set -e
root=$(git rev-parse --show-toplevel)
cd "$root"
paths=$(python3 - <<'EOF'
import json
reg = json.load(open("research/VERSION_REGISTRY.json"))
for e in reg["entries"]:
    if e.get("status") in ("COMPLETED", "FROZEN", "SUPERSEDED") and e.get("kind") == "version_dir":
        print(e["path"])
EOF
)
case "$(uname -s)" in
  Darwin) cmd="sudo chflags -R schg" ;;
  Linux)  cmd="sudo chattr -R +i" ;;
  *) echo "unsupported system" >&2; exit 1 ;;
esac
for p in $paths; do
  if [ "$1" = "--apply" ]; then
    echo "locking $p"; $cmd "$p"
  else
    echo "$cmd \"$p\""
  fi
done
[ "$1" = "--apply" ] || echo "(dry run; add --apply to lock. Archives with new files allowed, e.g. research/final, are not locked.)"
