import logging
import os
from typing import Optional


def setup_logging(verbosity: Optional[int] = None) -> None:
    """Configure the root logger.

    Parameters
    ----------
    verbosity: int, optional
        Verbosity level. ``0`` means warnings and above, ``1`` for info,
        ``2`` for debug. If not provided, the ``LOG_LEVEL`` environment
        variable is used.
    """
    if verbosity is None:
        try:
            verbosity = int(os.getenv("LOG_LEVEL", "0"))
        except ValueError:
            verbosity = 0

    level = logging.WARNING
    if verbosity >= 1:
        level = logging.INFO
    if verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
