# -*- coding: utf-8 -*-

import os
import pytest
from mytext import run_mytext
from mytext import Mode
from mytext import Tone
from mytext import Provider


pytestmark = pytest.mark.integration


def test_cloudflare_real_api():
    api_key = os.getenv("CLOUDFLARE_API_KEY")
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    
    assert api_key, "Cloudflare real API keys are not available."
    assert account_id, "Cloudflare real API keys are not available."

    result = run_mytext(
        text="Hello world",
        auth={"api_key": api_key, "account_id": account_id},
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.CLOUDFLARE,
    )

    assert result["status"] is True
    assert isinstance(result["message"], str)
    assert result["message"].strip()
    assert result["model"]
