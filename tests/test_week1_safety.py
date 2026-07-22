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
    RouteKind,
    Scorecard,
    EvidencePacket,
    ParsedAction,
    _ROUTE_FACTORY_KEY,
    _create_replay_audit,
    _replay_entry_record,
    _reserved_token_collision,
    _safe_size,
    _validate_route_state,
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
    assert parsed_ok.route is RouteKind.ACTION
    assert not parsed_ok.used_fallback

    parsed_dict = parser.parse({"action": "STRUCTURAL_TOKEN_B"})
    assert parsed_dict.action == "STRUCTURAL_TOKEN_B"
    assert parsed_dict.route is RouteKind.ACTION
    assert not parsed_dict.used_fallback

    parsed_bad = parser.parse("   ")
    assert parsed_bad.action == "__SAFETY_FALLBACK__"
    assert parsed_bad.route is RouteKind.FALLBACK
    assert parsed_bad.used_fallback

    parsed_missing = parser.parse({"not_action": "STRUCTURAL_TOKEN_C"})
    assert parsed_missing.action == "__SAFETY_FALLBACK__"
    assert parsed_missing.route is RouteKind.FALLBACK
    assert parsed_missing.used_fallback

    parsed_none = parser.parse(None)
    assert parsed_none.action == "__SAFETY_FALLBACK__"
    assert parsed_none.route is RouteKind.FALLBACK
    assert parsed_none.used_fallback


@pytest.mark.parametrize("reserved", ["__SAFETY_FALLBACK__", "__OBSERVATION_ONLY__"])
@pytest.mark.parametrize("as_mapping", [False, True])
def test_action_parser_rejects_exact_reserved_tokens_then_uses_trusted_fallback(reserved, as_mapping):
    parser = ActionParser()
    candidate = {"action": f"  {reserved}  "} if as_mapping else f"  {reserved}  "

    parsed = parser.parse(candidate)

    assert parsed.route is RouteKind.FALLBACK
    assert parsed.action == "__SAFETY_FALLBACK__"
    assert parsed.used_fallback is True
    assert parsed.note == "fallback_due_to_reserved_exact_collision"


@pytest.mark.parametrize(
    "near_miss",
    [
        "__safety_fallback__",
        "__observation_only__",
        "__SAFETY_FALLBACK_",
        "X__SAFETY_FALLBACK__",
        "__OBSERVATION_ONLX__",
    ],
)
@pytest.mark.parametrize("as_mapping", [False, True])
def test_action_parser_rejects_finite_reserved_near_misses_then_uses_trusted_fallback(near_miss, as_mapping):
    parser = ActionParser()
    candidate = {"action": near_miss} if as_mapping else near_miss

    parsed = parser.parse(candidate)

    assert parsed.route is RouteKind.FALLBACK
    assert parsed.action == "__SAFETY_FALLBACK__"
    assert parsed.used_fallback is True
    assert parsed.note == "fallback_due_to_reserved_near_miss"


def test_finite_near_miss_classifier_covers_every_single_edit_position():
    for reserved in ("__SAFETY_FALLBACK__", "__OBSERVATION_ONLY__"):
        variants = {
            *(reserved[:index] + reserved[index + 1 :] for index in range(len(reserved))),
            *(reserved[:index] + "X" + reserved[index + 1 :] for index in range(len(reserved))),
            *(reserved[:index] + "X" + reserved[index:] for index in range(len(reserved) + 1)),
        }
        for variant in variants:
            assert _reserved_token_collision(variant) == "near_miss"


def test_reserved_text_outside_action_field_remains_ordinary_data():
    parser = ActionParser()
    candidate = {
        "action": "STRUCTURAL_TOKEN_A",
        "metadata": {
            "exact": "__OBSERVATION_ONLY__",
            "near": "__SAFETY_FALLBACK_",
        },
    }

    parsed = parser.parse(candidate)

    assert parsed.route is RouteKind.ACTION
    assert parsed.action == "STRUCTURAL_TOKEN_A"
    assert json.loads(parsed.raw_action_text) == candidate
    assert candidate["metadata"]["exact"] == "__OBSERVATION_ONLY__"
    assert candidate["metadata"]["near"] == "__SAFETY_FALLBACK_"


