import json
import settings
import checkManager
from tgTools import *
from session import logger
from textCollection import *
from pyrogram.enums import ParseMode
from checkAuth import check_dm_auth_decorator
from dmNewCheck import new_check_command, cancel_new_check
from dmDelCheck import del_check_command, cancel_del_check


async def dm_start(client, message):
    command = message.text
    if command.find(' ') != -1:
        parameter = command.split(' ')[1]
        if parameter in settings.start_commands:
            return await message.reply_text(DM_START_PARA.format(command=parameter))
    return await message.reply_text(DM_START)


async def dm_help(client, message):
    return await message.reply_text(DM_HELP)


async def dm_cancel(client, message):
    user_id = message.from_user.id
    if user_id not in checkManager.user_statuses:
        return await message.reply_text(NO_OPERATION)
    user_status = checkManager.user_statuses[user_id]
    if user_status['task'] == 'newCk':
        return await cancel_new_check(client, user_id)
    elif user_status['task'] == 'delCk':
        return await cancel_del_check(client, user_id)


@check_dm_auth_decorator
async def dm_new_check(client, message):
    return await new_check_command(client, message)


@check_dm_auth_decorator
async def dm_del_check(client, message):
    return await del_check_command(client, message)


async def dm_unavailable(client, message):
    return await message.reply_text(CMD_NOT_AVAILABLE)


async def admin_restart(client, message):
    user = message.from_user
    if user.id in settings.administrators:
        await message.reply('Updating...')
        import subprocess
        git_command = 'dbclient -y -i {host_key} -p {host_port} {host_user}@{host_ip} git -C {bot_dir} pull'.format(
            host_key=settings.host_key,
            host_port=settings.host_port,
            host_user=settings.host_user,
            host_ip=settings.host_ip,
            bot_dir=settings.bot_dir
        )
        git_pull = subprocess.run(git_command.split(), capture_output=True)
        last_line = git_pull.stdout.decode('utf-8').split('\n')[-2].strip()
        logger.info('[Bot]\tGit pull: {}'.format(last_line))
        await message.reply('Restarting...')
        logger.info('[Bot]\tRestart requested by: {} {} ({})'.format(user.first_name, user.last_name or "", user.id))
        checkManager.check_store.write_to_pickle()
        checkManager.check_status_store.write_to_pickle()
        import sys
        return sys.exit(0)
    else:
        return None


async def admin_debug(client, message):
    user = message.from_user
    if user.id in settings.administrators:
        if message.reply_to_message:
            message = message.reply_to_message
        debug_message = json.loads(str(message))
        debug_message = trim_key(trimmer(debug_message))
        return await message.reply(f'`{debug_message}`', parse_mode=ParseMode.MARKDOWN)
    else:
        return None
