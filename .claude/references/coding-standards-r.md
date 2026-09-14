# R: clear analysis with explicit inputs

Keep working packages and conventions. Retain R when already used or when it supplies the appropriate estimator. A short script can contain helpers; no mandatory package framework, roxygen blocks or one function per file.

State purpose, input and output briefly. Load dependencies together, put consequential research choices near the top, then validate, estimate and export. Run from a documented project root, e.g. `Rscript scripts/R/main.R`, or use the existing root helper.

Use readable names and formulas. Validate unique keys before joins and inspect unmatched cases and sample loss. Explain missing-data choices instead of silently using `na.rm = TRUE`. Preserve raw inputs and use separate objects for temporary subsets.

Choose estimation, weights and uncertainty for the design. Significance alone does not establish causality. Record nonconvergence and missing replications; do not silently retain only successful draws.

~~~r
# Reproducible toy draws, not empirical evidence.
set.seed(42)
draws <- rnorm(100)
stopifnot(length(draws) == 100L, all(is.finite(draws)))
~~~

Use a documented parallel-safe RNG mechanism when needed. Identical integer seeds across languages need not produce identical draws. Reinitializing the same seed each iteration can invalidate a bootstrap.

- Use `seq_len(n)` or `seq_along(x)` where empty input is possible.
- Avoid namespace masking that can change results, `attach()`, and global workspace clearing inside analysis.
- Use functions for meaningful repeated logic. Ordinary loops and `print()` for a result table are not forbidden.
- Use meaningful absolute/relative tolerances; diagnose numerical-domain errors before changing values.
- Keep the main fitted object named; robustness models should not replace it before export.
- Save useful handoffs with `saveRDS()` or interoperable formats, not every intermediate.
- Existing fixest/modelsummary/ggplot2 or other project tooling may be used after checking relevant options. Package preference is not a quality gate.

Record actual R/package versions and the environment, e.g. the project's `renv.lock` plus runtime information. Restore dependencies in setup; do not update packages inside estimation.

Run and capture the actual command's exit status/log. Static review cannot establish execution. Link main results through `research/EVIDENCE_LEDGER.md`; reviews use `quality_reports/reviews/YYYY-MM-DD_<task>.md` and **PASS / FAIL / NOT_RUN / NOT_APPLICABLE**, with **STALE** for changed inputs.
