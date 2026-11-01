# Reproduction and source identity

## Canonical carriers

Use the saved version URLs in `provenance/source_captures.json`. Do not substitute the notebook's latest version: the historical K2 result belongs to saved **Version 2 / 353983921**, while that notebook has later versions. Source transcriptions are preserved as captured, without execution or header edits.

## K0 and K1+VIR attached inputs

The K0 saved-version Input UI showed **11 inputs**: the ARC-AGI-3 competition, three datasets, and seven model variants. The datasets were `Qwen3.8 Flash Next vLLM NVFP4 runtime v1`, `Recovery Study II P01 Source v1.3`, and `Recovery Study II Source v1.3 SQLite`. The K0 spec records `alykassem202/qwen38-flash-next-vllm-nvfp4-runtime-v1` and `tsitsinodzotsenidze/recovery-study-ii-p01-source-v1-3`. The SQLite file is identified by its exact filename and payload hash below; a dataset URL/version was not recovered in this preparation and must not be guessed.

The seven version-1 model inputs are under `tsitsinodzotsenidze/rsii-qwen38-nvfp4-exact-r7b71922/PyTorch/`: `metadata-full`, then `weights-01` through `weights-06`. The full saved-version Input page is the authoritative attachment list. Dataset accessibility and licenses must be verified before claiming independent reproduction is complete.

The underlying model identity is `RadixArk/Qwen3.8-Flash-Next-NVFP4`, revision `7b719225242aacd3dbd3f9407468c2ee9a9d2594`: 419 files, 135,253,622,894 bytes. The historical source identity records original manifest SHA-256 `a09bdad3fe3240c73332c0f99f4388a547205cb488c127f9b9059c9267dd9a5b`, but its original manifest bytes were **not recovered**. The mirror uses an independently derived inventory for the pinned payload, replacement manifest SHA-256 `1af2f34b1be2734e68568fc9a214a25b68a4b2be89f0554ad475e3509da02748`; this replacement is the effective `model.manifest_sha256` in both submitted candidate specs. The specs require all 419 file hashes. These identities were read from preserved records; weights were not rehashed in this packaging pass. Distinct manifest hashes must not be described as identical manifest bytes.

The exact source SQLite filename is `recovery-study-ii-source-v1-3.sqlite`. It contains the ZIP payload selected by `source_payload.id=1`, size **15,201,714 bytes**, SHA-256 `6f65ba6b720e304fd66dcec701fe30632896d781db09622bf39773364b7567d1`. Size and hash were rechecked read-only during packaging. The archive has 4,408 members. It contains serialized benchmark/deploy objects and is not blindly redistributed here. No pickle was deserialized. Source and runtime remain external licensed dependencies, not silently relicensed repository content.

## Runtime

Use the saved notebook's GPU RTX Pro 6000 settings, Internet OFF, seed 1729, and recorded time-budget/serving configuration. The October measured Kaggle host was CPython **3.12.13**; repository Python 3.11 CI is separate. The carrier requires a compatible CPython 3.12 host with real NVIDIA driver, glibc >=2.28, and recorded build tools. Its selected vLLM layers are pinned in the source identity; they are not a byte-exact copy of the entire original root filesystem.

The K0 spec and source preserve frozen-policy identities and recovery `k=0`. The K1+VIR spec and source preserve their own overlay/configuration; do not interchange the two specs. The historical K2 carrier has its own saved runtime and inputs, which must be recovered from that exact version rather than assumed identical to October K0.

## Kaggle packaging and official scoring

1. Copy the intended saved carrier with all inputs. Replace only source code if needed; notebook import previously removed attached inputs. Configure compatible recorded runtime and verify the attached dependency list.
2. A normal saved run uses the carrier's packaging path. The official rerun is distinguished by `KAGGLE_IS_COMPETITION_RERUN`; the script routes to the competition gateway, which owns `submission.parquet`. A short packaging run is not hidden-game inference or a scored study arm.
3. The human competitor submits the exact saved notebook version and output file, then verifies successful scoring and final selections in Kaggle. Do not replace the official exporter with a local writer or treat a placeholder packaging output as scored predictions.

The archive does not reproduce Kaggle's hidden games or reveal their content. Public scores are descriptive competition outcomes. Full gameplay archive auditing and repeated matched experiments remain separate scientific work.
