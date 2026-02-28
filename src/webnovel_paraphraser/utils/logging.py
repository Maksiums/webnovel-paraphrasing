"""Project logging setup."""

from __future__ import annotations

import logging


def configure_logging(debug: bool = False) -> None:
    """Configure logging for CLI commands."""

    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )
