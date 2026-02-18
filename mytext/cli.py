# -*- coding: utf-8 -*-
"""mytext cli."""

import os
import argparse
from typing import Dict
from art import tprint
from .functions import run_mytext
from .params import MY_TEXT_VERSION, MY_TEXT_OVERVIEW, MY_TEXT_REPO
from .params import Mode, Tone, Provider
from .params import OUTPUT_TEMPLATE
from .params import TEXT_IS_REQUIRED_ERROR
from .params import NO_PROVIDER_SUCCEEDED_MESSAGE
from .params import LOOP_INPUT_MESSAGE


def _print_mytext_info() -> None:
    """Print mytext details."""
    tprint("MyText")
    tprint("V:" + MY_TEXT_VERSION)
    print(MY_TEXT_OVERVIEW)
    print("Repo : " + MY_TEXT_REPO)


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


def _load_model_from_env() -> Dict[Provider, str]:
    """Load model from environment."""
    return {
        Provider.AI_STUDIO: os.getenv("AI_STUDIO_MODEL"),
        Provider.CLOUDFLARE: os.getenv("CLOUDFLARE_MODEL"),
        Provider.OPENROUTER: os.getenv("OPENROUTER_MODEL"),
        Provider.CEREBRAS: os.getenv("CEREBRAS_MODEL"),
        Provider.GROQ: os.getenv("GROQ_MODEL"),
        Provider.NVIDIA: os.getenv("NVIDIA_MODEL"),
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
        "--provider",
        type=str.lower,
        choices=[x.value for x in Provider] + ["auto"],
        default="auto",
        help="Force a specific provider (default: auto)"
    )

    parser.add_argument(
        "--model",
        type=str,
        help="Override LLM model"
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
        model_map = _load_model_from_env()
        providers = [x for x in Provider]
        model = None
        if args.provider != "auto":
            providers = [Provider(args.provider)]
        while True:
            errors = []
            successful_attempt = False
            for provider in providers:
                auth = auth_map.get(provider)
                model = model_map.get(provider)
                if args.provider != "auto":
                    model = args.model or model
                if not auth or not all(auth.values()):
                    continue
                result = run_mytext(
                    auth=auth,
                    text=text,
                    mode=mode,
                    tone=tone,
                    provider=provider,
                    model=model
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
