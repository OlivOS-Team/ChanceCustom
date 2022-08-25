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
    ['变量', ['自定义名称'], ChanceCustom.replyBase.getValFunTemp()],
    ['更新变量', ['自定义名称'], ChanceCustom.replyBase.updateValFunTemp()],
    ['赋值变量', ['自定义名称', '赋值内容'], ChanceCustom.replyBase.setValFunTemp()],

    # >自定义常量<
    ['常量', ['自定义名称'], ChanceCustom.replyBase.getValFunTemp()],
    ['更新常量', ['自定义名称'], ChanceCustom.replyBase.updateValFunTemp()],
    ['赋值常量', ['自定义名称', '赋值内容'], ChanceCustom.replyBase.setValFunTemp()],

    # >Json解析<
    ['Json读', ['来源', '默认值', '...'], ChanceCustom.replyJson.jsonGetStrFunTemp()],
    ['Json写-插列表-自动', ['来源', '插入值', '...'], ChanceCustom.replyJson.jsonAppendStrFunTemp(flagValType = 'auto')],
    ['Json写-插列表-文本', ['来源', '插入值', '...'], ChanceCustom.replyJson.jsonAppendStrFunTemp(flagValType = 'str')],
    ['Json写-插列表', ['来源', '插入值', '...'], ChanceCustom.replyJson.jsonAppendStrFunTemp(flagValType = 'default')],
    ['Json写-自动', ['来源', '写入值', '...'], ChanceCustom.replyJson.jsonSetStrFunTemp(flagValType = 'auto')],
    ['Json写-文本', ['来源', '写入值', '...'], ChanceCustom.replyJson.jsonSetStrFunTemp(flagValType = 'str')],
    ['Json写', ['来源', '写入值', '...'], ChanceCustom.replyJson.jsonSetStrFunTemp(flagValType = 'default')],
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
    ['删Json', ['文件路径', '...'], ChanceCustom.replyJson.jsonDelFunTemp()],
    ['取Json', ['文件路径', '分隔符', '...'], ChanceCustom.replyJson.jsonGetListFunTemp()],

    # >常用变量2<
    ['随机数', ['X', 'Y'], ChanceCustom.replyRandom.RangeNumFunTemp(flagPadding = False)],
    ['补位随机数', ['X', 'Y'], ChanceCustom.replyRandom.RangeNumFunTemp(flagPadding = True)],
    ['随机字符', [], ChanceCustom.replyRandom.RangeCharFunTemp()],

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

    # >IO流<
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

    # >算法计算<
    ['计算', ['计算公式'], ChanceCustom.replyEval.evalExprFunTemp()],
    ['分割排序', ['排序文本', '分割符号', '依据序号', '排序正逆'], ChanceCustom.replyEval.splitSortFunTemp(type="sort")],
    ['随机排序', ['排序文本', '分割符号'], ChanceCustom.replyEval.splitSortFunTemp(type="shuffle")],
    ['统计', ['被统计文本', '统计出现的文本'], ChanceCustom.replyEval.wordCountFunTemp()],
    ['取MD5', ['被取目标', 'MD5位数'], ChanceCustom.replyEval.getMD5FunTemp()],
    ['进制', ['待转化数值', '原数值进制', '目标进制'], ChanceCustom.replyEval.baseConvFunTmp()],
    ['补位', ['待补位文本', '结果长度', '补位字符', '结尾/开头'], ChanceCustom.replyEval.charPaddingFunTemp()]
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
    ['#jh', '#']
]

listRegTotalDisEscape = [
    ['#zzk', '【'],
    ['#yzk', '】'],
    ['#fgf', '>=<'],
    ['#xh', '*'],
    ['#jh', '#']
]

listRegTotalEscape = [
    ['#', '#jh'],
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