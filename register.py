from pyrogram import filters
from session import dk, logger
from dmMessages import process_dm_msg
from groupFunctions import group_check
from processCallback import process_callback
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from dmFunctions import dm_start, dm_help, dm_cancel, restart, new_check_command


def register_handlers():
    dk.add_handler(MessageHandler(dm_start, filters.command(['start']) & filters.private))
    dk.add_handler(MessageHandler(dm_help, filters.command(['help']) & filters.private))
    dk.add_handler(MessageHandler(dm_cancel, filters.command(['cancel']) & filters.private))
    dk.add_handler(MessageHandler(restart, filters.command(['restart']) & filters.private))
    dk.add_handler(MessageHandler(new_check_command, filters.command(['new_check']) & filters.private))
    dk.add_handler(MessageHandler(process_dm_msg, filters.text & filters.private))

    dk.add_handler(MessageHandler(group_check, filters.command(['check']) & filters.group))

    dk.add_handler(CallbackQueryHandler(process_callback))

    return logger.info('Registered handlers')


# def manager():
#     scheduler = session.scheduler
#     scheduler.add_job(func, 'cron', [arg1], hour=4)
#     return logging.info('Scheduler started')
