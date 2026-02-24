# -*- coding: utf-8 -*-
"""mytext functions."""


from typing import Union, Dict, Any, Optional
from memor import Prompt, PromptTemplate
from .providers import _call_provider
from .params import Mode, Tone, Provider
from .params import DEFAULT_MODELS
from .params import INSTRUCTIONS
from .params import INVALID_TEXT_ERROR, INVALID_AUTH_ERROR, INVALID_MODE_ERROR
from .params import INVALID_TONE_ERROR, INVALID_PROVIDER_ERROR
from .params import INVALID_MODEL_ERROR
from .params import MISSING_AI_STUDIO_KEYS_ERROR, MISSING_CLOUDFLARE_KEYS_ERROR
from .params import MISSING_OPENROUTER_KEYS_ERROR
from .params import MISSING_CEREBRAS_KEYS_ERROR, MISSING_GROQ_KEYS_ERROR
from .params import MISSING_NVIDIA_KEYS_ERROR, MISSING_GITHUB_KEYS_ERROR


def _build_instruction(mode: Mode, tone: Tone) -> str:
    """
    Retrieve and format the instruction template for the given mode.

    :param mode: mode
    :param tone: tone
    """
    template = INSTRUCTIONS.get(mode, INSTRUCTIONS[Mode.PARAPHRASE])
    return template.format(tone=tone.value)


def _validate_run_mytext_inputs(
        text: Any,
        auth: Any,
        mode: Any,
        tone: Any,
        provider: Any,
        model: Any) -> None:
    """
    Validate run_mytext function inputs.

    :param text: user text
    :param auth: authentication parameters
    :param mode: mode
    :param tone: tone
    :param provider: API provider
    :param model: LLM model
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

    if model is not None and not isinstance(model, str):
        raise ValueError(INVALID_MODEL_ERROR)

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
    elif provider == Provider.GITHUB:
        if "api_key" not in auth:
            raise ValueError(MISSING_GITHUB_KEYS_ERROR)


def run_mytext(
        text: str,
        auth: dict,
        mode: Mode = Mode.PARAPHRASE,
        tone: Tone = Tone.NEUTRAL,
        provider: Provider = Provider.AI_STUDIO,
        model: Optional[str] = None) -> Dict[str, Union[bool, str]]:
    """
    Run mytext.

    :param text: user text
    :param auth: authentication parameters
    :param mode: mode
    :param tone: tone
    :param provider: API provider
    :param model: LLM model
    """
    try:
        _validate_run_mytext_inputs(text, auth, mode, tone, provider, model)
        instruction_str = _build_instruction(mode, tone)
        template = PromptTemplate(
            content="{instruction}\n\nUser text:\n{prompt[message]}",
            custom_map={"instruction": instruction_str},
        )
        prompt = Prompt(message=text, template=template)
        result = _call_provider(provider=provider,
                                prompt=prompt,
                                auth=auth,
                                model=model or DEFAULT_MODELS[provider])
        return result
    except Exception as e:
        return {
            "status": False,
            "message": str(e),
            "model": "unknown"}
