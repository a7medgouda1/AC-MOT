#!/bin/sh
# Enable the AC-MOT research hooks for this clone (Mac or Linux). Local git config
# only; reversible with: git config --unset core.hooksPath
set -e
root=$(git rev-parse --show-toplevel)
cd "$root"
current=$(git config --get core.hooksPath || true)
if [ -n "$current" ] && [ "$current" != ".githooks" ]; then
  echo "core.hooksPath is already '$current'; not changing it. Merge .githooks/* into it by hand." >&2
  exit 1
fi
for h in .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push; do
  if [ -f "$h" ]; then echo "note: $h exists and will be bypassed by core.hooksPath; review it." >&2; fi
done
chmod +x .githooks/pre-commit .githooks/commit-msg .githooks/pre-push
git config core.hooksPath .githooks
echo "research hooks enabled: $(git config --get core.hooksPath)"
