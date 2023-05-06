# create tasks by asking user with text input and inline keyboard

import asyncio
import checkManager
from textCollection import *
from datetime import datetime
from checkAuth import dm_user_in_group
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def new_check_message_handler(client, message):
    user_id = message.from_user.id
    user_status = checkManager.user_statuses[user_id]
    # if not user_status['task'] == 'newCk':
    #     await client.send_message(user_id, ERROR)
    #     del checkManager.user_statuses[user_id]
    #     return False
    if user_status['step'] == 1:
        return await step_1_get_msg_name(client, message)
    elif user_status['step'] == 3:
        if checkManager.user_statuses[user_id]['done']:
            return await step_4_1_send_btn_set_deadline(client, user_id)
        else:
            return await step_3_3_get_msg_remind_custom(client, message)
    elif user_status['step'] == 4:
        if checkManager.user_statuses[user_id]['done']:
            return await step_5_1_send_btn_set_enabled(client, user_id)
        else:
            return await step_4_3_get_msg_deadline_custom(client, message)
    elif user_status['step'] == 5:
        if checkManager.user_statuses[user_id]['done']:
            return await step_6_1_send_btn_until(client, user_id)
        else:
            return await step_5_3_get_msg_enabled_custom(client, message)
    elif user_status['step'] == 6:
        if checkManager.user_statuses[user_id]['done']:
            return await step_7_1_send_btn_confirm(client, user_id)
        else:
            return await step_6_3_get_msg_until_custom(client, message)


async def new_check_callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    step = int(step)
    if user_id not in checkManager.user_statuses:
        return await client.answer_callback_query(callback_query.id, NOT_IN_TASK)
    if step != checkManager.user_statuses[user_id]['step']:
        async_tasks = [
            client.send_message(user_id, ERROR),
            cancel_new_check(client, user_id),
            client.answer_callback_query(callback_query.id, ERROR)
        ]
        return await asyncio.gather(*async_tasks)
    if step == 2:
        await step_2_2_get_cb_verify(client, callback_query)
        return await step_3_1_send_btn_remind(client, user_id)
    elif step == 3:
        await step_3_2_get_cb_remind(client, callback_query)
        if checkManager.user_statuses[user_id]['done']:
            return await step_4_1_send_btn_set_deadline(client, user_id)
    elif step == 4:
        await step_4_2_get_cb_deadline(client, callback_query)
        if checkManager.user_statuses[user_id]['done']:
            return await step_5_1_send_btn_set_enabled(client, user_id)
    elif step == 5:
        await step_5_2_get_cb_enabled(client, callback_query)
        if checkManager.user_statuses[user_id]['done']:
            return await step_6_1_send_btn_until(client, user_id)
    elif step == 6:
        await step_6_2_get_cb_until(client, callback_query)
        if checkManager.user_statuses[user_id]['done']:
            return await step_7_1_send_btn_confirm(client, user_id)
    elif step == 7:
        return await step_7_2_get_cb_confirm(client, callback_query)


# /new_check
async def new_check_command(client, message):
    user_id = message.from_user.id
    user_current_checks = checkManager.check_store.get_checks_by_user(user_id)
    if len(user_current_checks) >= max_checks_per_user:
        return await client.send_message(user_id, MAX_CHECKS)
    await client.send_message(user_id, NEW_START, parse_mode=ParseMode.MARKDOWN)

    user_status = checkManager.gen_status()
    user_status['task'] = 'newCk'
    user_status['step'] = 1
    user_status['done'] = False
    checkManager.user_statuses[user_id] = user_status

    check_info = checkManager.gen_check_info()
    checkManager.temp_checks[user_id] = check_info

    await client.send_message(user_id, NEW_STEP_1)
    return True


async def step_1_get_msg_name(client, message):
    user_id = message.from_user.id
    check_name = message.text[:check_name_max_len]
    user_checks = checkManager.check_store.get_checks_by_user(user_id)
    for check in user_checks:
        if check.name == check_name:
            return await client.send_message(user_id, f'打卡名称 {check_name} 重复，请重新输入。')
    checkManager.temp_checks[user_id].name = check_name
    if checkManager.check_store.checks:
        last_key = list(checkManager.check_store.checks.keys())[-1]
        check_id = last_key + 1
    else:
        check_id = 1
    checkManager.temp_checks[user_id].id = check_id
    checkManager.temp_checks[user_id].user = user_id

    await client.send_message(user_id, f'打卡名称：{check_name}')
    checkManager.user_statuses[user_id]['done'] = True
    return await step_2_1_send_btn_verify(client, message)


async def step_2_1_send_btn_verify(client, message):
    user_id = message.from_user.id
    checkManager.user_statuses[user_id]['step'] = 2
    checkManager.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('是', callback_data='newCk_2_y')],
        [InlineKeyboardButton('否', callback_data='newCk_2_n')],
    ])
    return await client.send_message(user_id, NEW_STEP_2, reply_markup=reply_markup)


