import checkManager
from newCheck import new_check_command, cancel_new_check


START = '您好，欢迎使用打卡警察！\n使用 /help 查看帮助。'
HELP = '目前上线功能：\n' \
       '/new_check - 新建打卡\n' \
       '您需要是 @DaKaClub 的成员才能使用本 bot.'


async def dm_start(client, message):
    return await message.reply_text(START)


async def dm_help(client, message):
    return await message.reply_text(HELP)


async def dm_cancel(client, message):
    user_id = message.from_user.id
    if user_id not in checkManager.user_statuses:
        return await message.reply_text('您目前没有正在进行的操作。')
    user_status = checkManager.user_statuses[user_id]
    if user_status['task'] == 'newCk':
        return await cancel_new_check(client, user_id)
