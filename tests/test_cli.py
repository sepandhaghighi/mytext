# -*- coding: utf-8 -*-

from unittest.mock import patch
import pytest
from mytext import Provider
from mytext.cli import main
from mytext.params import MY_TEXT_VERSION, MY_TEXT_OVERVIEW, MY_TEXT_REPO

TEST_CASE_NAME = "CLI tests"


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
    assert "Provide text either as a positional argument or with --text." in err


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
def test_main_single_run_success3(mock_run, mock_env, capsys):
    mock_env.return_value = {
        Provider.AI_STUDIO: {"api_key": "x"},
        Provider.CLOUDFLARE: {"api_key": None, "account_id": None},
    }
    mock_run.return_value = {"status": True, "message": "AI RESULT", "model": "gemini"}

    with patch("sys.argv", ["mytext", "hello", "--provider", "ai-studio"]):
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


@patch("mytext.cli._load_auth_from_env")
@patch("mytext.cli.run_mytext")
def test_cli_custom_model(mock_run, mock_env, capsys):

    mock_env.return_value = {
        Provider.GROQ: {"api_key": "x"},
    }

    mock_run.return_value = {
        "status": True,
        "message": "DONE",
        "model": "custom"
    }

    with patch(
        "sys.argv",
        [
            "mytext",
            "--text",
            "hello",
            "--provider",
            "groq",
            "--model",
            "llama-custom"
        ]
    ):
        main()

    _, kwargs = mock_run.call_args

    assert kwargs["model"] == "llama-custom"


@pytest.mark.parametrize(
    "provider, env, expected",
    [
        (
            Provider.AI_STUDIO,
            {
                "AI_STUDIO_API_KEY": "ai-key",
            },
            {
                "api_key": "ai-key",
            },
        ),
        (
            Provider.CLOUDFLARE,
            {
                "CLOUDFLARE_API_KEY": "cloudflare-key",
                "CLOUDFLARE_ACCOUNT_ID": "cloudflare-account",
            },
            {
                "api_key": "cloudflare-key",
                "account_id": "cloudflare-account",
            },
        ),
        (
            Provider.OPENROUTER,
            {
                "OPENROUTER_API_KEY": "openrouter-key",
            },
            {
                "api_key": "openrouter-key",
            },
        ),
        (
            Provider.CEREBRAS,
            {
                "CEREBRAS_API_KEY": "cerebras-key",
            },
            {
                "api_key": "cerebras-key",
            },
        ),
        (
            Provider.GROQ,
            {
                "GROQ_API_KEY": "groq-key",
            },
            {
                "api_key": "groq-key",
            },
        ),
        (
            Provider.NVIDIA,
            {
                "NVIDIA_API_KEY": "nvidia-key",
            },
            {
                "api_key": "nvidia-key",
            },
        ),
        (
            Provider.GITHUB,
            {
                "GITHUB_API_KEY": "github-key",
            },
            {
                "api_key": "github-key",
            },
        ),
    ],
)
def test_load_auth_from_env_all_providers(provider, env, expected):
    with patch.dict("os.environ", env, clear=True):
        auth_map = _load_auth_from_env()

    assert provider in auth_map
    assert auth_map[provider] == expected