async def step_2_2_get_cb_verify(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'n':
        checkManager.temp_checks[user_id].verify = False
    # default is True
    checkManager.user_statuses[user_id]['done'] = True
    return await client.answer_callback_query(callback_query.id, '验证：{}'.format('是' if value == 'y' else '否'))


async def step_3_1_send_btn_remind(client, user_id):
    checkManager.user_statuses[user_id]['step'] = 3
    checkManager.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('默认 21:00', callback_data='newCk_3_def')],
        [InlineKeyboardButton('自定义', callback_data='newCk_3_cus')],
    ])
    return await client.send_message(user_id, NEW_STEP_3, reply_markup=reply_markup)


async def step_3_2_get_cb_remind(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'cus':
        async_tasks = [
            client.answer_callback_query(callback_query.id, '请设置提醒时间'),
            client.send_message(user_id, NEW_STEP_3_M)
        ]
        return await asyncio.gather(*async_tasks)
    else:  # default
        checkManager.user_statuses[user_id]['done'] = True
        return await client.answer_callback_query(callback_query.id, '提醒时间设为默认')


def is_valid_time(text):
    if len(text) == 5 and text[2] == ':' and text[:2].isdigit() and text[3:].isdigit():
        try:
            datetime.strptime(text, '%H:%M')
            return True
        except ValueError:
            return False
    else:
        return False


async def step_3_3_get_msg_remind_custom(client, message):
    user_id = message.from_user.id
    text = message.text
    text = text.replace('：', ':')

    if is_valid_time(text):
        checkManager.temp_checks[user_id].remind = text
        checkManager.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'提醒时间：{text}')
        return await step_4_1_send_btn_set_deadline(client, user_id)
    elif text == '无':
        checkManager.temp_checks[user_id].remind = None
        checkManager.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'提醒时间：{text}')
        return await step_4_1_send_btn_set_deadline(client, user_id)
    else:
        return await client.send_message(user_id, MALFORMED_TIME)


async def step_4_1_send_btn_set_deadline(client, user_id):
    checkManager.user_statuses[user_id]['step'] = 4
    checkManager.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('默认 00:00', callback_data='newCk_4_def')],
        [InlineKeyboardButton('自定义', callback_data='newCk_4_cus')],
    ])
    return await client.send_message(user_id, NEW_STEP_4, reply_markup=reply_markup)


async def step_4_2_get_cb_deadline(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'cus':
        async_tasks = [
            client.answer_callback_query(callback_query.id, '请设置截止时间'),
            client.send_message(user_id, NEW_STEP_4_M)
        ]
        return await asyncio.gather(*async_tasks)
    else:  # default
        checkManager.user_statuses[user_id]['done'] = True
        return await client.answer_callback_query(callback_query.id, '截止时间设为默认')


async def step_4_3_get_msg_deadline_custom(client, message):
    user_id = message.from_user.id
    text = message.text
    text = text.replace('：', ':')

    if is_valid_time(text):
        if checkManager.temp_checks[user_id].remind and text != '00:00':
            remind_time = datetime.strptime(checkManager.temp_checks[user_id].remind, '%H:%M')
            deadline_time = datetime.strptime(text, '%H:%M')
            if remind_time == deadline_time:
                return await client.send_message(user_id, '提醒时间和截止时间不能相同！请重新设置')
            elif remind_time > deadline_time:
                await client.send_message(user_id, '截止时间为第二天！如果不是你想要的，请使用 /cancel 取消。')
        checkManager.temp_checks[user_id].deadline = text
        checkManager.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'提醒时间：{text}')
        return await step_5_1_send_btn_set_enabled(client, user_id)
    elif text == '无':
        return await client.send_message(user_id, f'必须设置截止时间！请重新设置')
    else:
        return await client.send_message(user_id, MALFORMED_TIME)


async def step_5_1_send_btn_set_enabled(client, user_id):
    checkManager.user_statuses[user_id]['step'] = 5
    checkManager.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('工作日', callback_data='newCk_5_1111100')],
        [InlineKeyboardButton('周末', callback_data='newCk_5_0000011')],
        [InlineKeyboardButton('每天', callback_data='newCk_5_1111111')],
        [InlineKeyboardButton('自定义', callback_data='newCk_5_cus')],
    ])
    return await client.send_message(user_id, NEW_STEP_5, reply_markup=reply_markup)


def get_enabled_days(days: str):
    assert days.isdigit()
    enabled_days = []
    weekdays = ['一', '二', '三', '四', '五', '六', '日']
    for i, day in enumerate(days):
        if day == '1':
            enabled_days.append(weekdays[i])
    return '、'.join(enabled_days)


