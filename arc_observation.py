"""Week 2 Day 1 observation + environment interface scaffold.

This module provides structural observation intake, metadata validation,
and replay-compatible observation transport. It is intentionally semantic-free
and does not introduce planning or gameplay intelligence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from arc_week1 import ReplayEntry, ResetEvent


@dataclass(frozen=True)
class ObservationRecord:
    """Captures raw environment observation with deterministic structural metadata.

    Trust boundary note:
    - caller-provided episode_id/step_index/source_label are accepted as transport metadata
      (source_label is provenance only, never reasoning/planning/decision signal).
    - observation_type/summary_size/summary_keys are always derived from raw_observation.
    - raw_observation serializability is a future replay/logging contract concern.
    """

    episode_id: str
    step_index: int
    raw_observation: Any
    observation_type: str
    source_label: str
    summary_size: int
    summary_keys: tuple[str, ...]

    @staticmethod
    def create(
        episode_id: str,
        step_index: int,
        raw_observation: Any,
        source_label: str = "environment",
    ) -> "ObservationRecord":
        validate_observation_metadata(episode_id=episode_id, step_index=step_index, source_label=source_label)
        validate_observation_shape(raw_observation)
        return ObservationRecord(
            episode_id=episode_id,
            step_index=step_index,
            raw_observation=raw_observation,
            observation_type=type(raw_observation).__name__,
            source_label=source_label,
            summary_size=_safe_size(raw_observation),
            summary_keys=_summary_keys(raw_observation),
        )


class EnvironmentInterface(Protocol):
    """Minimal environment wrapper protocol for deterministic observation intake."""

    def reset(self, episode_id: str, seed: int) -> ResetEvent:
        ...

    def observe(self, episode_id: str, step_index: int) -> ObservationRecord:
        ...


class EnvironmentObserver:
    """Adapter that validates and standardizes environment observations."""

    def __init__(self, environment: EnvironmentInterface, source_label: str = "environment") -> None:
        self.environment = environment
        self.source_label = source_label

    def reset(self, episode_id: str, seed: int) -> ResetEvent:
        return self.environment.reset(episode_id, seed)

    def observe(self, episode_id: str, step_index: int) -> ObservationRecord:
        # Trust boundary:
        # - keep upstream episode_id/step_index/source_label as transport metadata only
        #   (source_label is provenance only, never a gameplay/evaluator hint).
        # - never trust upstream structural metadata fields; recompute canonical
        #   observation_type/summary_size/summary_keys from raw_observation.
        # - raw_observation serializability is intentionally out of scope for this scaffold.
        upstream = self.environment.observe(episode_id, step_index)
        validate_observation_metadata(
            episode_id=upstream.episode_id,
            step_index=upstream.step_index,
            source_label=upstream.source_label or self.source_label,
        )
        validate_observation_shape(upstream.raw_observation)
        return ObservationRecord.create(
            episode_id=upstream.episode_id,
            step_index=upstream.step_index,
            raw_observation=upstream.raw_observation,
            source_label=upstream.source_label or self.source_label,
        )

    @staticmethod
    def to_replay_entry(record: ObservationRecord, *, seed: int, status_note: str = "observation_only") -> ReplayEntry:
        return ReplayEntry(
            episode_id=record.episode_id,
            seed=seed,
            step_index=record.step_index,
            lifecycle="running",
            reset_event=False,
            raw_action_text=None,
            # Sentinel for observation-transport-only replay rows; not a real action.
            # Replay/action consumers must filter or treat this as non-action metadata.
            parsed_action="__OBSERVATION_ONLY__",
            used_fallback=False,
            observation_type=record.observation_type,
            observation_size=record.summary_size,
            status_note=status_note,
        )


def validate_observation_metadata(*, episode_id: str, step_index: int, source_label: str) -> None:
    if not isinstance(episode_id, str) or not episode_id.strip():
        raise ValueError("episode_id must be a non-empty string")
    if not isinstance(step_index, int) or step_index < 0:
        raise ValueError("step_index must be a non-negative integer")
    if not isinstance(source_label, str) or not source_label.strip():
        raise ValueError("source_label must be a non-empty string")


def validate_observation_shape(raw_observation: Any) -> None:
    if raw_observation is None:
        raise ValueError("raw_observation must not be None")


def _summary_keys(raw_observation: Any) -> tuple[str, ...]:
    if isinstance(raw_observation, dict):
        return tuple(sorted(str(k) for k in raw_observation.keys()))
    return ()


def _safe_size(value: Any) -> int:
    if isinstance(value, (str, bytes, list, tuple, dict, set)):
        return len(value)
    return 1
