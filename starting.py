from session import logger
from register import register_handlers


def starting():
    register_handlers()
    return logger.info("[TGBot] Initialized.")
