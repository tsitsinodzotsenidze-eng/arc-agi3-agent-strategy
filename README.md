# ARC-AGI-3 Agent Strategy

This repository is an early ARC-AGI-3 agent foundation focused on safety contracts and observation transport. It is intended to make reset behavior, observation records, replay/audit rows, and environment-facing interfaces explicit before any agent intelligence is added.

## Current status

Implemented scope is limited to:

- Week 1 safety/contracts infrastructure:
  - deterministic reset and seed handling;
  - structural observation and evidence envelopes;
  - strict action parsing with a fixed safety fallback;
  - per-episode lifecycle bookkeeping;
  - deterministic replay records;
  - local JSONL/CSV audit logging.
- Week 2 Day 1 observation-only environment interface scaffold:
  - minimal environment protocol;
  - observation metadata validation;
  - canonical structural metadata recomputation;
  - replay-compatible observation records using an observation-only sentinel.

The observation interface is designed to validate and record environment observations while keeping agent intelligence out of scope at this stage. Observation payloads are treated structurally; the scaffold does not infer semantics, choose actions, or implement gameplay behavior.

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
- the lifecycle/action context when bridging into existing `ReplayEntry` rows, including the observation-only sentinel `__OBSERVATION_ONLY__` for non-action rows.

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
- The repository already has Week 1 audit JSONL for `ReplayEntry`, but observation-specific JSONL rows are not implemented. Mixing action/replay rows and observation-only rows without a clear discriminator could make consumers treat observation transport as gameplay actions.
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
