from settings import *

# new check
NEW_START = '开始创建新的打卡任务！中途退出，请发送 /cancel'
NEW_STEP_1 = '第一步：请输入打卡任务的名称，{max_len}字以内。'.format(max_len=check_name_max_len)
NEW_STEP_2 = '第二步：请选择打卡时是否需要回复一条消息 (如打卡截图、学习小结等) 以验证。'
NEW_STEP_3 = '第三步：请选择打卡提醒时间。'
NEW_STEP_3_M = '请输入打卡提醒时间，格式为 HH:MM，如 21:00，时区为 UTC+8。\n如果不需要提醒，请发送「无」。'
NEW_STEP_4 = '第四步：请选择打卡截止时间。'
NEW_STEP_4_M = '请输入打卡截止时间，格式为 HH:MM，如 00:00，时区为 UTC+8。'
NEW_STEP_5 = '第五步：请选择打卡日期。'
NEW_STEP_5_M = '请输入打卡日期，格式示例 1111100。\n其中 1 代表当天需要打卡，0 代表当天不需要打卡。\n从周一开始，周日为最后一天。'
NEW_STEP_6 = '第六步：请选择结束打卡日期。'
NEW_STEP_6_M = '请输入结束打卡日期，格式为 YYYYMMDD，如 20231231。\n如果不需要结束日期，请发送「无」。'
NEW_STEP_7 = '第七步：请确认打卡任务信息。'
MALFORMED_TIME = '时间格式错误，请重新输入，格式为HH:MM，如 21:00。'
MALFORMED_DAYS = '启用日格式错误，请重新输入，格式示例 1111100。'
MALFORMED_DATE = '日期格式错误，请重新输入，格式为 YYYYMMDD，如 20231231。'
MAX_CHECKS = '你的打卡已达上限，请使用 /del_check 删除后再创建。'

# del check
DEL_START = '请选择你要删除的打卡任务：'
DEL_CONFIRM = '你确定要删除打卡任务 **{check_name}** 吗？\n一旦删除，所有的打卡记录将会消失！'
DEL_SUCCESS = '打卡任务 **{check_name}** 已删除。'
DEL_CANCEL = '删除操作已取消。'
DEL_NO_CHECKS = '你目前暂无打卡任务！'

# others
PROCESSING = '正在处理...'
ERROR = '程序错误！已重置状态。'
NOT_IN_TASK = '不要乱点无关的按钮 😡'

# auth
USER_NOT_IN_AUTH_GROUP = '你不是 @DaKaClub 的成员，请先加入！'
GROUP_NOT_IN_AUTH_LIST = '本群不在授权列表中！再见！'

# dm
DM_START = '你好，欢迎使用打卡警察！\n使用 /help 查看帮助。'
DM_START_PARA = '点它👉 /{command}'
DM_HELP = '目前上线功能：\n' \
          '/new_check - 新建打卡\n' \
          '你需要是 @DaKaClub 的成员才能使用本 bot.'
NO_OPERATION = '你目前没有正在进行的操作。'
DEFAULT_REPLY = '你好，欢迎使用打卡警察！\n使用 /help 查看帮助。'
CMD_NOT_AVAILABLE = '这个命令还没有开发哦！'

# group
NO_CHECKS = '你目前暂未添加打卡任务，请[私聊我使用 /new_check 命令](https://t.me/DKJCBot?start=new_check)添加。'
NO_VERIFY = '你的打卡任务 **{check_name}** 需要回复一条验证消息！请重试。'
CHECK_SUCCESS = '任务 **{check_name}** 打卡成功！'
FIRST_TIME = '这是你的第一次打卡，好的开始是成功的一半！'
FIRST_RECOVER = '这是你断签后重新开始的第一次打卡，要继续坚持哦 🥺'
STREAK = '当前已连续打卡 {streak} 天。'
ALREADY = '你今天已经打卡过 **{check_name}** 了。'
CHOOSE_CHECK = '请选择你要打卡的任务：'
REMINDER = '{mention} 你今天还没有完成 **{check_name}** 的打卡哦！截止时间是 {deadline}，要抓紧了！🥵'
DEADLINE = '{mention} 你今天没有打卡 **{check_name}** 哦！这是你第 {skipped} 次没有打卡！😡'
CLEAR_STALE_CHECK = '{mention} 你的打卡 **{check_name}** 已经连续{max_skipped}天没有打卡，已经删掉了！😡😡😡'
