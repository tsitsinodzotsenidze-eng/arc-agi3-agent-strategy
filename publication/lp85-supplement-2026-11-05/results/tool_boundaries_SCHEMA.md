# Schema and interpretation — tool_boundaries.csv

This CSV is an extract of **historical** tool/callback/analyzer receipts; it is not a synchronized clock trace or a new experimental measurement.

| Field | Meaning |
| --- | --- |
| `trace` | Unique selected arm/game trace key |
| `prefix_action` | Cumulative action ordinal at original rule eligibility |
| `callback_first_action`, `callback_last_action` | Callback span from retained audit |
| `python_tool_first_action`, `python_tool_last_action` | Python tool/batch action span |
| `next_analyzer_actions_completed` | Number of actions completed when a later analyzer entry is recorded |
| `next_analyzer_benchmark_elapsed_s` | Retained analyzer-entry time, with different subsecond alignment from trace action times |
| `native_completion_before_tool_return` | Whether a native level completion occurred before the tool returned |
| `full_grid_unchanged_through_tool_return` | Recorded full-grid equality through tool return, if available |
| `nonterminal_at_tool_return` | Whether native state remained nonterminal through tool return, if available |

The retained action and analyzer-entry timelines are **not strictly aligned at subsecond precision**. Event ordering is established from action cursors, native completion flags and callback/tool membership — **not** from direct timestamp comparison or a claimed dispatch-latency measurement. No offset has been invented or applied.

Examples retained exactly as observed:

| Trace / final action | Action elapsed time (s) | Analyzer-entry (s) | Difference (s) |
| --- | ---: | ---: | ---: |
| K2 LP85 / A77 | 5725.157301632 | 5724.989967 | -0.167334632 |
| K2 SP80 / A55 | 1762.579912911 | 1762.387675 | -0.192237911 |

A70 lies in the K2 LP85 tool spanning A66–A77; the receipt records a subsequent analyzer entry with 77 actions completed and unchanged/nonterminal observations. SP80 completed the flagged level at A55 before the next analyzer entry; an agent policy acting then must recheck eligibility. Neither case establishes an intervention that was actually applied at this boundary.
