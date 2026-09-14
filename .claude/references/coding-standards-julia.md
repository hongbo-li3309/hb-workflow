# Julia: transparent numerical economic work

Use Julia when the model or project justifies it. Keep small helpers near callers. Split model primitives, solution, estimation and export when this clarifies the economics.

Record actual Julia version, `Project.toml` and `Manifest.toml`. Run in the declared environment, e.g. `julia --project=. scripts/julia/main.jl`. Restore dependencies in setup; do not silently update them during estimation.

- Anchor paths from a documented entry point or `@__DIR__` and `joinpath`.
- Keep economic parameters, sample definitions, solver tolerances and simulation choices easy to find.
- Define agents, choices, constraints and equilibrium objects before the solver. Separate calibrated from estimated parameters.
- Check domains, residuals, convergence and sensitivity to starts/tolerances. Returning a number does not prove the intended equilibrium was found.
- Clipping, penalties and fallbacks can change the model; explain them and test boundaries.
- Use simple functions for inner loops; profile before elaborate parallelism or type machinery.
- Preserve raw data and keep temporary transformations separate from cleaned canonical inputs.
- Save model objects and table/plot data needed downstream, with documented formats and source versions.

~~~julia
# Reproducible toy draws, not empirical evidence.
using Random
rng = MersenneTwister(42)
draws = randn(rng, 100)
@assert length(draws) == 100 && all(isfinite, draws)
~~~

Pass the RNG through simulations and allocate documented streams for parallel work. Do not reset the same seed each iteration. Different valid generators produce different draws; assess Monte Carlo uncertainty rather than literal draw equality.

Test analytic special cases, boundaries, equilibrium residuals, known answers or genuine failure modes. Cross-language agreement cannot exclude shared model errors. Contrary signs and null estimates are not failures by themselves.

Keep actual commands, logs, input/output versions and artifacts. Use `scripts/run_check.py` or equivalent current records. Lint is not Julia execution. Report **PASS / FAIL / NOT_RUN / NOT_APPLICABLE**, or **STALE** after input changes, in `quality_reports/reviews/YYYY-MM-DD_<task>.md`; important results link to `research/EVIDENCE_LEDGER.md`.