def test_route_carriers_require_factories_and_reject_contradictory_states():
    assert RouteKind.ACTION.value == "ACTION"
    assert RouteKind.FALLBACK.value == "FALLBACK"
    assert RouteKind.OBSERVATION_ONLY.value == "OBSERVATION_ONLY"
    assert RouteKind.ACTION != "ACTION"

    with pytest.raises(PermissionError, match="factory-only"):
        ParsedAction(
            raw_action_text=None,
            action="__SAFETY_FALLBACK__",
            route=RouteKind.FALLBACK,
            used_fallback=False,
            note="contradiction",
        )

    with pytest.raises(PermissionError, match="factory-only"):
        ReplayEntry(
            episode_id="ep-invalid",
            seed=1,
            step_index=0,
            lifecycle="running",
            reset_event=False,
            raw_action_text=None,
            parsed_action="__OBSERVATION_ONLY__",
            route=RouteKind.OBSERVATION_ONLY,
            used_fallback=False,
            observation_type="dict",
            observation_size=1,
            status_note="direct-construction",
        )

    with pytest.raises(PermissionError, match="factory-only"):
        ParsedAction(
            raw_action_text="MOVE",
            action="MOVE",
            route=RouteKind.ACTION,
            used_fallback=False,
            note="wrong-key",
            _factory_key=object(),
        )

    with pytest.raises(ValueError, match="used_fallback=True"):
        ParsedAction(
            raw_action_text=None,
            action="__SAFETY_FALLBACK__",
            route=RouteKind.FALLBACK,
            used_fallback=False,
            note="contradiction",
            _factory_key=_ROUTE_FACTORY_KEY,
        )

    with pytest.raises(ValueError, match="OBSERVATION_ONLY"):
        ReplayEntry(
            episode_id="ep-invalid",
            seed=1,
            step_index=0,
            lifecycle="running",
            reset_event=False,
            raw_action_text=None,
            parsed_action="__OBSERVATION_ONLY__",
            route=RouteKind.OBSERVATION_ONLY,
            used_fallback=True,
            observation_type="dict",
            observation_size=1,
            status_note="contradiction",
            _factory_key=_ROUTE_FACTORY_KEY,
        )

    with pytest.raises(TypeError, match="RouteKind"):
        ReplayEntry(
            episode_id="ep-invalid",
            seed=1,
            step_index=0,
            lifecycle="running",
            reset_event=False,
            raw_action_text="MOVE",
            parsed_action="MOVE",
            route="ACTION",
            used_fallback=False,
            observation_type="dict",
            observation_size=1,
            status_note="raw-string-route",
            _factory_key=_ROUTE_FACTORY_KEY,
        )

    with pytest.raises(ValueError, match="raw_action_text=None"):
        ReplayEntry(
            episode_id="ep-invalid",
            seed=1,
            step_index=0,
            lifecycle="running",
            reset_event=False,
            raw_action_text="untrusted-text",
            parsed_action="__OBSERVATION_ONLY__",
            route=RouteKind.OBSERVATION_ONLY,
            used_fallback=False,
            observation_type="dict",
            observation_size=1,
            status_note="contradiction",
            _factory_key=_ROUTE_FACTORY_KEY,
        )

    with pytest.raises(ValueError, match="cannot carry"):
        ParsedAction(
            raw_action_text=None,
            action="__OBSERVATION_ONLY__",
            route=RouteKind.OBSERVATION_ONLY,
            used_fallback=False,
            note="contradiction",
            _factory_key=_ROUTE_FACTORY_KEY,
        )


