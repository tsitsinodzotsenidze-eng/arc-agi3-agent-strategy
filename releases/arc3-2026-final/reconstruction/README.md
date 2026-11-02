# K1+VIR: exact reconstruction from an authorized source

This public artifact is a reconstruction recipe, not the original full submitted script. It intentionally excludes the complete upstream-derived `tool_agent.py` and `solver.py` overlay bodies. The unchanged complete captured carrier is retained separately and is identified by SHA-256 `ff48afd724423b8de9ae5e0acc70952ad8d4dc4a5a75ac59516c719adcfe77ca`, saved Kaggle script version **362929164**.

The independently authored `vir_adapter.py` is included. `K1VIR_source_edits.json` contains base/target hashes, zero-based source-line edit positions, removal counts and inserted project text only. It does not reproduce unchanged or removed upstream source. `K1VIR_carrier.py.template` contains the original carrier with the two encoded overlay bodies replaced by placeholders. Do not use the template as a runnable submission.

With an authorized copy of the exact `recovery-study-ii-source-v1-3.sqlite`, run:

```sh
python reconstruct_k1vir.py --source-sqlite /path/to/recovery-study-ii-source-v1-3.sqlite --output /new/path/K1VIR_script_362929164.py
```

The utility reads SQLite in read-only mode, verifies source ZIP and base-file hashes, applies the numeric edits, verifies both target-file hashes, reconstructs the original compressed payloads, and finally verifies the complete captured-script SHA-256. It writes to a new output path only. It does not deserialize pickles, execute the resulting carrier, start inference or play games.

A source-only packaging verification reproduced all **201,145 bytes** of the captured K1+VIR script exactly. This verifies reconstruction from the pinned authorized base, not public accessibility of that base or live model performance. The source dataset is currently private with unknown license metadata; full independent reproduction remains limited by external access and terms.

Upstream original source remains subject to its own terms. The reconstruction instructions and independently authored changes do not grant or replace an upstream license.

