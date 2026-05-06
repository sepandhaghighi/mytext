# -*- coding: utf-8 -*-
"""mytext modules."""
from mytext.params import MY_TEXT_VERSION
from mytext.params import Provider, Mode, Tone
from mytext.errors import MyTextError, MyTextProviderError, MyTextValidationError
from mytext.functions import run_mytext
__version__ = MY_TEXT_VERSION

__all__ = ["Provider", "Mode", "Tone", "run_mytext", "MyTextError", "MyTextProviderError", "MyTextValidationError"]
