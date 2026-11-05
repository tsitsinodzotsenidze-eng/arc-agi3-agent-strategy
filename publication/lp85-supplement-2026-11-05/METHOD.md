# Method and decision boundaries (exact pseudocode)

**Scope:** six purposively selected traces; October 2026 offline diagnostic. The native per-action signal fields, not end-of-run labels, are the sole detector inputs. At every action, online level starts at 1 and increments only when `native_level_completed` is observed. An action ordinal is the game's cumulative ordinal.

```text
level = 1; level_entry_time = trace_start_elapsed_s; level_entry_ordinal = 0
previous_observation_time = trace_start_elapsed_s
full_n = 0; full_anchor = trace_start_elapsed_s
emit_first_event_once_per_(level, rule)

for each observed action a in chronological order:
    t = a.benchmark_elapsed_s; ordinal = a.action_ordinal
    if a.native_level_completed:
        level += 1
        level_entry_time = t; level_entry_ordinal = ordinal
        full_n = 0; full_anchor = t; previous_observation_time = t
        continue
    if native_terminal(a) or a.action starts with "RESET":
        full_n = 0; full_anchor = t; previous_observation_time = t
        continue  # P50T10 level exposure is NOT reset by ordinary RESET

    if a.full_grid_same_as_preceding:
        if full_n == 0: full_anchor = previous_observation_time
        full_n += 1
    else:
        full_n = 0; full_anchor = t

    F20T5 = full_n >= 20 AND (t - full_anchor) >= 300 seconds
    P50T10 = (ordinal - level_entry_ordinal) >= 50
              AND (t - level_entry_time) >= 600 seconds
    if any rule eligible and not yet emitted for current (level, rule):
        emit current action ordinal, time, current online level and counters
    previous_observation_time = t
```

Native terminal status means any of `game_over`, `done`, `run_complete`, or a native state other than `NOT_FINISHED`. Ordinary RESET/terminal observations cannot themselves trigger either rule. The source additionally evaluated M20T5 with the same F conditions but excluding row 63. **M20T5 is an inherited historical sensitivity result, not independently recomputable from this supplement**: the masked-grid comparison inputs are deliberately omitted. Its saved rows are retained as historical outputs only; manuscript claims rely on F20T5 and P50T10. M20T5 is not a general mask and does not constitute an independently validated detector. The source scanner first-event result was checked against prefix truncations and removal of final-derived levels; those checks were already present in the retained original diagnostic and **were not rerun for this export**.

**Visual click overlap:** Treat row and column as zero-based board pixel indices; a click at `(r,c)` intersects the candidate box `[r0,c0,r1,c1]` iff `r0 <= r <= r1 AND c0 <= c <= c1`. Intersects a candidate glyph iff `(r,c)` belongs to its listed 10 colored pixels. Use the 962 LP85 K2 level-4 click coordinates (online level 4), count occurrences and overlaps. These are coordinate checks against **visual shapes**, not engine hitboxes. The original component selection was LP85-specific: 4-connected same-color regions on the retained native entry frame, color indices 8 or 14 and area exactly 10 pixels. The derived 160 pixels are included; the source frame is not.

**Clock, boundaries, and later outcomes:** F20T5's unchanged-run start is anchored to the preceding observed frame's timestamp on the first unchanged transition; it does not become eligible through waiting alone. A70 is in a Python tool covering A66–A77; after its return, the next analyzer entry had 77 actions completed, 95.42 benchmark minutes and an unchanged nonterminal grid. P50T10 triggered at SP80 A50; by the next analyzer entry, SP80 had completed the flagged level at action 55. A policy acting at that boundary would therefore have to recheck eligibility. `later_baseline_completion` means a **subsequent completion in that same retained historical trajectory**; it is neither a separate matched baseline arm nor a post-intervention outcome. These later outcomes are retrospective labels only and do not enter eligibility. Six distinct action traces produce eight case summaries because LP85 K0 and LP85 K2 each appear once for their level-4 diagnostic and once as a whole-trace guard case. The export is not eight independent trajectories.

**Limitations:** thresholds selected after LP85 was known; no blind validation, no population accuracy, no hidden-state equivalence, no matched causal recovery evaluation, no replayed counterfactual click. A moving grid need not imply useful progress; an unmoving grid need not prove that context recovery will solve the game. Full-grid digest equality and selected coordinates are source-derived observations, not an independently replayed native environment.


## Timestamp alignment and boundary-table interpretation

The retained action and analyzer-entry timelines are **not strictly aligned at subsecond precision**. Event ordering is established by **cumulative action cursors, native completion observations, and callback/Python-tool membership**, not by comparing these timestamps or estimating dispatch latency. No artificial time offset has been added.

- K2 LP85 A77: action 5725.157301632 s; next analyzer-entry receipt 5724.989967 s (difference -0.167334632 s).
- K2 SP80 A55: action 1762.579912911 s; next analyzer-entry receipt 1762.387675 s (difference -0.192237911 s).

The boundary receipt shows a model-control opportunity after the recorded action batch, **not** an intervention executed there. The quoted elapsed times cannot support subsecond cause/order/latency assertions. See `results/tool_boundaries_SCHEMA.md`.

## Completion records versus per-action flags

`native_level_completion_flag_count` in `provenance.json` counts true action-level `native_level_completed` flags. The separate `retained_completion_record_count` preserves the original cache's count, which includes the final WIN record for K0 LP85 (7 true flags, 8 retained records; WIN at A160) and K2 FT09 (5 true flags, 6 retained records; WIN at A101). Both final WIN rows recorded `done=true`, `run_complete=true`, and `native_level_completed=false`. Historical totals and native flags have **not** been changed.
