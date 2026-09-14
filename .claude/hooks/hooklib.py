"""Small helpers for Claude command hooks. No transcript or home-directory writes."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timezone


def read_input():
    payload = json.load(sys.stdin)
    if not isinstance(payload, dict):
        raise ValueError("hook input must be a JSON object")
    return payload


def warning(message):
    print(json.dumps({"systemMessage": message}, ensure_ascii=False))


def context(event, message):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": event, "additionalContext": message}}, ensure_ascii=False))


def project(payload):
    value = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd")
    if not value:
        raise ValueError("project root is missing")
    return Path(value).resolve()


def session_file(root, session_id, name="snapshot.json"):
    if not isinstance(session_id, str) or not session_id:
        raise ValueError("session_id is missing")
    token = hashlib.sha256(f"{root}\0{session_id}".encode()).hexdigest()[:24]
    return root / ".claude/state/sessions" / token / name


def read_json(path):
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def atomic_write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False) as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def capture(payload):
    root, session_id = project(payload), payload.get("session_id")
    destination = session_file(root, session_id)
    local_pointer = destination.with_name("active-task.json")
    pointer = local_pointer if local_pointer.exists() else root / ".claude/state/active-task.json"
    if not pointer.exists():
        warning("Task snapshot NOT_RUN: no explicit active-task.json; no plan was guessed.")
        return
    task = read_json(pointer)
    if task.get("session_id") != session_id:
        warning("Task snapshot NOT_RUN: active task belongs to another or unbound session. Read research/PROJECT_BRIEF.md and the user's current request.")
        return
    if not isinstance(task.get("project_root"), str) or not task["project_root"]:
        raise ValueError("active task requires project_root")
    if Path(task["project_root"]).resolve() != root:
        raise ValueError("active task belongs to another project")
    for key in ("task", "next_action"):
        if not isinstance(task.get(key), str):
            raise ValueError(f"active task requires string field {key}")
    plan = task.get("plan_path")
    if plan:
        plan_path = (root / plan).resolve()
        if not plan_path.is_relative_to(root):
            raise ValueError("plan_path must stay inside this project")
    atomic_write(destination, {**task, "captured_at": datetime.now(timezone.utc).isoformat()})


def restore(payload):
    if payload.get("source") not in {"compact", "resume"}:
        return
    root, session_id = project(payload), payload.get("session_id")
    source = session_file(root, session_id)
    if not source.exists():
        context("SessionStart", "No snapshot for this project/session. Read research/PROJECT_BRIEF.md and the user's latest task; do not infer authorization from another session or the newest plan.")
        return
    snapshot = read_json(source)
    if (snapshot.get("session_id") != session_id or not snapshot.get("project_root")
            or Path(snapshot["project_root"]).resolve() != root):
        raise ValueError("snapshot identity mismatch")
    lines = ["Restored task pointer (recheck current files; this is not execution evidence):",
             f"Project: {root}", f"Task: {snapshot.get('task', '')}",
             f"Next action: {snapshot.get('next_action', '')}"]
    if snapshot.get("plan_path"):
        plan = (root / snapshot["plan_path"]).resolve()
        lines.append(f"Plan: {snapshot['plan_path']}" + (" [missing: NOT_RUN]" if not plan.is_file() else ""))
    lines.append("Read research/PROJECT_BRIEF.md, EVIDENCE_LEDGER.md and DECISIONS.md if present. Recheck git diff and input freshness before using prior results.")
    context("SessionStart", "\n".join(lines))
