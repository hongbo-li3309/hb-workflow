---
name: submit
description: Prepare journal targeting, manuscript and replication packages, and audit readiness against verified destination requirements.
argument-hint: "[target | package | audit | final] [journal or manuscript]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, Agent, WebSearch, WebFetch
---
# Submit

Preserve the user's manuscript, authorship and chosen destination. Read the project brief, evidence ledger and actual validation records. No score certifies a paper as ready for submission.

- `target`: compare fit of the economic question, contribution and evidence to actual recent papers; check official requirements using `.claude/references/journal-profiles.md`. Separate rules from judgment; avoid prestige-based demands for additional models.
- `package`: prepare a versioned manuscript and replication directory under `paper/replication/` or the user path. Document data provenance/access, exact dependencies, master entrypoint, seeds, runtime and figure/table mapping. Restricted data are described without redistribution; synthetic data are labeled and their testing limits stated.
- `audit`: use verifier and relevant critics to inspect actual runs, numeric claims, citations, anonymous files and current destination requirements. A missing run is NOT_RUN, stale evidence is STALE. Compare manuscript and package versions.
- `final`: resolve or explicitly disclose applicable material issues; produce a concrete list of files and remaining limitations. Final means readiness review, not an instruction to click a journal portal's submit button.

Installing dependencies, sharing confidential material, author attestations and external submission follow the user's specific authorization and actual access. Do not repeat permission already granted; do not infer permission to publish from permission to prepare. A response or cover letter must not claim analyses or approvals that did not occur.

Reference the current [AEA policies](https://www.aeaweb.org/journals/data) or destination's own policy and [replication README guidance](https://social-science-data-editors.github.io/template_README/). Stata `version` does not freeze user-written ado packages. Internal audit is not a journal's compliance certification.
