import info
import checkManager
from session import dk, logger
from pyrogram.enums import ChatMemberStatus


def init_auth_users():
    group_id = info.auth_groups[0]
    with dk:
        for member in dk.get_chat_members(group_id):
            checkManager.auth_members.append(member.user.id)
    return logger.info(f'auth members count: {len(checkManager.auth_members)}')


async def dm_user_in_group(client, user_id, chat_id=info.auth_groups[0]):
    if user_id in checkManager.auth_members:
        return True
    try:
        member = await client.get_chat_member(chat_id, user_id)
        status = member.status
        return status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]
    except Exception as e:
        logger.error(f'error in user_in_group: {e}')
        return False


def check_group_auth_decorator(func):
    async def wrapper(client, message):
        chat_id = message.chat.id
        if chat_id not in info.auth_groups:
            await message.reply_text('本群不在授权列表中！再见！')
            return await client.leave_chat(message.chat.id)
        else:
            return await func(client, message)
    return wrapper
