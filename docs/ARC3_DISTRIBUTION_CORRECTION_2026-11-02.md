# Distribution-scope correction — 2 November 2026

## Reason and scope

Release `arc3-2026-final-1` was published at commit `a327427e39b2b750927021983d68bd43d7cdb497`. Its captured K1+VIR script embeds two complete modified upstream-derived file bodies. The checked upstream Tufalabs/duck-harness repository has no root LICENSE; its MIT package classifier and downstream Apache notebook label do not establish an explicit component-level grant. Inspected issues #6 and #8 contained no rights-holder clarification.

This correction removes `code/K1VIR_script_362929164.py` from the current distribution and supplies `reconstruction/`: a carrier template, independently authored VIR adapter, numeric edit recipe, and reconstruction utility. The recipe includes project insertion text, line offsets and removal counts; it omits unchanged and deleted upstream text. Exact authorized upstream source remains an external prerequisite.

## Source identity and validation

The canonical submission remains Kaggle saved Version 1 / **362929164**. Its captured script is **201,145 bytes**, SHA-256 `ff48afd724423b8de9ae5e0acc70952ad8d4dc4a5a75ac59516c719adcfe77ca`. Read-only reconstruction reproduced those bytes exactly. The reconstruction check did not execute the generated carrier, deserialize pickle objects, run a model, play games, or launch Kaggle scoring.

The external SQLite dependency was identified as Version 1 of https://www.kaggle.com/datasets/tsitsinodzotsenidze/recovery-study-ii-source-v1-3-sqlite . It displayed Private and License: Unknown. It is excluded and is not relicensed. Model weights, serving layers, hidden games and full gameplay archives remain external.

## Version and archive handling

The existing `arc3-2026-final-1` tag and source commit are preserved. A new `arc3-2026-final-2` release is intended for this correction; its actual publication must be verified. Removing files from the current revision does not erase earlier public Git history.

The original complete preparation ZIP remains unchanged separately: 323,071 bytes; SHA-256 `908e2a4257ea735c00685427e41a70fed3ce87ede9154aa32d58d968f95d3011`. The corrected public ZIP is a different artifact and must have its own filename and checksums. It must replace the original file in the existing unpublished Zenodo draft **23869166** before publication. The reserved DOI **10.5281/zenodo.23869166** is not a published deposit yet.

## Scientific and competition boundaries

Public scores remain K0 **3.32**, historical K2 **3.10**, and K1+VIR **2.61**: descriptive, unreplicated observations. The correction does not change submitted notebook code, attached inputs, Kaggle visibility, scores, or human final selections. It does not certify a fully public runnable environment or claim that repository Apache-2.0 terms relicense external material.

