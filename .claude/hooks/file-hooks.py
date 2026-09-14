#!/usr/bin/env python3
"""Path-scoped protection and static lint feedback for file-edit tools."""
import json
import os
from pathlib import Path
import sys
from hooklib import context, project, read_input, warning


def main():
    payload = read_input()
    if payload.get("tool_name") not in {"Edit", "Write", "NotebookEdit"}:
        return
    root = project(payload)
    arguments = payload.get("tool_input", {})
    if not isinstance(arguments, dict):
        raise ValueError("tool_input must be a JSON object")
    value = arguments.get("file_path") or arguments.get("notebook_path")
    if not isinstance(value, str) or not value:
        raise ValueError("file tool input has no file_path/notebook_path")
    path = Path(value)
    if not path.is_absolute():
        path = Path(payload.get("cwd") or root) / path
    supplied = Path(os.path.abspath(path))
    path = path.resolve()
    relatives = [p.relative_to(root).as_posix() for p in (supplied, path) if p.is_relative_to(root)]
    if not relatives:
        return  # the normal sandbox/permissions still apply
    relative = relatives[-1]
    if sys.argv[1] == "protect":
        protected = ("data/raw/", "master_supporting_docs/referee_reports/", "research/approved/", "quality_reports/reviews/")
        if (path.exists() or supplied.is_symlink()) and any(p.startswith(protected) for p in relatives):
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse", "permissionDecision": "deny",
                "permissionDecisionReason": f"Existing source/history file: {relative}. Keep this version and write a new derived or revised file. This guard covers direct file tools only; do not bypass it through Bash/MCP."}}))
    elif path.is_relative_to(root) and not relative.startswith(".claude/") and path.suffix.lower() in {".py", ".r", ".jl", ".do", ".ado"}:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
        from lint_research import lint_file
        findings = lint_file(path)
        detail = "\n".join(findings) if findings else "No static finding."
        context("PostToolUse", f"Static lint: {relative}\n{detail}\nAnalysis execution: NOT_RUN. Static checks do not establish estimator validity or reproducibility.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, ImportError) as error:
        warning(f"File hook NOT_RUN: {error}")
