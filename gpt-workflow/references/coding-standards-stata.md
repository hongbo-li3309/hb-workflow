# Stata: inspectable and reproducible analysis

Use the project's installed Stata edition/version and existing conventions. Keep saved do-files and discover MCP tools at runtime. When MCP is absent, a licensed batch command is a valid fallback. If unavailable, execution is **NOT_RUN**.

## A small project

A short analysis can be one do-file. Larger projects may need an explicit entry point, setup, cleaning and estimation. Keep the sample, outcome, treatment, controls and inference choices near the top; prefer readable local macros to layers of configuration. Do not build one ado-file per simple helper.

Run from the project root. A setup file may establish the root once and define `$rawdata`, `$workingdata`, `$tempdata`, `$table` and `$figure`. Quote paths so spaces work. Actual data access may need a machine-local root override; do not commit private paths or secrets.

Use `version` compatible with the actual runtime; record the edition. Install dependencies separately from estimation. Capture expected optional operations only; check `_rc` immediately. Never hide a failed regression behind `capture` and export whatever model remains active.

## Main model and sample isolation

The example assumes `_setup.do` defines paths. The subgroup is illustrative, not a required robustness check.

~~~stata
do "scripts/stata/_setup.do"
local outcome log_wage
local treatment treat_post
local controls age age_sq
local sample_if "year >= 2010 & year <= 2019 & !missing(log_wage, treat_post, age, age_sq, firm_id)"
local subgroup_if "industry == 31"
local cluster_var firm_id

use "$workingdata/analysis_panel.dta", clear
count if `sample_if'
assert r(N) > 0
regress `outcome' `treatment' `controls' if `sample_if', vce(cluster `cluster_var')
estimates store m_baseline

preserve
    keep if `subgroup_if'
    regress `outcome' `treatment' `controls' if `sample_if', vce(cluster `cluster_var')
    estimates store m_subgroup
restore

* restore reloads data; it does not restore the baseline estimation results.
estimates restore m_baseline
estimates save "$tempdata/m_baseline.ster", replace
~~~

This OLS example demonstrates storage, not a causal design. Choose fixed effects and estimator based on the agreed design. Do not add controls merely because they exist; post-treatment adjustment changes interpretation.

`tempfile` is scoped to its Stata session/program. Use it for short-lived transformations; use a named path for the next process or session. Analysis never saves over raw/cleaned canonical inputs. Cleaning scripts can regenerate cleaned outputs from the raw sources.

## Checks that matter

- Validate key cardinality with `isid` or an equivalent before `merge`. Inspect `_merge`, matched/unmatched counts and composition; do not silently drop unmatched rows.
- Stata numeric missing values sort above finite values. `x > 0` can include missing observations: add `!missing(x)` where intended.
- Record sample counts after consequential restrictions, variable definitions, units, weighting and clustering. Check subgroup work has not contaminated the next sample.
- Set and use an intentional seed for random procedures. Document streams for parallel work; do not reset the same seed every replication.
- Investigate failure/convergence and missing estimates; a contrary coefficient sign is not a coding failure.
- Export the explicitly named model. `esttab`/`estout`, `collect` or existing tooling are options. Inspect generated fragments before adding LaTeX wrappers; `fragment` output need not be a complete `tabular`.
- Keep main estimates and plot data needed downstream; do not serialize every temporary object.

## Dependencies and handoff

`version` governs Stata behavior, not user-written ado versions. Use project-local ado dependencies, record resolved files (`which`/`adopath`) and actual versions/sources, and preserve their contents or pinned retrieval instructions. Follow package licenses. Do not silently reinstall latest versions during estimation.

The [AEA Data Editor dependency guidance](https://aeadataeditor.github.io/aea-de-guidance/preparing-replication-package-step3) was checked 2026-09-13. It recommends preserving the project package environment. Recheck applicable journal policy at submission; SSC package names alone do not establish reproducibility.

Retain the actual command/log, data/code/config version, named model and output. Inspect Stata log errors even when a process exits successfully. Lint of `.do`/`.ado` is static and execution stays **NOT_RUN** until a real runtime succeeds. Use **PASS / FAIL / NOT_RUN / NOT_APPLICABLE**, or **STALE** if inputs changed, in `quality_reports/reviews/YYYY-MM-DD_<task>.md` and relevant `research/EVIDENCE_LEDGER.md` entries.
