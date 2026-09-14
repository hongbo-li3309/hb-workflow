#!/usr/bin/env python3
"""Check active workflow structure, local references and runtime configuration.

This validates a library edition, not a paper's scientific claims or client execution.
Python 3.9+; optional Ruby/Psych or Python 3.11 tomllib add full syntax parsing.
"""

import argparse
import ast
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote


SKILLS = {"discover", "strategize", "learn", "analyze", "write", "review", "revise",
          "talk", "submit", "checkpoint", "new-project", "tools"}
AGENTS = {"librarian", "librarian-critic", "explorer", "explorer-critic", "strategist",
          "strategist-critic", "theorist", "theorist-critic", "orchestrator", "writer",
          "writer-critic", "storyteller", "storyteller-critic", "editor", "domain-referee",
          "methods-referee", "coder", "coder-critic", "data-engineer", "verifier"}
CLAUDE_RULES = {"agents", "content-invariants", "content-standards", "logging",
                "meta-governance", "quality", "revision", "workflow", "working-paper-format"}


def active_files(root, gpt):
    folders = ["references", ".agents", ".codex"] if gpt else [".claude", "guide", "tutorial"]
    folders += ["templates", "scripts", "tests", "cheatsheets", "explorations"]
    files = [root / ("AGENTS.md" if gpt else "CLAUDE.md"), root / "README.md", root / "MEMORY.md"]
    if gpt:
        folders.append("docs")
    for folder in folders:
        base = root / folder
        if base.exists():
            files.extend(p for p in base.rglob("*") if p.is_file()
                         and not any(part in {"state", "__pycache__", "ARCHIVE"} for part in p.relative_to(root).parts)
                         and p.suffix in {".md", ".qmd", ".py", ".sh", ".json", ".toml"}
                         and p.name not in {"settings.local.json", "lessons-from-day1.md"})
    return sorted(set(p for p in files if p.exists()))


