import checkMeta
import checkStore
import checkStatusStore
from session import logger
from checkMeta import Check
from datetime import datetime


check_store = checkStore.CheckStore()
logger.info(f'checks count: {len(check_store.checks)}')
check_status_store = checkStatusStore.CheckStatusStore()
logger.info(f'check statuses count: {len(check_status_store.check_statuses)}')
temp_checks = {}
user_statuses = {}
temp_messages = {}
auth_members = []


def gen_check_info():
    info = Check()
    return info


def gen_status():
    status = {
        'task': '',
        'step': 0,
        'done': False,
    }
    return status


def add_new_check(check: Check):
    check_id = check.id
    user_id = check.user
    check_store.add_check(check_id, check)
    check_store.write_to_pickle()
    temp_checks.pop(user_id)
    check_status_store.new_check(check)
    check_status_store.write_to_pickle()
    return logger.info(f'new check (id={check_id}) added by user {user_id}')


def check_in(check_id: int):
    check = check_store.get_check(check_id)
    if not check:
        logger.error(f'check_id {check_id} not exists')
        return 'check_id not exists', None

    check_status = check_status_store.get_check_status(check_id)
    check_history = check_status.check_history
    if check_history:
        last_check = check_history[-1]  # datetime
        deadline_str = check.deadline
        next_deadline_of_last_check = checkMeta.next_deadline(deadline_str, last_check)
        if datetime.now() < next_deadline_of_last_check:
            logger.error(f'check_id {check_id} already checked in today')
            return 'already checked in today', False

    # else:
    #     check_history.append(datetime.now())

    check_status_store.check_in(check_id)
    check_status_store.set_check_stats(check_id, check)
    check_status_store.write_to_pickle()
    return 'check in success', True