@pytest.mark.parametrize(
    ("route", "action", "used_fallback", "exception"),
    [
        (RouteKind.ACTION, "MOVE", True, ValueError),
        (RouteKind.ACTION, "__SAFETY_FALLBACK__", False, ValueError),
        (RouteKind.ACTION, "__OBSERVATION_ONLX__", False, ValueError),
        (RouteKind.FALLBACK, "__SAFETY_FALLBACK__", False, ValueError),
        (RouteKind.FALLBACK, "MOVE", True, ValueError),
        (RouteKind.OBSERVATION_ONLY, "__OBSERVATION_ONLY__", True, ValueError),
        (RouteKind.OBSERVATION_ONLY, "MOVE", False, ValueError),
        ("ACTION", "MOVE", False, TypeError),
        (RouteKind.ACTION, "MOVE", 0, TypeError),
    ],
)
def test_route_state_contradiction_matrix(route, action, used_fallback, exception):
    with pytest.raises(exception):
        _validate_route_state(route=route, action=action, used_fallback=used_fallback)


def test_two_edit_reserved_like_token_remains_outside_finite_near_miss_set():
    parsed = ActionParser().parse("__SAFETY_FALLBAXX__")

    assert parsed.route is RouteKind.ACTION
    assert parsed.action == "__SAFETY_FALLBAXX__"


def test_reserved_text_without_action_key_is_missing_action_not_collision():
    parsed = ActionParser().parse({"metadata": "__OBSERVATION_ONLY__"})

    assert parsed.route is RouteKind.FALLBACK
    assert parsed.note == "fallback_due_to_missing_structural_action_token"


def test_replay_digest_is_deterministic_for_same_entries():
    replay_a, owner_a = _create_replay_audit()
    replay_b, owner_b = _create_replay_audit()

    for replay in (replay_a, replay_b):
        replay.reset("ep-1", 7)
        replay.append(
            ReplayEntry.from_ordinary_action(
                episode_id="ep-1",
                seed=7,
                step_index=0,
                lifecycle="running",
                reset_event=True,
                raw_action_text="STRUCTURAL_TOKEN_A",
                parsed_action="STRUCTURAL_TOKEN_A",
                observation_type="dict",
                observation_size=1,
                status_note="ok",
            )
        )

    authority_a = owner_a.grant_read_authority()
    authority_b = owner_b.grant_read_authority()
    assert replay_a.digest(authority_a) == replay_b.digest(authority_b)


def test_replay_digest_uses_canonical_primitive_route_value():
    replay, owner = _create_replay_audit()
    entry = ReplayEntry.from_ordinary_action(
        episode_id="ep-digest",
        seed=7,
        step_index=0,
        lifecycle="running",
        reset_event=True,
        raw_action_text="MOVE",
        parsed_action="MOVE",
        observation_type="dict",
        observation_size=1,
        status_note="ok",
    )
    replay.append(entry)
    authority = owner.grant_read_authority()

    record = _replay_entry_record(entry)

    assert type(record["route"]) is str
    assert record["route"] == "ACTION"
    assert "_factory_key" not in record
    assert replay.digest(authority) == "71799432bf012673ee8bd363a3fd27468b780b0fe6dd5464f38473ee85e1a048"


