# -*- coding: utf-8 -*-
"""mytext params."""
from enum import Enum
MY_TEXT_VERSION = "0.1"


class Provider(Enum):
    """LLM provider enum."""

    AI_STUDIO = "ai_studio"
    MLVOCA = "mlvoca"


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

MLVOCA_API_URL = "https://mlvoca.com/api/generate"

MLVOCA_HEADERS = {
    "Content-Type": "application/json"
}

INSTRUCTIONS = {
    Mode.PARAPHRASE: "Paraphrase the following text clearly and naturally. Tone should be {tone}.",
    Mode.GRAMMAR: "Correct grammar and improve clarity while preserving meaning. Tone should be {tone}.",
}
