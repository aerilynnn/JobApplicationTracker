#!/usr/bin/env bash
# Start a work session: sign in to AWS, start Docker and the local services,
# then show where the repo stands.
set -euo pipefail
cd "$(dirname "$0")/.."

PROFILE=jobtracker

echo "==> AWS"
if aws sts get-caller-identity --profile "$PROFILE" >/dev/null 2>&1; then
  echo "Already signed in (profile: $PROFILE)."
else
  aws login --profile "$PROFILE"
fi

echo
echo "==> Docker"
if ! docker info >/dev/null 2>&1; then
  echo "Starting Docker Desktop..."
  open -a Docker
  for _ in $(seq 60); do
    docker info >/dev/null 2>&1 && break
    sleep 2
  done
  docker info >/dev/null 2>&1 || { echo "Docker didn't start within 2 minutes. Open Docker Desktop and run this again."; exit 1; }
fi
echo "Docker is running."

echo
echo "==> Local services (Postgres, LocalStack)"
# --wait blocks until the containers report healthy
docker compose up -d --wait
docker compose ps

echo
echo "==> Git"
git status -sb

echo
echo "Ready! Start the API from api/:  uv run fastapi dev app/main.py"
