'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyReg.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re

listRegTotalFun = [
    ['换行', [], '【换行】'],

    # >内置变量<
    ['间隔', [], ChanceCustom.replyFilter.getPreFilterFunTemp('间隔')],

    # >常用变量<
    ['内容', ['x'], ChanceCustom.replyBase.getContextFunTemp()],

    ['艾特', [], ChanceCustom.replyBase.getDefaultValFunTemp('艾特')],
    ['当前群号', [], ChanceCustom.replyBase.getDefaultValFunTemp('当前群号')],
    ['当前群名', [], ChanceCustom.replyBase.getDefaultValWithAPIFunTemp('当前群名')],
    ['当前群人数', [], ChanceCustom.replyBase.getDefaultValWithAPIFunTemp('当前群人数')],
    ['当前群上限', [], ChanceCustom.replyBase.getDefaultValWithAPIFunTemp('当前群上限')],
    ['当前频道号', [], ChanceCustom.replyBase.getDefaultValFunTemp('当前频道号')],
    ['发送者QQ', [], ChanceCustom.replyBase.getDefaultValFunTemp('发送者QQ')],
    ['发送者ID', [], ChanceCustom.replyBase.getDefaultValFunTemp('发送者ID')],
    ['发送者昵称', [], ChanceCustom.replyBase.getDefaultValFunTemp('发送者昵称')],
    ['机器人名字', [], ChanceCustom.replyBase.getDefaultValWithAPIFunTemp('机器人名字')],
    ['机器人QQ', [], ChanceCustom.replyBase.getDefaultValFunTemp('机器人QQ')],
    ['机器人ID', [], ChanceCustom.replyBase.getDefaultValFunTemp('机器人ID')],
    ['权限', [], ChanceCustom.replyBase.getDefaultValWithAPIFunTemp('权限')],
    ['发送者名片', [], ChanceCustom.replyBase.getDefaultValWithAPIFunTemp('发送者名片')],
    ['发送者专属头衔', [], ChanceCustom.replyBase.getDefaultValWithAPIFunTemp('发送者专属头衔')],

    # 转义
    ['转义', ['xxx'], ChanceCustom.replyBase.codeEscapeFunTemp()],
    ['反转义', ['xxx'], ChanceCustom.replyBase.codeDisEscapeFunTemp()],

    # 系统调用
    ['延时', ['秒'], ChanceCustom.replyContent.flowSleepFunTemp()],
    ['延迟', ['秒'], ChanceCustom.replyContent.flowSleepFunTemp()],

    # >自定义变量<
    ['变量', ['自定义名称'], ChanceCustom.replyBase.getValFunTemp(valLife = 'local')],
    ['更新变量', ['自定义名称'], ChanceCustom.replyBase.updateValFunTemp(valLife = 'local')],
    ['赋值变量', ['自定义名称', '赋值内容'], ChanceCustom.replyBase.setValFunTemp(valLife = 'local')],

    # >自定义常量<
    ['常量', ['自定义名称'], ChanceCustom.replyBase.getValFunTemp(valLife = 'global')],
    ['局部常量', ['自定义名称'], ChanceCustom.replyBase.getValFunTemp(valLife = 'globalOwned')],
    ['更新常量', ['自定义名称'], ChanceCustom.replyBase.updateValFunTemp(valLife = 'global')],
    ['更新局部常量', ['自定义名称'], ChanceCustom.replyBase.updateValFunTemp(valLife = 'globalOwned')],
    ['赋值常量', ['自定义名称', '赋值内容'], ChanceCustom.replyBase.setValFunTemp(valLife = 'global')],
    ['赋值局部常量', ['自定义名称', '赋值内容'], ChanceCustom.replyBase.setValFunTemp(valLife = 'globalOwned')],

    # >Json解析<
    ['Json读', ['来源', '默认值', '...'], ChanceCustom.replyJson.jsonGetStrFunTemp()],
    ['Json写-插列表-自动', ['来源', '插入值', '...'], ChanceCustom.replyJson.jsonAppendStrFunTemp(flagValType = 'auto')],
    ['Json写-插列表-文本', ['来源', '插入值', '...'], ChanceCustom.replyJson.jsonAppendStrFunTemp(flagValType = 'str')],
    ['Json写-插列表', ['来源', '插入值', '...'], ChanceCustom.replyJson.jsonAppendStrFunTemp(flagValType = 'default')],
    ['Json写-自动', ['来源', '写入值', '...'], ChanceCustom.replyJson.jsonSetStrFunTemp(flagValType = 'auto')],
    ['Json写-文本', ['来源', '写入值', '...'], ChanceCustom.replyJson.jsonSetStrFunTemp(flagValType = 'str')],
    ['Json写', ['来源', '写入值', '...'], ChanceCustom.replyJson.jsonSetStrFunTemp(flagValType = 'default')],
    ['Json删-过滤列表', ['来源', '删除值', '...'], ChanceCustom.replyJson.jsonDelListContentStrFunTemp()],
    ['Json删', ['来源', '...'], ChanceCustom.replyJson.jsonDelStrFunTemp()],
    ['Json取', ['来源', '分隔符', '...'], ChanceCustom.replyJson.jsonGetListStrFunTemp()],

    # >文件操作<
    ['读入', ['文件路径'], ChanceCustom.replyIO.fileReadFunTemp()],
    ['写出', ['欲写内容', '文件路径'], ChanceCustom.replyIO.fileWriteFunTemp()],
    ['读配置', ['文件路径', '配置节', '配置项', '默认值'], ChanceCustom.replyIO.iniGetFunTemp()],
    ['写配置', ['文件路径', '配置节', '配置项', '写入值'], ChanceCustom.replyIO.iniSetFunTemp()],
    ['取配置', ['文件路径', '配置节'], ChanceCustom.replyIO.iniGetOptionsFunTemp()],
    ['取配节', ['文件路径'], ChanceCustom.replyIO.iniGetSectionFunTemp()],

    ['读Json', ['文件路径', '默认值', '...'], ChanceCustom.replyJson.jsonGetFunTemp()],
    ['写Json-插列表-自动', ['文件路径', '插入值', '...'], ChanceCustom.replyJson.jsonAppendFunTemp(flagValType = 'auto')],
    ['写Json-插列表-文本', ['文件路径', '插入值', '...'], ChanceCustom.replyJson.jsonAppendFunTemp(flagValType = 'str')],
    ['写Json-插列表', ['文件路径', '插入值', '...'], ChanceCustom.replyJson.jsonAppendFunTemp(flagValType = 'default')],
    ['写Json-自动', ['文件路径', '写入值', '...'], ChanceCustom.replyJson.jsonSetFunTemp(flagValType = 'auto')],
    ['写Json-文本', ['文件路径', '写入值', '...'], ChanceCustom.replyJson.jsonSetFunTemp(flagValType = 'str')],
    ['写Json', ['文件路径', '写入值', '...'], ChanceCustom.replyJson.jsonSetFunTemp(flagValType = 'default')],
    ['删Json-过滤列表', ['文件路径', '删除值', '...'], ChanceCustom.replyJson.jsonDelListContentFunTemp()],
    ['删Json', ['文件路径', '...'], ChanceCustom.replyJson.jsonDelFunTemp()],
    ['取Json', ['文件路径', '分隔符', '...'], ChanceCustom.replyJson.jsonGetListFunTemp()],

    # >常用变量2<
    ['随机数', ['X', 'Y'], ChanceCustom.replyRandom.RangeNumFunTemp(flagPadding = False)],
    ['补位随机数', ['X', 'Y'], ChanceCustom.replyRandom.RangeNumFunTemp(flagPadding = True)],
    ['随机字符', [], ChanceCustom.replyRandom.RangeCharFunTemp()],

    ['随取', ['...'], ChanceCustom.replyRandom.ChoiceOneSTRFunTemp()],

    ['运行目录', [], ChanceCustom.replyBase.RunDirectoryFunTemp()],
    ['应用目录', [], ChanceCustom.replyBase.AppDirectoryFunTemp()],

    # >网页访问变量<
    ['访问-UTF', ['网址'], ChanceCustom.replyWeb.httpGetPageFunTemp(type = 'UTF')],
    ['访问-GBK', ['网址'], ChanceCustom.replyWeb.httpGetPageFunTemp(type = 'GBK')],
    ['访问', ['网址'], ChanceCustom.replyWeb.httpGetPageFunTemp()],

    # >循环变量<
    ['循环', ['循环次数', '循环体'], ChanceCustom.replyBase.forRangeFunTemp()],
    ['Fori', ['遍历体', '遍历文本', '分隔符'], ChanceCustom.replyBase.forEachFunTemp()],
    ['跳出', [], '[跳出]'],
    ['继续', [], '[继续]'],
    ['分页', [], '[分页]'],

    # >IO流<
    ['输入流', ['标识类型', '最大时间', '最大次数', '单Q次数', '是否继续匹配', '回调函数'], ChanceCustom.replyContent.flowInputFunTemp()],
    ['输出流', ['加入文本', '标识类型', '输出类型', '返回msgID'], ChanceCustom.replyContent.flowOutputFunTemp()],

    # >比较判断<
    ['判空', ['被判断文本', '为空替换文本'], ChanceCustom.replyBase.ifEmptyFunTemp()],
    ['判断', ['被比较文本', '比较文本', '不相同返回文本', '相同返回文本'], ChanceCustom.replyBase.ifIsFunTemp()],
    ['比较', ['被比较数值', '比较数值', '前者大返回', '否则返回'], ChanceCustom.replyBase.ifMoreFunTemp()],
    ['判含', ['被判断文本', '被包含文本', '不包含返回', '包含返回'], ChanceCustom.replyBase.ifInFunTemp()],
    ['判真', ['逻辑值', '为真返回', '否则返回'], ChanceCustom.replyBase.ifFunTemp()],

    # >OlivaDice联动<
    ['牌堆', ['牌堆名', '牌数', '是否放回', '分隔符'], ChanceCustom.replyOlivaDice.drawFunTemp()],
    ['RD', ['表达式'], ChanceCustom.replyOlivaDice.RDFunTemp()],
    ['今日人品', [], ChanceCustom.replyOlivaDice.JRRPFunTemp(mode = 'jrrp')],
    ['昨日人品', [], ChanceCustom.replyOlivaDice.JRRPFunTemp(mode = 'zrrp')],
    ['明日人品', [], ChanceCustom.replyOlivaDice.JRRPFunTemp(mode = 'mrrp')],

    ['人物卡-名称', [], ChanceCustom.replyOlivaDice.PcNameGetFunTemp()],
    ['人物卡-读技能', ['技能名'], ChanceCustom.replyOlivaDice.PcSkillGetFunTemp(action = 'get')],
    ['人物卡-写技能', ['技能名', '技能值'], ChanceCustom.replyOlivaDice.PcSkillGetFunTemp(action = 'set')],
    ['人物卡-切换', ['目标人物卡名'], ChanceCustom.replyOlivaDice.PcSwitchSetFunTemp()],
    ['人物卡-锁定', [], ChanceCustom.replyOlivaDice.PcLockSetFunTemp(action = 'lock')],
    ['人物卡-解锁', [], ChanceCustom.replyOlivaDice.PcLockSetFunTemp(action = 'unlock')],

    ['人物卡名', [], ChanceCustom.replyOlivaDice.PcNameGetFunTemp()],
    ['读人物卡', ['技能名'], ChanceCustom.replyOlivaDice.PcSkillGetFunTemp(action = 'get')],
    ['写人物卡', ['技能名', '技能值'], ChanceCustom.replyOlivaDice.PcSkillGetFunTemp(action = 'set')],
    ['切人物卡', ['目标人物卡名'], ChanceCustom.replyOlivaDice.PcSwitchSetFunTemp()],
    ['锁定人物卡', [], ChanceCustom.replyOlivaDice.PcLockSetFunTemp(action = 'lock')],
    ['解锁人物卡', [], ChanceCustom.replyOlivaDice.PcLockSetFunTemp(action = 'unlock')],

    ['DICE-指令注册', ['指令前缀'], ChanceCustom.replyOlivaDice.CommandRegFunTemp()],

    # >算法计算<
    ['计算', ['计算公式'], ChanceCustom.replyEval.evalExprFunTemp()],
    ['排序', ['排序文本', '分割符号', '排序正逆'], ChanceCustom.replyEval.splitSortFunTemp(type="sort")],
    ['分割排序', ['排序文本', '分割符号', '依据序号', '排序正逆'], ChanceCustom.replyEval.splitSortFunTemp(type="split")],
    ['随机排序', ['排序文本', '分割符号'], ChanceCustom.replyEval.splitSortFunTemp(type="shuffle")],
    ['统计', ['被统计文本', '统计出现的文本'], ChanceCustom.replyEval.wordCountFunTemp()],
    ['取MD5', ['被取目标', 'MD5位数'], ChanceCustom.replyEval.getMD5FunTemp()],
    ['进制', ['待转化数值', '原数值进制', '目标进制'], ChanceCustom.replyEval.baseConvFunTmp()],
    ['补位', ['待补位文本', '结果长度', '补位字符', '结尾/开头'], ChanceCustom.replyEval.charPaddingFunTemp()],

    # >时间类<
    ['时间戳转文本', ['时间戳'], ChanceCustom.replyTime.time2TextFunTemp()],
    ['现行日期', ['类型'], ChanceCustom.replyTime.getTimeOrDateFunTemp(type="date")],
    ['现行时间', ['类型'], ChanceCustom.replyTime.getTimeOrDateFunTemp(type="time")],
    ['13位时间', [], ChanceCustom.replyTime.getTimestampFunTemp(length=13)],
    ['10位时间', [], ChanceCustom.replyTime.getTimestampFunTemp(length=10)],
    ['时间间隔', ['时间文本1', '时间文本2'], ChanceCustom.replyTime.getTimeIntervalFunTemp()],

    # >文本操作<
    ['文本-取出中间', ['被取文本', '开始位置', '取出长度'], ChanceCustom.replyText.extractCharFunTemp(type="order")],
    ['文本-倒取中间', ['被取文本', '右边文本', '左边文本'], ChanceCustom.replyText.extractCharFunTemp(type="reverse")],
    ['文本-取出左边', ['被取文本', '取出长度'], ChanceCustom.replyText.extractCharFunTemp(type="left")],
    ['文本-取出右边', ['被取文本', '取出长度'], ChanceCustom.replyText.extractCharFunTemp(type="right")],
    ['文本-取出长度', ['被取文本'], ChanceCustom.replyText.extractCharFunTemp(type="len")],
    ['文本-寻找文本', ['被寻文本', '欲寻内容', '开始位置'], ChanceCustom.replyText.searchTextFunTemp()],
    ['文本-倒找文本', ['被寻文本', '欲寻内容', '开始位置'], ChanceCustom.replyText.searchTextFunTemp(reversed=True)],
    ['文本-反转文本', ['反转文本'], ChanceCustom.replyText.reverseTextFunTemp()],
    ['文本-替换文本', ['被替文本', '开始位置', '替换长度', '替换文本'], ChanceCustom.replyText.replaceTextFunTemp()],
    ['文本-转为大写', ['转换文本'], ChanceCustom.replyText.toggleCaseFunTemp(type="upper")],
    ['文本-转为小写', ['转换文本'], ChanceCustom.replyText.toggleCaseFunTemp(type="lower")],
    ['文本-取文本左', ['被取文本', '被寻内容'], ChanceCustom.replyText.extractCharFunTemp(type="searchL")],
    ['文本-取文本右', ['被取文本', '被寻内容'], ChanceCustom.replyText.extractCharFunTemp(type="searchR")],
    ['文本-中间替换', ['被取文本', '左边文本', '右边文本', '替换文本'], ChanceCustom.replyText.extractCharFunTemp(type="replace")],
    ['文本-删首尾空', ['被删文本'], ChanceCustom.replyText.textStripFunTemp()],

    # >文本行操作<
    ['行操作-删空白行', ['被删文本'], ChanceCustom.replyText.deleteLineFunTemp(type="blank")],
    ['行操作-删重复行', ['被删文本'], ChanceCustom.replyText.deleteLineFunTemp(type="repeat")],
    ['行操作-删首尾空', ['被删文本'], ChanceCustom.replyText.lineStripFunTemp()],
    ['行操作-删指定行', ['被删文本', '开头行序', '结尾行序'], ChanceCustom.replyText.deleteLineFunTemp(type="fix")],
    ['行操作-替换指定', ['被替文本', '开头行序', '结尾行序', '替换文本'], ChanceCustom.replyText.replaceLineFunTemp()],
    ['行操作-插入文本', ['被插文本', '插入内容', '行数'], ChanceCustom.replyText.insertTextFunTemp()],
    ['行操作-按字拆行', ['被拆文本', '每行字数'], ChanceCustom.replyText.splitTextByLengthFunTemp()],
    ['行操作-每行相连', ['被连文本1', '被连文本2', '连接字符'], ChanceCustom.replyText.concatTextFunTemp()],
    ['行操作-每行排序', ['被排文本', '排序顺逆'], ChanceCustom.replyText.sortByFirstLetterFunTemp()],
    ['行操作-每行反转', ['被转文本'], ChanceCustom.replyText.reverseContentFunTemp(type="char")],
    ['行操作-前后反转', ['被转文本'], ChanceCustom.replyText.reverseContentFunTemp(type="line")],
    ['行操作-按行分页', ['被分页文本', '每页行数'], ChanceCustom.replyText.splitTextByLinesFunTemp()],
    ['行操作-取出指定', ['被取文本', '开头行序', '结尾行序', '取出类型'], ChanceCustom.replyText.retrieveTextByLineIndexFunTemp()],
    ['行操作-添加文本', ['被添文本', '添加类型', '添加参数', '添加文本'], ChanceCustom.replyText.addTextForEachLineFunTemp()],
    ['行操作-替换文本', ['被替文本', '替换类型', '替换参数1', '替换参数2', '替换文本'], ChanceCustom.replyText.replaceTextForEachLineFunTemp()],

    # >高级文本操作<
    ['隐藏', ['内容'], ChanceCustom.replyText.hideResultFunTemp()],
    ['分割取出', ['被分割文本', '分隔符', '取出序号'], ChanceCustom.replyText.splitAndSelectFunTemp()],
    ['范围取整', ['数值', '下界', '上界'], ChanceCustom.replyText.roundNumberFunTemp()],
    ['取整', ['被取文本'], ChanceCustom.replyText.filterNumberFunTemp()],
    ['取中间', ['XX1', 'XX2', 'XX3', 'XX4'], ChanceCustom.replyText.selectMiddleFunTemp()],
    ['正则重构', ['重构文本', '表达式', '重构格式'], ChanceCustom.replyText.regExpRefactorFunTemp()],
    ['正则', ['表达式', '被搜索的文本', '序次', '替换文本'], ChanceCustom.replyText.regExpReplaceFunTemp()],
    ['子正则', ['表达式', '被搜索的文本', '序次'], ChanceCustom.replyText.subRegExpFunTemp()],
    ['删除', ['欲被删除文本', '删除文本开头', '删除文本结尾'], ChanceCustom.replyText.deleteTextFunTemp()],
    ['选择', ['序号或逻辑组', '...'], ChanceCustom.replyText.switchAndReturnFunTemp()],
    ['替换', ['被替换内容', '被替换文本', '替换文本', '替换次数', '并列替换'], ChanceCustom.replyText.replaceFunTemp()],

    # >自定义函数<
    ['函数全局', ['函数名称', '代码体'], ChanceCustom.replyBase.setFuncValFunTemp(flagGlobal = True)],
    ['函数', ['函数名称', '代码体'], ChanceCustom.replyBase.setFuncValFunTemp(flagGlobal = True)],
    ['', ['...'], ChanceCustom.replyBase.getFuncValFunTemp()]
]

