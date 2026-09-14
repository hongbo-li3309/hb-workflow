"""Behavioral tests for standalone project creation and explicit, isolated handoffs."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


new_project = module_at('gpt_new_project', ROOT / 'scripts/new_project.py')
checkpoint = module_at('gpt_checkpoint', ROOT / 'scripts/checkpoint.py')


class IndependentProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='gpt workflow isolated ')
        self.base = Path(self.temp.name).resolve()
        self.bundle = self.base / 'standalone GPT bundle'
        shutil.copytree(ROOT, self.bundle,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.workflow-state', '.git'))
        self.generator = module_at('detached_new_project', self.bundle / 'scripts/new_project.py')

    def tearDown(self):
        self.temp.cleanup()

    def test_detached_bundle_creates_four_languages_with_own_runtime(self):
        expected = {'stata': 'scripts/stata/00_master.do', 'python': 'scripts/python/00_master.py',
                    'r': 'scripts/R/00_master.R', 'julia': 'scripts/julia/00_master.jl'}
        for language, entry in expected.items():
            with self.subTest(language=language):
                target = self.base / ('研究 project ' + language)
                self.generator.create_project(target, language)
                self.assertTrue((target / 'AGENTS.md').is_file())
                self.assertIn(language, (target / 'AGENTS.md').read_text())
                self.assertNotIn('__PROJECT_NAME__', (target / 'AGENTS.md').read_text())
                self.assertTrue((target / entry).is_file())
                self.assertEqual(len(list((target / '.agents/skills').glob('*/SKILL.md'))), 12)
                self.assertEqual(len(list((target / '.codex/agents').glob('*.toml'))), 20)
                self.assertFalse((target / '.claude').exists())
                self.assertFalse((target / 'CLAUDE.md').exists())
                self.assertFalse((target / '.git').exists())
                self.assertFalse((target / 'tests').exists())
                self.assertFalse((target / 'scripts/validate_workflow.py').exists())
                for relative in self.generator.RUNTIME_FILES:
                    self.assertTrue((target / relative).is_file())
                if language == 'python':
                    result = subprocess.run([sys.executable, str(target / entry)], cwd=self.base,
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn('No research analysis has been run', result.stdout)
                if language == 'stata':
                    self.assertIn('"AGENTS.md"', (target / 'scripts/stata/_setup.do').read_text())
                if language == 'r':
                    self.assertIn('"AGENTS.md"', (target / entry).read_text())

    def test_existing_target_and_symlink_are_not_overwritten(self):
        target = self.base / 'already here'
        target.mkdir()
        marker = target / 'user draft.md'
        marker.write_text('Keep my draft')
        with self.assertRaises(ValueError):
            self.generator.create_project(target)
        self.assertEqual(marker.read_text(), 'Keep my draft')
        link = self.base / 'shortcut'
        link.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.generator.create_project(link)
        self.assertEqual(marker.read_text(), 'Keep my draft')

    def test_missing_runtime_fails_before_creating_any_destination(self):
        (self.bundle / 'scripts/checkpoint.py').unlink()
        target = self.base / 'incomplete project'
        with self.assertRaisesRegex(ValueError, 'checkpoint.py'):
            self.generator.create_project(target)
        self.assertFalse(target.exists())

    def test_nested_project_is_refused(self):
        target = self.bundle / 'paper project'
        with self.assertRaises(ValueError):
            self.generator.create_project(target)
        self.assertFalse(target.exists())

    def test_private_state_and_other_client_files_are_not_copied(self):
        for relative in ('.codex/auth.json', '.codex/config.local.toml',
                         '.workflow-state/tasks/private.json', '.claude/settings.json',
                         '.git/config', 'data/raw/private.csv', 'research/EVIDENCE_LEDGER.md'):
            path = self.bundle / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('private content')
        target = self.base / 'clean project'
        self.generator.create_project(target)
        for relative in ('.codex/auth.json', '.codex/config.local.toml', '.workflow-state',
                         '.claude', '.git', 'data/raw/private.csv', 'research/EVIDENCE_LEDGER.md'):
            self.assertFalse((target / relative).exists(), relative)

    def test_asset_symlink_is_not_followed_outside_bundle(self):
        source = self.base / 'external source.md'
        source.write_text('must not become a hidden dependency')
        (self.bundle / 'references/external.md').symlink_to(source)
        target = self.base / 'linked project'
        with self.assertRaises(ValueError):
            self.generator.create_project(target)
        self.assertFalse(target.exists())

    @unittest.skipUnless(shutil.which('git'), 'Git is unavailable')
    def test_git_option_creates_local_repo_without_commit_or_remote(self):
        target = self.base / 'local git project'
        self.generator.create_project(target, init_git=True)
        remote = subprocess.run(['git', 'remote'], cwd=target, capture_output=True, text=True)
        self.assertEqual(remote.stdout.strip(), '')
        head = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=target, capture_output=True)
        self.assertNotEqual(head.returncode, 0)


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='gpt task states ')
        self.root = Path(self.temp.name).resolve()
        (self.root / 'AGENTS.md').write_text('# Actual project')
        (self.root / 'research').mkdir()
        self.brief = self.root / 'research/PROJECT_BRIEF.md'
        self.brief.write_text('Current hypothesis; no author approval yet.')

    def tearDown(self):
        self.temp.cleanup()

    def test_separate_tasks_and_repeatable_resume_preserve_public_state(self):
        checkpoint.save_task(self.root, 'intro', 'Revise intro', 'Check claim', session_id='one')
        checkpoint.save_task(self.root, 'model', 'Solve model', 'Check boundary', session_id='two')
        first = checkpoint.load_task(self.root, 'intro', 'one')
        self.assertEqual(first, checkpoint.load_task(self.root, 'intro', 'one'))
        self.assertEqual(checkpoint.load_task(self.root, 'model', 'two')['task'], 'Solve model')
        self.assertEqual(len(checkpoint.list_tasks(self.root)), 2)
        self.assertEqual(self.brief.read_text(), 'Current hypothesis; no author approval yet.')

    def test_wrong_session_cannot_resume_or_overwrite_bound_task(self):
        checkpoint.save_task(self.root, 'intro', 'Revise intro', 'Check claim', session_id='one')
        before = checkpoint.load_task(self.root, 'intro')
        with self.assertRaises(ValueError):
            checkpoint.load_task(self.root, 'intro', 'two')
        with self.assertRaises(ValueError):
            checkpoint.save_task(self.root, 'intro', 'Other work', 'Overwrite', session_id='two')
        self.assertEqual(checkpoint.load_task(self.root, 'intro'), before)

    def test_moved_project_cannot_silently_reuse_prior_task_state(self):
        checkpoint.save_task(self.root, 'intro', 'Revise intro', 'Check claim')
        with tempfile.TemporaryDirectory(prefix='moved project ') as folder:
            moved = Path(folder).resolve()
            (moved / 'AGENTS.md').write_text('# Different project')
            shutil.copytree(self.root / '.workflow-state', moved / '.workflow-state')
            with self.assertRaises(ValueError):
                checkpoint.load_task(moved, 'intro')
            self.assertEqual(checkpoint.list_tasks(moved), [])

    def test_plan_must_exist_within_project_and_dry_run_has_no_write(self):
        for plan in ('missing.md', '../outside.md', str(self.root / 'AGENTS.md')):
            with self.subTest(plan=plan), self.assertRaises(ValueError):
                checkpoint.save_task(self.root, 'intro', 'Task', 'Next', plan=plan)
        plan = self.root / 'plan.md'
        plan.write_text('DRAFT: author has not approved')
        record = checkpoint.save_task(self.root, 'intro', 'Task', 'Next', plan='plan.md', dry_run=True)
        self.assertEqual(record['plan_path'], 'plan.md')
        self.assertFalse((self.root / '.workflow-state').exists())
        self.assertEqual(plan.read_text(), 'DRAFT: author has not approved')

    def test_malformed_or_unknown_state_is_not_accepted(self):
        path = checkpoint.record_path(self.root, 'intro')
        path.parent.mkdir(parents=True)
        path.write_text('{broken')
        with self.assertRaises(ValueError):
            checkpoint.load_task(self.root, 'intro')
        for invalid in ([], {'schema_version': 99},
                        {'schema_version': 1, 'project_root': str(self.root), 'task_key': 'intro'}):
            path.write_text(json.dumps(invalid))
            with self.assertRaises(ValueError):
                checkpoint.load_task(self.root, 'intro')

    def test_state_symlink_outside_project_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='external state ') as outside:
            (self.root / '.workflow-state').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                checkpoint.save_task(self.root, 'intro', 'Task', 'Next')
            self.assertEqual(list(Path(outside).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
