import info
import asyncio
import checkManager
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


CALLBACK_TASK = 'CK'
NO_CHECKS = '您目前暂未添加打卡任务，请私聊我使用 /new_check 命令添加。'
NO_VERIFY = '您的打卡任务 **{}** 需要回复一条验证消息！请重试。'
SUCCESS = '任务 **{}** 打卡成功！\n当前连续打卡 {} 天。'
ALREADY = '您今天已经打卡过 **{}** 了。'
CHOOSE_CHECK = '请选择您要打卡的任务：'
NOT_IN_TASK = '不要乱点无关的按钮 😡'


async def check_and_respond(client, message, check, callback_query=None):
    check_id = check.id
    if check.verify and not message.reply_to_message:
        return await message.reply_text(NO_VERIFY.format(check.name), parse_mode=ParseMode.MARKDOWN, quote=False)
    result_str, result_bool = checkManager.check_in(check_id)
    if result_bool:  # True
        check_status = checkManager.check_status_store.get_check_status(check_id)
        check_name = check.name
        streak = check_status.streak
        success_message = SUCCESS.format(check_name, streak)
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
    # if not group_authorized(chat_id):
    #     await message.reply_text('本群不在授权列表中！再见！')
    #     return await client.leave_chat(chat_id)
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
        user_status = checkManager.gen_status()
        user_status['task'] = CALLBACK_TASK
        user_status['step'] = 1
        user_status['done'] = False
        checkManager.user_statuses[user_id] = user_status

        keyboard = []
        group_index = info.auth_groups.index(chat_id)
        for check in user_checks:
            check_name = check.name
            callback_data = f'{CALLBACK_TASK}_{check.id}_{group_index}_{message_id}'
            keyboard.append([InlineKeyboardButton(check_name, callback_data=callback_data)])
        reply_markup = InlineKeyboardMarkup(keyboard)
        if group_index not in checkManager.temp_messages:
            checkManager.temp_messages[group_index] = {}
        checkManager.temp_messages[group_index][message_id] = message
        return await message.reply_text(CHOOSE_CHECK, reply_markup=reply_markup)


async def step_2_2_get_cb_check(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    check_id, group_index, message_id = map(int, callback_data.split('_')[1:])
    message = checkManager.temp_messages[group_index][message_id]
    check = checkManager.check_store.get_check(check_id)
    checkManager.user_statuses.pop(user_id)
    checkManager.temp_messages[group_index].pop(message_id)
    return await check_and_respond(client, message, check, callback_query)


async def group_check_callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in checkManager.user_statuses:
        return await client.answer_callback_query(callback_query.id, NOT_IN_TASK)
    # if checkManager.user_statuses[user_id]['task'] != CALLBACK_TASK:
    #     return await client.answer_callback_query(callback_query.id, NOT_IN_TASK)
    async_tasks = [
        client.answer_callback_query(callback_query.id, '正在处理……'),
        step_2_2_get_cb_check(client, callback_query)
    ]
    return await asyncio.gather(*async_tasks)
