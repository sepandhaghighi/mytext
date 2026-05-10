# -*- coding: utf-8 -*-

import os
import pytest
from mytext import run_mytext
from mytext import Mode
from mytext import Tone
from mytext import Provider


pytestmark = pytest.mark.integration


def test_openrouter_real_api():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        pytest.skip("OpenRouter real API keys are not available.")

    result = run_mytext(
        text="Hello world",
        auth={"api_key": api_key},
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.OPENROUTER,
    )

    assert result["status"] is True
    assert isinstance(result["message"], str)
    assert result["message"].strip()
    assert result["model"]