# License: MIT
# Copyright © 2026 Frequenz Energy-as-a-Service GmbH

"""Environment variable helpers."""

from __future__ import annotations

import os


def require_env(var: str) -> str:
    """Return an environment variable value or raise a clear error.

    Args:
        var: Name of the environment variable to read.

    Returns:
        Environment variable value.

    Raises:
        RuntimeError: If the environment variable is missing or empty.
    """
    val = os.getenv(var)
    if not val:
        raise RuntimeError(
            f"Missing or empty required environment variable `{var}`. "
            "Set it in your environment or .env file."
        )
    return val
