import checkManager
from newCheck import new_check_message_handler


DEFAULT_REPLY = '您好，欢迎使用打卡警察！\n使用 /help 查看帮助。'


async def process_dm_msg(client, message):
    if message:
        user_id = message.from_user.id
        if message.text:
            if user_id in checkManager.user_statuses:
                user_status = checkManager.user_statuses[user_id]
                if user_status['task'] == 'newCk':
                    return await new_check_message_handler(client, message)
            else:
                return await message.reply_text(DEFAULT_REPLY)
