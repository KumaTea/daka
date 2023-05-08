import asyncio
import checkManager
from textCollection import *
from tgTools import gen_checks_buttons
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

task_name = 'delCk'


# /del_check
async def del_check_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_checks = checkManager.check_store.get_checks_by_user(user_id)
    if not user_checks:
        return await client.send_message(chat_id, DEL_NO_CHECKS)

    checkManager.set_user_status(user_id, task_name, 1, False)
    reply_markup = gen_checks_buttons(user_checks, task_name)

    await client.send_message(chat_id, DEL_START, reply_markup=reply_markup)


async def step_2_get_cb_del_check(client, callback_query):
    step = 2
    callback_data = callback_query.data
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    checkManager.set_user_status(user_id, step=step)
    _, _, check_id = callback_data.split('_')
    check_id = int(check_id)
    check = checkManager.check_store.get_check(check_id)
    check_info = checkManager.print_check_info(check)
    await client.send_message(chat_id, check_info)

    checkManager.set_user_status(user_id, check=check, message=callback_query.message)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('是', callback_data=f'{task_name}_{step}_y'),
         InlineKeyboardButton('否', callback_data=f'{task_name}_{step}_n')]
    ])
    return await client.send_message(chat_id, DEL_CONFIRM.format(check_name=check.name), reply_markup=reply_markup)


async def step_3_get_cb_del_check_confirm(client, callback_query):
    callback_data = callback_query.data
    user_id = callback_query.from_user.id
    checkManager.set_user_status(user_id, step=3)
    check = checkManager.user_statuses[user_id]['check']
    check_name = check.name
    _, _, answer = callback_data.split('_')
    checkManager.user_statuses.pop(user_id)
    if answer == 'y':
        commit_del_check(check)
        return await callback_query.message.edit_text(DEL_SUCCESS.format(check_name=check_name))
    else:
        return await callback_query.message.edit_text(DEL_CANCEL)


def commit_del_check(check):
    checkManager.del_check(check.id)


async def cancel_del_check(client, user_id):
    if user_id in checkManager.user_statuses:
        checkManager.user_statuses.pop(user_id)
    return await client.send_message(user_id, DEL_CANCEL)


async def del_check_callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    callback_task_name, step, value = callback_data.split('_')
    step = int(step) + 1
    async_tasks = []
    if user_id not in checkManager.user_statuses:
        return await client.answer_callback_query(callback_query.id, NOT_IN_TASK)
    if step != checkManager.user_statuses[user_id]['step'] + 1:
        async_tasks.append(client.send_message(user_id, ERROR))
        async_tasks.append(cancel_del_check(client, user_id))
        async_tasks.append(client.answer_callback_query(callback_query.id, ERROR))
        return await asyncio.gather(*async_tasks)

    async_tasks.append(client.answer_callback_query(callback_query.id, PROCESSING))
    if step == 2:
        async_tasks.append(step_2_get_cb_del_check(client, callback_query))
    elif step == 3:
        async_tasks.append(step_3_get_cb_del_check_confirm(client, callback_query))
    return await asyncio.gather(*async_tasks)
