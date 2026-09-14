#!/usr/bin/env bash
# Narrow direct-file guard. Shell/MCP writes remain outside its scope.
set -eu
exec python3 "$(dirname "$0")/file-hooks.py" protect
