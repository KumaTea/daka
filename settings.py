try:
    from localSet import *
except ImportError:
    host_ip = '127.0.0.1'
    host_user = 'kuma'
    host_key = './cert/key.pem'
    host_port = 22


self_id = 6206355142
creator = 5273618487
administrators = [345060487, creator]

username = 'DKJCbot'
group_username = 'DaKaClub'
group_id = -1001263300787
auth_groups = [group_id]

data_dir = 'data'
check_pickle_file = 'checks.p'
check_ids_by_user_file = 'check_ids.p'
check_status_store_pickle_file = 'check_stats.p'
bot_dir = '/home/kuma/bots/dk'

check_name_max_len = 16
max_checks_per_user = 10
max_skipped_count = 7

start_commands = ['new_check']
