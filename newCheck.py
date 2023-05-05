# create tasks by asking user with text input and inline keyboard

import checkManager
import userStatus
from datetime import datetime
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_name_max_len = 16
max_checks_per_user = 10
replies = {
    'start': '开始创建新的打卡任务！中途退出，请发送 `/cancel`',
    'step_1': '第一步：请输入打卡任务的名称，{}字以内。'.format(check_name_max_len),
    'step_2': '第二步：请选择打卡时是否需要回复一条消息 (如打卡截图、学习小结等) 以验证。',
    'step_3': '第三步：请选择打卡提醒时间。',
    'step_3_m': '请输入打卡提醒时间，格式为 HH:MM，如 21:00。\n如果不需要提醒，请发送「无」。',
    'step_4': '第四步：请选择打卡截止时间。',
    'step_4_m': '请输入打卡截止时间，格式为 HH:MM，如 00:00。',
    'step_5': '第五步：请选择打卡日期。',
    'step_5_m': '请输入打卡日期，格式示例 1111100。\n其中 1 代表当天需要打卡，0 代表当天不需要打卡。\n从周一开始，周日为最后一天。',
    'step_6': '第六步：请选择结束打卡日期。',
    'step_6_m': '请输入结束打卡日期，格式为 YYYYMMDD，如 20231231。\n如果不需要结束日期，请发送「无」。',
    'step_7': '第七步：请确认打卡任务信息。',
    'malformed_time': '时间格式错误，请重新输入，格式为HH:MM，如 21:00。',
    'malformed_days': '启用日格式错误，请重新输入，格式示例 1111100。',
    'malformed_date': '日期格式错误，请重新输入，格式为 YYYYMMDD，如 20231231。',
    'max_checks': '您的打卡已达上限，请使用 /del_check 删除后再创建。',
    'error': '程序错误！已重置状态。'
}


def gen_check_info():
    info = checkManager.Check()
    return info


async def create_check_message_handler(client, message):
    user_id = message.from_user.id
    user_status = userStatus.user_statuses[user_id]
    # if not user_status['task'] == 'newCk':
    #     await client.send_message(user_id, replies['error'])
    #     del userStatus.user_statuses[user_id]
    #     return False
    if user_status['step'] == 1:
        return await step_1_set_name_of_check(client, message)
    elif user_status['step'] == 3:
        if userStatus.user_statuses[user_id]['done']:
            return await step_4_1_inform_set_deadline(client, user_id)
        else:
            return await step_3_3_set_custom_remind(client, message)
    elif user_status['step'] == 4:
        if userStatus.user_statuses[user_id]['done']:
            return await step_5_1_inform_set_enabled(client, user_id)
        else:
            return await step_4_3_set_custom_deadline(client, message)
    elif user_status['step'] == 5:
        if userStatus.user_statuses[user_id]['done']:
            return await step_6_1_inform_set_until(client, user_id)
        else:
            return await step_5_3_set_custom_enabled(client, message)
    elif user_status['step'] == 6:
        if userStatus.user_statuses[user_id]['done']:
            return await step_7_1_inform_confirm(client, user_id)
        else:
            return await step_6_3_set_custom_until(client, message)


async def create_check_callback_handler(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    step = int(step)
    if user_id not in userStatus.user_statuses:
        return await client.answer_callback_query(callback_query.id, '不要乱点无关的按钮 😡')
    if step == 2:
        await step_2_2_set_verify(client, callback_query)
        return await step_3_1_inform_set_remind(client, user_id)
    elif step == 3:
        await step_3_2_select_remind(client, callback_query)
        if userStatus.user_statuses[user_id]['done']:
            return await step_4_1_inform_set_deadline(client, user_id)
    elif step == 4:
        await step_4_2_select_deadline(client, callback_query)
        if userStatus.user_statuses[user_id]['done']:
            return await step_5_1_inform_set_enabled(client, user_id)
    elif step == 5:
        await step_5_2_select_enabled(client, callback_query)
        if userStatus.user_statuses[user_id]['done']:
            return await step_6_1_inform_set_until(client, user_id)
    elif step == 6:
        await step_6_2_select_until(client, callback_query)
        if userStatus.user_statuses[user_id]['done']:
            return await step_7_1_inform_confirm(client, user_id)
    elif step == 7:
        return await step_7_2_select_confirm(client, callback_query)


# /new_check
async def new_check(client, message):
    user_id = message.from_user.id
    user_current_checks = checkManager.check_store.get_checks_by_user(user_id)
    if len(user_current_checks) >= max_checks_per_user:
        return await client.send_message(user_id, replies['max_checks'])
    await client.send_message(user_id, replies['start'], parse_mode=ParseMode.MARKDOWN)

    user_status = userStatus.gen_status()
    user_status['task'] = 'newCk'
    user_status['step'] = 1
    user_status['done'] = False
    userStatus.user_statuses[user_id] = user_status

    check_info = gen_check_info()
    checkManager.temp_checks[user_id] = check_info

    await client.send_message(user_id, replies['step_1'])
    return True


async def step_1_set_name_of_check(client, message):
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
    userStatus.user_statuses[user_id]['done'] = True
    return await step_2_1_inform_set_verify(client, message)


async def step_2_1_inform_set_verify(client, message):
    user_id = message.from_user.id
    userStatus.user_statuses[user_id]['step'] = 2
    userStatus.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('是', callback_data='newCk_2_y')],
        [InlineKeyboardButton('否', callback_data='newCk_2_n')],
    ])
    return await client.send_message(user_id, replies['step_2'], reply_markup=reply_markup)


