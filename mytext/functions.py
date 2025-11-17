# -*- coding: utf-8 -*-
"""mytext functions."""

import os
import time
import json
import argparse
import requests
from memor import Prompt, PromptTemplate, RenderFormat
from .params import Mode, Tone, Provider
from .params import AI_STUDIO_API_URL, AI_STUDIO_HEADERS
from .params import INSTRUCTIONS



def build_instruction(mode: Mode, tone: Tone) -> str:
    """
    Retrieve and format the instruction template for the given mode.

    :param mode: mode
    :param tone: tone
    """
    template = INSTRUCTIONS.get(mode, INSTRUCTIONS[Mode.PARAPHRASE])
    return template.format(tone=tone.value)


def call_ai_studio(
        prompt: Prompt,
        api_key: str,
        main_model="gemini-2.0-flash",
        fallback_model="gemini-2.0-flash-lite",
        timeout=15,
        max_retries=3,
        retry_delay=0.5,
        backoff_factor=1):
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


def call_mlvoca(
        prompt: Prompt,
        main_model="deepseek-r1:1.5b",
        fallback_model="tinyllama",
        timeout=15,
        max_retries=3,
        retry_delay=0.5,
        backoff_factor=1):
    retry_index = 0
    error_message = ""
    next_delay = retry_delay
    selected_model = main_model
    data = {"model": selected_model, "prompt": prompt.render(RenderFormat.STRING), "stream": False}
    while retry_index < max_retries:
        try:
            api_url = MLVOCA_API_URL
            with requests.Session() as session:
                response = session.post(
                    api_url,
                    headers=MLVOCA_HEADERS,
                    json=data,
                    timeout=timeout)
                if response.status_code in (200, 201):
                    response_data = response.json()
                    return {
                        "status": True,
                        "message": response_data["response"],
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

def run_mytext(text: str, api_key: str = None, mode: Mode = Mode.PARAPHRASE, tone: Tone = Tone.NEUTRAL, provider: Provider = Provider.AI_STUDIO):
    instruction_str = build_instruction(mode, tone)
    template = PromptTemplate(
        content="{instruction}\n\nUser text:\n{prompt[text]}",
        custom_map={"instruction": instruction_str},
    )
    prompt = Prompt(message=text, template=template)
    if provider == Provider.AI_STUDIO:
        result = call_ai_studio(prompt=prompt, api_key=api_key)
    return result


def main():
    parser = argparse.ArgumentParser(description="mytext -- AI-powered text enhancer.")

    parser.add_argument(
        "--mode",
        choices=[x.value for x in Mode],
        default=Mode.PARAPHRASE,
        help="Processing mode (default: paraphrase)"
    )

    parser.add_argument(
        "--tone",
        choices=[x.value for x in Tone],
        default=Tone.NEUTRAL,
        help="Writing tone (default: neutral)"
    )

    parser.add_argument(
        "--text",
        required=True,
        help="The text you want to transform"
    )

    parser.add_argument(
        "--api-key",
        help="AI Studio API key."
    )

    args = parser.parse_args()
    text = args.text
    tone = args.tone
    mode = args.mode
    api_key = args.api_key or os.getenv("AI_STUDIO_API_KEY")
    result = run_mytext(api_key=api_key, text=text, mode=mode, tone=tone)
    print(result["message"])
