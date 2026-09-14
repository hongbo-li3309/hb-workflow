# Claude hook contracts

Checked against [Claude Code hooks](https://code.claude.com/docs/en/hooks) on 2026-09-13; the installed CLI reported 2.1.267. Tests invoke these scripts with real-shaped JSON. They do not establish that a live Claude session loaded this repository's settings.

- `PreToolUse` receives JSON on stdin. `protect-files.sh` guards existing files only under `data/raw/`, `master_supporting_docs/referee_reports/`, `research/approved/` and `quality_reports/reviews/`. It covers direct `Edit`, `Write` and `NotebookEdit`, including resolved aliases. First creation is allowed. Ordinary settings and draft strategies are editable. A protected history/source file should be preserved and revised or derived under a new path.
- This is a narrow accidental-edit guard, not a filesystem sandbox: Bash, MCP, other tools and external writes are outside its coverage. Do not bypass it through another tool. Permissions and research integrity instructions continue to apply. It does not establish that newly imported raw data are trustworthy.
- `PostToolUse` reads the same JSON and returns `hookSpecificOutput.additionalContext`. Python syntax and a few consequential patterns are inspected; `.do`, `.ado`, `.R` and `.jl` checks are advisory. No analysis is executed and feedback explicitly says `NOT_RUN`.
- `PreCompact` saves a snapshot and returns zero on normal completion. It never edits research decisions, guesses the newest approved plan or copies transcripts. Failure yields a diagnostic and never pretends a snapshot was saved.
- `SessionStart` checks `source=compact|resume`, restores only the matching project/session and preserves the snapshot for repeated resumes. Recovery text is context, not renewed authorization or execution evidence.

The shared pointer `.claude/state/active-task.json` contains:

```json
{
  "project_root": "/actual/project/root",
  "session_id": "actual-session-id-from-runtime",
  "plan_path": "quality_reports/plans/current.md",
  "task": "Current authorized task",
  "next_action": "Concrete next step"
}
```

Use a real runtime session ID only when available. An unbound pointer is a project clue, never a session authorization. Without a matching pointer/snapshot, recovery directs the agent to `research/PROJECT_BRIEF.md` and the user's latest task. It does not adopt another session's task.

Snapshots live at `.claude/state/sessions/<key>/snapshot.json`, where `<key>` is the first 24 hexadecimal characters of SHA256 of the canonical project root, a NUL byte, and `session_id`. A session may keep its own `active-task.json` beside that snapshot; it takes precedence over the shared pointer and must have the same identity fields. Writes are atomic. State is local and should stay out of Git.

`post-merge.sh` is an optional Git reminder and is not installed automatically. `lint-scripts.sh [file-or-directory]` is the standalone advisory entry point and requires `scripts/lint_research.py`. All hooks need Python 3.9+; shell wrappers are invoked through Bash in settings so executable bits are not required.
