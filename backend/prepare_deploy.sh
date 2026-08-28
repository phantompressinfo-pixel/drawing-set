#!/usr/bin/env bash
# Assembles a self-contained Cloud Functions source directory at
# backend/.deploy/, then prints the gcloud command to deploy it.
#
# Why this exists: Cloud Functions' Python buildpack requires main.py and
# requirements.txt at the top of --source, with no support for a
# subdirectory entry point or an env var to redirect it. But app.py reads
# code-library/ and .claude/skills/us-building-codes/scripts/codesearch.py
# from the repo root, two directories app.py itself doesn't live next to
# once it's the deploy root. So this script builds a flat bundle: app.py
# (renamed to main.py) and code_search.py at the top, with code-library/
# and .claude/skills/us-building-codes/{scripts,references}/ copied in
# as siblings - code_search.py's root-finding logic (see its
# _find_repo_root()) checks for that layout as well as the normal
# checkout layout, so no code changes are needed between the two.
#
# PDFs under code-library/ are skipped - they're for Claude Code to read
# figures from directly (see aspen-pitkin-code/SKILL.md), not something
# this backend's search tools ever open, and they're most of the bulk.
#
# Usage: backend/prepare_deploy.sh

set -euo pipefail
cd "$(dirname "$0")/.."  # repo root

DEST="backend/.deploy"
rm -rf "$DEST"
mkdir -p "$DEST"

cp backend/app.py "$DEST/main.py"
cp backend/code_search.py "$DEST/"
cp backend/requirements.txt "$DEST/"

cp -r code-library "$DEST/code-library"
# Drop pdf/ dirs after the fact rather than requiring rsync (not always
# installed) - finds any pdf/ dir under any jurisdiction, not just the
# ones that existed when this script was written.
find "$DEST/code-library" -type d -name pdf -exec rm -rf {} +

mkdir -p "$DEST/.claude/skills/us-building-codes/scripts"
mkdir -p "$DEST/.claude/skills/us-building-codes/references"
cp .claude/skills/us-building-codes/scripts/codesearch.py \
   "$DEST/.claude/skills/us-building-codes/scripts/"
cp .claude/skills/us-building-codes/references/*.txt \
   "$DEST/.claude/skills/us-building-codes/references/"

echo "Bundled deploy source ready at $DEST"
echo
echo "Deploy with:"
cat <<CMD
  gcloud functions deploy building-code-qa \\
    --gen2 \\
    --runtime=python312 \\
    --region=us-central1 \\
    --source=$DEST \\
    --entry-point=building_code_qa \\
    --trigger-http \\
    --allow-unauthenticated \\
    --set-secrets=ANTHROPIC_API_KEY=anthropic-api-key:latest \\
    --set-env-vars=ALLOWED_ORIGIN=https://sites.google.com
CMD
