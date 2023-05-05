import userStatus
from newCheck import create_check_message_handler


async def process_msg(client, message):
    if message:
        user_id = message.from_user.id
        if message.text:
            if user_id in userStatus.user_statuses:
                user_status = userStatus.user_statuses[user_id]
                if user_status['task'] == 'newCk':
                    return await create_check_message_handler(client, message)
