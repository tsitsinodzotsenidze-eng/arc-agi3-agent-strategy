# ARC3 Zenodo deposit — final publication text and GitHub release note

**Prepared:** 2 November 2026. **Status:** pre-publication review. This document supplements, but does not alter, the previously validated release ZIP and its embedded preliminary metadata.

## Zenodo fields

**Title:** ARC-AGI-3: Recovery Study II — competition carriers, provenance and reproducibility record (2026)

**Creator:** Dzotsenidze, Tsitsino

**Resource type:** Software

**Reserved DOI:** `10.5281/zenodo.23869166` — reserved in the human-created Zenodo draft, not published until Zenodo confirms.

**Version:** `2026-final-1` (record the actual final release/tag name consistently)

**Keywords:** ARC-AGI-3; interactive reasoning; recovery mechanisms; Kaggle; code provenance; reproducibility; Qwen3.8; human–AI collaboration

**Description (copyable):**

> This archival software deposit documents Tsitsino Dzotsenidze's ARC Prize 2026 ARC-AGI-3 research, focusing on recovery interventions in interactive agents and on reproducible competition carriers. It includes the captured rendered code of two exact Kaggle saved versions (K0 and K1+VIR), a transparently reconstructed historical K2 notebook containing nine captured source cells, selected original development receipts, recorded source/helper hashes, Kaggle version identifiers, reproduction instructions, a technical Solution Writeup draft, and attribution and third-party notices.
>
> Official observed **rounded public** Kaggle scores: K0 (recovery OFF) **3.32**, historical K2 **3.10**, and K1+VIR **2.61**. These results describe different observed submissions; they do **not** demonstrate a repeated, statistically tested causal effect of recovery. Public25 development traces are separate from official submissions. No hidden-game source content or final private leaderboard results are claimed.
>
> The archive does **not** include external model weights, original Tufa Labs/Duck source dataset, Kaggle runtime images or hidden evaluation data. The model was RadixArk/Qwen3.8-Flash-Next-NVFP4, pinned to revision `7b719225242aacd3dbd3f9407468c2ee9a9d2594`, under the applicable upstream Qwen model terms. Source and runtime dependencies retain their own licensing and access conditions. The repository's Apache-2.0 license applies to authorized original contributions and does not relicense third-party materials. Upstream Tufa Labs/Duck and Keith Tyser are credited; see `THIRD_PARTY_NOTICES.md` and the supplementary publication rights audit in GitHub.
>
> The K0 and K1+VIR source files preserve captured rendered source, not downloaded notebook binary identity; K2 is a reconstruction, not the original Kaggle notebook metadata and outputs. The archived ZIP is the immutable, pre-release preparation snapshot referenced by its accompanying hash manifest. Public GitHub source and supplementary audit: https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy .

**Related identifiers:**
- Repository: https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy
- Publication/right-scope addendum: https://github.com/tsitsinodzotsenidze-eng/arc-agi3-agent-strategy/blob/main/docs/ARC3_PUBLICATION_LICENSE_AND_DEPOSIT_AUDIT_2026-11-02.md (valid after PR merge)
- Saved K0: https://www.kaggle.com/code/tsitsinodzotsenidze/rsii-k0-submission-2?scriptVersionId=362927490
- Saved K1+VIR: https://www.kaggle.com/code/tsitsinodzotsenidze/rsii-k1vir-submission?scriptVersionId=362929164
- Saved historical K2: https://www.kaggle.com/code/tsitsinodzotsenidze/notebook43f8579dd8?scriptVersionId=353983921
- **Once created**, include the immutable GitHub release URL and commit/tag in Zenodo.

**Licensing field:** The existing Zenodo draft reportedly uses `Apache-2.0`, as does the existing repository. This does **not** grant that license to the upstream Tufa Labs source or Qwen weights. Zenodo supports listing multiple licenses for mixed-license deposits; apply only licenses actually held by the deposited material. Before clicking Publish, verify that the selected rights/description match the contents of the **actual ZIP**, rather than mechanically treating the archive as entirely Apache-2.0. See https://help.zenodo.org/docs/deposit/describe-records/licenses/ .

## GitHub Release text

**Suggested tag:** `arc3-2026-final-1` (only create if absent)

**Suggested title:** `ARC-AGI-3 Recovery Study II — final competition source and reproducibility record`

**Release notes (copyable):**

> Source and reproducibility records for the 2026 ARC-AGI-3 Recovery Study II experiments. Official public scores: K0 3.32, historical K2 3.10, K1+VIR 2.61; no causal recovery claim. Exact saved Kaggle version links, captured code, K2 source-cell reconstruction, selected PUBLIC25 evidence, SHA-256 manifests and dependencies are documented in `releases/arc3-2026-final/`. Model weights and source/runtime datasets are referenced externally, not redistributed. Rights and exact reproduction scope: `docs/ARC3_PUBLICATION_LICENSE_AND_DEPOSIT_AUDIT_2026-11-02.md`. Reserved Zenodo DOI: `10.5281/zenodo.23869166` (do not describe as published until confirmed). The separate ARC2+ARC3 joint paper is not part of this release.
>
> **Source identity:** This GitHub tag marks the reviewed repository snapshot. The separately deposited Zenodo ZIP is the earlier checked preparation snapshot described by its internal `SHA256SUMS.json`. Any subsequent supplementary GitHub documentation is outside that original ZIP. Do not claim byte-identity between GitHub's automatically generated repository archive and the manually prepared Zenodo release ZIP.

## Integrity / UI acceptance conditions

1. Verify PR is merged and the release tag targets the intended GitHub commit; confirm release page becomes publicly visible.
2. Check the Zenodo private draft contains the already validated ZIP, the reserved DOI, and these final metadata fields; attach the GitHub release URL.
3. Publish Zenodo only after final human record review; then confirm DOI resolves to a **published** landing page. Preserve the draft if publication is not finished—never delete it to restart.

No source package reconstruction is required solely to add this *external* supplementary note. If the file contents in the ZIP change, rebuild, rehash and reupload the modified ZIP before publication.