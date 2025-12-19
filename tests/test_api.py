# -*- coding: utf-8 -*-
import os
import pytest
from mytext import run_mytext
from mytext import Mode, Tone, Provider

TEST_CASE_NAME = "API tests"


def skip_if_no_env_ai_studio():
    if not os.getenv("AI_STUDIO_API_KEY"):
        pytest.skip("AI Studio real API keys are not available.")


def skip_if_no_env_cloudflare():
    if not os.getenv("CLOUDFLARE_API_KEY") or not os.getenv("CLOUDFLARE_ACCOUNT_ID"):
        pytest.skip("Cloudflare real API keys are not available.")


def skip_if_no_env_openrouter():
    if not os.getenv("OPENROUTER_API_KEY"):
        pytest.skip("OpenRouter real API keys are not available.")


def skip_if_no_env_cerebras():
    if not os.getenv("CEREBRAS_API_KEY"):
        pytest.skip("Cerebras real API keys are not available.")


def skip_if_no_env_groq():
    if not os.getenv("GROQ_API_KEY"):
        pytest.skip("Groq real API keys are not available.")


def skip_if_no_env_nvidia():
    if not os.getenv("NVIDIA_API_KEY"):
        pytest.skip("NVIDIA real API keys are not available.")


def test_ai_studio_real_api():
    skip_if_no_env_ai_studio()
    api_key = os.getenv("AI_STUDIO_API_KEY")

    result = run_mytext(
        text="Hello, how are you?",
        auth={"api_key": api_key},
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.AI_STUDIO,
    )

    assert result["status"]
    assert result["message"]
    assert result["model"]


def test_cloudflare_real_api():
    skip_if_no_env_cloudflare()
    api_key = os.getenv("CLOUDFLARE_API_KEY")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")

    result = run_mytext(
        text="Hello world!",
        auth={"api_key": api_key, "account_id": account_id},
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.CLOUDFLARE,
    )

    assert result["status"]
    assert result["message"]
    assert result["model"]


def test_openrouter_real_api():
    skip_if_no_env_openrouter()
    api_key = os.getenv("OPENROUTER_API_KEY")

    result = run_mytext(
        text="Hello, how are you?",
        auth={"api_key": api_key},
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.OPENROUTER,
    )

    assert result["status"]
    assert result["message"]
    assert result["model"]


def test_cerebras_real_api():
    skip_if_no_env_cerebras()
    api_key = os.getenv("CEREBRAS_API_KEY")

    result = run_mytext(
        text="Hello, how are you?",
        auth={"api_key": api_key},
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.CEREBRAS,
    )

    assert result["status"]
    assert result["message"]
    assert result["model"]


def test_groq_real_api():
    skip_if_no_env_groq()
    api_key = os.getenv("GROQ_API_KEY")

    result = run_mytext(
        text="Hello, how are you?",
        auth={"api_key": api_key},
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.GROQ,
    )

    assert result["status"]
    assert result["message"]
    assert result["model"]


def test_nvidia_real_api():
    skip_if_no_env_nvidia()
    api_key = os.getenv("NVIDIA_API_KEY")

    result = run_mytext(
        text="Hello, how are you?",
        auth={"api_key": api_key},
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.NVIDIA,
    )

    assert result["status"]
    assert result["message"]
    assert result["model"]
