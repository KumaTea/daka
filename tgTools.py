from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def trimmer(data):
    if type(data) is dict:
        new_data = {}
        for key in data:
            if data[key]:
                new_data[key] = trimmer(data[key])
        return new_data
    elif type(data) is list:
        new_data = []
        for index in range(len(data)):
            if data[index]:
                new_data.append(trimmer(data[index]))
        return new_data
    else:
        return data


def trim_key(data, char='_'):
    trim_list = []
    for i in data:
        if i.startswith(char):
            trim_list.append(i)
    for i in trim_list:
        data.pop(i)
    return data


def gen_checks_buttons(checks, task_name, step=1):
    """
    callback data: taskName_step_checkId
    """
    keyboard = []
    # two buttons each row
    row = []
    for check in checks:
        check_name = check.name
        callback_data = f'{task_name}_{step}_{check.id}'
        if len(row) == 2:
            keyboard.append(row)
            row = []
        row.append(InlineKeyboardButton(check_name, callback_data=callback_data))
    if row:
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
