import logging
import configparser
from pyrogram import Client


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%m/%d %H:%M:%S')
logger = logging.getLogger(__name__)
for name, l in logging.root.manager.loggerDict.items():
    if name.startswith('pyrogram') and isinstance(l, logging.Logger):
        l.setLevel(logging.WARNING)

config = configparser.ConfigParser()
config.read('config.ini')
dk = Client(
    'dk',
    api_id=config['dk']['api_id'],
    api_hash=config['dk']['api_hash'],
    bot_token=config['dk']['bot_token'],
)

# scheduler = BackgroundScheduler(misfire_grace_time=60, timezone='Asia/Shanghai')

data_dir = 'data'
check_pickle_file = 'checks.p'
check_ids_by_user_file = 'check_ids_by_user.p'
check_status_store_pickle_file = 'check_store.p'
