import logging, os, sys
from logging.config import dictConfig
def setup_logging(level: str | int | None = None):
    level = level or os.getenv("FASTBACK_LOG", "WARNING")
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "std": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "std",
                "stream": sys.stdout,
            }
        },
        "root": {"handlers": ["console"], "level": level},
    })