def test_named_factories_emit_frozen_consistent_route_states():
    parsed_action = ParsedAction.from_ordinary_action(
        raw_action_text="MOVE",
        action="MOVE",
    )
    parsed_fallback = ParsedAction._from_internal_fallback(
        raw_action_text=None,
        note="fallback_due_to_missing_structural_action_token",
    )
    replay_action = ReplayEntry.from_ordinary_action(
        episode_id="ep-factory",
        seed=1,
        step_index=0,
        lifecycle="running",
        reset_event=True,
        raw_action_text="MOVE",
        parsed_action="MOVE",
        observation_type="dict",
        observation_size=1,
    )
    replay_fallback = ReplayEntry._from_internal_fallback(
        episode_id="ep-factory",
        seed=1,
        step_index=1,
        lifecycle="running",
        reset_event=False,
        raw_action_text=None,
        observation_type="dict",
        observation_size=1,
    )
    replay_observation = ReplayEntry.from_observation_only(
        episode_id="ep-factory",
        seed=1,
        step_index=2,
        lifecycle="running",
        reset_event=False,
        observation_type="dict",
        observation_size=1,
    )

    assert (parsed_action.route, parsed_action.used_fallback) == (RouteKind.ACTION, False)
    assert (parsed_fallback.route, parsed_fallback.used_fallback) == (RouteKind.FALLBACK, True)
    assert (replay_action.route, replay_action.used_fallback) == (RouteKind.ACTION, False)
    assert (replay_fallback.route, replay_fallback.used_fallback) == (RouteKind.FALLBACK, True)
    assert (replay_observation.route, replay_observation.used_fallback) == (
        RouteKind.OBSERVATION_ONLY,
        False,
    )
    assert replay_observation.raw_action_text is None
    with pytest.raises(FrozenInstanceError):
        replay_observation.route = RouteKind.ACTION


@pytest.mark.parametrize("invalid_action", ["__SAFETY_FALLBACK__", "__OBSERVATION_ONLX__"])
def test_ordinary_action_factories_reject_reserved_and_near_miss_tokens(invalid_action):
    with pytest.raises(ValueError, match="reserved token or finite near miss"):
        ParsedAction.from_ordinary_action(
            raw_action_text=invalid_action,
            action=invalid_action,
        )

    with pytest.raises(ValueError, match="reserved token or finite near miss"):
        ReplayEntry.from_ordinary_action(
            episode_id="ep-invalid-action",
            seed=1,
            step_index=0,
            lifecycle="running",
            reset_event=True,
            raw_action_text=invalid_action,
            parsed_action=invalid_action,
            observation_type="dict",
            observation_size=1,
        )


