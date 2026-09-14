---
name: analyze
description: Implement and check economic analysis in the project's language, with traceable inputs and results that preserve the agreed research question.
argument-hint: "[dataset or task] [--dual stata,python]"
allowed-tools: Read,Grep,Glob,Write,Edit,Bash,Agent
---

# Analyze

Implement the requested analysis. Stata is the default; retain a project's existing language or use a suitable available implementation. Read the relevant language reference and existing scripts, then the current task in `research/PROJECT_BRIEF.md`. Do not require an approved numerical score before working.

## Workflow

1. **Frame the run.** Briefly state what quantity is being computed, from which sample, with which outcome/treatment and uncertainty calculation. Identify missing design choices. A descriptive task can proceed without a causal strategy memo; do not silently select the main estimand.
2. **Prepare only what is needed.** Inspect keys, units, missingness, merge cardinality and consequential sample restrictions. Preserve raw inputs. Use data-engineer for substantial cleaning or measurement; a small transformation does not need another agent.
3. **Implement transparently.** Keep key research choices near the top and a clear run entry point. A small task can be one script. Keep subgroup transformations separate and explicitly select the intended model before export. Persist useful handoffs, not every intermediate.
4. **Execute and check.** Discover the available runtime/MCP, save scripts and retain real command/tool output. Stata MCP is preferred when present; a licensed configured batch executable is an allowed fallback. Neither available means **NOT_RUN**. Lint is static.
5. **Review where valuable.** Use coder-critic for main estimates, complex transformations or consequential changes. Test the actual risk: known toy answer, key uniqueness, empty sample, model persistence or error handling. Correct implementation errors, then rerun affected checks. A contrary sign is not failure.
6. **Explain findings.** State the estimate with sample, units and uncertainty, how it bears on the main mechanism, competing explanations and the most useful next step. Distinguish descriptive, causal, calibrated, estimated and simulated quantities.

## Artifacts and verification

Scripts live under `scripts/stata/`, `scripts/python/`, `scripts/R/` or `scripts/julia/` as appropriate. Follow project paths for cleaned data, tables and figures. Update important evidence in `research/EVIDENCE_LEDGER.md`; major confirmed specification changes belong in `research/DECISIONS.md`. Avoid duplicate result summaries for every operation.

Reviews use `quality_reports/reviews/YYYY-MM-DD_<task>.md`; put machine execution logs/records in `quality_reports/runs/`. For a local run, the following example assumes the actual script and CSV exist:

```bash
python3 scripts/run_check.py --input scripts/python/describe.py --input data/cleaned/sample.csv --output paper/tables/group_means.json --report quality_reports/runs/2026-09-13_describe.json -- python3 scripts/python/describe.py
```

Declare all relevant code, data and configuration files; choose a new record name for each run. The helper preserves the command's failure status and checks that declared outputs were refreshed. MCP records need equivalent evidence, including runtime errors; Stata batch log errors require inspection even if the launcher returns zero.

Report required checks as **PASS / FAIL / NOT_RUN / NOT_APPLICABLE** with reasons. Changed inputs invalidate earlier evidence as **STALE**. Never infer a pass from a previous output file or another agent's unsupported claim.

## Correct storage and RNG patterns

Use `.claude/references/coding-standards-stata.md` for a main/subgroup example that executes `estimates restore m_baseline` before `estimates save`. `restore` only restores data. Stata `tempfile` does not survive as a handoff into the next session.

Use `.claude/references/coding-standards-python.md` for a runnable descriptive example and explicit `rng = np.random.default_rng(SEED)`; draw through `rng`. Discarding the object does not seed later global draws.

## Dual-language mode

When explicitly requested with `--dual`, compare two implementations of the same target quantity. Share the same input sample and specification; separate implementations can be delegated independently. Align missingness, weights, reference groups, variance correction, tolerances and package defaults before comparing.

Record point estimates, uncertainty, sample size and exact discrepancies, with tolerances justified by numerical scale and simulation error. Matching significance stars is not enough. Agreement is useful evidence, but both programs may implement the same wrong idea. Investigate divergence without treating every floating-point difference as a bug.
