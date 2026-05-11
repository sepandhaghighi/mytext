# -*- coding: utf-8 -*-

import os
import pytest
from mytext import run_mytext
from mytext import Mode
from mytext import Tone
from mytext import Provider


pytestmark = pytest.mark.integration


def test_nvidia_real_api():
    api_key = os.getenv("NVIDIA_API_KEY")
    
    assert api_key, "NVIDIA real API keys are not available."

    result = run_mytext(
        text="Hello world",
        auth={"api_key": api_key},
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.NVIDIA,
    )

    assert result["status"] is True
    assert isinstance(result["message"], str)
    assert result["message"].strip()
    assert result["model"]
