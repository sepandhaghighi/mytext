# -*- coding: utf-8 -*-
"""mytext errors."""


class MyTextError(Exception):
    """Base exception for all MyText errors."""


class MyTextValidationError(MyTextError, ValueError):
    """Raised when input validation fails."""


class MyTextProviderError(MyTextError):
    """Raised when a provider call fails."""
