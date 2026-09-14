#!/usr/bin/env python3
"""Explicit project-local handoffs. A saved record is context, never authorization."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile


def project_root(path):
    root = Path(path).expanduser().resolve()
    if not (root / "AGENTS.md").is_file():
        raise ValueError("Choose a project root containing AGENTS.md")
    return root


def record_path(root, task_key):
    if not task_key.strip():
        raise ValueError("task-key must be a nonempty local task label")
    key = hashlib.sha256(task_key.encode("utf-8")).hexdigest()[:24]
    path = root / ".workflow-state" / "tasks" / (key + ".json")
    try:
        path.resolve().relative_to(root)
    except ValueError:
        raise ValueError("Local task state must remain inside the project")
    return path


def check_record(record, root, task_key, session_id=None):
    if not isinstance(record, dict):
        raise ValueError("Checkpoint must be a JSON object")
    if record.get("schema_version") != 1:
        raise ValueError("Unknown checkpoint schema")
    if record.get("project_root") != str(root) or record.get("task_key") != task_key:
        raise ValueError("Checkpoint belongs to another project or task; use the public brief")
    for field in ("task", "next_action"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"Checkpoint has no valid {field}")
    if session_id is not None and record.get("session_id") != session_id:
        raise ValueError("Checkpoint session does not match; do not inherit its task authorization")
    return record


def load_task(root, task_key, session_id=None):
    root = project_root(root)
    record = json.loads(record_path(root, task_key).read_text(encoding="utf-8"))
    return check_record(record, root, task_key, session_id)


def save_task(root, task_key, task, next_action, plan=None, session_id=None, dry_run=False):
    root = project_root(root)
    if not task.strip() or not next_action.strip():
        raise ValueError("task and next-action must describe real work")
    plan_path = None
    if plan is not None:
        if Path(plan).is_absolute():
            raise ValueError("plan must be a project-relative path")
        resolved = (root / plan).resolve()
        try:
            plan_path = str(resolved.relative_to(root))
        except ValueError:
            raise ValueError("plan must remain inside the project")
        if not resolved.is_file():
            raise ValueError("The specified plan does not exist")
    path = record_path(root, task_key)
    if path.exists():
        previous = load_task(root, task_key)
        if previous.get("session_id") and previous.get("session_id") != session_id:
            raise ValueError("Task key is bound to another session; use its real ID or another task key")
    record = {
        "schema_version": 1,
        "project_root": str(root),
        "task_key": task_key,
        "session_id": session_id,
        "task": task,
        "next_action": next_action,
        "plan_path": plan_path,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if dry_run:
        return record
    path.parent.mkdir(parents=True, exist_ok=True)
    # Atomic replacement prevents an interrupted save from leaving truncated JSON.
    descriptor, temporary = tempfile.mkstemp(prefix="checkpoint-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(record, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return record


def list_tasks(root):
    root = project_root(root)
    directory = root / ".workflow-state" / "tasks"
    try:
        directory.resolve().relative_to(root)
    except ValueError:
        raise ValueError("Local task state must remain inside the project")
    records = []
    for path in sorted(directory.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            raise ValueError(f"Invalid checkpoint record: {path.name}")
        if record.get("project_root") == str(root):
            check_record(record, root, record.get("task_key"))
            records.append({field: record.get(field) for field in
                            ("task_key", "task", "next_action", "session_id", "updated_at")})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    save = commands.add_parser("save")
    save.add_argument("--task-key", required=True)
    save.add_argument("--task", required=True)
    save.add_argument("--next-action", required=True)
    save.add_argument("--plan")
    save.add_argument("--session-id")
    save.add_argument("--dry-run", action="store_true")
    load = commands.add_parser("load")
    load.add_argument("--task-key", required=True)
    load.add_argument("--session-id")
    commands.add_parser("list")
    args = parser.parse_args()
    try:
        if args.command == "save":
            result = save_task(args.project, args.task_key, args.task, args.next_action,
                               args.plan, args.session_id, args.dry_run)
        elif args.command == "load":
            result = load_task(args.project, args.task_key, args.session_id)
        else:
            result = list_tasks(args.project)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Checkpoint not completed: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
