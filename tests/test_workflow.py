"""Project-creation regression tests: protect user work and preserve portable roots."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("new_project", ROOT / "scripts/new_project.py")
new_project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(new_project)


class ProjectTests(unittest.TestCase):
    def test_existing_target_is_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing"
            target.mkdir()
            note = target / "my-notes.md"
            note.write_text("user work")
            with self.assertRaises(ValueError):
                new_project.create_project(target)
            self.assertEqual(note.read_text(), "user work")
            self.assertEqual(list(target.iterdir()), [note])

    def test_broken_symlink_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "existing"
            target.symlink_to(Path(tmp) / "missing")
            with self.assertRaises(ValueError):
                new_project.create_project(target)
            self.assertTrue(target.is_symlink())

    def test_project_inside_library_rejected(self):
        with self.assertRaises(ValueError):
            new_project.create_project(ROOT / "must-not-be-created")
        self.assertFalse((ROOT / "must-not-be-created").exists())

    def test_portable_python_project_with_spaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = new_project.create_project(Path(tmp) / "labor project", "python")
            text = (target / "CLAUDE.md").read_text()
            self.assertIn("labor project", text)
            self.assertIn("**python**", text)
            self.assertNotIn("__PROJECT_NAME__", text)
            self.assertFalse((target / "gpt-workflow").exists())
            self.assertFalse((target / ".agents").exists())
            self.assertFalse((target / ".git").exists())
            self.assertFalse((target / ".claude/settings.local.json").exists())
            self.assertEqual(list((target / ".claude/state").iterdir()), [])
            self.assertFalse((target / "research/DECISIONS.md").exists())
            result = subprocess.run([sys.executable, str(target / "scripts/python/00_master.py")],
                                    cwd=tmp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(target), result.stdout)
            self.assertIn("No research analysis", result.stdout)

    def test_stata_does_not_bake_in_absolute_root_or_fake_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = new_project.create_project(Path(tmp) / "stata project")
            setup = (target / "scripts/stata/_setup.do").read_text()
            self.assertNotIn(str(target), setup)
            self.assertIn('confirm file "CLAUDE.md"', setup)
            self.assertIn("exit 198", setup)
            self.assertFalse((target / "paper/main.tex").exists())

    def test_invalid_language_fails_before_creating_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "bad"
            with self.assertRaises(ValueError):
                new_project.create_project(target, "invalid")
            self.assertFalse(target.exists())

    def test_required_helper_missing_fails_before_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            library = Path(tmp) / "library"
            shutil.copytree(ROOT / ".claude", library / ".claude")
            shutil.copytree(ROOT / "templates", library / "templates")
            target = Path(tmp) / "project"
            with self.assertRaisesRegex(ValueError, "scripts/run_check.py"):
                new_project.create_project(target, library=library)
            self.assertFalse(target.exists())

    def test_private_state_excluded_and_generated_hook_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            library = Path(tmp) / "library"
            for folder in (".claude", "templates", "scripts"):
                shutil.copytree(ROOT / folder, library / folder)
            (library / ".claude/state").mkdir(exist_ok=True)
            (library / ".claude/state/active-task.json").write_text('{"task":"private"}')
            (library / ".claude/settings.local.json").write_text('{"private":"not to copy"}')
            target = new_project.create_project(Path(tmp) / "project", library=library)
            self.assertFalse((target / ".claude/settings.local.json").exists())
            self.assertEqual(list((target / ".claude/state").iterdir()), [])
            raw = target / "data/raw/input.csv"
            raw.write_text("id\n1\n")
            payload = {"cwd": str(target), "tool_name": "Edit", "tool_input": {"file_path": str(raw)}}
            result = subprocess.run(["bash", str(target / ".claude/hooks/protect-files.sh")],
                                    input=json.dumps(payload), cwd=target,
                                    env={**os.environ, "CLAUDE_PROJECT_DIR": str(target)},
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"], "deny")
            self.assertEqual(raw.read_text(), "id\n1\n")


if __name__ == "__main__":
    unittest.main()
