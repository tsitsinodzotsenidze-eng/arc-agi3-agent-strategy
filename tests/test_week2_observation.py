import pytest

from arc_observation import (
    EnvironmentObserver,
    ObservationRecord,
    validate_observation_metadata,
    validate_observation_shape,
)


class _FakeEnvironment:
    def reset(self, episode_id: str, seed: int):
        return None

    def observe(self, episode_id: str, step_index: int) -> ObservationRecord:
        return ObservationRecord.create(
            episode_id=episode_id,
            step_index=step_index,
            raw_observation={"pixels": [[1, 0], [0, 1]], "id": episode_id},
            source_label="fake_env",
        )


class _SpoofedMetadataEnvironment:
    def reset(self, episode_id: str, seed: int):
        return None

    def observe(self, episode_id: str, step_index: int) -> ObservationRecord:
        return ObservationRecord(
            episode_id=episode_id,
            step_index=step_index,
            raw_observation={"b": 2, "a": 1},
            observation_type="list",
            source_label="spoofed_env",
            summary_size=99,
            summary_keys=("wrong",),
        )


def test_valid_observation_record_creation_is_structural_and_deterministic():
    record = ObservationRecord.create(
        episode_id="ep-obs-1",
        step_index=2,
        raw_observation={"b": 2, "a": 1},
        source_label="grid_env",
    )

    assert record.episode_id == "ep-obs-1"
    assert record.step_index == 2
    assert record.observation_type == "dict"
    assert record.summary_size == 2
    assert record.summary_keys == ("a", "b")


def test_invalid_observation_shape_and_metadata_raise_value_error():
    with pytest.raises(ValueError):
        ObservationRecord.create("", 0, {"x": 1})

    with pytest.raises(ValueError):
        ObservationRecord.create("ep", -1, {"x": 1})

    with pytest.raises(ValueError):
        validate_observation_shape(None)

    with pytest.raises(ValueError):
        validate_observation_metadata(episode_id="ep", step_index=0, source_label="")


def test_environment_observer_generates_replay_compatible_entries():
    observer = EnvironmentObserver(_FakeEnvironment())
    record = observer.observe("ep-obs-2", 1)
    replay_entry = observer.to_replay_entry(record, seed=42)

    assert replay_entry.episode_id == "ep-obs-2"
    assert replay_entry.step_index == 1
    assert replay_entry.observation_type == "dict"
    assert replay_entry.observation_size == 2
    assert replay_entry.parsed_action == "__OBSERVATION_ONLY__"


def test_observation_record_deterministic_metadata_behavior():
    payload = {"z": 0, "a": [1, 2, 3]}
    r1 = ObservationRecord.create("ep-det", 0, payload, source_label="env")
    r2 = ObservationRecord.create("ep-det", 0, payload, source_label="env")

    assert r1.summary_size == r2.summary_size
    assert r1.summary_keys == r2.summary_keys
    assert r1.observation_type == r2.observation_type


def test_environment_observer_recomputes_spoofed_structural_metadata():
    observer = EnvironmentObserver(_SpoofedMetadataEnvironment())
    record = observer.observe("ep-spoof", 3)

    assert record.observation_type == "dict"
    assert record.summary_size == 2
    assert record.summary_keys == ("a", "b")
