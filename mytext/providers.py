# -*- coding: utf-8 -*-
"""mytext providers."""

import time
import requests
from typing import Union, Dict
from memor import Prompt, RenderFormat
from .params import Provider
from .params import AI_STUDIO_API_URL, AI_STUDIO_HEADERS
from .params import CLOUDFLARE_API_URL, CLOUDFLARE_HEADERS
from .params import OPENROUTER_API_URL, OPENROUTER_HEADERS
from .params import CEREBRAS_API_URL, CEREBRAS_HEADERS
from .params import GROQ_API_URL, GROQ_HEADERS
from .params import NVIDIA_API_URL, NVIDIA_HEADERS


def _call_ai_studio(
        prompt: Prompt,
        auth: Dict[str, str],
        model: str,
        timeout: float = 15) -> Dict[str, Union[bool, str]]:
    """
    Call AI Studio API and return the response.

    :param prompt: user prompt
    :param auth: authentication parameters
    :param model: model
    :param timeout: API timeout
    """
    data = dict()
    data.update({"contents": prompt.render(RenderFormat.AI_STUDIO)})
    api_url = AI_STUDIO_API_URL.format(
        api_key=auth["api_key"],
        model=model)
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
                "model": model}
        raise Exception(
            "Status Code: {status_code}\n\nContent:\n{content}".format(
                status_code=response.status_code,
                content=response.text))


def _call_cloudflare(
        prompt: Prompt,
        auth: Dict[str, str],
        model: str,
        timeout: float = 15) -> Dict[str, Union[bool, str]]:
    """
    Call Cloudflare API and return the response.

    :param prompt: user prompt
    :param auth: authentication parameters
    :param model: model
    :param timeout: API timeout
    """
    data = dict()
    data["messages"] = [prompt.render(RenderFormat.OPENAI)]
    api_url = CLOUDFLARE_API_URL.format(
        account_id=auth["account_id"],
        model=model)
    headers = CLOUDFLARE_HEADERS.copy()
    headers["Authorization"] = headers["Authorization"].format(api_key=auth["api_key"])
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
                "model": model}
        raise Exception(
            "Status Code: {status_code}\n\nContent:\n{content}".format(
                status_code=response.status_code,
                content=response.text))


def _call_openrouter(
        prompt: Prompt,
        auth: Dict[str, str],
        model: str,
        timeout: float = 15) -> Dict[str, Union[bool, str]]:
    """
    Call OpenRouter API and return the response.

    :param prompt: user prompt
    :param auth: authentication parameters
    :param model: model
    :param timeout: API timeout
    """
    data = {
        "model": model,
        "messages": [prompt.render(RenderFormat.OPENAI)]
    }
    headers = OPENROUTER_HEADERS.copy()
    headers["Authorization"] = headers["Authorization"].format(api_key=auth["api_key"])
    with requests.Session() as session:
        response = session.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=data,
            timeout=timeout)
        if response.status_code in (200, 201):
            response_data = response.json()
            message_text = response_data["choices"][0]["message"]["content"]
            return {
                "status": True,
                "message": message_text,
                "model": model}
        raise Exception(
            "Status Code: {status_code}\n\nContent:\n{content}".format(
                status_code=response.status_code,
                content=response.text))


def _call_cerebras(
        prompt: Prompt,
        auth: Dict[str, str],
        model: str,
        timeout: float = 15) -> Dict[str, Union[bool, str]]:
    """
    Call Cerebras API and return the response.

    :param prompt: user prompt
    :param auth: authentication parameters
    :param model: model
    :param timeout: API timeout
    """
    data = dict()
    data["messages"] = [prompt.render(RenderFormat.OPENAI)]
    headers = CEREBRAS_HEADERS.copy()
    headers["Authorization"] = headers["Authorization"].format(api_key=auth["api_key"])
    with requests.Session() as session:
        response = session.post(
            CEREBRAS_API_URL,
            headers=headers,
            json={
                "model": model,
                "messages": data["messages"]
            },
            timeout=timeout,
        )
        if response.status_code in (200, 201):
            response_data = response.json()
            return {
                "status": True,
                "message": response_data["choices"][0]["message"]["content"],
                "model": model
            }
        raise Exception(
            "Status Code: {status_code}\n\nContent:\n{content}".format(
                status_code=response.status_code,
                content=response.text
            )
        )


