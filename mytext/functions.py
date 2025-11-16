# -*- coding: utf-8 -*-
"""mytext functions."""

import os
import json
import argparse
import requests
from memor import Prompt, PromptTemplate, RenderFormat

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

INSTRUCTIONS = {
    "paraphrase": "Paraphrase the following text clearly and naturally. Tone should be {tone}.",
    "grammar": "Correct grammar and improve clarity while preserving meaning. Tone should be {tone}.",
}

def build_instruction(mode: str, tone: str) -> str:
    """
    Retrieve and format the instruction template for the given mode.

    :param mode: mode
    :param tone: tone
    """
    template = INSTRUCTIONS.get(mode, INSTRUCTIONS["paraphrase"])
    return template.format(tone=tone)


def call_llm(api_key: str, text: str):
    pass


def run_mytext(api_key: str, text: str, mode: str, tone: str):
    instruction_str = build_instruction(mode, tone)

    template = PromptTemplate(
        content="{instruction}\n\nUser text:\n{prompt[text]}",
        custom_map={"instruction": instruction_str},
    )

    prompt = Prompt(message=text, template=template)
    final_prompt = prompt.render(render_format=RenderFormat.AI_STUDIO)
    result = call_llm(api_key, final_prompt)
    return result


def main():
    parser = argparse.ArgumentParser(description="mytext -- AI-powered text enhancer.")

    parser.add_argument(
        "--mode",
        choices=["paraphrase", "grammar"],
        default="paraphrase",
        help="Processing mode (default: paraphrase)"
    )

    parser.add_argument(
        "--tone",
        choices=["neutral", "formal", "casual", "friendly", "professional", "academic", "creative"],
        default="neutral",
        help="Writing tone (default: neutral)"
    )

    parser.add_argument(
        "--text",
        required=True,
        help="The text you want to transform"
    )

    parser.add_argument(
        "--api-key",
        help="Gemini API key."
    )

    args = parser.parse_args()

    text = args.text
    tone = args.tone
    mode = args.mode
    api_key = args.api_key or os.getenv("GEMINI_API_KEY")
    result = run_mytext(api_key=api_key, text=text, mode=mode, tone=tone)
    print(result)

if __name__ == "__main__":
    main()
