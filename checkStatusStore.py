import os
import pickle
import checkMeta
from session import logger
from checkMeta import Check
from datetime import datetime, timedelta
from settings import data_dir, check_status_store_pickle_file


class CheckStatus:
    def __init__(self):
        self.name = ''
        self.id = 0
        self.check_history = []
        self.streak = 0  # continuous days of check-in
        self.skipped = 0  # continuous days of skipped


class CheckStatusStore:
    def __init__(self):
        self.check_statuses = {}
        self.read_from_pickle()

    def read_from_pickle(self):
        if os.path.exists(os.path.join(data_dir, check_status_store_pickle_file)):
            with open(os.path.join(data_dir, check_status_store_pickle_file), 'rb') as f:
                self.check_statuses = pickle.load(f)
            return logger.info('[ckSta]\tcheck statuses loaded from pickle')
        else:
            self.write_to_pickle()
            return logger.info('[ckSta]\tcheck statuses pickle created')

    def write_to_pickle(self):
        with open(os.path.join(data_dir, check_status_store_pickle_file), 'wb') as f:
            pickle.dump(self.check_statuses, f)

    def add_check(self, check: Check):
        check_status = CheckStatus()
        check_status.name = check.name
        check_status.id = check.id
        self.check_statuses[check_status.id] = check_status

    def del_check(self, check_id: int):
        if check_id not in self.check_statuses:
            return logger.error(f'[ckSta]\tcheck id {check_id} not exists')
        del self.check_statuses[check_id]

    def init(self, checks: dict):
        for check_id in checks:
            if check_id not in self.check_statuses:
                logger.info(f'[ckSta]\tcheck status (id={check_id}) not in statuses, initializing...')
                check_info = checks[check_id]
                self.add_check(check_info)
        for check_id in self.check_statuses.copy():
            if check_id not in checks:
                logger.info(f'[ckSta]\tcheck status (id={check_id}) not in checks, deleting...')
                self.del_check(check_id)
        self.write_to_pickle()

    def check_in(self, check_id: int):
        self.check_statuses[check_id].check_history.append(datetime.now())
        return logger.info(f'[ckSta]\tcheck status (id={check_id}) check-in')

    def set_check_stats(self, check: Check):
        changed = False
        check_id = check.id
        check_status = self.check_statuses[check_id]
        check_history = check_status.check_history
        check_since = check.since  # YYYYMMDD
        deadline = check.deadline  # HH:MM
        first_deadline = checkMeta.next_deadline(deadline, check_since)
        if len(check_history) == 0:
            if datetime.now() > first_deadline:
                old_skipped = check_status.skipped
                days_passed = (datetime.now() - first_deadline).days + 1
                if old_skipped != days_passed:
                    changed = True
                    check_status.streak = 0
                    check_status.skipped = days_passed
        else:
            last_check_time = check_history[-1]
            deadline_of_last_check = checkMeta.next_deadline(deadline, last_check_time)
            if datetime.now() - deadline_of_last_check > timedelta(days=1):
                # skipped
                old_skipped = check_status.skipped
                days_passed = (datetime.now() - deadline_of_last_check).days
                if old_skipped != days_passed:
                    changed = True
                    check_status.streak = 0
                    check_status.skipped = days_passed
            else:
                # check-in
                old_streak = check_status.streak
                streak = 1
                for i in range(len(check_history) - 1):
                    this_check_time = check_history[-i - 1]
                    last_check_time = check_history[-i - 2]
                    deadline_of_last_check = checkMeta.next_deadline(deadline, last_check_time)
                    if this_check_time - deadline_of_last_check < timedelta(days=1):
                        streak += 1
                    else:
                        break
                if streak != old_streak:
                    changed = True
                    check_status.streak = streak
                    check_status.skipped = 0
        if changed:
            logger.info(f'[ckSta]\tcheck status (id={check_id}) stats updated')
        return changed

    def get_check_status(self, check_id: int) -> CheckStatus:
        return self.check_statuses[check_id]
