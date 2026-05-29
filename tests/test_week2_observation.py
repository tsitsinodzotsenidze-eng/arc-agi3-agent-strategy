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
    raw_observation = {"b": 2, "a": 1}
    spoofed_observation_type = "list"
    spoofed_summary_size = 99
    spoofed_summary_keys = ("wrong",)

    def reset(self, episode_id: str, seed: int):
        return None

    def observe(self, episode_id: str, step_index: int) -> ObservationRecord:
        return ObservationRecord(
            episode_id=episode_id,
            step_index=step_index,
            raw_observation=self.raw_observation,
            observation_type=self.spoofed_observation_type,
            source_label="spoofed_env",
            summary_size=self.spoofed_summary_size,
            summary_keys=self.spoofed_summary_keys,
        )


class _InvalidShapeEnvironment:
    def reset(self, episode_id: str, seed: int):
        return None

    def observe(self, episode_id: str, step_index: int) -> ObservationRecord:
        return ObservationRecord(
            episode_id=episode_id,
            step_index=step_index,
            raw_observation={"pixels": object()},
            observation_type="dict",
            source_label="invalid_env",
            summary_size=1,
            summary_keys=("pixels",),
        )


class _InvalidReturnEnvironment:
    def reset(self, episode_id: str, seed: int):
        return None

    def observe(self, episode_id: str, step_index: int):
        return {"raw_observation": {"pixels": [[1]]}}


class _MismatchedEpisodeEnvironment:
    def reset(self, episode_id: str, seed: int):
        return None

    def observe(self, episode_id: str, step_index: int) -> ObservationRecord:
        return ObservationRecord.create(
            episode_id="different-episode",
            step_index=step_index,
            raw_observation={"pixels": [[1]]},
            source_label="mismatched_env",
        )


class _MismatchedStepEnvironment:
    def reset(self, episode_id: str, seed: int):
        return None

    def observe(self, episode_id: str, step_index: int) -> ObservationRecord:
        return ObservationRecord.create(
            episode_id=episode_id,
            step_index=step_index + 1,
            raw_observation={"pixels": [[1]]},
            source_label="mismatched_env",
        )


class _InvalidSourceLabelEnvironment:
    def __init__(self, source_label):
        self.source_label = source_label

    def reset(self, episode_id: str, seed: int):
        return None

    def observe(self, episode_id: str, step_index: int) -> ObservationRecord:
        return ObservationRecord(
            episode_id=episode_id,
            step_index=step_index,
            raw_observation={"pixels": [[1]]},
            observation_type="dict",
            source_label=self.source_label,
            summary_size=1,
            summary_keys=("pixels",),
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
    assert record.raw_observation == {"b": 2, "a": 1}
    assert record.observation_type == "dict"
    assert record.summary_size == 2
    assert record.summary_keys == ("a", "b")


def test_invalid_observation_shape_and_metadata_raise_value_error():
    with pytest.raises(ValueError):
        ObservationRecord.create("", 0, {"x": 1})

    with pytest.raises(ValueError):
        ObservationRecord.create("ep", -1, {"x": 1})

    with pytest.raises(ValueError):
        ObservationRecord.create("ep", True, {"x": 1})

    validate_observation_shape(None)
    validate_observation_shape({"pixels": [[1, None], [0, 1]], "done": False, "score": 1.5})

    with pytest.raises(ValueError):
        validate_observation_shape(b"raw-bytes")

    with pytest.raises(ValueError):
        validate_observation_shape({"colors": {1, 2, 3}})

    with pytest.raises(ValueError):
        validate_observation_shape({"pixels": object()})

    with pytest.raises(ValueError):
        validate_observation_shape({("not", "scalar"): 1})

    cyclic_observation = []
    cyclic_observation.append(cyclic_observation)
    with pytest.raises(ValueError):
        validate_observation_shape(cyclic_observation)

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
    assert replay_entry.used_fallback is False


def test_environment_observer_rejects_invalid_input_without_fallback_behavior():
    observer = EnvironmentObserver(_InvalidReturnEnvironment())

    with pytest.raises(ValueError, match="ObservationRecord"):
        observer.observe("ep-invalid-return", 0)


def test_environment_observer_rejects_invalid_shape_without_fallback_behavior():
    observer = EnvironmentObserver(_InvalidShapeEnvironment())

    with pytest.raises(ValueError, match="raw_observation"):
        observer.observe("ep-invalid-shape", 0)


def test_environment_observer_rejects_mismatched_episode_id():
    observer = EnvironmentObserver(_MismatchedEpisodeEnvironment())

    with pytest.raises(ValueError, match="episode_id"):
        observer.observe("requested-episode", 0)


def test_environment_observer_rejects_mismatched_step_index():
    observer = EnvironmentObserver(_MismatchedStepEnvironment())

    with pytest.raises(ValueError, match="step_index"):
        observer.observe("ep-step", 0)


@pytest.mark.parametrize("source_label", ["", "   ", None, 7])
def test_environment_observer_rejects_invalid_source_label_without_fallback(source_label):
    observer = EnvironmentObserver(_InvalidSourceLabelEnvironment(source_label), source_label="fallback_env")

    with pytest.raises(ValueError, match="source_label"):
        observer.observe("ep-source", 0)


def test_observation_record_deterministic_metadata_behavior():
    payload = {"z": 0, "a": [1, 2, 3]}
    r1 = ObservationRecord.create("ep-det", 0, payload, source_label="env")
    r2 = ObservationRecord.create("ep-det", 0, payload, source_label="env")

    assert r1.summary_size == r2.summary_size
    assert r1.summary_keys == r2.summary_keys
    assert r1.observation_type == r2.observation_type


def test_environment_observer_recomputes_spoofed_structural_metadata_from_raw_observation_only():
    environment = _SpoofedMetadataEnvironment()
    observer = EnvironmentObserver(environment)
    record = observer.observe("ep-spoof", 3)
    expected = ObservationRecord.create(
        episode_id="ep-spoof",
        step_index=3,
        raw_observation=environment.raw_observation,
        source_label="spoofed_env",
    )

    assert record.observation_type == expected.observation_type
    assert record.summary_size == expected.summary_size
    assert record.summary_keys == expected.summary_keys
    assert record.observation_type != environment.spoofed_observation_type
    assert record.summary_size != environment.spoofed_summary_size
    assert record.summary_keys != environment.spoofed_summary_keys
