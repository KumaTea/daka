from groupCheck import group_check_callback_handler


async def process_group_callback(client, callback_query):
    callback_data = callback_query.data
    task_name = callback_data.split('_')[0]
    if task_name == 'CK':
        return await group_check_callback_handler(client, callback_query)
