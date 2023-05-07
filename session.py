import logging
import configparser
from pyrogram import Client
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%m/%d %H:%M:%S')
logger = logging.getLogger(__name__)
for name, l in logging.root.manager.loggerDict.items():
    if name.startswith('pyrogram') and isinstance(l, logging.Logger):
        l.setLevel(logging.WARNING)
        # logger.info(f'[Init]\tLogger {name} level set to WARNING')
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

config = configparser.ConfigParser()
config.read('config.ini')
dk = Client(
    'dk',
    api_id=config['dk']['api_id'],
    api_hash=config['dk']['api_hash'],
    bot_token=config['dk']['bot_token'],
)

scheduler = AsyncIOScheduler(misfire_grace_time=60, timezone='Asia/Shanghai')
