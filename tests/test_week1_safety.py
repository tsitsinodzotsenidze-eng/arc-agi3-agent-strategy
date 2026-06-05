import csv
import json

from arc_week1 import (
    ActionParser,
    EvaluationLogger,
    ObservationEnvelope,
    ReplayAudit,
    ReplayEntry,
    ResetManager,
    Scorecard,
    EvidencePacket,
    _safe_size,
)


def test_reset_manager_is_deterministic_and_isolates_state():
    manager = ResetManager()
    manager.reset("ep-a", 123)
    seq_a = [manager.rng.randint(0, 1000) for _ in range(5)]

    manager.reset("ep-b", 123)
    seq_b = [manager.rng.randint(0, 1000) for _ in range(5)]
    assert seq_a == seq_b

    manager.reset("ep-c", 124)
    seq_c = [manager.rng.randint(0, 1000) for _ in range(5)]
    assert seq_c != seq_a


def test_observation_and_evidence_are_structural_only():
    payload = {"x": [1, 2], "y": "z"}
    obs = ObservationEnvelope.from_payload("ep-1", 0, payload)
    evidence = EvidencePacket.from_observation(obs)

    assert obs.payload is payload
    assert obs.payload_type == "dict"
    assert obs.payload_size == 2
    assert evidence.observation_type == "dict"
    assert evidence.observation_size == 2
    assert evidence.payload is payload


def test_safe_size_uses_only_json_like_structural_container_lengths():
    assert _safe_size("abc") == 3
    assert _safe_size([1, 2, 3]) == 3
    assert _safe_size((1, 2)) == 2
    assert _safe_size({"a": 1, "b": 2}) == 2

    assert _safe_size(b"abc") == 1
    assert _safe_size({1, 2, 3}) == 1

    assert _safe_size(7) == 1
    assert _safe_size(None) == 1
    assert _safe_size(3.14) == 1


def test_action_parser_uses_fixed_fallback_for_invalid_inputs():
    parser = ActionParser()

    parsed_ok = parser.parse("STRUCTURAL_TOKEN_A")
    assert parsed_ok.action == "STRUCTURAL_TOKEN_A"
    assert not parsed_ok.used_fallback

    parsed_dict = parser.parse({"action": "STRUCTURAL_TOKEN_B"})
    assert parsed_dict.action == "STRUCTURAL_TOKEN_B"
    assert not parsed_dict.used_fallback

    parsed_bad = parser.parse("   ")
    assert parsed_bad.action == "__SAFETY_FALLBACK__"
    assert parsed_bad.used_fallback

    parsed_missing = parser.parse({"not_action": "STRUCTURAL_TOKEN_C"})
    assert parsed_missing.action == "__SAFETY_FALLBACK__"
    assert parsed_missing.used_fallback

    parsed_none = parser.parse(None)
    assert parsed_none.action == "__SAFETY_FALLBACK__"
    assert parsed_none.used_fallback


def test_replay_digest_is_deterministic_for_same_entries():
    replay_a = ReplayAudit()
    replay_b = ReplayAudit()

    for replay in (replay_a, replay_b):
        replay.reset("ep-1", 7)
        replay.append(
            ReplayEntry(
                episode_id="ep-1",
                seed=7,
                step_index=0,
                lifecycle="running",
                reset_event=True,
                raw_action_text="STRUCTURAL_TOKEN_A",
                parsed_action="STRUCTURAL_TOKEN_A",
                used_fallback=False,
                observation_type="dict",
                observation_size=1,
                status_note="ok",
            )
        )

    assert replay_a.digest() == replay_b.digest()


def test_evaluation_logger_writes_jsonl_and_csv_schema(tmp_path):
    logger = EvaluationLogger(tmp_path)
    entry = ReplayEntry(
        episode_id="ep-2",
        seed=11,
        step_index=1,
        lifecycle="running",
        reset_event=False,
        raw_action_text="",
        parsed_action="__SAFETY_FALLBACK__",
        used_fallback=True,
        observation_type="list",
        observation_size=3,
        status_note="fallback",
    )

    logger.log(entry)

    jsonl_lines = (tmp_path / "evaluation_log.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(jsonl_lines) == 1
    payload = json.loads(jsonl_lines[0])
    required = {
        "episode_id",
        "seed",
        "step_index",
        "raw_action_text",
        "parsed_action",
        "used_fallback",
        "observation_type",
        "observation_size",
        "lifecycle",
        "reset_event",
        "status_note",
    }
    assert required.issubset(payload)

    with (tmp_path / "evaluation_summary.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 1
    assert set(rows[0]) == set(EvaluationLogger.CSV_FIELDS)


def test_scorecard_lifecycle_scaffold_is_per_episode_only():
    score = Scorecard(episode_id="ep-3", seed=3)
    assert score.lifecycle == "initialized"

    score.transition("running", "started")
    score.step_count += 1
    score.transition("finished", "done")

    assert score.lifecycle == "finished"
    assert score.step_count == 1
    assert score.status_note == "done"
