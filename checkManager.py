import checkMeta
import checkStore
import checkTimer
import checkStatusStore
from session import logger
from checkMeta import Check
from datetime import datetime


check_store = checkStore.CheckStore()
logger.info(f'[ckMgr]\tchecks count: {len(check_store.checks)}')
check_status_store = checkStatusStore.CheckStatusStore()
check_status_store.init(check_store.checks)
logger.info(f'[ckMgr]\tcheck statuses count: {len(check_status_store.statuses)}')
check_timer = checkTimer.CheckTimer()
check_timer.init(check_store.checks)
logger.info(f'[ckMgr]\tcheck timer: reminders: {len(check_timer.reminders)}, deadlines: {len(check_timer.deadlines)}')
user_statuses = {}
auth_members = []


def gen_check_info():
    info = Check()
    return info


def gen_user_status():
    status = {
        'task': '',
        'step': 0,
        'done': False,
        'check': None,
        'message': None,
    }
    return status


def set_user_status(user_id: int, task=None, step=None, done=None, check=None, message=None):
    if user_id not in user_statuses:
        user_statuses[user_id] = gen_user_status()
    status = user_statuses[user_id]
    if not any([task, step, done, check, message]):
        return None
    for i in ['task', 'step', 'done', 'check', 'message']:
        if eval(i) is not None:
            status[i] = eval(i)


def add_new_check(check: Check):
    check_id = check.id
    user_id = check.user
    check_store.add_check(check_id, check)
    check_store.write_to_pickle()
    check_status_store.add_check(check)
    check_status_store.write_to_pickle()
    check_timer.add_check(check)
    return logger.info(f'[ckMgr]\tnew check (id={check_id}) added by user {user_id}')


def del_check(check_id: int):
    check = check_store.get_check(check_id)
    check_timer.del_check(check)
    check_store.del_check(check_id)
    check_store.write_to_pickle()
    check_status_store.del_check(check_id)
    check_status_store.write_to_pickle()
    return logger.info(f'[ckMgr]\tcheck (id={check_id}) deleted')


def check_in(check_id: int):
    check = check_store.get_check(check_id)
    if not check:
        logger.error(f'[ckMgr]\tcheck_id {check_id} not exists')
        return 'check_id not exists', None

    check_status = check_status_store.get_check_status(check_id)
    check_history = check_status.check_history
    if check_history:
        last_check = check_history[-1]  # datetime
        deadline_str = check.deadline
        deadline_of_last_check = checkMeta.next_deadline(deadline_str, last_check)
        if datetime.now() < deadline_of_last_check:
            logger.error(f'[ckMgr]\tcheck_id {check_id} already checked in today')
            return 'already checked in today', False

    # else:
    #     check_history.append(datetime.now())

    check_status_store.check_in(check_id)
    check_status_store.set_check_stats(check)
    check_status_store.write_to_pickle()
    return 'check in success', True


def get_enabled_days(days: str):
    assert days.isdigit()
    enabled_days = []
    weekdays = ['一', '二', '三', '四', '五', '六', '日']
    for i, day in enumerate(days):
        if day == '1':
            enabled_days.append(weekdays[i])
    return '、'.join(enabled_days)


def print_check_info(check):
    check_info = '**打卡信息**\n\n'
    check_info += f'打卡名称：{check.name}\n'
    check_info += f'需要验证：{"是" if check.verify else "否"}\n'
    check_info += f'提醒时间：{check.remind}\n'
    check_info += f'截止时间：{check.deadline}\n'
    check_info += f'打卡日期：{get_enabled_days(check.enabled)}\n'
    check_info += f'结束日期：{check.until or "无"}\n'
    return check_info
