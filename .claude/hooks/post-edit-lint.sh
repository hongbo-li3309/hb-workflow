#!/usr/bin/env bash
# stdin JSON from PostToolUse; advisory static checks, never run analysis.
set -eu
exec python3 "$(dirname "$0")/file-hooks.py" lint
