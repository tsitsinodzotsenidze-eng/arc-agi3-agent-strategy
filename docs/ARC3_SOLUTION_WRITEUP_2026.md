# Recovery, task progress, and execution evidence in ARC-AGI-3

**ARC-AGI-3 technical Solution Writeup — draft, 2 November 2026 (Georgia)**

Author: Tsitsino Dzotsenidze. This is an ARC3-specific technical account. The broader joint ARC-AGI-2/ARC-AGI-3 paper is a separate manuscript. This draft has not been posted as an official Kaggle Solution Writeup.

## Question and approach

Our project examines how an interactive language-model agent responds when progress stalls in an unfamiliar game. The central question is when a recovery intervention helps, and which observations can support that conclusion. We distinguish a recovery mechanism being executed, a subsequent action being taken, progress in a game, and an official competition score. These are related observations, but none is a substitute for the others.

The submitted carriers use the Qwen3.8 Flash Next NVFP4 model family with pinned source/runtime configuration and offline Kaggle inputs. The October carriers assemble exact model mirrors and restore a hash-bound source payload. K0 disables the specified recovery route. K1+VIR uses the recorded response-recovery and additional VIR intervention policy. The earlier K2 carrier represents a historical recovery-enabled configuration and retains its own saved-version provenance.

The carrier distinguishes a normal saved packaging run from an official competition rerun using Kaggle's rerun environment flag. Official execution routes through the competition gateway, which produces `submission.parquet`. A successful short packaging run verifies packaging only; it does not demonstrate hidden-game performance. Time budgets, cleanup reserve, game discovery, and serving configuration belong to the preserved scripts and must not be reconstructed from notebook titles alone.

## Official competition outcomes

The signed-in Kaggle Submissions page displayed these successful public scores at the final-window observation:

| Carrier | Public score | Saved script version |
|---|---:|---:|
| October K0, recovery OFF | **3.32** | 362927490 |
| Historical K2, Version 2 | **3.10** | 353983921 |
| V11 baseline, Version 1 | **3.07** | 350894675 |
| October K1+VIR | **2.61** | 362929164 |
| Historical K0 hidden twin | **2.60** | Not recovered in this packaging pass |
| Earlier V12-A K2 | **2.49** | Not recovered in this packaging pass |

These are displayed rounded public leaderboard scores, not final private leaderboard outcomes. An earlier K0 attempt showed `Kaggle Error`; an unchanged Version 1 retry subsequently succeeded. That infrastructure outcome is retained separately and is not assigned a gameplay score of zero.

The October K0 result exceeds the October K1+VIR result by **0.71 public-score points**. This is a descriptive contrast between the observed submissions. It is not a replicated causal estimate of recovery: effective runtime provenance, budgets, trajectory variation, and other configuration differences must be reconciled before stronger attribution. The historical K2 score is useful competition evidence but must not be treated as an automatically matched contemporary control.

## Development observations and mechanism evidence

The retained R6m1 PUBLIC25 result records 25 games, mean **8.377080297476786**, median **2.7777777777777777**, 40 of 183 completed levels, zero full-game wins, 7,687 actions, and 3,306,410 benchmark-accounted tokens. Its finalization record states that benchmark and scoring completed, all 25 games were finalized, and no measurement write errors were reported. This is development evidence, not an official hidden-test submission.

The same retained mechanism summary records eight K1 intervention attempts with context application and a subsequent environment action, and one VIR intervention with the corresponding downstream action chain. These records establish observed execution of the intervention path within that run. They do not show that the intervention caused useful progress or explain the aggregate score difference.

The dated 31 October handoff reports the corresponding K0 development mean as **12.838496455050274**, with 55 of 183 completed levels and one full-game win. That K0 aggregate is currently attributed to the handoff rather than re-certified from a complete native K0 archive in this packaging pass. It must remain distinct from both the R6m1 primary result and the official public score. The handoff also identifies concentration of the aggregate difference in LP85, motivating per-game sensitivity analysis rather than relying on one overall mean.

## Engineering and reproducibility

The source record separates policy changes from carrier and infrastructure changes. Source restoration verifies an exact 15,201,714-byte ZIP payload against its SHA-256; embedded helper hashes are preserved. The original model identity records 419 files and 135,253,622,894 bytes. These identifiers support reconstruction without claiming that every model file was independently rehashed during release preparation.

Earlier work exposed source-version mismatches, input-removing notebook imports, and GPU-process accounting issues. Such events belong in the engineering chronology. A stopped mount attempt, a successful readiness diagnostic, and a completed gameplay arm are different outcomes. The October measured serving parent used CPython 3.12.13, while repository foundation CI uses Python 3.11. Recording that distinction prevents an apparently successful repository test from being misrepresented as proof of live serving compatibility.

The release retains exact rendered K0/K1+VIR script transcriptions and nine source cells from the saved K2 version. The K1+VIR transcription was verified byte-identical to the prepared code-only artifact. The K2 notebook is explicitly reconstructed; original notebook metadata and outputs are not claimed. Selected R6m1 result and finalization JSON files are included, with hashes. Full model weights, hidden games, external source bundles, and the complete gameplay archive are not republished in this package.

## Limits and next analysis

The current contribution is an auditable competition and development record with explicit limits on comparison. One observed run per condition does not establish statistical significance, repeatability, or general recovery effectiveness. The analysis should next reconcile per-game trajectories, recovery eligibility and timing, progress after intervention, and resource accounting under sufficiently matched conditions. The historical FT09 trajectory analysis and the new LP85 sensitivity question are separate cases and should not be merged.

Our broader interdisciplinary manuscript can discuss human–AI collaboration, open knowledge, and learning under uncertainty. Those interpretations require their own evidence and argument; ARC benchmark scores alone do not establish claims about education, institutions, or a country's economic development.

## Artifacts

Repository: https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy

Exact notebook URLs, capture methods, configuration, selected receipts, and hashes are in `releases/arc3-2026-final/`. External source/model licenses and public accessibility must be checked before claiming reproduction is complete. Zenodo deposit/DOI and the official Kaggle writeup association remain to be completed and must not be inferred from this draft.
