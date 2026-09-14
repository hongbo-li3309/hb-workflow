#!/usr/bin/env python3
"""Restore the same session repeatedly without deleting its snapshot."""
import sys
from hooklib import read_input, restore, warning

if __name__ == "__main__":
    try:
        restore(read_input())
    except (OSError, ValueError, TypeError) as error:
        warning(f"Task restoration NOT_RUN: {error}")
    sys.exit(0)
