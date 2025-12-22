# -*- coding: utf-8 -*-
"""mytext functions."""

import os
import argparse
from typing import Union, Dict, Any
from art import tprint
from memor import Prompt, PromptTemplate
from .providers import _call_provider
from .params import MY_TEXT_VERSION, MY_TEXT_OVERVIEW, MY_TEXT_REPO
from .params import Mode, Tone, Provider
from .params import DEFAULT_MODELS
from .params import INSTRUCTIONS, OUTPUT_TEMPLATE
from .params import INVALID_TEXT_ERROR, INVALID_AUTH_ERROR, INVALID_MODE_ERROR
from .params import INVALID_TONE_ERROR, INVALID_PROVIDER_ERROR
from .params import TEXT_IS_REQUIRED_ERROR
from .params import MISSING_AI_STUDIO_KEYS_ERROR, MISSING_CLOUDFLARE_KEYS_ERROR
from .params import NO_PROVIDER_SUCCEEDED_MESSAGE, MISSING_OPENROUTER_KEYS_ERROR
from .params import MISSING_CEREBRAS_KEYS_ERROR, MISSING_GROQ_KEYS_ERROR
from .params import MISSING_NVIDIA_KEYS_ERROR
from .params import LOOP_INPUT_MESSAGE


def _print_mytext_info() -> None:
    """Print mytext details."""
    tprint("MyText")
    tprint("V:" + MY_TEXT_VERSION)
    print(MY_TEXT_OVERVIEW)
    print("Repo : " + MY_TEXT_REPO)


def _build_instruction(mode: Mode, tone: Tone) -> str:
    """
    Retrieve and format the instruction template for the given mode.

    :param mode: mode
    :param tone: tone
    """
    template = INSTRUCTIONS.get(mode, INSTRUCTIONS[Mode.PARAPHRASE])
    return template.format(tone=tone.value)


def _validate_run_mytext_inputs(text: Any, auth: Any, mode: Any, tone: Any, provider: Any) -> None:
    """
    Validate run_mytext function inputs.

    :param text: user text
    :param auth: authentication parameters
    :param mode: mode
    :param tone: tone
    :param provider: API provider
    """
    if not isinstance(text, str):
        raise ValueError(INVALID_TEXT_ERROR)

    if not isinstance(auth, dict):
        raise ValueError(INVALID_AUTH_ERROR)

    if not isinstance(mode, Mode):
        raise ValueError(INVALID_MODE_ERROR)

    if not isinstance(tone, Tone):
        raise ValueError(INVALID_TONE_ERROR)

    if not isinstance(provider, Provider):
        raise ValueError(INVALID_PROVIDER_ERROR)

    if provider == Provider.AI_STUDIO:
        if "api_key" not in auth:
            raise ValueError(MISSING_AI_STUDIO_KEYS_ERROR)
    elif provider == Provider.CLOUDFLARE:
        if "api_key" not in auth or "account_id" not in auth:
            raise ValueError(MISSING_CLOUDFLARE_KEYS_ERROR)
    elif provider == Provider.OPENROUTER:
        if "api_key" not in auth:
            raise ValueError(MISSING_OPENROUTER_KEYS_ERROR)
    elif provider == Provider.CEREBRAS:
        if "api_key" not in auth:
            raise ValueError(MISSING_CEREBRAS_KEYS_ERROR)
    elif provider == Provider.GROQ:
        if "api_key" not in auth:
            raise ValueError(MISSING_GROQ_KEYS_ERROR)
    elif provider == Provider.NVIDIA:
        if "api_key" not in auth:
            raise ValueError(MISSING_NVIDIA_KEYS_ERROR)


