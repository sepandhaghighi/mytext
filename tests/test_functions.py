# -*- coding: utf-8 -*-

from unittest.mock import patch
import pytest
from mytext import Mode, Tone, Provider
from mytext import run_mytext
from mytext.functions import main
from mytext.params import MY_TEXT_VERSION, MY_TEXT_OVERVIEW, MY_TEXT_REPO

TEST_CASE_NAME = "Functions tests"


@patch("mytext.functions._call_provider")
def test_run_mytext_nvidia_success(mock_call):
    mock_call.return_value = {
        "status": True,
        "message": "OK!",
        "model": "model"
    }

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


@patch("mytext.functions._call_provider")
def test_run_mytext_groq_success(mock_call):
    mock_call.return_value = {
        "status": True,
        "message": "OK!",
        "model": "model"
    }

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


@patch("mytext.functions._call_provider")
def test_run_mytext_cerebras_success(mock_call):
    mock_call.return_value = {
        "status": True,
        "message": "OK!",
        "model": "model"
    }

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


@patch("mytext.functions._call_provider")
def test_run_mytext_openrouter_success(mock_call):
    mock_call.return_value = {
        "status": True,
        "message": "OK!",
        "model": "gemini"
    }

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


@patch("mytext.functions._call_provider")
def test_run_mytext_ai_studio_success(mock_call):
    mock_call.return_value = {
        "status": True,
        "message": "OK!",
        "model": "gemini"
    }

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


@patch("mytext.functions._call_provider")
def test_run_mytext_cloudflare_success(mock_call):
    mock_call.return_value = {
        "status": True,
        "message": "OK2",
        "model": "cf"
    }

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


def test_run_mytext_cloudflare_failure():

    auth = {"api_key": "KEY", "account_id": "ACC"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.CLOUDFLARE
    )
    assert not result["status"]
    assert "error" in result["message"]


def test_run_mytext_ai_studio_failure():

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.AI_STUDIO
    )
    assert not result["status"]
    assert "error" in result["message"]


def test_run_mytext_openrouter_failure():

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.OPENROUTER
    )
    assert not result["status"]
    assert "error" in result["message"]


def test_run_mytext_cerebras_failure():

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.CEREBRAS
    )
    assert not result["status"]
    assert "error" in result["message"]


def test_run_mytext_groq_failure():

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.GROQ
    )
    assert not result["status"]
    assert "error" in result["message"]


def test_run_mytext_nvidia_failure():

    auth = {"api_key": "KEY"}
    result = run_mytext(
        text="hello",
        auth=auth,
        mode=Mode.PARAPHRASE,
        tone=Tone.NEUTRAL,
        provider=Provider.NVIDIA
    )
    assert not result["status"]
    assert "failed" in result["message"]


@patch("mytext.functions._load_auth_from_env")
@patch("mytext.functions.run_mytext")
def test_main_success(mock_run, mock_env, capsys):
    mock_env.return_value = {
        Provider.AI_STUDIO: {"api_key": "x"},
        Provider.CLOUDFLARE: {"api_key": "y", "account_id": "z"},
    }
    mock_run.return_value = {"status": True, "message": "AI RESULT", "model": "gemini"}

    with patch("sys.argv", ["mytext", "--text", "hello"]):
        main()

    out, _ = capsys.readouterr()
    assert "AI RESULT" in out


@patch("mytext.functions._load_auth_from_env")
@patch("mytext.functions.run_mytext")
def test_main_loop_success(mock_run, mock_env, capsys):
    mock_env.return_value = {
        Provider.AI_STUDIO: {"api_key": "x"},
        Provider.CLOUDFLARE: {"api_key": "y", "account_id": "z"},
    }
    mock_run.return_value = {"status": True, "message": "AI RESULT", "model": "gemini"}

    inputs = ["hello", "world"]

    def fake_input(_):
        if inputs:
            return inputs.pop(0)
        raise KeyboardInterrupt

    with patch("builtins.input", side_effect=fake_input):
        with patch("sys.argv", ["mytext", "--loop"]):
            try:
                main()
            except KeyboardInterrupt:
                pass

    out, _ = capsys.readouterr()
    assert out.count("AI RESULT") == 2


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


@patch("mytext.functions._load_auth_from_env")
@patch("mytext.functions.run_mytext")
def test_main_all_failures(mock_run, mock_env, capsys):
    mock_env.return_value = {
        Provider.AI_STUDIO: {"api_key": "a"},
        Provider.CLOUDFLARE: {"api_key": "b", "account_id": "c"},
        Provider.OPENROUTER: {"api_key": "d"},
        Provider.CEREBRAS: {"api_key": "e"},
        Provider.GROQ: {"api_key": "f"},
        Provider.NVIDIA: {"api_key": "g"},
    }
    mock_run.return_value = {"status": False, "message": "ERR", "model": "m"}

    with patch("sys.argv", ["mytext", "--text", "hello"]):
        main()

    out, _ = capsys.readouterr()
    assert "No provider succeeded" in out
