#!/usr/bin/env python3
"""Create a local Claude research project from this library, without overwriting work."""

import argparse
from pathlib import Path
import shutil
import subprocess


LIBRARY = Path(__file__).resolve().parents[1]
LANGUAGES = ("stata", "python", "r", "julia")


def copy_file(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def render(template, destination, name, language):
    text = template.read_text(encoding="utf-8")
    text = text.replace("__PROJECT_NAME__", name).replace("__LANGUAGE__", language)
    destination.write_text(text, encoding="utf-8")


def create_project(destination, language="stata", init_git=False, library=LIBRARY):
    destination = Path(destination).expanduser().absolute()
    library = Path(library).resolve()
    if language not in LANGUAGES:
        raise ValueError("Choose stata, python, r or julia")
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Destination already exists; nothing changed: {destination}")
    if destination.resolve() == library or library in destination.resolve().parents:
        raise ValueError("Create the research project outside the workflow library")
    for relative in (".claude/settings.json", ".claude/hooks/hooklib.py",
                     ".claude/hooks/file-hooks.py", ".claude/hooks/protect-files.sh",
                     ".claude/hooks/post-edit-lint.sh", ".claude/hooks/pre-compact.py",
                     ".claude/hooks/post-compact-restore.py", "scripts/run_check.py",
                     "scripts/lint_research.py", "templates/project-claude.md",
                     "templates/project-readme.md", "templates/project-brief.md"):
        if not (library / relative).is_file():
            raise ValueError(f"Incomplete library: missing {relative}")
    if init_git and not shutil.which("git"):
        raise ValueError("git is unavailable; omit --git to create a local project")

    # Refusing even an empty existing directory keeps a failed/partial run reviewable.
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copytree(
        library / ".claude", destination / ".claude",
        ignore=shutil.ignore_patterns("state", "settings.local.json", "__pycache__", "*.pyc"),
    )
    shutil.copytree(library / "templates", destination / "templates")
    for directory in ("data/raw", "data/cleaned", "data/temp", "research", "explorations",
                      "quality_reports/plans", "quality_reports/reviews", "quality_reports/runs",
                      "paper/sections", "paper/figures", "paper/tables", "paper/preambles",
                      "paper/talks", "paper/supplementary", "paper/replication",
                      "master_supporting_docs", ".claude/state"):
        (destination / directory).mkdir(parents=True, exist_ok=True)
    for relative in (".gitignore", "Bibliography_base.bib", "paper/latexmkrc",
                     "paper/talks/latexmkrc", "scripts/run_check.py", "scripts/lint_research.py"):
        source = library / relative
        if source.is_file():
            copy_file(source, destination / relative)
    name = destination.name
    for source, target in (("project-claude.md", "CLAUDE.md"), ("project-readme.md", "README.md"),
                           ("project-brief.md", "research/PROJECT_BRIEF.md")):
        render(library / "templates" / source, destination / target, name, language)
    (destination / "MEMORY.md").write_text(
        "# Project memory\n\nRecord confirmed preferences with date and scope; no inferred research facts.\n",
        encoding="utf-8",
    )
    add_language_skeleton(destination, language)
    if init_git:
        subprocess.run(["git", "init", "-b", "main"], cwd=destination, check=True)
    return destination


def add_language_skeleton(destination, language):
    if language == "stata":
        folder = destination / "scripts/stata"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "ado").mkdir()
        (folder / "_setup.do").write_text('''* Run the master from the project root. Pin your actual Stata version before analysis.
capture confirm file "CLAUDE.md"
if _rc {
    display as error "Start Stata in the research project root before running the master."
    exit 198
}
global root "`c(pwd)'"
global rawdata "$root/data/raw"
global workingdata "$root/data/cleaned"
global tempdata "$root/data/temp"
global figure "$root/paper/figures"
global table "$root/paper/tables"
adopath ++ "$root/scripts/stata/ado"
set more off
* Record actual ado versions/sources; do not install or update packages in estimation scripts.
''', encoding="utf-8")
        (folder / "00_master.do").write_text('''do "scripts/stata/_setup.do"
* Add data construction, analysis and output scripts here after defining the research task.
display "Project setup loaded. No research analysis has been run."
''', encoding="utf-8")
    elif language == "python":
        folder = destination / "scripts/python"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "setup.py").write_text('''from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAWDATA = ROOT / "data/raw"
WORKINGDATA = ROOT / "data/cleaned"
FIGURE = ROOT / "paper/figures"
TABLE = ROOT / "paper/tables"
''', encoding="utf-8")
        (folder / "00_master.py").write_text('''from setup import ROOT

if __name__ == "__main__":
    print(f"Project: {ROOT}. No research analysis has been run.")
''', encoding="utf-8")
    elif language == "r":
        folder = destination / "scripts/R"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "00_master.R").write_text('''# Run Rscript scripts/R/00_master.R from the project root.
stopifnot(file.exists("CLAUDE.md"))
ROOT <- normalizePath(".")
message("Project setup only. No research analysis has been run.")
''', encoding="utf-8")
    else:
        folder = destination / "scripts/julia"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "00_master.jl").write_text('''const ROOT = normpath(joinpath(@__DIR__, "..", ".."))
println("Project setup only. No research analysis has been run.")
''', encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--lang", choices=LANGUAGES, default="stata")
    git = parser.add_mutually_exclusive_group()
    git.add_argument("--git", action="store_true", help="Initialize local git only; no commit or remote")
    git.add_argument("--no-git", action="store_true", help="Compatibility option: already the default")
    args = parser.parse_args()
    try:
        result = create_project(args.destination, args.lang, args.git)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Project not completed: {error}\nInspect any partial destination; it is never deleted automatically.\n")
    print(f"Created {result}\nOpen this directory in Claude Code and read CLAUDE.md.")


if __name__ == "__main__":
    main()
