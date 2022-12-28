'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyTime.py
@Author    :   Fitz161
@Contact   :   
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re
import time
from datetime import datetime, timedelta, timezone


def time2TextFunTemp():
    def time2TextFun(valDict):
        def time2Text_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '时间戳', '0', groupDict, valDict)
            try:
                date = datetime.fromtimestamp(int(resDict['时间戳'][:10]))
                res = date.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                res = '错误的时间文本格式'
            return res
        return time2Text_f
    return time2TextFun

def getTimestampFunTemp(length:int):
    def getTimestampFun(valDict):
        def getTimestamp_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            res = str(time.time()).replace('.', '')[:length]
            return res
        return getTimestamp_f
    return getTimestampFun

def getTimeIntervalFunTemp():
    def str2timestamp(time):
        time_pattern1 = '(\d{4})[- \/.年](\d{1,2})[- \/.月](\d{1,2})[- \/.日](\d{1,2})[- :\/.时](\d{1,2})[- :\/.分](\d{1,2})秒?'
        time_pattern2 = '(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})'
        if time.isdigit():
            match = re.match(time_pattern2, time)
            if match is None:
                raise ValueError('错误的时间文本格式')
            return datetime(*map(int, match.groups())).astimezone(timezone(timedelta(hours=8))).timestamp()
        else:
            match = re.match(time_pattern1, time)
            if match is None:
                raise ValueError('错误的时间文本格式')
            return datetime(*map(int, match.groups())).astimezone(timezone(timedelta(hours=8))).timestamp()
        
    def getTimeIntervalFun(valDict):
        def getTimeInterval_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '时间文本1', '0', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '时间文本2', '0', groupDict, valDict)
            try:
                interval = str2timestamp(resDict['时间文本1']) - str2timestamp(resDict['时间文本2'])
                res = str(round(interval))
            except ValueError:
                res = '错误的时间文本格式'
            return res
        return getTimeInterval_f
    return getTimeIntervalFun

def getTimeOrDateFunTemp(type):
    weekdayDict = {'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三',
                   'Thursday': '星期四', 'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期日'}
    typeDict = {'年': '%Y', '月': '%m', '日': '%d', '星期': '%A',
                '时': '%H', '分': '%M', '秒': '%S',
                'date': '%Y-%m-%d', 'time': '%H:%M:%S'}
    def getTimeOrDateFun(valDict):
        def getTimeOrDate_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '类型', '', groupDict, valDict)
            key = typeDict.get(resDict['类型'].lstrip('-'), '')
            date = datetime.fromtimestamp(time.time())
            if key == '':
                res = date.strftime(typeDict[type])
            else:
                res = weekdayDict[date.strftime(key)] if key == '%A' else date.strftime(key)
            return res
        return getTimeOrDate_f
    return getTimeOrDateFun
