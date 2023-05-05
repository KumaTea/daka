import checkManager
import userStatus
from datetime import datetime
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# info = {
#     'name': '',
#     'id': 0,
#     'user': 0,
#     'verify': True,
#     'remind': '21:00',
#     'deadline': '00:00',
#     'enabled': '1111100',  # enabled day of week, monday is 0
#     'until': None
# }

NO_CHECKS = '您目前暂未添加打卡任务，请私聊我使用 /new_check 命令添加。'
NO_VERIFY = '请回复您的打卡截图。'


# /check
async def check_command(client, message):
    user_id = message.from_user.id
    user_checks = checkManager.check_store.get_checks_by_user(user_id)
    reply_to_message_id = None
    if message.reply_to_message:
        reply_to_message_id = message.reply_to_message_id
    if not user_checks:
        return await message.reply_text(NO_CHECKS)
    elif len(user_checks) == 1:
        check_info = user_checks[0]
        if check_info.verify and not reply_to_message_id:
            return await message.reply_text(NO_VERIFY)



def check_in(check_id):
    pass


