import os
from session import *


if not os.path.isdir(data_dir):
    os.mkdir(data_dir)


from register import register_handlers


def starting():
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    register_handlers()
    return logger.info("[TGBot] Initialized.")
