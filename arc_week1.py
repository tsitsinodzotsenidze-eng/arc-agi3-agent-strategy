"""Week 1 safety-only infrastructure for deterministic, auditable ARC-AGI-3 runs.

This module intentionally provides only structural and safety contracts:
- deterministic reset/seeding
- structural observation and evidence transport
- strict action parsing with a single fixed fallback
- per-episode lifecycle bookkeeping
- deterministic replay records
- local JSONL/CSV audit logging

It explicitly does NOT implement gameplay intelligence, planning, hypothesis
formation, world modeling, semantic interpretation, or optimization.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import hashlib
import json
import random
from pathlib import Path
from typing import Any, Literal

LifecyclePhase = Literal["initialized", "running", "finished", "failed", "reset"]

_SAFETY_FALLBACK_PLACEHOLDER = "__SAFETY_FALLBACK__"
"""Single structural fallback token used whenever parsing cannot find an action."""


@dataclass(frozen=True)
class ResetEvent:
    episode_id: str
    seed: int


@dataclass(frozen=True)
class ObservationEnvelope:
    """Structural observation contract.

    Only stores raw payload and structural metadata; performs no semantic analysis.
    """

    episode_id: str
    step_index: int
    payload: Any
    payload_type: str
    payload_size: int

    @staticmethod
    def from_payload(episode_id: str, step_index: int, payload: Any) -> "ObservationEnvelope":
        return ObservationEnvelope(
            episode_id=episode_id,
            step_index=step_index,
            payload=payload,
            payload_type=type(payload).__name__,
            payload_size=_safe_size(payload),
        )


@dataclass(frozen=True)
class EvidencePacket:
    """Structural evidence package.

    Performs only type/schema validation and normalized transport.
    """

    episode_id: str
    step_index: int
    observation_type: str
    observation_size: int
    payload: Any

    @staticmethod
    def from_observation(obs: ObservationEnvelope) -> "EvidencePacket":
        return EvidencePacket(
            episode_id=obs.episode_id,
            step_index=obs.step_index,
            observation_type=obs.payload_type,
            observation_size=obs.payload_size,
            payload=obs.payload,
        )


@dataclass(frozen=True)
class ParsedAction:
    raw_action_text: str | None
    action: str
    used_fallback: bool
    note: str


@dataclass
class Scorecard:
    """Per-episode lifecycle scaffold only (no cross-episode metrics)."""

    episode_id: str
    seed: int
    lifecycle: LifecyclePhase = "initialized"
    status_note: str = ""
    step_count: int = 0

    def transition(self, lifecycle: LifecyclePhase, note: str = "") -> None:
        self.lifecycle = lifecycle
        self.status_note = note


@dataclass(frozen=True)
class ReplayEntry:
    episode_id: str
    seed: int
    step_index: int
    lifecycle: LifecyclePhase
    reset_event: bool
    raw_action_text: str | None
    parsed_action: str
    used_fallback: bool
    observation_type: str
    observation_size: int
    status_note: str = ""


class ResetManager:
    """Central deterministic seed/reset harness for stateful components."""

    def __init__(self) -> None:
        self.episode_id = ""
        self.seed = 0
        self.rng = random.Random(0)

    def reset(self, episode_id: str, seed: int) -> ResetEvent:
        self.episode_id = episode_id
        self.seed = seed
        self.rng = random.Random(seed)
        return ResetEvent(episode_id=episode_id, seed=seed)


class ReplayAudit:
    """Deterministic in-memory replay/audit collector.

    Audit artifacts are write-only from perspective of gameplay logic.
    """

    def __init__(self) -> None:
        self._entries: list[ReplayEntry] = []

    def reset(self, episode_id: str, seed: int) -> ResetEvent:
        self._entries.clear()
        return ResetEvent(episode_id=episode_id, seed=seed)

    def append(self, entry: ReplayEntry) -> None:
        self._entries.append(entry)

    @property
    def entries(self) -> tuple[ReplayEntry, ...]:
        return tuple(self._entries)

    def digest(self) -> str:
        payload = json.dumps([asdict(e) for e in self._entries], sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class ActionParser:
    """Strict structural parser with single safe fallback action."""

    def reset(self, episode_id: str, seed: int) -> ResetEvent:
        """Return reset metadata only; parser holds no mutable per-episode state."""
        return ResetEvent(episode_id=episode_id, seed=seed)

    def parse(self, candidate: str | dict[str, Any] | None) -> ParsedAction:
        raw: str | None
        token: str | None

        if isinstance(candidate, str):
            raw = candidate
            token = candidate.strip()
        elif isinstance(candidate, dict):
            raw = json.dumps(candidate, sort_keys=True)
            action_value = candidate.get("action")
            token = action_value.strip() if isinstance(action_value, str) else None
        else:
            raw = None
            token = None

        if isinstance(token, str) and token:
            return ParsedAction(raw_action_text=raw, action=token, used_fallback=False, note="structurally_present")

        return ParsedAction(
            raw_action_text=raw,
            action=_SAFETY_FALLBACK_PLACEHOLDER,
            used_fallback=True,
            note="fallback_due_to_missing_structural_action_token",
        )


class EvaluationLogger:
    """Audit-only local logger for JSONL detail + CSV summary."""

    CSV_FIELDS = [
        "episode_id",
        "seed",
        "step_index",
        "parsed_action",
        "used_fallback",
        "lifecycle",
        "reset_event",
        "status_note",
    ]

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.jsonl_path = self.output_dir / "evaluation_log.jsonl"
        self.csv_path = self.output_dir / "evaluation_summary.csv"

    def reset(self, episode_id: str, seed: int) -> ResetEvent:
        """Return reset metadata only; logger does not mutate persistent episode state."""
        return ResetEvent(episode_id=episode_id, seed=seed)

    def log(self, entry: ReplayEntry) -> None:
        record = asdict(entry)
        with self.jsonl_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, sort_keys=True) + "\n")

        csv_exists = self.csv_path.exists()
        with self.csv_path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_FIELDS)
            if not csv_exists:
                writer.writeheader()
            writer.writerow({k: record[k] for k in self.CSV_FIELDS})


def _safe_size(value: Any) -> int:
    """Return a deterministic structural size for envelope metadata.

    This is intentionally shallow and semantic-free: for common collection/string
    types, use ``len(value)``; for all other payloads, emit ``1`` as a stable
    placeholder unit size.
    """
    if isinstance(value, (str, bytes, list, tuple, dict, set)):
        return len(value)
    return 1
