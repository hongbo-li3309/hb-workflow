#!/usr/bin/env python3
"""Advisory checks only. Never execute imported modules or analysis scripts."""
import argparse
import ast
from pathlib import Path
import re


def lint_file(path):
    path = Path(path)
    if not path.is_file():
        return [f"NOT_RUN: file missing: {path}"]
    text = path.read_text(encoding="utf-8")
    findings = []
    if path.suffix.lower() == ".py":
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as error:
            findings.append(f"Line {error.lineno}: Python syntax error: {error.msg}")
        else:
            for node in ast.walk(tree):
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    function = node.value.func
                    if isinstance(function, ast.Attribute) and function.attr == "default_rng":
                        findings.append(f"Line {node.lineno}: RNG object is discarded; assign rng and use it for draws.")
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    findings.append(f"Line {node.lineno}: Bare except can hide analysis failure; report a specific error.")
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "//", "*")):
            continue
        if re.search(r"""["'](?:/Users/|/home/|[A-Za-z]:\\)""", line):
            findings.append(f"Line {number}: Machine-specific path; use the project's configured root.")
        if path.suffix.lower() in {".do", ".ado"}:
            if re.search(r'(?i)^\s*save\s+["\x27]?\$rawdata\b', line):
                findings.append(f"Line {number}: Saving to raw data risks changing source evidence.")
            if re.search(r"(?i)^\s*capture\s+(?:noisily\s+)?(?:regress|reghdfe|csdid|ivregress)\b", line):
                findings.append(f"Line {number}: Captured estimation failure must be checked through _rc.")
        if path.suffix.lower() == ".r" and re.search(r"\b1:(?:nrow|length)\(", line):
            findings.append(f"Line {number}: Empty inputs make 1:n unsafe; consider seq_len/seq_along.")
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="scripts")
    args = parser.parse_args()
    target = Path(args.target)
    if target.is_dir():
        files = sorted(p for p in target.rglob("*") if p.suffix.lower() in {".py", ".r", ".jl", ".do", ".ado"})
    else:
        files = [target]
    for path in files:
        for finding in lint_file(path):
            print(f"{path}: {finding}")
    print(f"Static files checked: {len(files)}; analysis execution: NOT_RUN. Findings are advisory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
