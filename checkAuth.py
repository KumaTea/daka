import settings
import checkManager
from textCollection import *
from session import dk, logger
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant


def init_auth_users():
    with dk:
        for member in dk.get_chat_members(settings.group_id):
            checkManager.auth_members.append(member.user.id)
    return logger.info(f'[Auth]\tauth members count: {len(checkManager.auth_members)}')


async def dm_user_in_group(client, user_id, chat_id=settings.group_id):
    if user_id in checkManager.auth_members:
        return True
    try:
        member = await client.get_chat_member(chat_id, user_id)
        status = member.status
        return status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]
    except UserNotParticipant:
        logger.error(f'[Auth]\tan user ({user_id}) was rejected in dm')
        return False


def check_group_auth_decorator(func):
    async def wrapper(client, message):
        chat_id = message.chat.id
        if chat_id not in settings.auth_groups:
            logger.error(f'[Auth]\tgroup ({chat_id}) not in auth list. Leaving...')
            await message.reply_text(GROUP_NOT_IN_AUTH_LIST)
            return await client.leave_chat(message.chat.id)
        else:
            return await func(client, message)

    return wrapper


def check_dm_auth_decorator(func):
    async def wrapper(client, message):
        user_id = message.from_user.id
        if await dm_user_in_group(client, user_id):
            return await func(client, message)
        else:
            return await message.reply_text(USER_NOT_IN_AUTH_GROUP)

    return wrapper
