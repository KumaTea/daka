import checkManager
import userStatus
from newCheck import new_check, cancel_new_check


async def cancel(client, message):
    user_id = message.from_user.id
    if user_id not in userStatus.user_statuses:
        return await message.reply_text('您目前没有正在进行的操作。')
    user_status = userStatus.user_statuses[user_id]
    if user_status['task'] == 'newCk':
        return await cancel_new_check(client, user_id)
