# ARC-AGI-3 Agent Strategy

ARC-AGI-3 Agent Strategy is a multi-phase research and engineering programme for an agent that must operate in novel, changing, and partially uncertain interactive environments. Its long-term architecture is organised around evidence-grounded observation, structural interpretation, bounded hypothesis management, planning, action selection, causal traceability, plan revision, and recovery when conditions, evidence, or prior assumptions change. This repository contains the implemented safety and observation foundation together with the public architecture and governance record. It does not yet implement solver, planner, memory, model inference, or gameplay intelligence.

## Seven structured ARC-AGI-3 work weeks

### Week 1 — Safety and contract foundations
Established the first implemented foundation for controlled reset/lifecycle behaviour, strict action handling, audit visibility, deterministic replay, and explicit boundaries between environment-facing data and later intelligence.

### Week 2 — Observation and environment-interface foundation
Extended the implemented foundation with a structural observation boundary, provenance-aware transport, validation/recomputation rules, and replay-compatible observation records.

### Week 3 — Adaptive-agent architecture foundations
Developed the core architectural concepts required for behaviour in changing interactive environments: evidence interpretation, safe baseline control loop, action history with causal tracing, bounded hypothesis and planning structures, information-gain discipline, recovery mechanisms, and explicit cross-layer contracts and review gates.

### Week 4 — Platform formation and architecture-to-code readiness
Turned the architecture toward implementation readiness through platform formation, source and file inventory work, architecture-to-code contract definition, and explicit verification of what must be true before code-bearing work can be considered.

### Week 5 — Evidence mapping and governance hardening
Mapped unresolved evidence gates and dependency relationships. Produced multiple corrective governance records to restore documentary completeness and re-establish clean before-evidence and opening-gate discipline after a pause boundary.

### Week 6 — Controlled write-route qualification design
Designed a bounded, human-controlled, externally auditable candidate route for future implementation qualification while maintaining strict separation between evidence design, route governance, and any later implementation decision.

### Week 7 — Adaptive milestone response
When the initially planned execution route could not meet the project’s evidence requirements, the project kept the candidate in quarantine, isolated the uncertainty, and designed a governed first-stage alternative pathway. Any future implementation decision remains subject to fresh evidence capture and separate qualification.

## Milestone update — adaptive strategy under changing conditions

When the initially planned execution route could not meet the project’s evidence requirements, we did not lower the standard or manufacture activity to meet a deadline. Instead, we treated the constraint itself as a new problem of adaptation and control.

This response is aligned with the central ARC-AGI-3 challenge: operating when conditions change and the next problem no longer matches earlier assumptions. Instead of forcing a compromised path, the project preserved the candidate under quarantine and designed a governed, evidence-first alternative pathway. That pathway requires fresh evidence capture and separate qualification before any implementation decision.

This milestone does not claim qualification of the pathway or release of the candidate. It records a disciplined adaptive result: the constraint was converted into a bounded, auditable next step without compromising the integrity of the work.

## Current status

Implemented scope is limited to safety/contracts infrastructure plus an observation/interface scaffold. The repository validates and records reset, action, lifecycle, replay, audit, and observation transport boundaries; it does not implement planner logic, solver behavior, strategy, memory, model inference, hidden evaluator assumptions, Undo/`ACTION7` logic, or gameplay intelligence.

Completed repository-level scope includes:

- Week 1 safety/contracts infrastructure:
  - deterministic reset and seed handling;
  - structural observation and evidence envelopes;
  - strict action parsing with authoritative typed `ACTION`/`FALLBACK` outcomes, exact/finite reserved-token collision handling, and a fixed safety fallback;
  - per-episode lifecycle bookkeeping;
  - owner-bound, audit-instance-bound, revocable read capabilities for `ReplayAudit` entries and digest access, with authority validation before protected work or disclosure;
  - deterministic replay records carrying the typed route as the authoritative discriminator;
  - local JSONL/CSV audit logging with explicit primitive route serialization;
