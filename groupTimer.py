import asyncio
import settings
import checkMeta
import checkManager
from textCollection import *
from datetime import datetime
from session import dk, logger
from pyrogram.enums import ParseMode
from tgTools import get_user_mention_text


def get_unchecked_reminders():
    unchecked_reminders = []
    time_now = datetime.now()
    time_now_str = time_now.strftime('%H:%M')
    if time_now_str not in checkManager.check_timer.reminders:
        return []

    check_ids = checkManager.check_timer.reminders[time_now_str]
    for check_id in check_ids:
        to_remind = False
        check_status = checkManager.check_status_store.get_check_status(check_id)
        if check_status.check_history:
            last_check = check_status.check_history[-1]
            deadline_str = checkManager.check_store.get_check(check_id).deadline
            deadline_of_last_check = checkMeta.next_deadline(deadline_str, last_check)
            if time_now > deadline_of_last_check:
                to_remind = True
        else:
            to_remind = True
        if to_remind:
            unchecked_reminders.append(check_id)
    return unchecked_reminders


def get_unchecked_deadlines():
    unchecked_deadlines = []
    time_now = datetime.now()
    time_now_str = time_now.strftime('%H:%M')
    if time_now_str not in checkManager.check_timer.deadlines:
        return []

    check_ids = checkManager.check_timer.deadlines[time_now_str]
    for check_id in check_ids:
        # update_status
        check = checkManager.check_store.get_check(check_id)
        checkManager.check_status_store.set_check_stats(check)
        check_status = checkManager.check_status_store.get_check_status(check_id)
        if check_status.skipped:
            unchecked_deadlines.append(check_id)
    return unchecked_deadlines


async def send_notification():
    unchecked_reminders = get_unchecked_reminders()
    unchecked_deadlines = get_unchecked_deadlines()
    user_ids = []
    users = {}
    async_tasks = []
    for check_id in list(set(unchecked_reminders + unchecked_deadlines)):
        check = checkManager.check_store.get_check(check_id)
        user_id = check.user
        user_ids.append(user_id)
    user_ids = list(set(user_ids))
    # asynchronous get users
    for user_id in user_ids:
        async_tasks.append(dk.get_users(user_id))
    users_list = await asyncio.gather(*async_tasks)
    for user in users_list:
        users[user.id] = user

    async_tasks = []
    if unchecked_reminders:
        logger.info(f'[ckTmr]\tremind {len(unchecked_reminders)} checks')
        for check_id in unchecked_reminders:
            check = checkManager.check_store.get_check(check_id)
            user_mention = await get_user_mention_text(dk, user=users[check.user])
            message = REMINDER.format(check.name, check.remind, user_mention)
            async_tasks.append(dk.send_message(settings.auth_groups[0], message, parse_mode=ParseMode.MARKDOWN))
    await asyncio.gather(*async_tasks)

    async_tasks = []
    if unchecked_deadlines:
        logger.info(f'[ckTmr]\tdeadline {len(unchecked_deadlines)} checks')
        for check_id in unchecked_deadlines:
            check = checkManager.check_store.get_check(check_id)
            check_status = checkManager.check_status_store.get_check_status(check_id)
            skipped_count = check_status.skipped
            user_mention = await get_user_mention_text(dk, user=users[check.user])
            message = DEADLINE.format(check.name, skipped_count, user_mention)
            async_tasks.append(dk.send_message(settings.auth_groups[0], message, parse_mode=ParseMode.MARKDOWN))
    await asyncio.gather(*async_tasks)

    return True
