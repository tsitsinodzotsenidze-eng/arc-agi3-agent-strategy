# Interpretation of saved case and first-event records

`results/fixed_rule_case_results.csv` contains **eight case summaries from six distinct selected action traces**, because each LP85 K0 and LP85 K2 trace is represented twice: a level-4 case and a whole-trace guard check. These are **not** eight independent games or independent observations.

- **F20T5**: 20 consecutive full-grid-unchanged transitions spanning at least 300 s in a level, no intervening native completion, visible change, RESET or terminal state. Exact pseudocode: `../METHOD.md`.
- **P50T10**: at least 50 actions and 600 s from the current online level boundary without native completion; ordinary RESET does not erase accumulated level exposure. RESET/terminal rows do not themselves trigger the alert.
- **M20T5**: **inherited historical sensitivity output only.** Recalculation needs masked-grid comparison inputs (row 63 excluded), which are **not distributed in this candidate**. Retained M20T5 rows are not independently reproducible from these CSVs; the paper does not rely on them.
- **`later_baseline_completion`**: completion later in the **same historical trace**, a retrospective label, **not** a separate baseline arm or an outcome of a recovery intervention. Related time/action-to-later-completion fields are similarly retrospective. Do not include these fields in prefix-only detector eligibility logic.
- **`eligible_levels` / `eligible_later_completed_levels`**: historical summaries, not an independently randomized or held-out validation estimate.

`results/first_eligible_events.csv` records saved, first observed prefix-eligible events and includes separate retrospective labels. The package's methods permit recalculating F20T5/P50T10 from the selected action fields; **the historical algorithms have not been rerun or re-evaluated** in this documentary patch.
