#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-https://github.com/Neilcc/finance_skills.git}"
BRANCH="${BRANCH:-develop}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT"

python3 scripts/validate_repo.py

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  git init
fi

if git remote | grep -q '^origin$'; then
  git remote set-url origin "$REMOTE"
else
  git remote add origin "$REMOTE"
fi

git branch -M "$BRANCH"
git add .
if git diff --cached --quiet; then
  echo "No staged changes to commit."
else
  git commit -m "Optimize finance research scripts and playbook"
fi
git push -u origin "$BRANCH"
