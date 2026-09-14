#!/usr/bin/env python3
"""Run an argv command and record current evidence; no shell evaluation or auto-install.

Example:
python3 scripts/run_check.py --input scripts/python/main.py --input data/cleaned/panel.csv \
  --output paper/tables/main.csv --report quality_reports/runs/run_main.json \
  -- python3 scripts/python/main.py

Use --verify REPORT to detect changed inputs/outputs. Only explicitly declared files
are covered; include code, data, configuration and environment manifests as inputs.
A command must refresh each declared output; cached artifacts alone cannot pass.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def fingerprint(path):
    path = Path(path)
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"sha256": digest.hexdigest(), "size": path.stat().st_size}


def file_state(path):
    value = fingerprint(path)
    return None if value is None else {**value, "mtime_ns": Path(path).stat().st_mtime_ns}


def verify_report(path):
    if not Path(path).is_file():
        return {"status": "NOT_RUN", "reason": "No execution record."}
    record = json.loads(Path(path).read_text())
    if not isinstance(record, dict):
        return {"status": "NOT_RUN", "reason": "Execution record must be a JSON object."}
    if record.get("status") != "PASS":
        status = record.get("status")
        return {"status": status if status in {"FAIL", "NOT_RUN", "NOT_APPLICABLE", "STALE"} else "NOT_RUN",
                "reason": "Recorded run did not pass."}
    if record.get("exit_code") != 0 or not isinstance(record.get("command"), list) or not record["command"]:
        return {"status": "NOT_RUN", "reason": "Execution evidence is incomplete."}
    for group in ("inputs", "outputs", "logs"):
        if not isinstance(record.get(group), dict) or (group == "logs" and not record[group]):
            return {"status": "NOT_RUN", "reason": f"No recorded {group}."}
        for filename, saved in record[group].items():
            if not isinstance(saved, dict) or "sha256" not in saved or "size" not in saved:
                return {"status": "NOT_RUN", "reason": f"Incomplete {group} fingerprint: {filename}"}
            if fingerprint(filename) != saved:
                return {"status": "STALE", "reason": f"{group} changed or disappeared: {filename}"}
    return {"status": "PASS", "reason": "Recorded command succeeded; declared fingerprints still match. This is not a rerun or a scientific review."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--output", action="append", default=[])
    parser.add_argument("--report", type=Path)
    parser.add_argument("--timeout", type=float, default=600)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.verify:
        try:
            result = verify_report(args.verify)
        except (OSError, ValueError, TypeError, KeyError) as error:
            result = {"status": "NOT_RUN", "reason": f"Invalid execution record: {error}"}
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["status"] == "PASS" else 1
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not args.report or not command:
        parser.error("--report and a command after -- are required")
    root = args.cwd.resolve()
    inputs = [str((root / value).resolve()) for value in args.input]
    outputs = [str((root / value).resolve()) for value in args.output]
    if set(inputs) & set(outputs):
        parser.error("an output cannot overwrite a declared input")
    if args.report.is_symlink():
        parser.error("report path is a symlink; choose a new regular-file path")
    report = args.report.resolve()
    if report.exists():
        parser.error("report already exists; choose a new run name to preserve history")
    report.parent.mkdir(parents=True, exist_ok=True)
    log = report.with_suffix(".log")
    if log == report:
        parser.error("report and log would have the same path; use a .json report name")
    if log.exists() or log.is_symlink():
        parser.error("log already exists; choose a new run name")
    if str(report) in inputs + outputs or str(log) in inputs + outputs:
        parser.error("report/log cannot also be an analysis input or output")
    before_inputs = {p: fingerprint(p) for p in inputs}
    before_outputs = {p: file_state(p) for p in outputs}
    record = {"status": "NOT_RUN", "command": command, "cwd": str(root),
              "started_at": datetime.now(timezone.utc).isoformat(),
              "exit_code": None, "inputs": before_inputs, "outputs": {}, "logs": {}}
    start = time.monotonic()
    missing = [p for p, value in before_inputs.items() if value is None]
    # Claim the record before execution; concurrent runs must not overwrite history.
    try:
        report_handle = report.open("x")
    except FileExistsError:
        parser.error("report already exists; choose a new run name")
    with report_handle:
        json.dump(record, report_handle, ensure_ascii=False, indent=2)
        report_handle.flush()
        try:
            with log.open("xb") as handle:
                if missing:
                    record["reason"] = "Missing declared input: " + ", ".join(missing)
                else:
                    try:
                        process = subprocess.run(command, cwd=root, stdout=handle, stderr=subprocess.STDOUT,
                                                 timeout=args.timeout, check=False)
                        record["exit_code"] = process.returncode
                        record["status"] = "PASS" if process.returncode == 0 else "FAIL"
                        record["reason"] = "Command completed." if process.returncode == 0 else "Command returned nonzero."
                    except subprocess.TimeoutExpired:
                        record.update(status="FAIL", reason="Command timed out.")
                    except OSError as error:
                        record.update(status="NOT_RUN", reason=f"Could not start command: {error}")
        except OSError as error:
            record.update(status="NOT_RUN", reason=f"Could not create an exclusive log: {error}")
        record["elapsed_seconds"] = round(time.monotonic() - start, 3)
        record["outputs"] = {p: fingerprint(p) for p in outputs}
        record["logs"] = {str(log): fingerprint(log)}
        if record["status"] == "PASS":
            if before_inputs != {p: fingerprint(p) for p in inputs}:
                record.update(status="STALE", reason="Declared input changed during execution.")
            else:
                for path in outputs:
                    current = file_state(path)
                    if current is None or current["size"] == 0 or current == before_outputs[path]:
                        record.update(status="FAIL", reason=f"Expected output missing, empty or not refreshed: {path}")
                        break
        report_handle.seek(0)
        json.dump(record, report_handle, ensure_ascii=False, indent=2)
        report_handle.write("\n")
        report_handle.truncate()
    print(json.dumps({"status": record["status"], "reason": record["reason"], "report": str(report)}))
    return 0 if record["status"] == "PASS" else (record["exit_code"] if isinstance(record["exit_code"], int) and 0 < record["exit_code"] < 126 else 1)


if __name__ == "__main__":
    raise SystemExit(main())
