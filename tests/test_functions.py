# -*- coding: utf-8 -*-

from unittest.mock import patch
import pytest
from mytext import Mode, Tone, Provider
from mytext import run_mytext
from mytext.cli import main
from mytext.params import MY_TEXT_VERSION, MY_TEXT_OVERVIEW, MY_TEXT_REPO

TEST_CASE_NAME = "Functions tests"


@patch("requests.Session.post")
def test_run_mytext_github_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "OK!"
                }
            }
        ]
    }

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.GITHUB
    )

    assert result["status"]
    assert result["message"] == "OK!"


@patch("requests.Session.post")
def test_run_mytext_nvidia_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "OK!"
                }
            }
        ]
    }

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.NVIDIA
    )

    assert result["status"]
    assert result["message"] == "OK!"


@patch("requests.Session.post")
def test_run_mytext_groq_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "OK!"
                }
            }
        ]
    }

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.GROQ
    )

    assert result["status"]
    assert result["message"] == "OK!"


@patch("requests.Session.post")
def test_run_mytext_cerebras_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "OK!"
                }
            }
        ]
    }

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.CEREBRAS
    )

    assert result["status"]
    assert result["message"] == "OK!"


@patch("requests.Session.post")
def test_run_mytext_openrouter_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "OK!"
                }
            }
        ]
    }

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.OPENROUTER
    )

    assert result["status"]
    assert result["message"] == "OK!"


@patch("requests.Session.post")
def test_run_mytext_ai_studio_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": "OK!"
                        }
                    ]
                }
            }
        ]
    }

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.AI_STUDIO
    )

    assert result["status"]
    assert result["message"] == "OK!"


@patch("requests.Session.post")
def test_run_mytext_cloudflare_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": {
            "response": "OK2"
        }
    }

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY", "account_id": "ACC"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.CLOUDFLARE
    )

    assert result["status"]
    assert result["message"] == "OK2"


@patch("mytext.functions._call_provider")
def test_run_mytext_api_failure(mock_call):
    mock_call.return_value = {
        "status": False,
        "message": "error",
        "model": "unknown"
    }

    auth = {"api_key": "KEY"}
    result = run_mytext(text="hi", auth=auth, provider=Provider.AI_STUDIO)
    assert not result["status"]
    assert "error" in result["message"]


@patch("requests.Session.post")
def test_run_mytext_cloudflare_failure(mock_post):

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY", "account_id": "ACC"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.CLOUDFLARE
    )
    assert not result["status"]
    assert "Unauthorized" in result["message"]


@patch("requests.Session.post")
def test_run_mytext_ai_studio_failure(mock_post):

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.AI_STUDIO
    )
    assert not result["status"]
    assert "Unauthorized" in result["message"]


@patch("requests.Session.post")
def test_run_mytext_openrouter_failure(mock_post):

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.OPENROUTER
    )
    assert not result["status"]
    assert "Unauthorized" in result["message"]


@patch("requests.Session.post")
def test_run_mytext_cerebras_failure(mock_post):

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.CEREBRAS
    )
    assert not result["status"]
    assert "Unauthorized" in result["message"]


@patch("requests.Session.post")
def test_run_mytext_groq_failure(mock_post):

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_post.return_value = mock_response
    
    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.GROQ
    )
    assert not result["status"]
    assert "Unauthorized" in result["message"]


@patch("requests.Session.post")
def test_run_mytext_nvidia_failure(mock_post):

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_post.return_value = mock_response

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.NVIDIA
    )
    assert not result["status"]
    assert "Unauthorized" in result["message"]


@patch("requests.Session.post")
def test_run_mytext_github_failure(mock_post):

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    mock_post.return_value = mock_response
    
    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.GITHUB
    )
    assert not result["status"]
    assert "Unauthorized" in result["message"]


def test_main_version(capsys):
    with patch("sys.argv", ["mytext", "--version"]):
        main()
    out, _ = capsys.readouterr()
    assert MY_TEXT_VERSION in out


def test_main_info(capsys):
    with patch("sys.argv", ["mytext", "--info"]):
        main()
    out, _ = capsys.readouterr()
    assert MY_TEXT_OVERVIEW in out
    assert MY_TEXT_REPO in out


def test_main_no_text(capsys):
    with patch("sys.argv", ["mytext"]):
        with pytest.raises(SystemExit):
            main()
    _, err = capsys.readouterr()
    assert "--text is required" in err
