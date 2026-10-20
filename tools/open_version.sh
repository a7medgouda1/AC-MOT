#!/bin/sh
# Open a historical AC-MOT version for inspection WITHOUT touching current work.
#   tools/open_version.sh <tag|commit|branch> [target-dir]
# Creates a detached git worktree (default ../AC-MOT-versions/<ref>) and makes it
# read-only. Refuses to reuse an existing directory. Close it later with
#   chmod -R u+w <dir> && git worktree remove <dir>
set -e
ref=${1:?usage: tools/open_version.sh <tag|commit|branch> [target-dir]}
root=$(git rev-parse --show-toplevel)
sha=$(git -C "$root" rev-parse --verify "$ref^{commit}")
safe=$(printf '%s' "$ref" | tr '/:' '__')
dir=${2:-"$root/../AC-MOT-versions/$safe"}
if [ -e "$dir" ]; then echo "refusing: $dir already exists" >&2; exit 1; fi
mkdir -p "$(dirname "$dir")"
git -C "$root" worktree add --detach "$dir" "$sha" >/dev/null
chmod -R a-w "$dir"
echo "opened $ref ($sha) read-only at $dir"
