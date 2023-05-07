from dmNewCheck import new_check_callback_handler
from dmDelCheck import del_check_callback_handler
from groupCheck import group_check_callback_handler


async def process_dm_callback(client, callback_query):
    callback_data = callback_query.data
    task_name = callback_data.split('_')[0]
    if task_name == 'newCk':
        return await new_check_callback_handler(client, callback_query)
    elif task_name == 'delCk':
        return await del_check_callback_handler(client, callback_query)


async def process_group_callback(client, callback_query):
    callback_data = callback_query.data
    task_name = callback_data.split('_')[0]
    if task_name == 'CK':
        return await group_check_callback_handler(client, callback_query)


async def process_callback(client, callback_query):
    if callback_query.message.chat.id > 0:
        return await process_dm_callback(client, callback_query)
    else:
        return await process_group_callback(client, callback_query)
