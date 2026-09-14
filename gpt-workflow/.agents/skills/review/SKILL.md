---
name: review
description: Review a manuscript, analysis, identification argument, proof, talk or replication evidence; route by the requested scope and return actionable findings.
---

# Review

Read the target/version and current `research/PROJECT_BRIEF.md` when present. Apply `references/protocols/quality.md`; findings distinguish demonstrated errors, missing evidence and editorial suggestions. Save a report to `quality_reports/reviews/YYYY-MM-DD_<task>.md` only when useful. Do not edit the manuscript during review.

| Target / mode | Review |
|---|---|
| Paper, `--proofread` | writer-critic for argument, evidence and prose; selected format, not LaTeX assumptions |
| Code, `--code` | coder-critic static review; verifier or permitted executor checks actual runs |
| `--methods` | strategist-critic: estimand, variation, assumptions, threats and discriminating checks |
| `--theory` | theorist-critic: assumptions, proof/identification, boundary cases and economic meaning |
| Talk | storyteller-critic, against actual source evidence and audience |
| `--peer [journal]` | editor coordinates domain-referee and methods-referee; constraints are verified, tastes labeled |
| `--stress [journal]` | same independent scrutiny, emphasize strongest counterargument; no hostile theatrics |
| `--peer --r2 [journal]` / `--r2` | compare actual prior comments, responses and changed evidence; do not invent referee memory |
| `--replicate [language]` | independent implementation when requested; compare estimand, data and tolerances before numeric agreement |
| `--all` | scope relevant checks to available artifacts; missing required checks are NOT_RUN, not silently excluded |

A file extension alone does not justify dispatching every critic. A paragraph edit needs a focused check; a major result warrants independent scrutiny. Parallelize independent reviews with an explicit input and file-ownership boundary. Verify important critic claims rather than trusting a confident verdict.

For execution use saved scripts and actual logs, preserve exit status, and distinguish compile, analysis and conceptual checks. Equal outputs from two implementations do not prove correctness. A clean build does not verify causal identification. Use PASS/FAIL/NOT_RUN/NOT_APPLICABLE; changed inputs make old checks STALE.

Return the few findings that most affect the argument, their locations, supporting evidence and minimum repair. Explain what would change the judgment. Do not predict acceptance probability, manufacture scores, or require every possible robustness check.
