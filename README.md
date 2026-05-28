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
