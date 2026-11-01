"""LLM client tests — all responses are mocked; no network access."""

import json
from unittest import mock

import pytest

from simscenario import llm
from simscenario.config import EndpointConfig
from simscenario.drafter import SOURCE_FALLBACK, SOURCE_LLM, draft_packet
from simscenario.llm import LLMError, build_user_prompt, chat_completion, parse_json_payload


def _fake_payload():
    return {
        "skill_id": "hand-hygiene",
        "room_id": "med-surg-double",
        "skill_title": "Hand Hygiene & Glove Use",
        "room_title": "Med-Surg Double Room",
        "objectives": ["o1", "o2", "o3", "o4", "o5"],
        "room_setup": "Fake room setup.",
        "ambient_noise": "Fake paging.",
        "patient_statements": [
            "stmt one", "stmt two", "stmt three",
            "stmt four", "stmt five", "stmt six",
        ],
        "distractions": ["d1", "d2", "d3"],
        "props": ["p1", "p2", "p3", "p4"],
        "expected_actions": ["a1", "a2", "a3", "a4"],
        "debrief_questions": ["q1", "q2", "q3", "q4", "q5"],
    }


def _mock_urlopen_json(payload_body, code_status=200):
    resp = mock.MagicMock()
    resp.read.return_value = json.dumps(payload_body).encode("utf-8")
    resp.__enter__ = mock.MagicMock(return_value=resp)
    resp.__exit__ = mock.MagicMock(return_value=False)
    return mock.MagicMock(return_value=resp)


def test_chat_completion_sends_openai_shape_and_returns_content():
    body = {"choices": [{"message": {"content": "hello"}}]}
    with mock.patch("urllib.request.urlopen", _mock_urlopen_json(body)) as fake:
        out = chat_completion("http://localhost:11434/v1", "llama3.1:8b", "hi")
    assert out == "hello"
    req = fake.call_args.args[0]
    sent = json.loads(req.data.decode())
    assert sent["model"] == "llama3.1:8b"
    assert sent["stream"] is False
    assert sent["messages"][0]["role"] == "system"
    assert req.get_header("Content-type") == "application/json"


def test_chat_completion_includes_env_sourced_key():
    body = {"choices": [{"message": {"content": "x"}}]}
    with mock.patch("urllib.request.urlopen", _mock_urlopen_json(body)) as fake:
        chat_completion("http://x/v1", "m", "hi", api_key="sk-test")
    req = fake.call_args.args[0]
    assert req.get_header("Authorization") == "Bearer sk-test"


def test_chat_completion_http_error_maps_to_llm_error():
    import urllib.error
    with mock.patch("urllib.request.urlopen",
                    side_effect=urllib.error.HTTPError("u", 503, "boom", None, None)):
        with pytest.raises(LLMError, match="HTTP 503"):
            chat_completion("http://x/v1", "m", "hi")


def test_chat_connection_failure_maps_to_llm_error():
    with mock.patch("urllib.request.urlopen",
                    side_effect=ConnectionRefusedError()):
        with pytest.raises(LLMError, match="could not reach endpoint"):
            chat_completion("http://localhost:59999/v1", "m", "hi")


def test_parse_json_payload_plain():
    assert parse_json_payload('{"a": 1}') == {"a": 1}


def test_parse_json_payload_fenced():
    text = "Here is your scenario:\n```json\n" + json.dumps(_fake_payload()) + "\n```"
    assert parse_json_payload(text) == _fake_payload()


def test_parse_json_payload_with_prose():
    text = "Sure! " + json.dumps({"k": [1, 2]}) + " Have a nice day."
    assert parse_json_payload(text) == {"k": [1, 2]}


def test_parse_json_payload_invalid_raises_llm_error():
    with pytest.raises(LLMError):
        parse_json_payload("{not json")


def test_build_user_prompt_includes_skill_and_room():
    from simscenario.data import ROOMS, SKILLS
    prompt = build_user_prompt("hand-hygiene", "med-surg-double",
                               SKILLS["hand-hygiene"], ROOMS["med-surg-double"])
    assert "hand-hygiene" in prompt and "med-surg-double" in prompt
    assert "No real patient data" in prompt


def test_draft_packet_uses_llm_with_mocked_response():
    cfg = EndpointConfig(base_url="http://mock/v1", model="mock-model")
    with mock.patch.object(llm, "draft_via_llm", return_value=_fake_payload()):
        notes = []
        packet = draft_packet(cfg, "hand-hygiene", "med-surg-double",
                              attempt_report=notes)
    assert packet["source"] == SOURCE_LLM
    assert packet["patient_statements"]["Opening"], "phases must be non-empty"
    assert notes[0][0] == SOURCE_LLM and notes[0][1] is None


def test_draft_packet_falls_back_when_llm_errors():
    cfg = EndpointConfig(base_url="http://mock/v1", model="mock-model")
    with mock.patch.object(llm, "draft_via_llm", side_effect=LLMError("down")):
        notes = []
        packet = draft_packet(cfg, "hand-hygiene", "med-surg-double",
                              attempt_report=notes)
    assert packet["source"] == SOURCE_FALLBACK
    assert "down" in notes[0][1]


def test_draft_packet_offline_flag_forces_fallback():
    cfg = EndpointConfig(base_url="http://mock/v1", model="mock-model")
    with mock.patch.object(llm, "draft_via_llm") as never:
        packet = draft_packet(cfg, "hand-hygiene", "med-surg-double",
                              force_fallback=True)
    never.assert_not_called()
    assert packet["source"] == SOURCE_FALLBACK


def test_draft_packet_without_config_stays_offline():
    packet = draft_packet(EndpointConfig(), "iv-insertion", "pre-op-holding")
    assert packet["source"] == SOURCE_FALLBACK
    assert packet["skill_id"] == "iv-insertion"
