from dmFunctions import *
from dmMessages import process_msg
from dmCallback import process_callback
from pyrogram import filters
from session import dk, logger
from pyrogram.handlers import MessageHandler, CallbackQueryHandler


def register_handlers():
    dk.add_handler(MessageHandler(cancel, filters.command(['cancel']) & filters.private))

    dk.add_handler(MessageHandler(new_check, filters.command(['new_check']) & filters.private))
    dk.add_handler(MessageHandler(process_msg, filters.text & filters.private))
    dk.add_handler(CallbackQueryHandler(process_callback))

    return logger.info('Registered handlers')


# def manager():
#     scheduler = session.scheduler
#     scheduler.add_job(func, 'cron', [arg1], hour=4)
#     return logging.info('Scheduler started')
