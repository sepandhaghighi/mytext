# -*- coding: utf-8 -*-

from unittest.mock import patch
import pytest
from mytext import Mode, Tone, Provider
from mytext import run_mytext
from mytext.cli import main
from mytext.params import MY_TEXT_VERSION, MY_TEXT_OVERVIEW, MY_TEXT_REPO

TEST_CASE_NAME = "CLI tests"


@patch("mytext.cli._load_auth_from_env")
@patch("mytext.cli.run_mytext")
def test_main_single_run_success1(mock_run, mock_env, capsys):
    mock_env.return_value = {
        Provider.AI_STUDIO: {"api_key": "x"},
        Provider.CLOUDFLARE: {"api_key": "y", "account_id": "z"},
    }
    mock_run.return_value = {"status": True, "message": "AI RESULT", "model": "gemini"}

    with patch("sys.argv", ["mytext", "--text", "hello"]):
        main()

    out, _ = capsys.readouterr()
    assert "AI RESULT" in out


@patch("mytext.cli._load_auth_from_env")
@patch("mytext.cli.run_mytext")
def test_main_single_run_success2(mock_run, mock_env, capsys):
    mock_env.return_value = {
        Provider.AI_STUDIO: {"api_key": "x"},
        Provider.CLOUDFLARE: {"api_key": None, "account_id": None},
    }
    mock_run.return_value = {"status": True, "message": "AI RESULT", "model": "gemini"}

    with patch("sys.argv", ["mytext", "--text", "hello", "--provider", "ai-studio"]):
        main()

    out, _ = capsys.readouterr()
    assert "AI RESULT" in out


@patch("mytext.cli._load_auth_from_env")
@patch("mytext.cli.run_mytext")
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
            with pytest.raises(SystemExit):
                main()

    out, _ = capsys.readouterr()
    assert out.count("AI RESULT") == 2


@patch("mytext.cli._load_auth_from_env")
@patch("mytext.cli.run_mytext")
def test_main_all_providers_failure(mock_run, mock_env, capsys):
    mock_env.return_value = {
        Provider.AI_STUDIO: {"api_key": "a"},
        Provider.CLOUDFLARE: {"api_key": "b", "account_id": "c"},
        Provider.OPENROUTER: {"api_key": "d"},
        Provider.CEREBRAS: {"api_key": "e"},
        Provider.GROQ: {"api_key": "f"},
        Provider.NVIDIA: {"api_key": "g"},
        Provider.GITHUB: {"api_key": "h"},
    }
    mock_run.return_value = {"status": False, "message": "ERR", "model": "m"}

    with patch("sys.argv", ["mytext", "--text", "hello"]):
        main()

    out, _ = capsys.readouterr()
    assert "No provider succeeded" in out


@patch("mytext.cli._load_auth_from_env")
@patch("mytext.cli.run_mytext")
def test_main_specific_provider_failure(mock_run, mock_env, capsys):
    mock_env.return_value = {
        Provider.AI_STUDIO: {"api_key": "a"},
        Provider.CLOUDFLARE: {"api_key": "b", "account_id": "c"},
        Provider.OPENROUTER: {"api_key": "d"},
        Provider.CEREBRAS: {"api_key": "e"},
        Provider.GROQ: {"api_key": "f"},
        Provider.GITHUB: {"api_key": "g"},
        Provider.NVIDIA: {"api_key": None},
    }
    mock_run.return_value = {"status": False, "message": "ERR", "model": "m"}

    with patch("sys.argv", ["mytext", "--text", "hello", "--provider", "nvidia"]):
        main()

    out, _ = capsys.readouterr()
    assert "No provider succeeded" in out
