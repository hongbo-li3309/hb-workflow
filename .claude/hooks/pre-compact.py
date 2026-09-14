#!/usr/bin/env python3
"""Capture the explicit task for this project and session; never infer approval."""
import sys
from hooklib import capture, read_input, warning

if __name__ == "__main__":
    try:
        capture(read_input())
    except (OSError, ValueError, TypeError) as error:
        warning(f"Task snapshot NOT_RUN: {error}")
    sys.exit(0)
