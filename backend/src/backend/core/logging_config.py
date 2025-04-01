import logging
import sys


def setup_logger(name: str | None = None) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)

    # Only configure if handlers haven't been set up
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
