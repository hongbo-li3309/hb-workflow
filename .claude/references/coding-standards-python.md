# Python: short scripts a researcher can inspect

Use the existing environment and paths. A small analysis can remain one script with helper functions; extract modules when reuse or distinct stages justify it. Put consequential research settings near the top. Explain sample choices, identification and units; do not narrate every line.

## Minimal descriptive example

Save as `scripts/python/describe.py`; run from any directory. The input is a project CSV with `group` and `wage` fields. This computes group means, not a causal effect. Synthetic test data must be labeled as fixtures.

~~~python
from pathlib import Path
import csv
import json
import math

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data/cleaned/sample.csv"
OUTPUT = ROOT / "paper/tables/group_means.json"
groups = {}

with INPUT.open(newline="") as handle:
    for row in csv.DictReader(handle):
        value = float(row["wage"])
        if not math.isfinite(value):
            raise ValueError("wage must be finite; define missing-data handling explicitly")
        groups.setdefault(row["group"], []).append(value)

if not groups:
    raise ValueError("Empty analysis sample")
summary = {group: {"n": len(values), "mean_wage": sum(values) / len(values)}
           for group, values in sorted(groups.items())}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(summary, indent=2) + "\n")
~~~

When stochastic work is needed, keep and use the RNG object:

~~~python
import numpy as np
SEED = 42
rng = np.random.default_rng(SEED)
draws = rng.normal(size=100)
~~~

Discarding `np.random.default_rng(SEED)` does not seed later global NumPy draws. For parallel simulation, allocate explicit independent streams; record software and RNG settings. Package-specific estimators may require their own random-state argument.

## Data, estimation and outputs

Use pandas/polars when they simplify the task; do not add them to a trivial standard-library script. Validate key uniqueness and intended merge cardinality. Check missingness, attrition, time ordering and units. Preserve raw inputs and use a new object for a temporary subgroup.

Choose estimator and covariance settings for the design. Record package versions actually used and verify unfamiliar APIs against official docs. A readable formula is often better than a custom framework. Distinguish fitted parameters, calibrated values, predictions and causal estimates.

Fail visibly on invalid input, nonconvergence or inconsistent output. Avoid broad exceptions that continue with a previous model. Use tolerances suitable for quantity and scale; do not blindly clip invalid probabilities or require exact floating-point equality.

Persist useful outputs and expensive handoffs in documented formats; not every object. Only load trusted pickle/joblib files. Tables and plots preserve sample, units and uncertainty, with small underlying plot data saved when useful.

## Verification

Use `scripts/run_check.py` with code, data and configuration as explicit inputs. Changed inputs make old evidence **STALE**. Lint checks syntax/patterns without importing or executing the script; execution remains **NOT_RUN**.

Test meaningful boundaries or a known small answer when correctness is at risk. The descriptive example is exercised with known group means, bad values and empty samples in `tests/test_analysis_examples.py`; this does not validate an empirical estimator. Record **PASS / FAIL / NOT_RUN / NOT_APPLICABLE** and actual logs in `quality_reports/reviews/YYYY-MM-DD_<task>.md`.
