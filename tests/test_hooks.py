"""Exercise actual hook entry points with Claude-shaped JSON in temporary projects."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / ".claude/hooks"


class HookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workflow hook space ")
        self.root = Path(self.temp.name).resolve()
        self.env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)}

    def tearDown(self):
        self.temp.cleanup()

    def hook(self, name, payload):
        command = (["bash"] if name.endswith(".sh") else [sys.executable]) + [str(HOOKS / name)]
        result = subprocess.run(command, input=payload if isinstance(payload, str) else json.dumps(payload),
                                capture_output=True, text=True, env=self.env, cwd=self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else None

    def payload(self, filename, tool="Write"):
        return {"session_id": "session-a", "cwd": str(self.root),
                "tool_name": tool, "tool_input": {"file_path": str(filename)}}

    def make_file(self, name, content="original"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_existing_raw_protected_first_creation_allowed(self):
        path = self.root / "data/raw/input with spaces.csv"
        self.assertIsNone(self.hook("protect-files.sh", self.payload(path)))
        self.make_file("data/raw/input with spaces.csv")
        result = self.hook("protect-files.sh", self.payload(path))
        self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(path.read_text(), "original")

    def test_unrelated_settings_and_first_review_allowed(self):
        for name in ("app/settings.json", ".claude/settings.json", "research/strategy-memo-new.md"):
            self.assertIsNone(self.hook("protect-files.sh", self.payload(self.make_file(name))))
        self.assertIsNone(self.hook("protect-files.sh", self.payload(self.root / "quality_reports/reviews/new.md")))
        result = self.hook("protect-files.sh", self.payload(self.make_file("quality_reports/reviews/old.md")))
        self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_resolved_alias_and_external_path_scope(self):
        target = self.make_file("data/raw/keep.csv")
        alias = self.root / "alias.csv"
        alias.symlink_to(target)
        result = self.hook("protect-files.sh", self.payload(alias))
        self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIsNone(self.hook("protect-files.sh", self.payload(self.root.parent / "settings.json")))
        outbound = self.root / "data/raw/external.csv"
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / "source.csv"
            external.write_text("untouched")
            outbound.symlink_to(external)
            result = self.hook("protect-files.sh", self.payload(outbound))
            self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")
            self.assertEqual(external.read_text(), "untouched")

    def test_notebook_tool_and_non_file_tool(self):
        target = self.make_file("data/raw/source.ipynb")
        payload = {"cwd": str(self.root), "tool_name": "NotebookEdit",
                   "tool_input": {"notebook_path": str(target)}}
        self.assertEqual(self.hook("protect-files.sh", payload)["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIsNone(self.hook("protect-files.sh", {"tool_name": "Read"}))

    def test_malformed_input_has_diagnostic_not_success_claim(self):
        result = self.hook("protect-files.sh", "{broken")
        self.assertIn("NOT_RUN", result["systemMessage"])
        result = self.hook("protect-files.sh", {"tool_name": "Edit", "tool_input": None})
        self.assertIn("NOT_RUN", result["systemMessage"])

    def test_stata_do_and_ado_lint_are_static(self):
        for extension in ("do", "ado"):
            path = self.make_file(f"scripts/stata/test.{extension}", 'save "$rawdata/source.dta", replace\n')
            result = self.hook("post-edit-lint.sh", self.payload(path))
            output = result["hookSpecificOutput"]
            self.assertEqual(output["hookEventName"], "PostToolUse")
            self.assertIn("raw data", output["additionalContext"])
            self.assertIn("Analysis execution: NOT_RUN", output["additionalContext"])

    def test_python_syntax_lint_does_not_execute(self):
        path = self.make_file("scripts/python/test.py", "from pathlib import Path\nPath('executed').touch()\nif:\n")
        result = self.hook("post-edit-lint.sh", self.payload(path))
        self.assertIn("syntax error", result["hookSpecificOutput"]["additionalContext"])
        self.assertFalse((self.root / "executed").exists())

    def pointer(self, session, task):
        self.make_file(".claude/state/active-task.json", json.dumps({
            "project_root": str(self.root), "session_id": session, "plan_path": "quality_reports/plans/approved.md",
            "task": task, "next_action": "inspect evidence"}))

    def restore(self, session, source="compact"):
        return self.hook("post-compact-restore.py",
                         {"cwd": str(self.root), "session_id": session, "source": source})

    def test_two_sessions_and_repeated_resume(self):
        self.make_file("quality_reports/plans/approved.md", "# Approved plan")
        for session, task in (("session-a", "estimate wages"), ("session-b", "inspect hiring")):
            self.pointer(session, task)
            self.assertIsNone(self.hook("pre-compact.py", {"cwd": str(self.root), "session_id": session, "trigger": "auto"}))
        for source in ("compact", "resume", "resume"):
            a = self.restore("session-a", source)["hookSpecificOutput"]["additionalContext"]
            b = self.restore("session-b", source)["hookSpecificOutput"]["additionalContext"]
            self.assertIn("estimate wages", a)
            self.assertNotIn("inspect hiring", a)
            self.assertIn("inspect hiring", b)
        self.assertEqual(len(list((self.root / ".claude/state/sessions").glob("*/snapshot.json"))), 2)

    def test_unknown_session_and_unbound_pointer_do_not_guess_plan(self):
        self.make_file("quality_reports/plans/newest.md", "APPROVED\n- [ ] unauthorized task")
        self.pointer(None, "unbound task")
        result = self.hook("pre-compact.py", {"session_id": "new", "cwd": str(self.root)})
        self.assertIn("NOT_RUN", result["systemMessage"])
        text = self.restore("new")["hookSpecificOutput"]["additionalContext"]
        self.assertIn("PROJECT_BRIEF", text)
        self.assertNotIn("unauthorized task", text)
        self.assertIsNone(self.restore("new", source="startup"))

    def test_wrong_project_and_session_cannot_capture(self):
        self.pointer("session-a", "private")
        self.hook("pre-compact.py", {"session_id": "session-b", "cwd": str(self.root)})
        pointer = self.root / ".claude/state/active-task.json"
        task = json.loads(pointer.read_text())
        task["project_root"] = str(self.root / "other")
        pointer.write_text(json.dumps(task))
        result = self.hook("pre-compact.py", {"session_id": "session-a", "cwd": str(self.root)})
        self.assertIn("another project", result["systemMessage"])
        self.assertFalse((self.root / ".claude/state/sessions").exists())

    def test_malformed_pointer_does_not_destroy_saved_session(self):
        self.pointer("session-a", "known task")
        payload = {"session_id": "session-a", "cwd": str(self.root)}
        self.hook("pre-compact.py", payload)
        pointer = self.root / ".claude/state/active-task.json"
        for malformed in ("{broken", "[]", json.dumps({"session_id": "session-a", "task": "bad", "next_action": "bad"})):
            pointer.write_text(malformed)
            result = self.hook("pre-compact.py", payload)
            self.assertIn("NOT_RUN", result["systemMessage"])
            self.assertIn("known task", self.restore("session-a")["hookSpecificOutput"]["additionalContext"])


if __name__ == "__main__":
    unittest.main()
