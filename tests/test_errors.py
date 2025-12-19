# -*- coding: utf-8 -*-

from mytext import run_mytext
from mytext import Mode, Tone, Provider

TEST_CASE_NAME = "Errors tests"


def test_run_mytext_invalid_text_type():
    result = run_mytext(text=123, auth={}, mode=Mode.PARAPHRASE, tone=Tone.NEUTRAL)
    assert not result["status"]
    assert result["message"] == "`text` must be a string."


def test_run_mytext_invalid_auth_type():
    result = run_mytext(text="a", auth="bad", mode=Mode.PARAPHRASE, tone=Tone.NEUTRAL)
    assert not result["status"]
    assert result["message"] == "`auth` must be a dictionary."


def test_run_mytext_invalid_mode_type():
    result = run_mytext(text="a", auth={}, mode="wrong", tone=Tone.NEUTRAL)
    assert not result["status"]
    assert result["message"] == "`mode` must be an instance of Mode enum."


def test_run_mytext_invalid_tone_type():
    result = run_mytext(text="a", auth={}, mode=Mode.PARAPHRASE, tone="wrong")
    assert not result["status"]
    assert result["message"] == "`tone` must be an instance of Tone enum."


def test_run_mytext_invalid_provider_type():
    result = run_mytext(text="a", auth={}, mode=Mode.PARAPHRASE, tone=Tone.NEUTRAL, provider="AI")
    assert not result["status"]
    assert result["message"] == "`provider` must be an instance of Provider enum."


def test_run_mytext_missing_api_key_for_ai_studio():
    auth = {}
    result = run_mytext(text="test", auth=auth, provider=Provider.AI_STUDIO)
    assert not result["status"]
    assert result["message"] == "AI_STUDIO provider requires keys: `api_key`"


def test_run_mytext_missing_keys_for_cloudflare():
    auth = {"api_key": "x"}
    result = run_mytext(text="test", auth=auth, provider=Provider.CLOUDFLARE)
    assert not result["status"]
    assert result["message"] == "CLOUDFLARE provider requires keys: `api_key`, `account_id`"


def test_run_mytext_missing_api_key_for_openrouter():
    auth = {}
    result = run_mytext(text="test", auth=auth, provider=Provider.OPENROUTER)
    assert not result["status"]
    assert result["message"] == "OPENROUTER provider requires keys: `api_key`"


def test_run_mytext_missing_api_key_for_cerebras():
    auth = {}
    result = run_mytext(text="test", auth=auth, provider=Provider.CEREBRAS)
    assert not result["status"]
    assert result["message"] == "CEREBRAS provider requires keys: `api_key`"


def test_run_mytext_missing_api_key_for_groq():
    auth = {}
    result = run_mytext(text="test", auth=auth, provider=Provider.GROQ)
    assert not result["status"]
    assert result["message"] == "GROQ provider requires keys: `api_key`"


def test_run_mytext_missing_api_key_for_nvidia():
    auth = {}
    result = run_mytext(text="test", auth=auth, provider=Provider.NVIDIA)
    assert not result["status"]
    assert result["message"] == "NVIDIA provider requires keys: `api_key`"
