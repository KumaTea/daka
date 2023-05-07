from settings import *

NEW_START = '开始创建新的打卡任务！中途退出，请发送 /cancel'
NEW_STEP_1 = '第一步：请输入打卡任务的名称，{}字以内。'.format(check_name_max_len)
NEW_STEP_2 = '第二步：请选择打卡时是否需要回复一条消息 (如打卡截图、学习小结等) 以验证。'
NEW_STEP_3 = '第三步：请选择打卡提醒时间。'
NEW_STEP_3_M = '请输入打卡提醒时间，格式为 HH:MM，如 21:00。\n如果不需要提醒，请发送「无」。'
NEW_STEP_4 = '第四步：请选择打卡截止时间。'
NEW_STEP_4_M = '请输入打卡截止时间，格式为 HH:MM，如 00:00。'
NEW_STEP_5 = '第五步：请选择打卡日期。'
NEW_STEP_5_M = '请输入打卡日期，格式示例 1111100。\n其中 1 代表当天需要打卡，0 代表当天不需要打卡。\n从周一开始，周日为最后一天。'
NEW_STEP_6 = '第六步：请选择结束打卡日期。'
NEW_STEP_6_M = '请输入结束打卡日期，格式为 YYYYMMDD，如 20231231。\n如果不需要结束日期，请发送「无」。'
NEW_STEP_7 = '第七步：请确认打卡任务信息。'
MALFORMED_TIME = '时间格式错误，请重新输入，格式为HH:MM，如 21:00。'
MALFORMED_DAYS = '启用日格式错误，请重新输入，格式示例 1111100。'
MALFORMED_DATE = '日期格式错误，请重新输入，格式为 YYYYMMDD，如 20231231。'
MAX_CHECKS = '您的打卡已达上限，请使用 /del_check 删除后再创建。'
ERROR = '程序错误！已重置状态。'
NOT_IN_TASK = '不要乱点无关的按钮 😡'
USER_NOT_IN_AUTH_GROUP = '您不是 @DaKaClub 的成员，请先加入！'
GROUP_NOT_IN_AUTH_LIST = '本群不在授权列表中！再见！'
DEFAULT_REPLY = '您好，欢迎使用打卡警察！\n使用 /help 查看帮助。'
NO_CHECKS = '您目前暂未添加打卡任务，请私聊我使用 /new_check 命令添加。'
NO_VERIFY = '您的打卡任务 **{}** 需要回复一条验证消息！请重试。'
SUCCESS = '任务 **{}** 打卡成功！'
FIRST_TIME = '这是你的第一次打卡，好的开始是成功的一半！'
STREAK = '当前已连续打卡 {} 天。'
ALREADY = '您今天已经打卡过 **{}** 了。'
CHOOSE_CHECK = '请选择您要打卡的任务：'
CMD_NOT_AVAILABLE = '这个命令还没有开发哦！'
DM_START = '您好，欢迎使用打卡警察！\n使用 /help 查看帮助。'
DM_HELP = '目前上线功能：\n' \
          '/new_check - 新建打卡\n' \
          '您需要是 @DaKaClub 的成员才能使用本 bot.'
NO_OPERATION = '您目前没有正在进行的操作。'
