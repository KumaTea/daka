import os
import pickle
from session import logger
from checkMeta import Check
from settings import data_dir, check_pickle_file, check_ids_by_user_file


class CheckStore:
    def __init__(self):
        self.checks = {}
        self.check_ids_by_user = {}
        self.read_from_pickle()

    def read_from_pickle(self):
        if os.path.exists(os.path.join(data_dir, check_pickle_file)):
            with open(os.path.join(data_dir, check_pickle_file), 'rb') as f:
                self.checks = pickle.load(f)
            with open(os.path.join(data_dir, check_ids_by_user_file), 'rb') as f:
                self.check_ids_by_user = pickle.load(f)
            return logger.info('checks loaded from pickle')
        else:
            self.write_to_pickle()
            return logger.info('checks pickle created')

    def write_to_pickle(self):
        with open(os.path.join(data_dir, check_pickle_file), 'wb') as f:
            pickle.dump(self.checks, f)
        with open(os.path.join(data_dir, check_ids_by_user_file), 'wb') as f:
            pickle.dump(self.check_ids_by_user, f)

    def add_check(self, check_id: int, check_info: Check):
        if check_id in self.checks:
            raise IndexError('check_id already exists')
        assert check_info.id == check_id
        self.checks[check_id] = check_info
        if check_info.user not in self.check_ids_by_user:
            self.check_ids_by_user[check_info.user] = [check_id]
        else:
            self.check_ids_by_user[check_info.user].append(check_id)

    def edit_check(self, check_id: int, check_info: Check):
        if check_id not in self.checks:
            raise IndexError('check_id not exists')
        self.checks[check_id] = check_info

    def del_check(self, check_id: int):
        if check_id not in self.checks:
            return logger.warning('check_id not exists')
        user_id = self.checks[check_id].user
        self.check_ids_by_user[user_id].remove(check_id)
        if not self.check_ids_by_user[user_id]:
            del self.check_ids_by_user[user_id]
        del self.checks[check_id]

    def get_check(self, check_id: int):
        if check_id not in self.checks:
            return None
        return self.checks[check_id]

    def get_checks_by_user(self, user_id: int):
        # return [self.checks[check_id] for check_id in self.checks if self.checks[check_id]['user'] == user_id]
        if user_id not in self.check_ids_by_user:
            return []
        checks = []
        for check_id in self.check_ids_by_user[user_id]:
            checks.append(self.checks[check_id])
        return checks