def _call_groq(
        prompt: Prompt,
        auth: Dict[str, str],
        model: str,
        timeout: float = 15) -> Dict[str, Union[bool, str]]:
    """
    Call Groq API and return the response.

    :param prompt: user prompt
    :param auth: authentication parameters
    :param model: model
    :param timeout: API timeout
    """
    data = dict()
    data["messages"] = [prompt.render(RenderFormat.OPENAI)]
    data["model"] = model
    headers = GROQ_HEADERS.copy()
    headers["Authorization"] = headers["Authorization"].format(api_key=auth["api_key"])
    with requests.Session() as session:
        response = session.post(
            GROQ_API_URL,
            headers=headers,
            json=data,
            timeout=timeout)
        if response.status_code in (200, 201):
            response_data = response.json()
            return {
                "status": True,
                "message": response_data["choices"][0]["message"]["content"],
                "model": model}
        raise Exception(
            "Status Code: {status_code}\n\nContent:\n{content}".format(
                status_code=response.status_code,
                content=response.text))


def _call_nvidia(
        prompt: Prompt,
        auth: Dict[str, str],
        model: str,
        timeout: float = 15) -> Dict[str, Union[bool, str]]:
    """
    Call NVIDIA NIM API and return the response.

    :param prompt: user prompt
    :param auth: authentication parameters
    :param model: model
    :param timeout: API timeout
    """
    data = {
        "messages": [prompt.render(RenderFormat.OPENAI)],
        "model": model
    }
    headers = NVIDIA_HEADERS.copy()
    headers["Authorization"] = headers["Authorization"].format(api_key=auth["api_key"])
    with requests.Session() as session:
        response = session.post(
            NVIDIA_API_URL,
            headers=headers,
            json=data,
            timeout=timeout
        )
        if response.status_code in (200, 201):
            response_data = response.json()
            return {
                "status": True,
                "message": response_data["choices"][0]["message"]["content"],
                "model": model
            }
        raise Exception(
            "Status Code: {status_code}\n\nContent:\n{content}".format(
                status_code=response.status_code,
                content=response.text
            )
        )


PROVIDER_MAP = {
    Provider.AI_STUDIO: _call_ai_studio,
    Provider.CLOUDFLARE: _call_cloudflare,
    Provider.OPENROUTER: _call_openrouter,
    Provider.CEREBRAS: _call_cerebras,
    Provider.GROQ: _call_groq,
    Provider.NVIDIA: _call_nvidia,
}


def _call_provider(
        provider: Provider,
        prompt: Prompt,
        auth: Dict[str, str],
        main_model: str,
        fallback_model: str,
        timeout: float = 15,
        max_retries: int = 4,
        retry_delay: float = 0.5,
        backoff_factor: float = 1.2) -> Dict[str, Union[bool, str]]:
    """
    Call a provider and return the response.

    :param provider: LLM provider
    :param prompt: user prompt
    :param auth: authentication parameters
    :param main_model: main model
    :param fallback_model: fallback model
    :param timeout: API timeout
    :param max_retries: max retries
    :param retry_delay: retry delay
    :param backoff_factor: backoff factor
    """
    retry_index = 0
    error_message = ""
    next_delay = retry_delay
    selected_model = main_model
    while retry_index < max_retries:
        if retry_index >= (max_retries / 2):
            selected_model = fallback_model
        try:
            return PROVIDER_MAP[provider](prompt=prompt, auth=auth, model=selected_model, timeout=timeout)
        except Exception as e:
            error_message = str(e)
            retry_index += 1
            time.sleep(next_delay)
            next_delay = next_delay * backoff_factor
    return {
        "status": False,
        "message": error_message,
        "model": selected_model}
