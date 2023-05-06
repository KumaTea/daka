from dmFunctions import *
from groupFunctions import *
from pyrogram import filters
from session import dk, logger
from dmMessages import process_dm_msg
from processCallback import process_callback
from pyrogram.handlers import MessageHandler, CallbackQueryHandler


def register_handlers():
    dk.add_handler(MessageHandler(dm_start, filters.command(['start']) & filters.private))
    dk.add_handler(MessageHandler(dm_help, filters.command(['help']) & filters.private))
    dk.add_handler(MessageHandler(dm_cancel, filters.command(['cancel']) & filters.private))
    dk.add_handler(MessageHandler(dm_new_check, filters.command(['new_check']) & filters.private))
    dk.add_handler(MessageHandler(dm_unavailable, filters.command(['edit_check']) & filters.private))
    dk.add_handler(MessageHandler(dm_unavailable, filters.command(['del_check']) & filters.private))
    dk.add_handler(MessageHandler(dm_unavailable, filters.command(['my_checks']) & filters.private))
    dk.add_handler(MessageHandler(admin_restart, filters.command(['restart']) & filters.private))
    dk.add_handler(MessageHandler(process_dm_msg, filters.text & filters.private))

    dk.add_handler(MessageHandler(group_check, filters.command(['check']) & filters.group))
    dk.add_handler(MessageHandler(group_unavailable, filters.command(['my_stats']) & filters.group))

    dk.add_handler(CallbackQueryHandler(process_callback))

    return logger.info('Registered handlers')


# def manager():
#     scheduler = session.scheduler
#     scheduler.add_job(func, 'cron', [arg1], hour=4)
#     return logging.info('Scheduler started')
