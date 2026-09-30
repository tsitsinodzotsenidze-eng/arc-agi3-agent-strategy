# ARC-AGI-3 Agent Strategy

Open-source research and engineering record for **ARC Prize 2026 — ARC-AGI-3**.

> **Milestone 2 — 30 Sep 2026:** the successful K2 hidden submission carrier has a public score of **3.10**. An otherwise matched **K0 hidden twin** was submitted the same day with stagnation recovery disabled and was still in hidden rerun/scoring when this README snapshot was written.

The project studies how an interactive agent can remain evidence-grounded, auditable, and adaptive under changing or partially uncertain conditions. The repository contains the safety, observation, replay/audit, typed-routing, and evaluation-logging foundations developed during the project. The public Kaggle notebook remains the authoritative competition submission carrier; this repository is not a byte-for-byte mirror of every Kaggle runtime asset.

## Milestone 2 experiment

The current comparison isolates one behavioral variable:

- **K2:** `LOCAL_ANALYZER_STAGNATION_RECOVERY_STREAK=2` — recovery enabled.
- **K0:** `LOCAL_ANALYZER_STAGNATION_RECOVERY_STREAK=0` — recovery disabled.

The K0 twin preserves the same model, runtime, integrated source, frozen source identities, seed `1729`, controller, budget logic, and submission logic. This creates a clean hidden comparison of recovery **ON** versus **OFF** using the same carrier.

Current public-score snapshot:

| Submission | Public Score |
|---|---:|
| K2 milestone carrier — Version 2 | **3.10** |
| V11 baseline | **3.07** |
| Earlier V12-A K2 | **2.49** |
| K0 hidden twin — Version 3 | **Pending at snapshot** |

For exact provenance, hashes, verifier evidence, and timing, see [MILESTONE_2_2026-09-30.md](MILESTONE_2_2026-09-30.md).

## Repository scope

Current `main` includes the implemented foundation for:

- deterministic reset and seed handling;
- structural observation validation and provenance-aware transport;
- typed `ACTION`, `FALLBACK`, and `OBSERVATION_ONLY` routing;
- replay/audit records with deterministic serialization;
- owner-bound and revocable audit-read authorization;
- JSONL/CSV evaluation logging with schema checks;
- C-08 evaluation-output path safety, including containment, symlink, traversal, and state-change guards;
- pytest-based regression coverage and a GitHub Actions CI workflow.

The current repository head before this documentation refresh was:

`6ea243d45b78ad42dd0d61ac5843703117e9bec5` — **Implement C-08 evaluation logger path safety**.

## What is not mirrored here

This repository should not be read as a complete packaged copy of the live Kaggle submission environment. In particular, model weights, Kaggle-provided runtime assets, and the exact competition execution container are external to this repository.

The public Kaggle notebook is the competition-facing source of truth for the submitted carrier. This repository documents and tests reusable project foundations and the research trail around them.

## Research question

Earlier PUBLIC25 testing showed that K0 can occasionally reach a high ceiling but can also be highly variable. A formal paired comparison favored K2 on mean score, while the hidden milestone carrier gives a more direct test under competition scoring.

The practical question is therefore not simply whether recovery exists, but **when recovery helps**. The K0/K2 twin comparison is intended to inform whether later development should use recovery always, never, or selectively under stricter gating.

## Reproducibility notes

Repository CI runs `pytest` under **Python 3.11**.

For the Milestone 2 submission carrier, the competition environment used:

- seed `1729`;
- GPU: RTX Pro 6000;
- Internet: OFF;
- pinned/original Kaggle environment dated 2026-06-30;
- Qwen3.8 Flash Next NVFP4 runtime/model assets supplied through Kaggle inputs.

The K0 native-factory verifier reported:

```text
K0_VERIFY_PASS env=0 native_factory=True effective_k=0 seed=1729
```

## Project history

The earlier long-form governance README has been preserved as [PROJECT_HISTORY.md](PROJECT_HISTORY.md). It remains useful for chronology, but its status statements may describe an earlier project phase.

## Competition and open source

ARC Prize 2026 — ARC-AGI-3 requires competition submissions through Kaggle. For milestone prizes, Kaggle states that qualifying notebooks must be public under an open-source license by the milestone deadline.

Competition page: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3

## License

This repository is licensed under the **Apache License 2.0**. See [LICENSE](LICENSE).
