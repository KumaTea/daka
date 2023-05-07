import settings
import asyncio
import checkManager
from textCollection import *
from tgTools import gen_checks_buttons
from pyrogram.enums.parse_mode import ParseMode

CALLBACK_TASK = 'CK'


async def check_and_respond(client, message, check, callback_query=None):
    check_id = check.id
    if check.verify and not message.reply_to_message:
        return await message.reply_text(NO_VERIFY.format(check.name), parse_mode=ParseMode.MARKDOWN, quote=False)
    result_str, result_bool = checkManager.check_in(check_id)
    if result_bool:  # True
        check_status = checkManager.check_status_store.get_check_status(check_id)
        check_name = check.name
        streak = check_status.streak
        success_message = SUCCESS.format(check_name) + '\n'
        if streak == 1:
            success_message += FIRST_TIME
        else:
            success_message += STREAK.format(streak)
        if callback_query:
            await callback_query.message.edit_text(success_message, parse_mode=ParseMode.MARKDOWN)
        else:
            return await message.reply_text(success_message, parse_mode=ParseMode.MARKDOWN, quote=False)
    elif result_bool is False:  # already checked in today
        already_message = ALREADY.format(check.name)
        if callback_query:
            await callback_query.message.edit_text(already_message, parse_mode=ParseMode.MARKDOWN)
        else:
            return await message.reply_text(already_message, parse_mode=ParseMode.MARKDOWN, quote=False)
    else:  # None
        raise FileNotFoundError(result_str)


# /check
async def check_command(client, message):
    chat_id = message.chat.id
    message_id = message.id
    user_id = message.from_user.id
    user_checks = checkManager.check_store.get_checks_by_user(user_id)
    if not user_checks:
        return await message.reply_text(NO_CHECKS)
    elif len(user_checks) == 1:
        # only one check, check in immediately
        return await check_and_respond(client, message, user_checks[0])
    else:
        # more than two checks, return inline keyboard buttons
        checkManager.set_status(user_id, CALLBACK_TASK, 1, False)
        reply_markup = gen_checks_buttons(user_checks, CALLBACK_TASK)
        group_index = settings.auth_groups.index(chat_id)
        checkManager.set_status(user_id, message=message)
        return await message.reply_text(CHOOSE_CHECK, reply_markup=reply_markup)


async def step_2_get_cb_check(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    _, _, check_id = callback_data.split('_')
    check_id = int(check_id)
    message = checkManager.user_statuses[user_id]['message']
    check = checkManager.check_store.get_check(check_id)
    if user_id != check.user:
        return await client.answer_callback_query(callback_query.id, NOT_IN_TASK)
    checkManager.user_statuses.pop(user_id)
    return await check_and_respond(client, message, check, callback_query)


async def group_check_callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in checkManager.user_statuses:
        return await client.answer_callback_query(callback_query.id, NOT_IN_TASK)
    async_tasks = [
        client.answer_callback_query(callback_query.id, PROCESSING),
        step_2_get_cb_check(client, callback_query)
    ]
    return await asyncio.gather(*async_tasks)