- Week 2 observation lifecycle hardening:
  - observation-only environment interface scaffold with a minimal environment protocol and replay-compatible observation records using the typed `OBSERVATION_ONLY` route; the legacy sentinel text remains a compatibility projection, not the route authority;
  - stricter observation metadata validation, including rejection of invalid requested `step_index` values before environment calls;
  - type-strict upstream observation identity matching for requested `episode_id` and `step_index`;
  - JSON-like structural-only `raw_observation` validation that rejects non-structural values such as `bytes`, `set`, arbitrary objects, and cyclic structures at the observation boundary;
  - canonical structural metadata recomputation from `raw_observation` instead of trusting upstream-provided summaries;
  - documentation-only observation JSONL/replay compatibility notes;
  - Week 1 `_safe_size()` consistency cleanup so only `str`, `list`, `tuple`, and `dict` are treated as sized containers, while `bytes`, `set`, scalar-like values, and other unsupported values fall through to the stable placeholder size `1`.

Observation payloads are treated structurally. The observation boundary validates metadata and structural shape, records provenance, and recomputes structural summaries without inferring semantics, choosing actions, or adding gameplay behavior.

## Governance and implementation status

This status snapshot reconciles repository state assessed at the pre-README baseline `main` commit `633fab9db4de72e4907ef36e6222c8b0adf6cfaf`. A later README-only commit or merge will necessarily advance the branch tip; this SHA remains the assessed implementation baseline rather than a claim about the later tip. This section records repository and governance state; it does not create implementation, execution, merge, migration, README, activation, or living-status authority.

### Living implementations

