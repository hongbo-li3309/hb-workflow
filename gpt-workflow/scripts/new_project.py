#!/usr/bin/env python3
"""Create a self-contained local GPT/Codex research project without overwriting work."""
import argparse
from pathlib import Path
import shutil
import subprocess

LIBRARY = Path(__file__).resolve().parents[1]
LANGUAGES = ("stata", "python", "r", "julia")
ASSET_DIRS = (".agents/skills", ".codex/agents", "references", "templates")
RUNTIME_FILES = ("scripts/run_check.py", "scripts/lint_research.py", "scripts/checkpoint.py")
REQUIRED_FILES = (".codex/config.toml", "AGENTS.md", ".gitignore", "templates/project-agents.md",
                  "templates/project-readme.md", "templates/project-brief.md", "docs/usage.md",
                  "docs/platform.md") + RUNTIME_FILES


def copy_file(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def render(source, destination, name, language):
    text = source.read_text(encoding="utf-8")
    destination.write_text(text.replace("__PROJECT_NAME__", name).replace("__LANGUAGE__", language),
                           encoding="utf-8")


def create_project(destination, language="stata", init_git=False, library=LIBRARY):
    library = Path(library).resolve()
    destination = Path(destination).expanduser().absolute()
    if language not in LANGUAGES:
        raise ValueError("Choose stata, python, r or julia")
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Destination already exists; nothing changed: {destination}")
    if destination.resolve() == library or library in destination.resolve().parents:
        raise ValueError("Create the research project outside this workflow library")
    for relative in ASSET_DIRS:
        if not (library / relative).is_dir():
            raise ValueError(f"Incomplete library: missing directory {relative}")
    for relative in REQUIRED_FILES:
        if not (library / relative).is_file():
            raise ValueError(f"Incomplete library: missing {relative}")
    # A portable bundle must not obtain its assets from outside itself through links.
    for relative in ASSET_DIRS:
        source = library / relative
        if source.is_symlink() or any(path.is_symlink() for path in source.rglob("*")):
            raise ValueError(f"Resolve asset symlinks inside the bundle first: {relative}")
    if any((library / relative).is_symlink() for relative in REQUIRED_FILES):
        raise ValueError("Required library files must be local files, not symlinks")
    if init_git and not shutil.which("git"):
        raise ValueError("git is unavailable; omit --git for a local project")

    destination.mkdir(parents=True, exist_ok=False)
    for relative in ASSET_DIRS:
        shutil.copytree(library / relative, destination / relative,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.local.*", ".DS_Store"))
    for relative in (".codex/config.toml", ".gitignore", "Bibliography_base.bib", "LICENSE",
                     "paper/latexmkrc", "paper/talks/latexmkrc", "docs/usage.md", "docs/platform.md",
                     "docs/migration.md", "docs/VERSION.md") + RUNTIME_FILES:
        if (library / relative).is_file():
            copy_file(library / relative, destination / relative)
    for directory in ("data/raw", "data/cleaned", "data/temp", "research", "explorations",
                      "quality_reports/plans", "quality_reports/reviews", "quality_reports/runs",
                      "paper/sections", "paper/figures", "paper/tables", "paper/preambles",
                      "paper/talks", "paper/quarto", "paper/supplementary", "paper/replication"):
        (destination / directory).mkdir(parents=True, exist_ok=True)
    for template, target in (("project-agents.md", "AGENTS.md"), ("project-readme.md", "README.md"),
                             ("project-brief.md", "research/PROJECT_BRIEF.md")):
        render(library / "templates" / template, destination / target, destination.name, language)
    (destination / "MEMORY.md").write_text(
        "# Confirmed preferences\n\nRecord date and scope; current findings belong in research/.\n",
        encoding="utf-8")
    add_language_skeleton(destination, language)
    if init_git:
        subprocess.run(["git", "init", "-b", "main"], cwd=destination, check=True)
    return destination


def add_language_skeleton(destination, language):
    if language == "stata":
        folder = destination / "scripts/stata"
        folder.mkdir(parents=True)
        (folder / "ado").mkdir()
        (folder / "_setup.do").write_text("""* Run from the research project root. Set the actual Stata version before analysis.
capture confirm file "AGENTS.md"
if _rc {
    display as error "Start Stata in the research project root."
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
* Record actual ado versions and sources. Do not update packages inside estimation.
""", encoding="utf-8")
        (folder / "00_master.do").write_text('do "scripts/stata/_setup.do"\n'
            '* Add data construction, analysis and outputs for the agreed research task.\n'
            'display "Setup only. No research analysis has been run."\n', encoding="utf-8")
    elif language == "python":
        folder = destination / "scripts/python"
        folder.mkdir(parents=True)
        (folder / "setup.py").write_text('from pathlib import Path\n\n'
            'ROOT = Path(__file__).resolve().parents[2]\n'
            'RAWDATA = ROOT / "data/raw"\nWORKINGDATA = ROOT / "data/cleaned"\n'
            'FIGURE = ROOT / "paper/figures"\nTABLE = ROOT / "paper/tables"\n', encoding="utf-8")
        (folder / "00_master.py").write_text('from setup import ROOT\n\n'
            'if __name__ == "__main__":\n'
            '    print(f"Project: {ROOT}. No research analysis has been run.")\n', encoding="utf-8")
    elif language == "r":
        folder = destination / "scripts/R"
        folder.mkdir(parents=True)
        (folder / "00_master.R").write_text('# Run Rscript scripts/R/00_master.R from the project root.\n'
            'stopifnot(file.exists("AGENTS.md"))\nROOT <- normalizePath(".")\n'
            'message("Setup only. No research analysis has been run.")\n', encoding="utf-8")
    else:
        folder = destination / "scripts/julia"
        folder.mkdir(parents=True)
        (folder / "00_master.jl").write_text('const ROOT = normpath(joinpath(@__DIR__, "..", ".."))\n'
            'println("Setup only. No research analysis has been run.")\n', encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--lang", choices=LANGUAGES, default="stata")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--git", action="store_true", help="Initialize local Git; no commit or remote")
    group.add_argument("--no-git", action="store_true", help="Already the default")
    args = parser.parse_args()
    try:
        result = create_project(args.destination, args.lang, args.git)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Project not completed: {error}\nInspect any partial destination; it is not deleted automatically.\n")
    print(f"Created {result}\nOpen this directory in Codex and read AGENTS.md.")


if __name__ == "__main__":
    main()
