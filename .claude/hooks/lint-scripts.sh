#!/usr/bin/env bash
# Standalone advisory linter; .do/.ado are inspected, not executed.
set -eu
exec python3 "$(dirname "$0")/../../scripts/lint_research.py" "$@"
