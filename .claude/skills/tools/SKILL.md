---
name: tools
description: Maintain the research workspace with scoped Git actions, compilation, bibliography checks, lint, context handoff, workflow learning and reviewed upgrades.
argument-hint: "[commit | compile | validate-bib | lint | journal | context | deploy | learn | upgrade] [args]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, Agent, WebSearch, WebFetch
---
# Tools

Use the requested subcommand; do not launch the paper pipeline for maintenance. Preserve existing user changes and actual authorization.

| Subcommand | Action |
|---|---|
| `commit` | Inspect status/diff, run relevant checks, stage explicit related paths, commit. Push if authorized. A commit request alone does not authorize PR merge or public deployment. |
| `compile [file]` | Use the specified document's build command; for new LaTeX skeletons run `latexmk` in its directory. Preserve the compiler exit status and inspect the rendered result. No unrelated paper compilation. |
| `validate-bib` | Compare citation keys with bibliography; check duplicate identities/versions. Existence of a BibTeX entry does not verify that the source supports its sentence. Verify substantive citations from original sources when needed. |
| `lint [path]` | Run `.claude/hooks/lint-scripts.sh` for scoped advisory checks, including Stata. Lexical warnings need review; absence of warnings does not mean execution passed. |
| `journal` | Summarize real decisions and results from current state/evidence; preserve historical logs rather than manufacturing a timeline of agent scores. |
| `context` | Report current task, active plan, modified artifacts, evidence state and next step. Do not claim access to a context usage counter if none is available. |
| `learn` | Extract confirmed, reusable workflow preferences into MEMORY or a proposed skill; distinct from economic learning via `/learn`. |
| `deploy` | Prepare and verify the guide/site using its build tools; publish only under an explicit existing deployment authorization. |
| `upgrade` | Inspect local customization and candidate version, prepare file-level diffs, preserve names/paths/custom state; apply only scoped changes. Never delete the entire `.claude/` directory. |

For library checks: `python3 scripts/validate_workflow.py` and `python3 -m unittest discover -s tests`. From the workflow library, create new projects with `python3 scripts/new_project.py <destination> --lang stata` (or the chosen language); generated research projects do not contain this library initializer or its tests. Do not modify shell startup files or global client configuration unless requested.

When a tool is missing, say which action is NOT_RUN and provide the next concrete command; continue independent work. Do not mask nonzero exit codes with `tail` or `|| true`, claim automatic Git hooks are installed when they are not, or promise a conflict-free upgrade.
