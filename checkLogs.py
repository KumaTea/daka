import pickle
import checkManager
from session import *
from datetime import datetime, timedelta


class CheckStatus:
    def __init__(self):
        self.name = ''
        self.id = 0
        self.check_times = []
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
            return logger.info('check statuses loaded from pickle')
        else:
            self.write_to_pickle()
            return logger.info('check statuses pickle created')

    def write_to_pickle(self):
        with open(os.path.join(data_dir, check_status_store_pickle_file), 'wb') as f:
            pickle.dump(self.check_statuses, f)

    def new_check(self, check: checkManager.Check):
        check_status = CheckStatus()
        check_status.name = check.name
        check_status.id = check.id
        self.check_statuses[check_status.id] = check_status
        return logger.info(f'new check status (id={check_status.id}) added')

    def init(self):
        for check_id in checkManager.check_store.checks:
            if check_id not in self.check_statuses:
                check_info = checkManager.check_store.checks[check_id]
                self.new_check(check_info)
        self.write_to_pickle()
        return logger.info('check statuses initialized')

    def check_in(self, check_id: int):
        self.check_statuses[check_id].check_times.append(datetime.now())
        return logger.info(f'check status (id={check_id}) check-in')

    def set_check_stats(self, check_id: int):
        check_status = self.check_statuses[check_id]
        check_times = check_status.check_times
        check_since = checkManager.check_store.checks[check_id].since  # YYYYMMDD
        deadline = checkManager.check_store.checks[check_id].deadline  # HH:MM
        first_deadline = datetime.strptime(f'{check_since} {deadline}', '%Y%m%d %H:%M')
        if len(check_times) == 0:
            if datetime.now() > first_deadline:
                days_passed = (datetime.now() - first_deadline).days + 1
                check_status.streak = 0
                check_status.skipped = days_passed
        else:
            last_check_time = check_times[-1]
            deadline_of_last_check = datetime.strptime(
                f'{last_check_time.year}{last_check_time.month}{last_check_time.day} {deadline}', '%Y%m%d %H:%M')
            if last_check_time > deadline_of_last_check:
                deadline_of_last_check += timedelta(days=1)
            if datetime.now() > deadline_of_last_check + timedelta(days=1):
                # skipped
                days_passed = (datetime.now() - deadline_of_last_check).days + 1
                check_status.streak = 0
                check_status.skipped = days_passed
            else:
                # check-in
                streak = 0
                for i in range(len(check_times) - 1):
                    this_check_time = check_times[-i - 1]
                    last_check_time = check_times[-i - 2]
                    deadline_of_last_check = datetime.strptime(
                        f'{last_check_time.year}{last_check_time.month}{last_check_time.day} {deadline}', '%Y%m%d %H:%M')
                    if this_check_time - deadline_of_last_check < timedelta(days=1):
                        streak += 1
                    else:
                        break
                check_status.streak = streak + 1
                check_status.skipped = 0
        return logger.info(f'check status (id={check_id}) stats set')

    def get_check_status(self, check_id: int):
        return self.check_statuses[check_id]
