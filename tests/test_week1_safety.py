import csv
import json
from dataclasses import FrozenInstanceError
from unittest.mock import Mock

import pytest

from arc_week1 import (
    ActionParser,
    AuditReadAuthority,
    EvaluationLogger,
    ObservationEnvelope,
    ReplayAudit,
    ReplayAuditOwner,
    ReplayEntry,
    ResetManager,
    Scorecard,
    EvidencePacket,
    _create_replay_audit,
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
    replay_a, owner_a = _create_replay_audit()
    replay_b, owner_b = _create_replay_audit()

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

    authority_a = owner_a.grant_read_authority()
    authority_b = owner_b.grant_read_authority()
    assert replay_a.digest(authority_a) == replay_b.digest(authority_b)


def _replay_entry(*, step_index=0):
    return ReplayEntry(
        episode_id="ep-read",
        seed=17,
        step_index=step_index,
        lifecycle="running",
        reset_event=step_index == 0,
        raw_action_text="STRUCTURAL_TOKEN_A",
        parsed_action="STRUCTURAL_TOKEN_A",
        used_fallback=False,
        observation_type="dict",
        observation_size=1,
        status_note="ok",
    )


def test_replay_audit_factory_creates_audit_and_separate_owner():
    replay, owner = _create_replay_audit()

    assert isinstance(replay, ReplayAudit)
    assert isinstance(owner, ReplayAuditOwner)
    with pytest.raises(TypeError, match="_create_replay_audit"):
        ReplayAudit()
    with pytest.raises(TypeError, match="no public constructor"):
        ReplayAuditOwner()


def test_replay_entries_require_valid_authority_and_return_immutable_snapshot():
    replay, owner = _create_replay_audit()
    replay.append(_replay_entry())
    authority = owner.grant_read_authority()

    snapshot = replay.entries(authority)
    replay.append(_replay_entry(step_index=1))

    assert snapshot == (_replay_entry(),)
    assert isinstance(snapshot, tuple)
    assert replay.entries(authority) == (_replay_entry(), _replay_entry(step_index=1))


def test_replay_authority_is_typed_audit_bound_and_immutable():
    replay, owner = _create_replay_audit()
    authority = owner.grant_read_authority()

    assert isinstance(authority, AuditReadAuthority)
    with pytest.raises(TypeError, match="no public constructor"):
        AuditReadAuthority()
    with pytest.raises(FrozenInstanceError):
        authority._token = object()
    assert replay.entries(authority) == ()


@pytest.mark.parametrize("invalid_authority", [None, True, False, "token", object()])
def test_replay_reads_reject_missing_boolean_string_and_untyped_authority(invalid_authority):
    replay, _ = _create_replay_audit()

    with pytest.raises(PermissionError, match="authority"):
        replay.entries(invalid_authority)
    with pytest.raises(PermissionError, match="authority"):
        replay.digest(invalid_authority)


def test_replay_reads_reject_lookalike_and_field_identical_forged_authority():
    replay, owner = _create_replay_audit()
    authority = owner.grant_read_authority()
    lookalike = Mock(spec=AuditReadAuthority)
    forged = object.__new__(AuditReadAuthority)
    object.__setattr__(forged, "_audit_instance_id", authority._audit_instance_id)
    object.__setattr__(forged, "_token", authority._token)

    for invalid_authority in (lookalike, forged):
        with pytest.raises(PermissionError, match="authority"):
            replay.entries(invalid_authority)
        with pytest.raises(PermissionError, match="authority"):
            replay.digest(invalid_authority)


def test_replay_reads_reject_cross_audit_authority():
    replay_a, owner_a = _create_replay_audit()
    replay_b, _ = _create_replay_audit()
    authority_a = owner_a.grant_read_authority()

    with pytest.raises(PermissionError, match="authority"):
        replay_b.entries(authority_a)
    with pytest.raises(PermissionError, match="authority"):
        replay_b.digest(authority_a)


def test_replay_reads_reject_revoked_authority():
    replay, owner = _create_replay_audit()
    authority = owner.grant_read_authority()
    assert replay.entries(authority) == ()

    owner.revoke_read_authority(authority)

    with pytest.raises(PermissionError, match="authority"):
        replay.entries(authority)
    with pytest.raises(PermissionError, match="authority"):
        replay.digest(authority)


def test_denied_replay_reads_disclose_nothing_compute_no_digest_and_do_not_mutate(monkeypatch):
    replay, owner = _create_replay_audit()
    replay.append(_replay_entry())
    valid_authority = owner.grant_read_authority()
    before = replay.entries(valid_authority)

    def fail_json_dumps(*args, **kwargs):
        raise AssertionError("digest serialization must not run without authority")

    monkeypatch.setattr("arc_week1.json.dumps", fail_json_dumps)
    with pytest.raises(PermissionError, match="authority"):
        replay.entries(None)
    with pytest.raises(PermissionError, match="authority"):
        replay.digest(None)

    assert replay.entries(valid_authority) == before


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
