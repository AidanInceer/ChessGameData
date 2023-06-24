import logging
from logging import Logger


def create_logger() -> Logger:
    """Initializes the Logger object

    Returns:
        Logger: logger object directed at userlogfile path.
    """
    logging.basicConfig(
        format="[%(levelname)s %(module)s] %(message)s",
        level=logging.INFO,
        datefmt="%Y/%m/%d %I:%M:%S",
    )
    return logging.getLogger(__name__)
