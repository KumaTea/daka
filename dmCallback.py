from newCheck import new_check_callback_handler


async def process_dm_callback(client, callback_query):
    callback_data = callback_query.data
    task_name = callback_data.split('_')[0]
    if task_name == 'newCk':
        return await new_check_callback_handler(client, callback_query)
