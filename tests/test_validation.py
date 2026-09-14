"""Make sure structural checks reject real broken dependencies and configuration."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_workflow", ROOT / "scripts/validate_workflow.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def fixture(root):
    (root / "CLAUDE.md").write_text("# Fixture\n")
    for name in checker.SKILLS:
        path = root / ".claude/skills" / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nname: {name}\ndescription: Fixture\n---\n")
    for name in checker.AGENTS:
        path = root / ".claude/agents" / (name + ".md")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nname: {name}\ndescription: Fixture\n---\n")
    for name in checker.CLAUDE_RULES:
        path = root / ".claude/rules" / (name + ".md")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Fixture\n")
    (root / ".claude/settings.json").write_text('{"hooks":{}}')


class ValidatorTests(unittest.TestCase):
    def test_valid_structure_then_broken_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            self.assertEqual(checker.validate(root)[0], [])
            (root / "CLAUDE.md").write_text("[Absent instructions](missing.md)\n")
            self.assertTrue(any("broken local link" in e for e in checker.validate(root)[0]))

    def test_missing_skill_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            (root / ".claude/skills/learn/SKILL.md").unlink()
            self.assertIn("Missing skill: learn", checker.validate(root)[0])

    def test_invalid_json_and_nonexistent_hook_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            settings = root / ".claude/settings.json"
            settings.write_text("{invalid}")
            self.assertTrue(any("invalid JSON" in e for e in checker.validate(root)[0]))
            settings.write_text('{"hooks":{"PreToolUse":[{"hooks":[{"type":"command",'
                                '"command":"bash .claude/hooks/missing.sh"}]}]}}')
            self.assertTrue(any("nonexistent hook" in e for e in checker.validate(root)[0]))


if __name__ == "__main__":
    unittest.main()
