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


_REPLAY_AUDIT_FACTORY_KEY = object()
_MISSING_AUTHORITY = object()


@dataclass(frozen=True, slots=True, eq=False, init=False)
class AuditReadAuthority:
    """Opaque, immutable capability for one specific ReplayAudit instance.

    Capabilities are minted only through ReplayAuditOwner. Object identity is
    intentionally significant; matching field values never confer authority.
    """

    _audit_instance_id: object
    _token: object

    def __init__(self) -> None:
        raise TypeError("AuditReadAuthority has no public constructor")

    @classmethod
    def _mint(cls, *, factory_key: object, audit_instance_id: object) -> "AuditReadAuthority":
        if factory_key is not _REPLAY_AUDIT_FACTORY_KEY:
            raise PermissionError("AuditReadAuthority may be minted only by ReplayAuditOwner")
        authority = object.__new__(cls)
        object.__setattr__(authority, "_audit_instance_id", audit_instance_id)
        object.__setattr__(authority, "_token", object())
        return authority

    @property
    def audit_instance_id(self) -> object:
        return self._audit_instance_id


class ReplayAudit:
    """Deterministic in-memory replay/audit collector.

    Audit artifacts are write-only from the perspective of gameplay logic.
    Reads require an active capability issued by this audit's paired owner.

    This is an internal repository-integrity boundary, not adversarial
    isolation from arbitrary Python code executing in the same process.
    """

    def __init__(self) -> None:
        raise TypeError("ReplayAudit instances must be created by _create_replay_audit()")

    @classmethod
    def _create(cls, *, factory_key: object) -> "ReplayAudit":
        if factory_key is not _REPLAY_AUDIT_FACTORY_KEY:
            raise PermissionError("ReplayAudit may be created only by the internal factory")
        audit = object.__new__(cls)
        audit._entries = []
        audit._audit_instance_id = object()
        audit._owner = None
        audit._active_read_authorities = {}
        return audit

    def _bind_owner(self, owner: "ReplayAuditOwner", *, factory_key: object) -> None:
        if factory_key is not _REPLAY_AUDIT_FACTORY_KEY or self._owner is not None:
            raise PermissionError("ReplayAudit owner binding is factory-only and single-use")
        self._owner = owner

    def _require_owner(self, owner: "ReplayAuditOwner") -> None:
        if owner is not self._owner:
            raise PermissionError("ReplayAudit owner does not match this audit")

    def _grant_read_authority(self, owner: "ReplayAuditOwner") -> AuditReadAuthority:
        self._require_owner(owner)
        authority = AuditReadAuthority._mint(
            factory_key=_REPLAY_AUDIT_FACTORY_KEY,
            audit_instance_id=self._audit_instance_id,
        )
        self._active_read_authorities[authority] = authority._token
        return authority

    def _revoke_read_authority(self, owner: "ReplayAuditOwner", authority: object) -> None:
        self._require_owner(owner)
        self._require_read_authority(authority)
        del self._active_read_authorities[authority]

    def _require_read_authority(self, authority: object) -> AuditReadAuthority:
        if type(authority) is not AuditReadAuthority:
            raise PermissionError("ReplayAudit read authority is required")
        registered_token = self._active_read_authorities.get(authority, _MISSING_AUTHORITY)
        if (
            registered_token is _MISSING_AUTHORITY
            or authority._audit_instance_id is not self._audit_instance_id
            or authority._token is not registered_token
        ):
            raise PermissionError("ReplayAudit read authority is invalid or inactive")
        return authority

    def reset(self, episode_id: str, seed: int) -> ResetEvent:
        self._entries.clear()
        return ResetEvent(episode_id=episode_id, seed=seed)

    def append(self, entry: ReplayEntry) -> None:
        self._entries.append(entry)

    def entries(self, authority: AuditReadAuthority) -> tuple[ReplayEntry, ...]:
        self._require_read_authority(authority)
        return tuple(self._entries)

    def digest(self, authority: AuditReadAuthority) -> str:
        self._require_read_authority(authority)
        payload = json.dumps([asdict(e) for e in self._entries], sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class ReplayAuditOwner:
    """Owner paired with one ReplayAudit and sole issuer of read authority."""

    __slots__ = ("_audit",)

    def __init__(self) -> None:
        raise TypeError("ReplayAuditOwner has no public constructor")

    @classmethod
    def _create(cls, audit: ReplayAudit, *, factory_key: object) -> "ReplayAuditOwner":
        if factory_key is not _REPLAY_AUDIT_FACTORY_KEY:
            raise PermissionError("ReplayAuditOwner may be created only by the internal factory")
        owner = object.__new__(cls)
        owner._audit = audit
        return owner

    def grant_read_authority(self) -> AuditReadAuthority:
        return self._audit._grant_read_authority(self)

    def revoke_read_authority(self, authority: object) -> None:
        self._audit._revoke_read_authority(self, authority)


def _create_replay_audit() -> tuple[ReplayAudit, ReplayAuditOwner]:
    """Create a ReplayAudit and its sole authority owner as one atomic pair."""
    audit = ReplayAudit._create(factory_key=_REPLAY_AUDIT_FACTORY_KEY)
    owner = ReplayAuditOwner._create(audit, factory_key=_REPLAY_AUDIT_FACTORY_KEY)
    audit._bind_owner(owner, factory_key=_REPLAY_AUDIT_FACTORY_KEY)
    return audit, owner


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
    if isinstance(value, (str, list, tuple, dict)):
        return len(value)
    return 1
