# ARC-AGI-3 — publication, rights and deposit audit (2 November 2026)

**Scope:** Supplemental publication note accompanying PR #39. This note is **not in the already validated Zenodo ZIP**. It does not replace or alter the immutable Kaggle saved-version source captures, the packaged `SHA256SUMS.json`, the stored ZIP, or the reserved DOI.

## Verified identifiers and status

- Competitor and record creator: **Tsitsino Dzotsenidze**; Zenodo creator metadata: **Dzotsenidze, Tsitsino**.
- GitHub PR #39 originally prepared at head `1e3af78d66b0bbb938989c31bc796f658bec1c16`; CI `Python tests` succeeded. When merged, cite the resulting release/tag or immutable GitHub commit.
- Zenodo manually prepared draft: **https://zenodo.org/uploads/23869166**; DOI **10.5281/zenodo.23869166**, **reserved, not yet registered/published**. The competitor's handoff reports complete ZIP upload, a saved draft and a file identity check against the prepared original; this supplementary audit has not reauthenticated to Zenodo or independently read the private draft.
- Official rounded *public* Kaggle scores: K0 **3.32** ([saved version 362927490](https://www.kaggle.com/code/tsitsinodzotsenidze/rsii-k0-submission-2?scriptVersionId=362927490)); historical K2 **3.10** ([saved version 353983921](https://www.kaggle.com/code/tsitsinodzotsenidze/notebook43f8579dd8?scriptVersionId=353983921)); K1+VIR **2.61** ([saved version 362929164](https://www.kaggle.com/code/tsitsinodzotsenidze/rsii-k1vir-submission?scriptVersionId=362929164)). No replicated causal recovery effect or final/private score is claimed.

## License and authorship matrix — do not conflate

1. **Original code/methodology and documentation authored for this repository:** repository `LICENSE` states Apache-2.0. This applies to original repository material to which the author holds the necessary rights, **not** by default to embedded or referenced upstream code.
2. **Keith Tyser's [Duck Qwen3.8 Flash Next NVFP4 MTP Kaggle notebook](https://www.kaggle.com/code/keithtyser/duck-qwen3-8-flash-next-nvfp4-mtp):** Kaggle displays **Apache License 2.0** for that *notebook*. Record its author and saved-version provenance. This label does **not independently license every external bundled dependency**.
3. **Tufa Labs, the Duck/TAAF harness:** source project [Tufalabs/duck-harness](https://github.com/Tufalabs/duck-harness) and [Tufa Labs' public research post](https://tufalabs.ai/research/duck-harness/) identify their authorship. The GitHub project has **no root `LICENSE` file** in the checked revision; a public [license clarification issue #8](https://github.com/Tufalabs/duck-harness/issues/8) remains open. Therefore do not assign it Apache, MIT, CC0 or any other code license based solely on the GitHub URL or public availability. The referenced source SQLite and complete upstream harness are **not separately included as extracted source archives** in this repository's release ZIP. Provenance/credit remains required.
4. **Model:** [RadixArk/Qwen3.8-Flash-Next-NVFP4](https://huggingface.co/RadixArk/Qwen3.8-Flash-Next-NVFP4), pinned revision `7b719225242aacd3dbd3f9407468c2ee9a9d2594`, is based on Qwen/Qwen3.8-Flash-Next. RadixArk points to the **base model terms** (Qwen Community License 1.0); separate third-party mirrors confirm that inheritance. **Model weights are NOT in this release ZIP.** This archive does not sublicense the external weights.
5. **Requests 2.32.5 embedded helper wheel:** its Apache-2.0 license text is retained as `releases/arc3-2026-final/third_party/requests-2.32.5-LICENSE`. Other source/carrier helper notices need to remain with the transcriptions.
6. **Dataset/benchmark and runtime inputs:** Kaggle competition content, Tufa/Duck source archives, runtime images, seven Kaggle model partitions and hidden tests are **not included** as independent datasets/weights. External terms and public access are source-dependent.

**ARC Prize general licensing distinction:** [ARC Prize 2026](https://arcprize.org/competitions/2026) says submitter-authored code and methods should be publicly released under a permissive *public-domain* license (examples MIT-0/CC0), while third-party code must be under a shareable open-source license. The repository currently retains Apache-2.0 for the author's original contributions. **Prize-license conformance is not certified by this audit**; changing grants for original material requires an explicit rights-holder decision, and no grant can cover third-party content without authority. GitHub public visibility does not itself settle this requirement.

## Dependency/source reproducibility boundary

The source SQLite file is exactly `recovery-study-ii-source-v1-3.sqlite`, containing selected ZIP payload `source_payload.id=1`, length **15,201,714 bytes**, SHA-256 `6f65ba6b720e304fd66dcec701fe30632896d781db09622bf39773364b7567d1`. Its authenticated *Kaggle dataset URL and version* have not been independently recovered from the current sources; avoid guessing a slug. The relevant source and seven model attachments must be inspected on the exact saved notebook Input pages when access is available.

K2 code in the ZIP is reconstructed from nine source cells, **not** claimed as the byte-exact original Kaggle notebook; K0 and K1+VIR are exact captured rendered source text, not raw download bytes. Original and replacement model manifest hashes are different even when the pinned model file identity is preserved. Full independent re-execution is not claimed.

## Publication procedure / archive integrity

- The previously uploaded and verified ZIP corresponds to the **original preparation snapshot**. Files in that ZIP must remain unchanged if its identity is to remain valid. This additional outside-the-ZIP note can be linked from the final repository/Zenodo metadata without silently altering that ZIP.
- **If any packaged file is changed**, rebuild the archive, regenerate its SHA-256 manifest and ZIP digest, recheck the contents and **replace/re-upload the Zenodo draft asset before publication**. Never claim that a changed ZIP is byte-identical to the previous upload.
- First publish/merge the examined GitHub source. Create a stable GitHub release/tag, record the exact commit hash and release URL. Zenodo's related identifier should link to that release; the ZIP/description must identify the snapshot it represents, including any separate supplementary note.
- Zenodo draft must show the correct creator, artifact type (software), reserved DOI, descriptive-only results, external-code/weight exclusions and appropriate rights/attribution statement. **Do not state that the DOI is published until Zenodo confirms publication**.
- Kaggle final selection and source notebook visibility are separate human-controlled competition actions; GitHub/Zenodo publishing does not perform these actions.
- The joint ARC-AGI-2 + ARC-AGI-3 Paper Track manuscript is a distinct deliverable, not this ARC3-specific technical archive.

## Sources checked

- https://www.kaggle.com/code/keithtyser/duck-qwen3-8-flash-next-nvfp4-mtp
- https://github.com/Tufalabs/duck-harness
- https://github.com/Tufalabs/duck-harness/issues/8
- https://tufalabs.ai/research/duck-harness/
- https://huggingface.co/RadixArk/Qwen3.8-Flash-Next-NVFP4
- https://huggingface.co/Qwen/Qwen3.8-Flash-Next
- https://arcprize.org/competitions/2026
- https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/