async def step_2_2_set_verify(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'n':
        checkManager.temp_checks[user_id].verify = False
    # default is True
    userStatus.user_statuses[user_id]['done'] = True
    return await client.answer_callback_query(callback_query.id, '验证：{}'.format('是' if value == 'y' else '否'))


async def step_3_1_inform_set_remind(client, user_id):
    userStatus.user_statuses[user_id]['step'] = 3
    userStatus.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('默认 21:00', callback_data='newCk_3_def')],
        [InlineKeyboardButton('自定义', callback_data='newCk_3_cus')],
    ])
    return await client.send_message(user_id, replies['step_3'], reply_markup=reply_markup)


async def step_3_2_select_remind(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'cus':
        await client.answer_callback_query(callback_query.id, '请设置提醒时间')
        return await client.send_message(user_id, replies['step_3_m'])
    else:  # default
        userStatus.user_statuses[user_id]['done'] = True
        return await client.answer_callback_query(callback_query.id, '提醒时间设为默认')


def is_valid_time(text):
    return len(text) == 5 and text[2] == ':' and text[:2].isdigit() and text[3:].isdigit()


async def step_3_3_set_custom_remind(client, message):
    user_id = message.from_user.id
    text = message.text
    text = text.replace('：', ':')

    if is_valid_time(text):
        checkManager.temp_checks[user_id].remind = text
        userStatus.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'提醒时间：{text}')
        return await step_4_1_inform_set_deadline(client, user_id)
    elif text == '无':
        checkManager.temp_checks[user_id].remind = None
        userStatus.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'提醒时间：{text}')
        return await step_4_1_inform_set_deadline(client, user_id)
    else:
        return await client.send_message(user_id, replies['malformed_time'])


async def step_4_1_inform_set_deadline(client, user_id):
    userStatus.user_statuses[user_id]['step'] = 4
    userStatus.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('默认 00:00', callback_data='newCk_4_def')],
        [InlineKeyboardButton('自定义', callback_data='newCk_4_cus')],
    ])
    return await client.send_message(user_id, replies['step_4'], reply_markup=reply_markup)


async def step_4_2_select_deadline(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'cus':
        await client.answer_callback_query(callback_query.id, '请设置截止时间')
        return await client.send_message(user_id, replies['step_4_m'])
    else:  # default
        userStatus.user_statuses[user_id]['done'] = True
        return await client.answer_callback_query(callback_query.id, '截止时间设为默认')


async def step_4_3_set_custom_deadline(client, message):
    user_id = message.from_user.id
    text = message.text
    text = text.replace('：', ':')

    if is_valid_time(text):
        if checkManager.temp_checks[user_id].remind and text != '00:00':
            remind_time = datetime.strptime(checkManager.temp_checks[user_id].remind, '%H:%M')
            deadline_time = datetime.strptime(text, '%H:%M')
            if not remind_time < deadline_time:
                return await client.send_message(user_id, '截止时间应晚于提醒时间')
        checkManager.temp_checks[user_id].deadline = text
        userStatus.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'提醒时间：{text}')
        return await step_5_1_inform_set_enabled(client, user_id)
    elif text == '无':
        return await client.send_message(user_id, f'必须设置截止时间')
    else:
        return await client.send_message(user_id, replies['malformed_time'])


async def step_5_1_inform_set_enabled(client, user_id):
    userStatus.user_statuses[user_id]['step'] = 5
    userStatus.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('工作日', callback_data='newCk_5_1111100')],
        [InlineKeyboardButton('周末', callback_data='newCk_5_0000011')],
        [InlineKeyboardButton('每天', callback_data='newCk_5_1111111')],
        [InlineKeyboardButton('自定义', callback_data='newCk_5_cus')],
    ])
    return await client.send_message(user_id, replies['step_5'], reply_markup=reply_markup)


def get_enabled_days(days: str):
    assert days.isdigit()
    enabled_days = []
    weekdays = ['一', '二', '三', '四', '五', '六', '日']
    for i, day in enumerate(days):
        if day == '1':
            enabled_days.append(weekdays[i])
    return '、'.join(enabled_days)


