# -*- coding: utf-8 -*-
"""mytext functions."""

import os
import time
import argparse
import requests
from typing import Union, Dict, Any
from memor import Prompt, PromptTemplate, RenderFormat
from .params import Mode, Tone, Provider
from .params import AI_STUDIO_API_URL, AI_STUDIO_HEADERS
from .params import CLOUDFLARE_API_URL, CLOUDFLARE_HEADERS
from .params import INSTRUCTIONS, OUTPUT_TEMPLATE
from .params import INVALID_TEXT_ERROR, INVALID_AUTH_ERROR, INVALID_MODE_ERROR
from .params import INVALID_TONE_ERROR, INVALID_PROVIDER_ERROR
from .params import MISSING_AI_STUDIO_KEYS_ERROR, MISSING_CLOUDFLARE_KEYS_ERROR
from .params import NO_PROVIDER_SUCCEEDED_MESSAGE, NO_VALID_PROVIDER_CREDENTIALS_MESSAGE, ALL_PROVIDERS_FAILED_MESSAGE


def _build_instruction(mode: Mode, tone: Tone) -> str:
    """
    Retrieve and format the instruction template for the given mode.

    :param mode: mode
    :param tone: tone
    """
    template = INSTRUCTIONS.get(mode, INSTRUCTIONS[Mode.PARAPHRASE])
    return template.format(tone=tone.value)


def _call_ai_studio(
        prompt: Prompt,
        api_key: str,
        main_model: str="gemini-2.0-flash",
        fallback_model: str="gemini-2.0-flash-lite",
        timeout: float=15,
        max_retries: int=3,
        retry_delay: float=0.5,
        backoff_factor: float=1) -> Dict[str, Union[bool, str]]:
    """
    Call AI Studio API and return the response.

    :param prompt: user prompt
    :param api_key: API key
    :param main_model: main model
    :param fallback_model: fallback model
    :param timeout: API timeout
    :param max_retries: max retries
    :param retry_delay: retry delay
    :param backoff_factor: backoff factor
    """
    data = dict()
    data.update({"contents": prompt.render(RenderFormat.AI_STUDIO)})
    retry_index = 0
    error_message = ""
    next_delay = retry_delay
    selected_model = main_model
    while retry_index < max_retries:
        try:
            api_url = AI_STUDIO_API_URL.format(
                api_key=api_key,
                model=selected_model)
            with requests.Session() as session:
                response = session.post(
                    api_url,
                    headers=AI_STUDIO_HEADERS,
                    json=data,
                    timeout=timeout)
                if response.status_code in (200, 201):
                    response_data = response.json()
                    return {
                        "status": True,
                        "message": response_data['candidates'][0]['content']['parts'][0]['text'],
                        "model": selected_model}
                elif response.status_code == 503:
                    selected_model = fallback_model
                raise Exception(
                    "Status Code: {status_code}\n\nContent:\n{content}".format(
                        status_code=response.status_code,
                        content=response.text))
        except Exception as e:
            error_message = str(e)
            retry_index += 1
            time.sleep(next_delay)
            next_delay = next_delay * backoff_factor
    return {
        "status": False,
        "message": error_message,
        "model": selected_model}


def _call_cloudflare(
        prompt: Prompt,
        account_id: str,
        api_key: str,
        main_model: str ="meta/llama-3-8b-instruct",
        fallback_model: str ="qwen/qwen3-30b-a3b-fp8",
        timeout: float=15,
        max_retries: int=3,
        retry_delay: float=0.5,
        backoff_factor: float=1) -> Dict[str, Union[bool, str]]:
    """
    Call Cloudflare API and return the response.

    :param prompt: user prompt
    :param account_id: account ID
    :param api_key: API key
    :param main_model: main model
    :param fallback_model: fallback model
    :param timeout: API timeout
    :param max_retries: max retries
    :param retry_delay: retry delay
    :param backoff_factor: backoff factor
    """
    data = dict()
    data["messages"] = [prompt.render(RenderFormat.OPENAI)]
    retry_index = 0
    error_message = ""
    next_delay = retry_delay
    selected_model = main_model
    headers = CLOUDFLARE_HEADERS.copy()
    headers["Authorization"] = headers["Authorization"].format(api_key=api_key)
    while retry_index < max_retries:
        try:
            api_url = CLOUDFLARE_API_URL.format(
                account_id=account_id,
                model=selected_model)
            with requests.Session() as session:
                response = session.post(
                    api_url,
                    headers=headers,
                    json=data,
                    timeout=timeout)
                if response.status_code in (200, 201):
                    response_data = response.json()
                    return {
                        "status": True,
                        "message": response_data["result"]["response"],
                        "model": selected_model}
                elif response.status_code == 503:
                    selected_model = fallback_model
                raise Exception(
                    "Status Code: {status_code}\n\nContent:\n{content}".format(
                        status_code=response.status_code,
                        content=response.text))
        except Exception as e:
            error_message = str(e)
            retry_index += 1
            time.sleep(next_delay)
            next_delay = next_delay * backoff_factor
    return {
        "status": False,
        "message": error_message,
        "model": selected_model}


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
        if provider == Provider.AI_STUDIO:
            api_key = auth["api_key"]
            result = _call_ai_studio(prompt=prompt, api_key=api_key)
        if provider == Provider.CLOUDFLARE:
            api_key = auth["api_key"]
            account_id = auth["account_id"]
            result = _call_cloudflare(prompt=prompt, api_key=api_key, account_id=account_id)
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
    }


def main() -> None:
    """CLI main function."""
    parser = argparse.ArgumentParser(description="mytext -- AI-powered text enhancer.")

    parser.add_argument(
        "--mode",
        choices=[x.value for x in Mode],
        default=Mode.PARAPHRASE.value,
        help="Processing mode (default: paraphrase)"
    )

    parser.add_argument(
        "--tone",
        choices=[x.value for x in Tone],
        default=Tone.NEUTRAL.value,
        help="Writing tone (default: neutral)"
    )

    parser.add_argument(
        "--text",
        required=True,
        help="The text you want to transform"
    )

    args = parser.parse_args()
    text = args.text
    tone = Tone(args.tone)
    mode = Mode(args.mode)
    auth_map = _load_auth_from_env()
    errors = []
    for provider in [Provider.AI_STUDIO, Provider.CLOUDFLARE]:
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
            print(OUTPUT_TEMPLATE.format(result = result["message"].strip()))
            return
        else:
            errors.append((provider, result["message"]))
    print(NO_PROVIDER_SUCCEEDED_MESSAGE)
    if not errors:
        print(NO_VALID_PROVIDER_CREDENTIALS_MESSAGE)
    else:
        print(ALL_PROVIDERS_FAILED_MESSAGE)