def validate(root):
    root = Path(root).resolve()
    gpt = (root / "AGENTS.md").exists() and not (root / "CLAUDE.md").exists()
    skill_dir = root / (".agents/skills" if gpt else ".claude/skills")
    errors, notes = [], []
    if not (root / ("AGENTS.md" if gpt else "CLAUDE.md")).is_file():
        errors.append("Missing edition entrypoint")
    for name in sorted(SKILLS):
        if not (skill_dir / name / "SKILL.md").is_file():
            errors.append(f"Missing skill: {name}")
    if not gpt:
        for name in sorted(AGENTS):
            if not (root / ".claude/agents" / (name + ".md")).is_file():
                errors.append(f"Missing existing Claude agent: {name}")
        for name in sorted(CLAUDE_RULES):
            if not (root / ".claude/rules" / (name + ".md")).is_file():
                errors.append(f"Missing existing Claude rule: {name}")
    else:
        for name in sorted((AGENTS - {"explorer"}) | {"data-explorer"}):
            if not (root / ".codex/agents" / (name + ".toml")).is_file():
                errors.append(f"Missing GPT agent: {name}")
        if not (root / ".codex/config.toml").is_file():
            errors.append("Missing GPT configuration")

    frontmatters = []
    for path in active_files(root, gpt):
        rel = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as error:
            errors.append(f"{rel}: unreadable: {error}")
            continue
        if path.suffix == ".py":
            try:
                ast.parse(text, filename=str(rel))
            except SyntaxError as error:
                errors.append(f"{rel}: {error}")
        if path.suffix == ".sh":
            result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
            if result.returncode:
                errors.append(f"{rel}: {result.stderr.strip()}")
        if path.suffix == ".json":
            try:
                json.loads(text)
            except ValueError as error:
                errors.append(f"{rel}: invalid JSON: {error}")
        if path.suffix == ".toml":
            try:
                import tomllib
                parsed = tomllib.loads(text)
                if gpt and path.parent == root / ".codex/agents":
                    for field in ("name", "description", "developer_instructions"):
                        if not isinstance(parsed.get(field), str) or not parsed[field].strip():
                            errors.append(f"{rel}: missing agent field {field}")
                    if parsed.get("name") != path.stem:
                        errors.append(f"{rel}: agent name differs from filename")
            except ImportError:
                notes.append("Full TOML parsing NOT_RUN under Python <3.11; run this checker with Python 3.11+.")
            except ValueError as error:
                errors.append(f"{rel}: invalid TOML: {error}")
        if path.name == "SKILL.md" or (not gpt and path.parent == root / ".claude/agents"):
            match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
            if not match:
                errors.append(f"{rel}: missing YAML frontmatter")
            else:
                fields = match.group(1)
                frontmatters.append(path)
                name = re.search(r"^name:\s*['\"]?([a-z0-9-]+)['\"]?\s*$", fields, re.M)
                expected = path.parent.name if path.name == "SKILL.md" else path.stem
                if not name or name.group(1) != expected:
                    errors.append(f"{rel}: name must match {expected}")
                if not re.search(r"^description:\s*\S", fields, re.M):
                    errors.append(f"{rel}: missing description")
                if gpt and re.search(r"^(allowed-tools|argument-hint|context|agent):", fields, re.M):
                    errors.append(f"{rel}: unconverted Claude-specific skill frontmatter")
        if path.suffix not in {".md", ".qmd"}:
            continue
        if sum(line.startswith("```") for line in text.splitlines()) % 2:
            errors.append(f"{rel}: unclosed Markdown code fence")
        # Check literal local Markdown links. Runtime/example paths in code are separate.
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", prose):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            target = unquote(target.split("#", 1)[0].strip("<>"))
            if not target or any(token in target for token in ("[", "]", "*", "<", ">")):
                continue
            destination = (path.parent / target).resolve()
            if not destination.exists():
                errors.append(f"{rel}: broken local link: {target}")
            elif gpt and root not in destination.parents and destination != root:
                errors.append(f"{rel}: link depends on parent library: {target}")
        # References explicitly named as project paths should exist in this edition.
        for target in re.findall(r"(?<![\w./])(?:\.claude/references|\.claude/rules|references)/[a-zA-Z0-9_./-]+\.md", prose):
            if not (root / target).is_file():
                errors.append(f"{rel}: missing reference: {target}")
        if gpt and not rel.parts[0] == "docs":
            for token in ("../.claude/", "$CLAUDE_PROJECT_DIR", "$ARGUMENTS", "EnterPlanMode"):
                if token in prose:
                    errors.append(f"{rel}: unconverted runtime dependency: {token}")
        if not rel.parts[0] in {"tests", "scripts"}:
            for token in ("/Users/hsantanna/", "confirming parallel trends", "Ready for top-5",
                          "efficient under homogeneity", "Both are bug-free"):
                if token in prose:
                    errors.append(f"{rel}: stale or incorrect instruction: {token}")

    if frontmatters and shutil.which("ruby"):
        code = "require 'psych'; ARGV.each { |p| s=File.read(p); m=s.match(/\\A---\\n(.*?)\\n---/m); Psych.safe_load(m[1], aliases: false) }"
        result = subprocess.run(["ruby", "-e", code] + [str(p) for p in frontmatters], capture_output=True, text=True)
        if result.returncode:
            errors.append("YAML parsing failed: " + result.stderr.strip())
    elif frontmatters:
        notes.append("Full YAML parsing NOT_RUN: Ruby/Psych unavailable; required fields and names checked.")

    if not gpt:
        settings = root / ".claude/settings.json"
        try:
            config = json.loads(settings.read_text())
            for groups in config.get("hooks", {}).values():
                for group in groups:
                    for hook in group.get("hooks", []):
                        command = hook.get("command", "")
                        for relative in re.findall(r"\.claude/hooks/[a-zA-Z0-9_.-]+", command):
                            if not (root / relative).is_file():
                                errors.append(f"settings.json: nonexistent hook {relative}")
                        if hook.get("type") == "command" and not command:
                            errors.append("settings.json: empty hook command")
        except (OSError, ValueError, AttributeError, TypeError) as error:
            errors.append(f"Cannot inspect hook configuration: {error}")
    else:
        if (root / ".claude").exists():
            errors.append("GPT edition contains a Claude configuration directory")
        for path in root.rglob("*"):
            if path.is_symlink() and root not in path.resolve().parents:
                errors.append(f"External symlink dependency: {path.relative_to(root)}")
    return errors, sorted(set(notes))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors, notes = validate(args.root)
    for error in errors:
        print("FAIL:", error)
    for note in notes:
        print("NOTE:", note)
    print(f"{'FAIL' if errors else 'PASS'}: workflow structure and reference checks ({len(errors)} errors).")
    print("Client execution, scientific validity and writing quality are separate checks.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
