# LP85 Selected-Case Evidence Supplement

**Status:** 5 November 2026, author-authorized public source/evidence supplement in `tsitsinodzotsenidze-eng/arc-agi3-agent-strategy`. MIT-0 applies only to the author-owned methodological prose and pseudocode specified in `ATTRIBUTION_AND_RIGHTS.md`. Benchmark-derived records and third-party material retain their own rights status. This is not a complete native benchmark reproduction.

## Research question and provenance

This is a limited supporting package for *Two Worlds, One Challenge* (ARC-AGI-2/3 paper). It was assembled **solely from the existing** `ARC_AGI3_LP85_Control_And_Progress_Diagnostic_2026-10-21(1).zip`, without rerunning the ARC games, agent, GPU, or diagnostic experiment. The source diagnostic is dated 21 October 2026; its selected K0 run began 18 October 2026 and K2 run began 19 October 2026. Both are **historical K0/K2**, not the later K1+VIR PUBLIC25 run. Underlying ARC3 source ancestry and separate version DOI are cited in the manuscript. The original diagnostic package and its saved author review are retained privately.

The original archive identities, their **previously verified** SHA256 receipts and benchmark-start UTC timestamps are in `provenance.json`. Private workspace paths have been removed; hash verification of the large original archives **was not repeated**. Inherited `analysis_sha256` and `selected_frames_sha256` identify upstream retained inputs, not hashes newly generated or reinterpreted by this package. Each `trace_start_utc` is a calculated alignment from the run's benchmark-start UTC and the source trace's `start_elapsed_s` and is **not** an independently logged wall-clock start. `benchmark_elapsed_s` is the retained controller/benchmark elapsed time; this package makes no subsecond cross-clock latency claims.

## Contents and permitted inference

- `traces/*.csv`: six normalized action-level retained traces: K0/K2 LP85, K0/K2 FT09, K2 SP80, K2 TN36. Fields include action ordinal, time, mouse coordinates, full-grid equality/digest, native level-completion indicator, native state and RESET/terminal flags. `online_level_before_observation` is reconstructed from preceding **per-action native completion flags**. Source cache's final-derived fields are intentionally excluded.
- `controls/glyph_boxes.csv`: 16 arrow-like **candidate** control footprints; inclusive zero-based row/column boxes. `controls/glyph_colored_pixels.csv`: all 160 derived colored pixels (10 per glyph). `controls/K0_effective_clicks.csv` describes the four K0-associated effective locations; `controls/K2_click_frequencies.csv` contains observed position counts.
- `results/fixed_rule_case_results.csv`: saved F20T5 and P50T10 cases. **M20T5 is retained only as a historical sensitivity result; its masked-grid inputs are omitted and it cannot be independently recalculated from these CSVs**. Later completion labels are **retrospective same-trace outcomes**, not a different baseline arm or post-intervention outcomes.
- `results/first_eligible_events.csv`: first eligibility events per level/rule. Later-baseline-completion columns are post-hoc labels and must **not** be used for online eligibility.
- `results/tool_boundaries.csv` plus `results/tool_boundaries_SCHEMA.md`: retained callback/tool-return/analyzer receipts for LP85 A70→A77 and SP80 A50→A55, with an explicit warning against subsecond ordering or latency inferences.
- `METHOD.md` and `results/RESULTS_SCHEMA.md`: reproducible F20T5/P50T10 and overlap pseudocode, plus results-label and M20T5 limits.
- `ATTRIBUTION_AND_RIGHTS.md`: attribution, source ancestry, and the limited license scope.
- `PUBLICATION_AUTHORIZATION.json`: the author's authorization of this selected GitHub publication, separately from the earlier method-license decision.
- `LICENSE-MIT-0.txt` and `AUTHOR_LICENSE_APPROVAL.json`: approved limited method/pseudocode license and scope.
- `SHA256SUMS.txt`: file-level hashes of the curated files.

The `provenance.json` records separate counts for (a) native per-action completion flags and (b) retained completion records including terminal WIN when applicable. K0 LP85 is 7/8 (WIN A160), and K2 FT09 is 5/6 (WIN A101); the historical events remain unchanged.

**Timing:** Retained action and analyzer-entry clocks are not strictly aligned at subsecond precision; use action cursors and tool/callback membership for ordering. No artificial timestamp correction has been made.

No original complete level frames, runtime model dialogues, reasoning transcripts, private SQLite, entire source archives or third-party solver bodies are included. Without native frames, independent readers can check retained action/threshold arithmetic, digest/equality records, K0/K2 coordinate overlap, and box intersection calculations, but **cannot independently re-extract the glyphs, verify their native appearance, reconstruct the original full frames, or replay the games**. The 16 bounding boxes represent **visual candidate footprints**, not measured hitboxes, and the four K0 points are demonstrated only on the retained K0 trajectory.

## What the evidence does and does not support

LP85 level 4 began from **equal visible entry arrays** in K0 and K2 (source entry SHA256 `9cd442096ed2d71f8fea369042eecdb138d17209a134fe1ea76a769e7cc342f8`). K0 level 4 completed in 18 state-changing actions; K2 issued 962 mouse actions with no visible full-grid change or native completion. None of K2's 962 clicks overlapped any of the 16 candidate glyph pixels or their inclusive boxes. F20T5 retrospectively became eligible at cumulative A70; its condition still held at the recorded analyzer boundary after A77. These are **observations on selected historical runs**, not an estimate of general recovery effectiveness, hidden-state equality, or guaranteed counterfactual rescue.

The P50T10 comparator illustrates why noncompletion alone can be misleading: FT09 K0 later completed a flagged level; SP80 K2 completed a level inside the same tool batch after a P alert. F20T5 missed other changing-board no-progress cases. Rules were fixed after seeing the LP85 failure, so no held-out sensitivity/specificity is established. A detector alert is not a completed intervention; context rebuild followed by a subsequent action is not proof of improved outcome.

## Source and distribution boundary

Author: Tsitsino Dzotsenidze (ORCID 0000-0002-9432-1803), with attribution to source ARC-AGI-3 agent upstream providers as recorded in the companion paper/technical archive. The package is newly assembled from **retained analysis**, not newly observed native data. It carries **no assertion of license transfer** for underlying game data or any third-party material. The author has approved MIT-0 for her independently authored methodological prose and pseudocode only; see `LICENSE-MIT-0.txt`, `AUTHOR_LICENSE_APPROVAL.json`, and `ATTRIBUTION_AND_RIGHTS.md` for the exact file scope. The MIT-0 grant does not cover the CSV datasets or third-party/benchmark material. The author separately authorized this selected GitHub publication, as recorded in `PUBLICATION_AUTHORIZATION.json`; publication does not create a new blanket reuse license for underlying material. The checksum manifest covers this public supplement. Cite the immutable repository commit containing this directory as manuscript reference [5]. The two existing Zenodo DOIs remain unchanged and separate: ARC2 `10.5281/zenodo.23895859`; ARC3 `10.5281/zenodo.23869166`.