listRegTotal = [
    ['\n', '']
]

listRegTotalAfter = [
    ['【(?P<函数名>换行)】', '\n'],

    ['#zzk', '【'],
    ['#yzk', '】'],
    ['#fgf', '>=<'],
    ['#xh', '*'],
    ['#hz', '||'],
    ['#jh', '#']
]

listRegTotalDisEscape = [
    ['#zzk', '【'],
    ['#yzk', '】'],
    ['#fgf', '>=<'],
    ['#xh', '*'],
    ['#hz', '||'],
    ['#jh', '#']
]

listRegTotalEscape = [
    ['#', '#jh'],
    ['||', '#hz'],
    ['*', '#xh'],
    ['>=<', '#fgf'],
    ['】', '#yzk'],
    ['【', '#zzk']
]

def replyValueRegTotal(message, valDict):
    res_message = message
    for listRegTotal_this in listRegTotal:
        res_message = re.sub(listRegTotal_this[0], listRegTotal_this[1], res_message)
    res_message = replyValueReg(res_message, valDict)
    for listRegTotal_this in listRegTotalAfter:
        res_message = re.sub(listRegTotal_this[0], listRegTotal_this[1], res_message)
    return res_message

def replyValueReg(message, valDict):
    flag_now = 'plant'
    count = 0
    len_count = len(message)
    res_message = ''
    rule = None
    cal_pos = 0
    calDict = {}
    cal_this = ''
    stack_count = 0
    flag_isArgs = False
    while count < len_count:
        if 'plant' == flag_now:
            if replyValueRegJudge('【', message, count):
                flag_now = 'para_before'
                count += len('【')
            else:
                res_message += message[count]
                count += 1
        elif 'para_before' == flag_now:
            for listRegTotalFun_this in listRegTotalFun:
                if replyValueRegJudge(listRegTotalFun_this[0], message, count):
                    rule = listRegTotalFun_this
                    calDict['函数名'] = rule[0]
                    count += len(listRegTotalFun_this[0])
                    break
            if rule == None:
                calDict['函数名'] = ''
            flag_now = 'para'
        elif 'para' == flag_now:
            if replyValueRegJudge('【', message, count):
                stack_count += 1
                if (rule != None and cal_pos < len(rule[1])) or flag_isArgs:
                    cal_this += message[count]
                count += len('【')
            elif replyValueRegJudge('】', message, count):
                if stack_count > 0:
                    stack_count -= 1
                    if (rule != None and cal_pos < len(rule[1])) or flag_isArgs:
                        cal_this += message[count]
                else:
                    if rule != None and cal_pos < len(rule[1]) - 1:
                        calDict[rule[1][cal_pos]] = cal_this
                    elif rule != None and cal_pos == len(rule[1]) - 1 and rule[1][cal_pos] != '...':
                        calDict[rule[1][cal_pos]] = cal_this
                    elif rule != None and cal_pos >= len(rule[1]) - 1 and len(rule[1]) > 0 and rule[1][-1] == '...':
                        if '...' not in calDict:
                            calDict['...'] = []
                        calDict['...'].append(cal_this)
                    if rule != None:
                        if type(rule[2]) == str:
                            res_message += rule[2]
                        else:
                            res_message += rule[2](valDict)(calDict)
                    rule = None
                    cal_pos = 0
                    calDict = {}
                    cal_this = ''
                    stack_count = 0
                    flag_isArgs = False
                    flag_now = 'plant'
                count += len('】')
            elif stack_count == 0 and replyValueRegJudge('>=<', message, count):
                if rule != None and cal_pos < len(rule[1]) - 1:
                    calDict[rule[1][cal_pos]] = cal_this
                elif rule != None and cal_pos == len(rule[1]) - 1 and rule[1][cal_pos] != '...':
                    calDict[rule[1][cal_pos]] = cal_this
                elif rule != None and cal_pos >= len(rule[1]) - 1 and len(rule[1]) > 0 and rule[1][-1] == '...':
                    if '...' not in calDict:
                        calDict['...'] = []
                    calDict['...'].append(cal_this)
                    flag_isArgs = True
                cal_this = ''
                cal_pos += 1
                count += len('>=<')
            else:
                if (rule != None and cal_pos < len(rule[1])) or flag_isArgs:
                    cal_this += message[count]
                count += 1
    return res_message

def replyValueRegJudge(matchRaw, message, count):
    res = False
    if len(message) > len(matchRaw) and message[count:count + len(matchRaw)] == matchRaw:
        res = True
    return res