async def step_5_2_get_cb_enabled(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'cus':
        async_tasks = [
            client.answer_callback_query(callback_query.id, '请设置打卡日期'),
            client.send_message(user_id, NEW_STEP_5_M)
        ]
        return await asyncio.gather(*async_tasks)
    else:  # value.isdigit():
        checkManager.temp_checks[user_id].enabled = value
        checkManager.user_statuses[user_id]['done'] = True
        enabled_days = get_enabled_days(value)
        return await client.answer_callback_query(callback_query.id, '打卡日：{}'.format(enabled_days))


async def step_5_3_get_msg_enabled_custom(client, message):
    user_id = message.from_user.id
    text = message.text

    if len(text) == 7 and text.isdigit():
        if text == '0' * 7:
            return await client.send_message(user_id, '请至少选择一天')
        elif text.replace('0', '').replace('1', ''):  # digits other than 0 and 1
            return await client.send_message(user_id, '请使用 0 和 1 代表不打卡和打卡')
        else:
            checkManager.temp_checks[user_id].enabled = text
            checkManager.user_statuses[user_id]['done'] = True
            enabled_days = get_enabled_days(text)
            await client.send_message(user_id, f'打卡日：{enabled_days}')
            return await step_6_1_send_btn_until(client, user_id)
    else:
        return await client.send_message(user_id, MALFORMED_DAYS)


async def step_6_1_send_btn_until(client, user_id):
    checkManager.user_statuses[user_id]['step'] = 6
    checkManager.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('无结束日期', callback_data='newCk_6_inf')],
        [InlineKeyboardButton('自定义', callback_data='newCk_6_cus')],
    ])
    return await client.send_message(user_id, NEW_STEP_6, reply_markup=reply_markup)


async def step_6_2_get_cb_until(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'cus':
        async_tasks = [
            client.answer_callback_query(callback_query.id, '请设置结束日期'),
            client.send_message(user_id, NEW_STEP_6_M)
        ]
        return await asyncio.gather(*async_tasks)
    else:  # default
        checkManager.user_statuses[user_id]['done'] = True
        return await client.answer_callback_query(callback_query.id, '该打卡无结束日期')


async def step_6_3_get_msg_until_custom(client, message):
    user_id = message.from_user.id
    text = message.text

    if len(text) == 8 and text.isdigit():
        # check if date is valid
        try:
            until_date = datetime.strptime(text, '%Y%m%d')
        except ValueError:
            return await client.send_message(user_id, MALFORMED_DATE)
        today = datetime.today()
        if until_date < today:
            return await client.send_message(user_id, '结束日期必须晚于今天')
        checkManager.temp_checks[user_id].until = text
        checkManager.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'结束日期：{text}')
        return await step_7_1_send_btn_confirm(client, user_id)
    elif text == '无':
        checkManager.temp_checks[user_id].until = None
        checkManager.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'该打卡无结束日期')
        return await step_7_1_send_btn_confirm(client, user_id)
    else:
        return await client.send_message(user_id, MALFORMED_DATE)


async def step_7_1_send_btn_confirm(client, user_id):
    checkManager.user_statuses[user_id]['step'] = 7
    checkManager.user_statuses[user_id]['done'] = False

    check_info = '**打卡信息**\n\n'
    check_info += f'打卡名称：{checkManager.temp_checks[user_id].name}\n'
    check_info += f'需要验证：{"是" if checkManager.temp_checks[user_id].verify else "否"}\n'
    check_info += f'提醒时间：{checkManager.temp_checks[user_id].remind}\n'
    check_info += f'截止时间：{checkManager.temp_checks[user_id].deadline}\n'
    check_info += f'打卡日期：{get_enabled_days(checkManager.temp_checks[user_id].enabled)}\n'
    check_info += f'结束日期：{checkManager.temp_checks[user_id].until or "无"}\n'
    await client.send_message(user_id, check_info, parse_mode=ParseMode.MARKDOWN)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('确认', callback_data='newCk_7_1')],
        [InlineKeyboardButton('取消', callback_data='newCk_7_0')],
    ])
    return await client.send_message(user_id, NEW_STEP_7, reply_markup=reply_markup)


def write_check(user_id, check):
    check.since = datetime.today().strftime('%Y%m%d')
    checkManager.add_new_check(check)
    checkManager.user_statuses.pop(user_id)
    return True


async def step_7_2_get_cb_confirm(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == '1':
        write_check(user_id, checkManager.temp_checks[user_id])
        async_tasks = [
            client.answer_callback_query(callback_query.id, '打卡创建成功'),
            client.send_message(user_id, '打卡创建成功')
        ]
        return await asyncio.gather(*async_tasks)
    else:  # value == '0'
        async_tasks = [
            client.answer_callback_query(callback_query.id, '打卡创建已取消'),
            cancel_new_check(client, user_id)
        ]
        return await asyncio.gather(*async_tasks)


async def cancel_new_check(client, user_id):
    checkManager.temp_checks.pop(user_id)
    checkManager.user_statuses.pop(user_id)
    return await client.send_message(user_id, '打卡创建已取消')
