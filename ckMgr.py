import os
import pickle
from session import logger

# info = {
#     'name': '',
#     'id': 0,
#     'user': 0,
#     'verify': True,
#     'remind': '21:00',
#     'deadline': '00:00',
#     'enabled': '1111100',  # enabled day of week, monday is 0
#     'until': None
# }

check_db_file = 'checks.p'


class Checks:
    def __init__(self):
        self.checks = {}
        self.read_from_pickle()

    def read_from_pickle(self):
        if os.path.exists(check_db_file):
            with open(check_db_file, 'rb') as f:
                self.checks = pickle.load(f)
            return logger.info('checks loaded from pickle')
        else:
            with open(check_db_file, 'wb') as f:
                pickle.dump(self.checks, f)

    def write_to_pickle(self):
        with open(check_db_file, 'wb') as f:
            pickle.dump(self.checks, f)

    def add_check(self, check_id: int, check_info: dict):
        if check_id in self.checks:
            raise IndexError('check_id already exists')
        assert check_info['id'] == check_id
        self.checks[check_id] = check_info
        logger.info(f'new check (id={check_id}) added by user {check_info["user"]}')
        self.write_to_pickle()

    def edit_check(self, check_id: int, check_info: dict):
        if check_id not in self.checks:
            raise IndexError('check_id not exists')
        self.checks[check_id] = check_info
        logger.info(f'check (id={check_id}) edited by user {check_info["user"]}')
        self.write_to_pickle()

    def del_check(self, check_id: int):
        if check_id not in self.checks:
            return logger.warning('check_id not exists')
        logger.info(f'check (id={check_id}) deleted by user {self.checks[check_id]["user"]}')
        del self.checks[check_id]
        self.write_to_pickle()

    def get_check(self, check_id: int):
        if check_id not in self.checks:
            return None
        return self.checks[check_id]

    def get_check_by_user(self, user_id: int):
        return [self.checks[check_id] for check_id in self.checks if self.checks[check_id]['user'] == user_id]


checks = Checks()
temp_checks = {}
