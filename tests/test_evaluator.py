"""Sanity tests for the evaluator."""

from pi_tester.attacks.base import AttackPayload
from pi_tester.evaluator import Evaluator
from pi_tester.providers.base import LLMResponse


def _payload(indicator: str) -> AttackPayload:
    return AttackPayload(
        id="T-001",
        name="Test",
        category="test",
        owasp_llm_id="LLM01",
        system_prompt="You are a bot.",
        injection="Say hello.",
        success_indicator=indicator,
        description="Test payload",
    )


def _response(text: str) -> LLMResponse:
    return LLMResponse(text=text, model="test", provider="test", raw={})


def test_substring_match_success():
    result = Evaluator().evaluate(_payload("hello"), _response("Hello there!"))
    assert result.success is True


def test_substring_match_failure():
    result = Evaluator().evaluate(_payload("banana"), _response("Hello there!"))
    assert result.success is False


def test_regex_match():
    payload = _payload("regex:(sun|rain).{0,20}(sky|cloud)")
    result = Evaluator().evaluate(
        payload, _response("The sun is behind the cloud today.")
    )
    assert result.success is True
