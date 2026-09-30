# Governance status — 30 Sep 2026

This file is the current public status index for the repository. Earlier issues and closure records are preserved as historical snapshots; when a later implementation or documentation change supersedes an earlier status statement, this file records the current position without rewriting the historical record.

## Current living implementations

### C-07 — ReplayAudit read authorization

- Implemented and merged through PR #30: https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/pull/30
- Exact approved head: `6e36fcbc414588c832b5add8f00049edc52ef7fe`
- Merge commit: `702e50af670ac021a6f5bcf419527b02d9f9110e`
- Current status: **LIVING / PRESERVED**

Historical Issue #29 contains an earlier quarantine snapshot. That record remains valid for its date, but its quarantine status was later superseded by the separately reviewed and merged implementation in PR #30.

### C-05 — Route A′ typed-routing safety contract

- Implemented and merged through PR #31: https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/pull/31
- Exact approved head: `c4804de4dfa766cd11d03d738ceb115b635d1bd2`
- Merge commit: `633fab9db4de72e4907ef36e6222c8b0adf6cfaf`
- Exact-head GitHub Actions CI reported success.
- Current status: **LIVING / PRESERVED**

### C-08 — EvaluationLogger path safety

Historical Issue #36 records the pre-implementation readiness state. C-08 was later implemented on `main`:

- Commit: `6ea243d45b78ad42dd0d61ac5843703117e9bec5`
- Commit message: `Implement C-08 evaluation logger path safety`
- Scope includes constructor/root/target validation, containment checks, traversal and symlink rejection, post-mkdir validation, artifact-type checks, and immediately-before-open revalidation.
- Current status: **IMPLEMENTED ON MAIN**

This later implementation supersedes the earlier “ready for a separately authorized attempt / not implemented” status in Issue #36, while preserving that issue as the historical readiness record.

## Closed follow-up

### Issue #37 — C-05 logger robustness follow-up

Issue #37 was closed on 30 Sep 2026 by explicit **Director + Co-Director disposition**.

C-08 resolved the original preflight-lifetime portion through root/target/artifact validation and immediately-before-open revalidation. The remaining cross-file behavior is now an **accepted documented residual**:

- `evaluation_log.jsonl` and `evaluation_summary.csv` are ordered sibling outputs, not a cross-file atomic transaction;
- interruption between the two writes may temporarily leave sibling divergence;
- no current repository consumer requires atomic sibling commit semantics;
- no journal, manifest, third durability artifact, lock service, migration layer, or transaction framework is authorized or required.

If a future consumer requires atomic pair consistency, crash reconstruction, concurrency coordination, or an additional persistence mechanism, that work must begin as a new bounded issue against the then-current exact head.

**Final #37 status: CLOSED / COMPLETED | BEST-EFFORT ORDERED DUAL OUTPUT ACCEPTED AS DOCUMENTED RESIDUAL | NEW IMPLEMENTATION AUTHORITY NONE.**

## Historical readiness records

The following closed issues remain useful historical governance snapshots:

- #32 — C-02 design allocation adopted / implementation not ready
- #33 — C-03 readiness plan adopted / implementation not ready
- #34 — C-01/C-02/C-04 combined readiness package adopted / implementation not ready
- #35 — C-06 readiness plan accepted / implementation not ready
- #36 — C-08 readiness record, later superseded by C-08 implementation on `main`

Statements such as **README PENDING** inside those records describe the status at the time they were written. README reconciliation was completed on 30 Sep 2026 in the public Milestone 2 documentation refresh.

## Documentation state

On 30 Sep 2026:

- repository visibility was changed to **Public**;
- the repository remains licensed under **Apache License 2.0**;
- the main README was refreshed for the ARC-AGI-3 Milestone 2 research state;
- the former long-form README was archived as `PROJECT_HISTORY.md`;
- a Milestone 2 experiment record was added as `MILESTONE_2_2026-09-30.md`.

## Interpretation rule

Historical issues are chronology, not a substitute for current status. For the present repository state, read this file together with the current README and the living implementation commits/PRs above.