- **C-07 — replay-audit read authorization:** historical documentary chronology remains in [Issue #29](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/issues/29); the living implementation was merged through [PR #30](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/pull/30) at exact approved head `6e36fcbc414588c832b5add8f00049edc52ef7fe`; merge commit `702e50af670ac021a6f5bcf419527b02d9f9110e`; exact-head CI run `29766181102` completed successfully. C-07 remains living and preserved.
- **C-05 — Route A′ typed-routing safety contract:** merged through [PR #31](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/pull/31) at exact approved head `c4804de4dfa766cd11d03d738ceb115b635d1bd2`; merge commit and assessed implementation baseline `633fab9db4de72e4907ef36e6222c8b0adf6cfaf`; exact-head CI run `30013919819` completed successfully. C-05 remains living and preserved.
- [Issue #37](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/issues/37) is an open, non-blocking C-05 logger-robustness follow-up covering preflight lifetime and cross-file durability disposition. It does not reopen or weaken C-05 and grants no implementation authority.

### Documentary and readiness controls

- **C-02:** [Issue #32](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/issues/32) is closed/completed; design allocation adopted and G-02d closed at the documentary/design level; implementation not ready.
- **C-03:** [Issue #33](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/issues/33) is closed/completed; implementation-readiness plan adopted; implementation not ready.
- **C-01/C-02/C-04 combined package (C124):** [Issue #34](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/issues/34) is closed/completed; package v0.4 adopted; implementation not ready.
- **C-06:** [Issue #35](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/issues/35) is closed/completed; implementation-readiness plan accepted at the documentary/design level; implementation not ready.
- **C-08:** [Issue #36](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/issues/36) is closed/completed; ready for a separately authorized implementation attempt at the exact assessed `main`; not implemented, executed, passed, merge-ready, activated, or living.

### Sequence and authority boundary

The adopted implementation sequence is `C-08 → C-03 → C124 → C-06`. C-08 is the only present candidate for the next separately authorized implementation attempt. That position is status-contingent and is not itself implementation or execution authority.

**CURRENT GOVERNANCE STATUS: C-07 LIVING IMPLEMENTATION PRESERVED | C-05 LIVING IMPLEMENTATION PRESERVED | C-05 LOGGER-ROBUSTNESS FOLLOW-UP OPEN / NON-BLOCKING | C-02, C-03, C124, AND C-06 IMPLEMENTATION NOT READY | C-08 READY FOR A SEPARATELY AUTHORIZED ATTEMPT / NOT IMPLEMENTED | NEW IMPLEMENTATION AUTHORITY NONE | NEW EXECUTION AUTHORITY NONE.**

## Week 2 Day 3 observation JSONL/replay compatibility notes

**Pure documentation review findings only — this PR adds no code, no types, no behavior, no new files, and makes no implementation commitments.**

This section is documentation-only guidance for preserving the existing observation lifecycle while future JSONL observation logging and deterministic replay are designed. It does not add a logger, replay engine, memory system, strategy, evaluator assumption, environment adapter behavior, or action-selection behavior.

### Stable observation fields

Future observation JSONL rows should preserve the following `ObservationRecord` fields as stable transport names and meanings:

- `episode_id`: a non-empty string that identifies the current episode/run namespace. It is transport identity, not a gameplay hint, and should not be rewritten by logging or replay tooling.
- `step_index`: a non-negative integer for the observation's position inside the episode. It must not be accepted as a string, boolean, float, or parser-coerced numeric value, so ordering and replay checks do not depend on runtime-specific coercion.
- `source_label`: a non-empty provenance label for the upstream observation source. It is useful for audit/debug attribution, but must not become a reasoning, planning, evaluator, or strategy signal.
- `raw_observation`: the structural environment payload exactly as accepted at the validation boundary. Future JSONL tooling should preserve or encode it only under an explicit lossless JSONL serialization contract, without semantic enrichment, lossy normalization, or hidden state injection.
- `observation_type`, `summary_size`, and `summary_keys`: deterministic structural summaries derived from `raw_observation`. They should be recomputed or verified from the raw payload rather than trusted if supplied by an upstream source or external caller.

### Deterministic replay compatibility requirements

For later deterministic replay, an observation row should be able to establish at least:

- the episode identity (`episode_id`) and deterministic seed associated with the episode;
- the exact observation order (`step_index`) within that episode;
- the validated source provenance (`source_label`);
- the raw structural observation payload (`raw_observation`) used by the observation boundary;
- the derived structural metadata (`observation_type`, `summary_size`, `summary_keys`) or enough data to recompute it;
- the lifecycle/action context when bridging into existing `ReplayEntry` rows, including the authoritative typed `OBSERVATION_ONLY` route for non-action rows; the legacy `__OBSERVATION_ONLY__` text is retained only as a compatibility projection.

Timestamps, if introduced later, should be optional audit metadata only. They should not participate in deterministic replay identity, ordering, digest inputs, action selection, or observation normalization unless a future contract explicitly says so, because wall-clock values can make replay nondeterministic.

### Validation and normalization boundaries

The observation boundary validates metadata and structural shape only. It accepts JSON-like structural payloads, rejects cyclic or non-structural values, and recomputes structural summaries from `raw_observation`. Parsed or normalized observation data should remain a deterministic structural projection of `raw_observation`; it must not add inferred semantics, evaluator-specific hints, memory lookups, similarity-search annotations, or planner state. If future JSONL logging needs a normalized form, the normalization rule should be documented as a pure transformation and stored separately from `raw_observation` so replay can distinguish source data from derived data.

### Current out of scope

For this phase, observation JSONL/replay work remains documentation-only. The repository should not add or change any of the following as part of this scope:

- observation log writer implementation or JSONL schema migration code;
- replay engine or replay reader;
- memory, episodic storage, similarity search, planner, strategy, evaluator assumptions, gameplay intelligence, or action selection;
- environment adapter semantics beyond the existing validation/recompute boundary;
- dependencies or architecture expansions.

### Risks and ambiguities to keep visible

- `raw_observation` is currently accepted as structural data, but future JSONL serialization details are not yet specified; tuples, numeric edge cases, and object ordering should be handled deliberately before relying on byte-identical logs.
- The repository already has Week 1 audit JSONL for `ReplayEntry`, but observation-specific JSONL rows are not implemented. `ReplayEntry.route` now supplies the clear typed discriminator; consumers must use its serialized primitive value rather than infer route meaning from legacy marker text.
- The typed-route schema adds `route` to audit JSONL, CSV, and digest inputs. On its first write, each logger instance refuses to append unless existing artifacts have the complete canonical schema and a consistent typed route state; use a fresh output directory rather than mixing or silently migrating schemas. This startup preflight does not provide continuous external-mutation detection or cross-file transactional durability.
- `source_label` is provenance only. If future components use it as a policy or evaluator feature, replay behavior could depend on logging metadata rather than environment state.
- Timestamps can help audits but can also make digests and ordering nondeterministic if included in replay-critical fields.
- Derived summaries should be verified against `raw_observation`; trusting upstream-provided summaries risks inconsistent replay and unsafe cross-environment comparisons.

## Explicit non-goals in the current codebase

This repository currently does **not** include:

- planner logic;
- world model logic;
- solver implementation;
- gameplay strategy;
- persistent memory;
- Undo or `ACTION7` logic;
- hidden evaluator assumptions;
- model inference.

## Project scope

The current scope is safety/contracts plus an observation/interface scaffold only. Any future planner, solver, memory, model, or game-playing component should be added separately and should preserve the safety and audit boundaries established here.
