import os
from session import logger
from settings import data_dir

if not os.path.isdir(data_dir):
    os.mkdir(data_dir)

from checkAuth import init_auth_users
from register import register_handlers, cron_schedule


def starting():
    init_auth_users()
    register_handlers()
    cron_schedule()
    logger.info("[Bot]\tInitialized.")
