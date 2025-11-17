# -*- coding: utf-8 -*-
"""mytext params."""
from enum import Enum
MY_TEXT_VERSION = "0.1"


class Provider(Enum):
    """LLM provider enum."""

    AI_STUDIO = "ai_studio"


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
