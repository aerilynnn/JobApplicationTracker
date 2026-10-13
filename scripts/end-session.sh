#!/usr/bin/env bash
# End a work session: stop the local services (data is kept) and flag any
# work that isn't committed or pushed yet.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "==> Local services"
if docker info >/dev/null 2>&1; then
  # stop (not down -v) keeps the containers and the Postgres data volume
  docker compose stop
else
  echo "Docker isn't running; nothing to stop."
fi

echo
echo "==> Git"
git status -sb
if [ -n "$(git status --porcelain)" ]; then
  echo "You have uncommitted changes."
fi
if git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
  unpushed=$(git log --oneline '@{u}..')
  if [ -n "$unpushed" ]; then
    echo "Commits not pushed yet:"
    echo "$unpushed"
  fi
else
  echo "This branch isn't on GitHub yet."
fi

echo
echo "Before you go, ask Claude for a \"where we left off\" summary."
