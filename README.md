# ARC-AGI-3 Agent Strategy

Research code and reproducibility record for **ARC Prize 2026 — ARC-AGI-3**.

## Published software release and Zenodo archive

**Distribution-scope correction:** the current revision replaces the complete K1+VIR script with a hash-bound reconstruction kit. Two complete upstream-derived overlay files are excluded pending an explicit component-level license grant. The saved Kaggle version and original captured-source SHA-256 are unchanged. See [the correction record](docs/ARC3_DISTRIBUTION_CORRECTION_2026-11-02.md).

The corrected [GitHub Release **arc3-2026-final-2**](https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/releases/tag/arc3-2026-final-2) was published on **2 November 2026**, pinned to reviewed merge commit `293f1564f373b002c19176beb850ab6dd2548078`. The earlier `arc3-2026-final-1` tag and history are preserved. This is the ARC-AGI-3 source and technical-evidence release, separate from the combined ARC2+ARC3 manuscript.

The corrected software archive is **published on Zenodo (2 November 2026), version `2026-final-2`**: [record 23869166](https://zenodo.org/records/23869166), DOI [10.5281/zenodo.23869166](https://doi.org/10.5281/zenodo.23869166). It contains only `ARC_AGI3_Public_Release_v2_2026-11-02.zip` (307,808 bytes; SHA-256 `fd50ac4cebd5ee261902d582e9101c343d61ef878b8ec3aacc44c0fb11cc51af`; MD5 `5d5407547b4a9903888ba2fad5e796b7`). The original complete preparation ZIP is not part of this published deposit. OpenAIRE EXPLORE also displays the record as research software. GitHub's automatic source archives have a separate byte identity.

See the [rights/provenance audit](docs/ARC3_PUBLICATION_LICENSE_AND_DEPOSIT_AUDIT_2026-11-02.md) and [final Zenodo description/release notes](zenodo/ARC3_FINAL_DESCRIPTION_AND_RELEASE_NOTES_2026-11-02.md) for creator, external dependency, license and archive-scope details.

## Final-window update — 2 November 2026 (Georgia)

The official public leaderboard shows **K0 3.32**, historical **K2 3.10**, V11 **3.07**, and **K1+VIR 2.61**. These are successful Kaggle submission scores, distinct from PUBLIC25 development scores. Final private scores are unknown.

| Candidate | Public score | Exact saved Kaggle version |
|---|---:|---|
| K0, recovery OFF | **3.32** | [Version 1 / 362927490](https://www.kaggle.com/code/tsitsinodzotsenidze/rsii-k0-submission-2?scriptVersionId=362927490) |
| Historical K2 | **3.10** | [Version 2 / 353983921](https://www.kaggle.com/code/tsitsinodzotsenidze/notebook43f8579dd8?scriptVersionId=353983921) |
| K1+VIR | **2.61** | [Version 1 / 362929164](https://www.kaggle.com/code/tsitsinodzotsenidze/rsii-k1vir-submission?scriptVersionId=362929164) |

The two highest public scores are the proposed final choices. The preparation observation showed **0/2 selected**; the human competitor must complete and verify final selection in Kaggle. K1+VIR remains part of the research record.

## Competition source and reproducibility

The [final-window package](releases/arc3-2026-final/README.md) contains saved-version source transcriptions, hashes, selected development receipts, reproduction instructions, and an ARC3-specific [Solution Writeup draft](docs/ARC3_SOLUTION_WRITEUP_2026.md). K0 preserves its exact rendered source text. K1+VIR is provided as a template, original VIR adapter, changes-only recipe, and reconstruction utility; authorized exact upstream source is required to reconstruct the original submitted carrier. The K2 notebook is explicitly reconstructed from nine rendered source cells; original notebook metadata and outputs are not claimed.

Model weights, the external source carrier, Kaggle runtime datasets, and the competition environment are external dependencies. This repository alone is not a self-contained executable Kaggle environment. See the [dependency and provenance record](releases/arc3-2026-final/REPRODUCING.md) and [third-party notices](releases/arc3-2026-final/THIRD_PARTY_NOTICES.md).

## Research scope

The project asks when recovery helps an interactive agent facing unfamiliar tasks. Mechanism execution, task progress, official scores, and infrastructure failures are recorded separately. Scores from different historical carriers do not by themselves isolate a recovery effect. One development run per condition does not establish replication or statistical significance.

The separate combined ARC-AGI-2/ARC-AGI-3 paper remains a broader research deliverable. This repository and its technical writeup document ARC-AGI-3 specifically.

## Reusable foundations

The existing code provides deterministic reset/seed handling, structural observation checks, typed action routing, replay/audit serialization, evaluation logging, and path safety. Existing regression tests and CI remain in place. Repository CI uses **Python 3.11**; this must not be conflated with the measured October Kaggle serving parent, **CPython 3.12.13**. The pinned serving carrier requires the recorded CPython 3.12-compatible host and runtime assets.

## Historical records

The dated [Milestone 2 record](MILESTONE_2_2026-09-30.md), [governance record](GOVERNANCE_STATUS_2026-09-30.md), and [project history](PROJECT_HISTORY.md) remain unchanged. Their pending/result statements apply to their original dates. In particular, September descriptions of an intended matched K0/K2 comparison must not be read as proof that all later October conditions form a fully matched causal experiment.

## License and attribution

Original project contributions retain this repository's [Apache License 2.0](LICENSE). External model weights, runtime assets, upstream source, and embedded dependencies retain their own terms. The package preserves the Requests license and identifies upstream provenance; the repository license does not relicense external artifacts.

Competition: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3