def _replay_entry(*, step_index=0):
    return ReplayEntry.from_ordinary_action(
        episode_id="ep-read",
        seed=17,
        step_index=step_index,
        lifecycle="running",
        reset_event=step_index == 0,
        raw_action_text="STRUCTURAL_TOKEN_A",
        parsed_action="STRUCTURAL_TOKEN_A",
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

    def fail_replay_entry_record(*args, **kwargs):
        raise AssertionError("route serialization must not run without authority")

    monkeypatch.setattr("arc_week1.json.dumps", fail_json_dumps)
    monkeypatch.setattr("arc_week1._replay_entry_record", fail_replay_entry_record)
    with pytest.raises(PermissionError, match="authority"):
        replay.entries(None)
    with pytest.raises(PermissionError, match="authority"):
        replay.digest(None)

    assert replay.entries(valid_authority) == before


def test_evaluation_logger_writes_jsonl_and_csv_schema(tmp_path):
    logger = EvaluationLogger(tmp_path)
    entries = [
        ReplayEntry.from_ordinary_action(
            episode_id="ep-2",
            seed=11,
            step_index=0,
            lifecycle="running",
            reset_event=True,
            raw_action_text="STRUCTURAL_TOKEN_A",
            parsed_action="STRUCTURAL_TOKEN_A",
            observation_type="list",
            observation_size=3,
            status_note="action",
        ),
        ReplayEntry._from_internal_fallback(
            episode_id="ep-2",
            seed=11,
            step_index=1,
            lifecycle="running",
            reset_event=False,
            raw_action_text="",
            observation_type="list",
            observation_size=3,
            status_note="fallback",
        ),
        ReplayEntry.from_observation_only(
            episode_id="ep-2",
            seed=11,
            step_index=2,
            lifecycle="running",
            reset_event=False,
            observation_type="dict",
            observation_size=1,
            status_note="observation_only",
        ),
    ]

    for entry in entries:
        logger.log(entry)

    jsonl_lines = (tmp_path / "evaluation_log.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(jsonl_lines) == 3
    payloads = [json.loads(line) for line in jsonl_lines]
    required = {
        "episode_id",
        "seed",
        "step_index",
        "raw_action_text",
        "parsed_action",
        "route",
        "used_fallback",
        "observation_type",
        "observation_size",
        "lifecycle",
        "reset_event",
        "status_note",
    }
    assert all(set(payload) == required for payload in payloads)
    assert [payload["route"] for payload in payloads] == ["ACTION", "FALLBACK", "OBSERVATION_ONLY"]

    with (tmp_path / "evaluation_summary.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 3
    assert all(set(row) == set(EvaluationLogger.CSV_FIELDS) for row in rows)
    assert [row["route"] for row in rows] == ["ACTION", "FALLBACK", "OBSERVATION_ONLY"]


@pytest.mark.parametrize(
    ("artifact_name", "legacy_content", "other_artifact"),
    [
        (
            "evaluation_log.jsonl",
            '{"episode_id":"legacy-without-route"}\n',
            "evaluation_summary.csv",
        ),
        (
            "evaluation_log.jsonl",
            "not-json\n",
            "evaluation_summary.csv",
        ),
        (
            "evaluation_summary.csv",
            "episode_id,seed,step_index,parsed_action,used_fallback,lifecycle,reset_event,status_note\n",
            "evaluation_log.jsonl",
        ),
        (
            "evaluation_summary.csv",
            "episode_id,seed,step_index,parsed_action,route,used_fallback,lifecycle,reset_event,status_note\n"
            "legacy,1,0,MOVE,,False,running,True,ok\n",
            "evaluation_log.jsonl",
        ),
    ],
)
def test_evaluation_logger_rejects_legacy_artifacts_before_any_write(
    tmp_path,
    artifact_name,
    legacy_content,
    other_artifact,
):
    legacy_path = tmp_path / artifact_name
    legacy_path.write_text(legacy_content, encoding="utf-8")
    logger = EvaluationLogger(tmp_path)
    entry = ReplayEntry.from_ordinary_action(
        episode_id="ep-new",
        seed=2,
        step_index=0,
        lifecycle="running",
        reset_event=True,
        raw_action_text="MOVE",
        parsed_action="MOVE",
        observation_type="dict",
        observation_size=1,
    )

    with pytest.raises(ValueError, match="fresh output directory"):
        logger.log(entry)

    assert legacy_path.read_text(encoding="utf-8") == legacy_content
    assert not (tmp_path / other_artifact).exists()


def test_evaluation_logger_appends_to_existing_canonical_artifacts(tmp_path):
    action_entry = ReplayEntry.from_ordinary_action(
        episode_id="ep-canonical",
        seed=3,
        step_index=0,
        lifecycle="running",
        reset_event=True,
        raw_action_text="MOVE",
        parsed_action="MOVE",
        observation_type="dict",
        observation_size=1,
    )
    observation_entry = ReplayEntry.from_observation_only(
        episode_id="ep-canonical",
        seed=3,
        step_index=1,
        lifecycle="running",
        reset_event=False,
        observation_type="dict",
        observation_size=1,
    )

    EvaluationLogger(tmp_path).log(action_entry)
    EvaluationLogger(tmp_path).log(observation_entry)

    jsonl_rows = [
        json.loads(line)
        for line in (tmp_path / "evaluation_log.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    with (tmp_path / "evaluation_summary.csv").open(encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))

    assert [row["route"] for row in jsonl_rows] == ["ACTION", "OBSERVATION_ONLY"]
    assert [row["route"] for row in csv_rows] == ["ACTION", "OBSERVATION_ONLY"]


def test_scorecard_lifecycle_scaffold_is_per_episode_only():
    score = Scorecard(episode_id="ep-3", seed=3)
    assert score.lifecycle == "initialized"

    score.transition("running", "started")
    score.step_count += 1
    score.transition("finished", "done")

    assert score.lifecycle == "finished"
    assert score.step_count == 1
    assert score.status_note == "done"
