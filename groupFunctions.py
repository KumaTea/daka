from groupCheck import check_command
from checkAuth import check_group_auth_decorator


# /check
@check_group_auth_decorator
async def group_check(client, message):
    return await check_command(client, message)