async def step_5_2_select_enabled(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'cus':
        await client.answer_callback_query(callback_query.id, '请设置打卡日期')
        return await client.send_message(user_id, replies['step_5_m'])
    else:  # value.isdigit():
        checkManager.temp_checks[user_id].enabled = value
        userStatus.user_statuses[user_id]['done'] = True
        enabled_days = get_enabled_days(value)
        return await client.answer_callback_query(callback_query.id, '打卡日：{}'.format(enabled_days))


async def step_5_3_set_custom_enabled(client, message):
    user_id = message.from_user.id
    text = message.text

    if len(text) == 7 and text.isdigit():
        if text == '0' * 7:
            return await client.send_message(user_id, '请至少选择一天')
        elif text.replace('0', '').replace('1', ''):  # digits other than 0 and 1
            return await client.send_message(user_id, '请使用 0 和 1 代表不打卡和打卡')
        else:
            checkManager.temp_checks[user_id].enabled = text
            userStatus.user_statuses[user_id]['done'] = True
            enabled_days = get_enabled_days(text)
            await client.send_message(user_id, f'打卡日：{enabled_days}')
            return await step_6_1_inform_set_until(client, user_id)
    else:
        return await client.send_message(user_id, replies['malformed_days'])


async def step_6_1_inform_set_until(client, user_id):
    userStatus.user_statuses[user_id]['step'] = 6
    userStatus.user_statuses[user_id]['done'] = False
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('无结束日期', callback_data='newCk_6_inf')],
        [InlineKeyboardButton('自定义', callback_data='newCk_6_cus')],
    ])
    return await client.send_message(user_id, replies['step_6'], reply_markup=reply_markup)


async def step_6_2_select_until(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == 'cus':
        await client.answer_callback_query(callback_query.id, '请设置结束日期')
        return await client.send_message(user_id, replies['step_6_m'])
    else:  # default
        userStatus.user_statuses[user_id]['done'] = True
        return await client.answer_callback_query(callback_query.id, '该打卡无结束日期')


async def step_6_3_set_custom_until(client, message):
    user_id = message.from_user.id
    text = message.text

    if len(text) == 8 and text.isdigit():
        # check if date is valid
        try:
            until_date = datetime.strptime(text, '%Y%m%d')
        except ValueError:
            return await client.send_message(user_id, replies['malformed_date'])
        today = datetime.today()
        if until_date < today:
            return await client.send_message(user_id, '结束日期必须晚于今天')
        checkManager.temp_checks[user_id].until = text
        userStatus.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'结束日期：{text}')
        return await step_7_1_inform_confirm(client, user_id)
    elif text == '无':
        checkManager.temp_checks[user_id].until = None
        userStatus.user_statuses[user_id]['done'] = True
        await client.send_message(user_id, f'该打卡无结束日期')
        return await step_7_1_inform_confirm(client, user_id)
    else:
        return await client.send_message(user_id, replies['malformed_date'])


async def step_7_1_inform_confirm(client, user_id):
    userStatus.user_statuses[user_id]['step'] = 7
    userStatus.user_statuses[user_id]['done'] = False

    check_info = '打卡信息\n\n'
    check_info += f'打卡名称：{checkManager.temp_checks[user_id].name}\n'
    check_info += f'需要验证：{"是" if checkManager.temp_checks[user_id].verify else "否"}\n'
    check_info += f'提醒时间：{checkManager.temp_checks[user_id].remind}\n'
    check_info += f'截止时间：{checkManager.temp_checks[user_id].deadline}\n'
    check_info += f'打卡日期：{get_enabled_days(checkManager.temp_checks[user_id].enabled)}\n'
    check_info += f'结束日期：{checkManager.temp_checks[user_id].until if checkManager.temp_checks[user_id].until else "无"}\n'
    await client.send_message(user_id, check_info)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('确认', callback_data='newCk_7_1')],
        [InlineKeyboardButton('取消', callback_data='newCk_7_0')],
    ])
    return await client.send_message(user_id, replies['step_7'], reply_markup=reply_markup)


def write_check(user_id, check):
    check.since = datetime.today().strftime('%Y%m%d')
    checkManager.check_store.add_check(check.id, check)
    checkManager.temp_checks.pop(user_id)
    userStatus.user_statuses.pop(user_id)
    return True


async def step_7_2_select_confirm(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    task_name, step, value = callback_data.split('_')
    if value == '1':
        write_check(user_id, checkManager.temp_checks[user_id])
        await client.answer_callback_query(callback_query.id, '打卡创建成功')
        return await client.send_message(user_id, '打卡创建成功')
    else:  # value == '0'
        await client.answer_callback_query(callback_query.id, '打卡创建已取消')
        return await cancel_new_check(client, user_id)


async def cancel_new_check(client, user_id):
    checkManager.temp_checks.pop(user_id)
    userStatus.user_statuses.pop(user_id)
    return await client.send_message(user_id, '打卡创建已取消')
