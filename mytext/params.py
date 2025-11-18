# -*- coding: utf-8 -*-
"""mytext params."""
from enum import Enum
MY_TEXT_VERSION = "0.1"


class Provider(Enum):
    """LLM provider enum."""

    AI_STUDIO = "ai_studio"
    CLOUDFLARE = "cloudflare"


class Mode(Enum):
    """Mode enum."""

    PARAPHRASE = "paraphrase"
    GRAMMAR = "grammar"


class Tone(Enum):
    """Tone enum."""

    NEUTRAL = "neutral"
    FORMAL = "formal"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    ACADEMIC = "academic"
    CREATIVE = "creative"


AI_STUDIO_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

AI_STUDIO_HEADERS = {
    "Content-Type": "application/json"
}

CLOUDFLARE_API_URL = "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/{model}"

CLOUDFLARE_HEADERS = {
    "Authorization": "Bearer {api_key}",
    "Content-Type": "application/json"
}

INSTRUCTIONS = {
    Mode.PARAPHRASE: "Paraphrase the following text clearly and naturally. Tone should be {tone}.",
    Mode.GRAMMAR: "Correct grammar and improve clarity while preserving meaning. Tone should be {tone}.",
}

INVALID_TEXT_ERROR = "`text` must be a non-empty string."
INVALID_AUTH_ERROR = "`auth` must be a dictionary."
INVALID_MODE_ERROR = "`mode` must be an instance of Mode enum, got: {value}"
INVALID_TONE_ERROR = "`tone` must be an instance of Tone enum, got: {value}"
INVALID_PROVIDER_ERROR = "`provider` must be an instance of Provider enum, got: {value}"
UNSUPPORTED_PROVIDER_ERROR = "Unsupported provider: {value}"


MISSING_API_KEY_ERROR = "AI_STUDIO provider requires `api_key` in auth."
MISSING_CLOUDFLARE_KEYS_ERROR = "CLOUDFLARE provider requires keys: {keys}"