def run_mytext(
        text: str,
        auth: dict,
        mode: Mode = Mode.PARAPHRASE,
        tone: Tone = Tone.NEUTRAL,
        provider: Provider = Provider.AI_STUDIO) -> Dict[str, Union[bool, str]]:
    """
    Run mytext.

    :param text: user text
    :param auth: authentication parameters
    :param mode: mode
    :param tone: tone
    :param provider: API provider
    """
    try:
        _validate_run_mytext_inputs(text, auth, mode, tone, provider)
        instruction_str = _build_instruction(mode, tone)
        template = PromptTemplate(
            content="{instruction}\n\nUser text:\n{prompt[message]}",
            custom_map={"instruction": instruction_str},
        )
        prompt = Prompt(message=text, template=template)
        result = _call_provider(provider=provider,
                                prompt=prompt,
                                auth=auth,
                                main_model=DEFAULT_MODELS[provider]["main"],
                                fallback_model=DEFAULT_MODELS[provider]["fallback"])
        return result
    except Exception as e:
        return {
            "status": False,
            "message": str(e),
            "model": "unknown"}


def _load_auth_from_env() -> Dict[Provider, Dict[str, str]]:
    """Load authentication parameters from environment."""
    return {
        Provider.AI_STUDIO: {
            "api_key": os.getenv("AI_STUDIO_API_KEY")
        },
        Provider.CLOUDFLARE: {
            "api_key": os.getenv("CLOUDFLARE_API_KEY"),
            "account_id": os.getenv("CLOUDFLARE_ACCOUNT_ID"),
        },
        Provider.OPENROUTER: {
            "api_key": os.getenv("OPENROUTER_API_KEY"),
        },
        Provider.CEREBRAS: {
            "api_key": os.getenv("CEREBRAS_API_KEY"),
        },
        Provider.GROQ: {
            "api_key": os.getenv("GROQ_API_KEY"),
        },
        Provider.NVIDIA: {
            "api_key": os.getenv("NVIDIA_API_KEY"),
        },
    }


def main() -> None:
    """CLI main function."""
    parser = argparse.ArgumentParser(description="mytext -- AI-powered text enhancer.")

    parser.add_argument('--version', help='Version', nargs="?", const=1)

    parser.add_argument('--info', help='Info', nargs="?", const=1)

    parser.add_argument(
        "--mode",
        type=str.lower,
        choices=[x.value for x in Mode],
        default=Mode.PARAPHRASE.value,
        help="Processing mode (default: paraphrase)"
    )

    parser.add_argument(
        "--tone",
        type=str.lower,
        choices=[x.value for x in Tone],
        default=Tone.NEUTRAL.value,
        help="Writing tone (default: neutral)"
    )

    parser.add_argument(
        "--text",
        type=str,
        help="The text you want to transform"
    )

    parser.add_argument("--loop", help="Loop mode flag", action='store_true', default=False)

    args = parser.parse_args()
    if args.version:
        print(MY_TEXT_VERSION)
    elif args.info:
        _print_mytext_info()
    else:
        text = args.text
        if not text:
            if args.loop:
                text = input(LOOP_INPUT_MESSAGE)
            else:
                parser.error(TEXT_IS_REQUIRED_ERROR)
        tone = Tone(args.tone)
        mode = Mode(args.mode)
        auth_map = _load_auth_from_env()
        while True:
            errors = []
            successful_attempt = False
            for provider in [
                    Provider.AI_STUDIO,
                    Provider.CLOUDFLARE,
                    Provider.OPENROUTER,
                    Provider.CEREBRAS,
                    Provider.GROQ,
                    Provider.NVIDIA]:
                auth = auth_map.get(provider)
                if not auth or not all(auth.values()):
                    continue
                result = run_mytext(
                    auth=auth,
                    text=text,
                    mode=mode,
                    tone=tone,
                    provider=provider
                )
                if result["status"]:
                    print(OUTPUT_TEMPLATE.format(result=result["message"].strip()))
                    successful_attempt = True
                    break
                else:
                    errors.append((provider, result["message"]))
            if not successful_attempt:
                print(NO_PROVIDER_SUCCEEDED_MESSAGE)
            # if not errors:
            #    print(NO_VALID_PROVIDER_CREDENTIALS_MESSAGE)
            # else:
            #    print(ALL_PROVIDERS_FAILED_MESSAGE)
            if args.loop:
                text = input(LOOP_INPUT_MESSAGE)
            else:
                break
