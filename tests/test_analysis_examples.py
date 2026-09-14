"""Known-answer and failure tests of run records and documented toy examples."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lint_research import lint_file
from run_check import verify_report


class RunCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="analysis run space ")
        self.root = Path(self.temp.name).resolve()
        self.input = self.root / "input data.txt"
        self.input.write_text("2")
        self.output = self.root / "output data.txt"
        self.report = self.root / "review.json"

    def tearDown(self):
        self.temp.cleanup()

    def run_check(self, program, *, executable=None, report=None):
        command = [sys.executable, str(ROOT / "scripts/run_check.py"),
                   "--cwd", str(self.root), "--input", str(self.input), "--output", str(self.output),
                   "--report", str(report or self.report), "--",
                   executable or sys.executable]
        if executable is None:
            command += ["-c", program]
        return subprocess.run(command, capture_output=True, text=True)

    def test_success_and_stale_input_output_log(self):
        result = self.run_check("from pathlib import Path; Path('output data.txt').write_text(str(int(Path('input data.txt').read_text())*3))")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.output.read_text(), "6")
        self.assertEqual(verify_report(self.report)["status"], "PASS")
        self.input.write_text("3")
        self.assertEqual(verify_report(self.report)["status"], "STALE")
        self.input.write_text("2")
        self.output.write_text("tampered")
        self.assertEqual(verify_report(self.report)["status"], "STALE")
        self.output.write_text("6")
        self.report.with_suffix(".log").write_text("changed log")
        self.assertEqual(verify_report(self.report)["status"], "STALE")

    def test_nonzero_exit_survives_success_looking_output(self):
        self.output.write_text("old")
        result = self.run_check("print('all done'); raise SystemExit(7)")
        self.assertEqual(result.returncode, 7)
        record = json.loads(self.report.read_text())
        self.assertEqual(record["status"], "FAIL")
        self.assertEqual(record["exit_code"], 7)
        self.assertEqual(verify_report(self.report)["status"], "FAIL")

    def test_old_missing_empty_outputs_cannot_pass(self):
        for index, program in enumerate(("pass", "from pathlib import Path; Path('output data.txt').write_text('')")):
            report = self.root / f"review-{index}.json"
            result = self.run_check(program, report=report)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(report.read_text())["status"], "FAIL")
        self.output.write_text("old")
        result = self.run_check("print('no write')")
        self.assertEqual(json.loads(self.report.read_text())["status"], "FAIL")

    def test_unavailable_runtime_and_missing_input_are_not_run(self):
        result = self.run_check("", executable=str(self.root / "not installed"))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(self.report.read_text())["status"], "NOT_RUN")
        self.input.unlink()
        report = self.root / "missing.json"
        result = self.run_check("raise RuntimeError('should not execute')", report=report)
        self.assertEqual(json.loads(report.read_text())["status"], "NOT_RUN")
        self.assertEqual(report.with_suffix(".log").read_text(), "")

    def test_changed_input_during_run_is_stale(self):
        self.run_check("from pathlib import Path; Path('input data.txt').write_text('4'); Path('output data.txt').write_text('12')")
        self.assertEqual(json.loads(self.report.read_text())["status"], "STALE")

    def test_history_cannot_be_overwritten(self):
        self.run_check("from pathlib import Path; Path('output data.txt').write_text('6')")
        old = self.report.read_bytes()
        result = self.run_check("raise SystemExit(9)")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.report.read_bytes(), old)

    def test_no_record_does_not_imply_pass(self):
        self.assertEqual(verify_report(self.root / "absent.json")["status"], "NOT_RUN")

    def test_incomplete_pass_record_is_not_execution_evidence(self):
        self.report.write_text(json.dumps({"status": "PASS", "exit_code": 0,
                                         "command": ["echo", "done"], "inputs": {},
                                         "outputs": {}, "logs": {}}))
        self.assertEqual(verify_report(self.report)["status"], "NOT_RUN")

    def test_input_output_overlap_is_rejected_before_execution(self):
        self.output = self.input
        result = self.run_check("from pathlib import Path; Path('input data.txt').write_text('corrupted')")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.input.read_text(), "2")
        self.assertFalse(self.report.exists())

    def test_parent_symlink_alias_cannot_hide_input_output_overlap(self):
        alias = self.root / "directory alias"
        alias.symlink_to(self.root, target_is_directory=True)
        self.output = alias / self.input.name
        result = self.run_check("raise RuntimeError('must not execute')")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.input.read_text(), "2")
        self.assertFalse(self.report.exists())

    def test_log_suffix_and_dangling_symlinks_do_not_execute(self):
        result = self.run_check("raise RuntimeError('must not execute')", report=self.root / "bad.log")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "bad.log").exists())
        self.report.symlink_to(self.root / "redirected report")
        result = self.run_check("raise RuntimeError('must not execute')")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "redirected report").exists())
        self.report.unlink()
        self.report.with_suffix(".log").symlink_to(self.root / "redirected log")
        result = self.run_check("raise RuntimeError('must not execute')")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "redirected log").exists())
        self.assertFalse(self.report.exists())

    def test_concurrent_same_record_runs_only_once(self):
        program = "from pathlib import Path; import time; Path('marker').write_text('run'); time.sleep(0.1); Path('output data.txt').write_text('6')"
        command = [sys.executable, str(ROOT / "scripts/run_check.py"), "--cwd", str(self.root),
                   "--input", str(self.input), "--output", str(self.output),
                   "--report", str(self.report), "--", sys.executable, "-c", program]
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                     for _ in range(2)]
        for process in processes:
            process.communicate(timeout=10)
        self.assertEqual(sum(p.returncode == 0 for p in processes), 1)
        self.assertEqual(verify_report(self.report)["status"], "PASS")

    def test_malformed_record_is_not_run(self):
        self.report.write_text("[]")
        self.assertEqual(verify_report(self.report)["status"], "NOT_RUN")
        self.report.write_text("{broken")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/run_check.py"), "--verify", str(self.report)],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["status"], "NOT_RUN")


class ExampleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="economic toy space ")
        self.root = Path(self.temp.name).resolve()
        self.script = self.root / "scripts/python/describe.py"
        self.script.parent.mkdir(parents=True)
        reference = (ROOT / ".claude/references/coding-standards-python.md").read_text()
        self.script.write_text(re.findall(r"~~~python\n(.*?)\n~~~", reference, re.S)[0])
        self.data = self.root / "data/cleaned/sample.csv"
        self.data.parent.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def execute(self, rows):
        self.data.write_text(rows)
        return subprocess.run([sys.executable, str(self.script)], cwd=self.root.parent,
                              capture_output=True, text=True)

    def test_descriptive_known_answer_and_source_unchanged(self):
        rows = "group,wage\nA,10\nA,20\nB,5\nB,9\n"
        result = self.execute(rows)
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads((self.root / "paper/tables/group_means.json").read_text())
        self.assertEqual(summary, {"A": {"n": 2, "mean_wage": 15}, "B": {"n": 2, "mean_wage": 7}})
        self.assertEqual(self.data.read_text(), rows)

    def test_empty_bad_and_nonfinite_samples_fail(self):
        for rows in ("group,wage\n", "group,wage\nA,not_a_number\n", "group,wage\nA,nan\n"):
            self.assertNotEqual(self.execute(rows).returncode, 0)

    def test_rng_discard_detected_without_running_numpy(self):
        self.script.write_text("np.random.default_rng(42)\n")
        self.assertTrue(any("discarded" in issue for issue in lint_file(self.script)))
        self.script.write_text("rng = np.random.default_rng(42)\ndraws = rng.normal(size=10)\n")
        self.assertFalse(any("discarded" in issue for issue in lint_file(self.script)))

    def test_stata_example_selects_baseline_before_save(self):
        source = (ROOT / ".claude/references/coding-standards-stata.md").read_text()
        example = re.findall(r"~~~stata\n(.*?)\n~~~", source, re.S)[0]
        # A regression check for the original model mix-up; no Stata execution claim.
        restored = example.index("estimates restore m_baseline")
        self.assertGreater(restored, example.index("estimates store m_subgroup"))
        self.assertLess(restored, example.index("estimates save"))
        self.assertNotIn("tempfile", example)


if __name__ == "__main__":
    unittest.main()
