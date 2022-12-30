'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyFilter.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re
import os
import time
import threading

gPreFilterLock = threading.Lock()

def preFilter(replyKey:str, replyValue:str, valDict:dict):
    res = True
    flagSkip = False

    ChanceCustom.replyFilter.gPreFilterLock.acquire()

    try:
        nowTime = int(time.time())
        releaseDir('./plugin')
        releaseDir('./plugin/data')
        releaseDir('./plugin/data/ChanceCustom')
        print(valDict['innerVal']['bot_hash'])
        bot_hash = 'unity'
        if 'plugin_event' in valDict['innerVal'] and valDict['innerVal']['plugin_event'] != None:
            bot_hash = valDict['innerVal']['plugin_event'].bot_info.hash
        if not flagSkip:
            res_re = re.match('【回复间隔(\d+)】', replyValue)
            if res_re != None:
                flagSkip = True
                res_re_list = res_re.groups()
                if len(res_re_list) >= 1 and type(res_re_list[0]) == str:
                    setCount = int(res_re_list[0])
                    if setCount <= 0:
                        setCount = 1
                    lastTime = ChanceCustom.replyJson.jsonGetFunTemp()({})(
                        {
                            '文件路径': './plugin/data/ChanceCustom/冷却.json',
                            '默认值': '0',
                            '...': [
                                str(bot_hash),
                                str(valDict['innerVal']['chat_id'])
                            ]
                        }
                    )
                    lastTime = str2int(lastTime)
                    if nowTime > lastTime + setCount:
                        res = True
                        ChanceCustom.replyJson.jsonSetFunTemp(flagValType = 'default')({})(
                            {
                                '文件路径': './plugin/data/ChanceCustom/冷却.json',
                                '写入值': str(nowTime),
                                '...': [
                                    str(bot_hash),
                                    str(valDict['innerVal']['chat_id'])
                                ]
                            }
                        )
                    else:
                        res = False
        if not flagSkip:
            res_re = re.match('【一次间隔(\d+)】', replyValue)
            if res_re != None:
                flagSkip = True
                res_re_list = res_re.groups()
                if len(res_re_list) >= 1 and type(res_re_list[0]) == str:
                    setCount = int(res_re_list[0])
                    if setCount <= 0:
                        setCount = 1
                    lastTime = ChanceCustom.replyJson.jsonGetFunTemp()({})(
                        {
                            '文件路径': './plugin/data/ChanceCustom/间隔.json',
                            '默认值': '0',
                            '...': [
                                str(bot_hash),
                                str(replyKey)
                            ]
                        }
                    )
                    lastTime = str2int(lastTime)
                    if nowTime > lastTime + setCount * 60:
                        res = True
                        ChanceCustom.replyJson.jsonSetFunTemp(flagValType = 'default')({})(
                            {
                                '文件路径': './plugin/data/ChanceCustom/间隔.json',
                                '写入值': str(nowTime),
                                '...': [
                                    str(bot_hash),
                                    str(replyKey)
                                ]
                            }
                        )
                    else:
                        res = False
        if not flagSkip:
            res_re = re.match('【一月上限(\d+)】', replyValue)
            if res_re != None:
                flagSkip = True
                res_re_list = res_re.groups()
                if len(res_re_list) >= 1 and type(res_re_list[0]) == str:
                    setCount = int(res_re_list[0])
                    if setCount <= 0:
                        setCount = 1
                    lastCount = ChanceCustom.replyJson.jsonGetFunTemp()({})(
                        {
                            '文件路径': './plugin/data/ChanceCustom/上限.json',
                            '默认值': '0',
                            '...': [
                                str(bot_hash),
                                str(time.strftime('%Y-%m', time.localtime(nowTime))),
                                str(replyKey)
                            ]
                        }
                    )
                    lastCount = str2int(lastCount)
                    if lastCount < setCount:
                        res = True
                        ChanceCustom.replyJson.jsonSetFunTemp(flagValType = 'default')({})(
                            {
                                '文件路径': './plugin/data/ChanceCustom/上限.json',
                                '写入值': str(lastCount + 1),
                                '...': [
                                    str(bot_hash),
                                    str(time.strftime('%Y-%m', time.localtime(nowTime))),
                                    str(replyKey)
                                ]
                            }
                        )
                    else:
                        res = False
        if not flagSkip:
            res_re = re.match('【一周上限(\d+)】', replyValue)
            if res_re != None:
                flagSkip = True
                res_re_list = res_re.groups()
                if len(res_re_list) >= 1 and type(res_re_list[0]) == str:
                    setCount = int(res_re_list[0])
                    if setCount <= 0:
                        setCount = 1
                    lastCount = ChanceCustom.replyJson.jsonGetFunTemp()({})(
                        {
                            '文件路径': './plugin/data/ChanceCustom/上限.json',
                            '默认值': '0',
                            '...': [
                                str(bot_hash),
                                str(time.strftime('%Y-%m/%W', time.localtime(nowTime))),
                                str(replyKey)
                            ]
                        }
                    )
                    lastCount = str2int(lastCount)
                    if lastCount < setCount:
                        res = True
                        ChanceCustom.replyJson.jsonSetFunTemp(flagValType = 'default')({})(
                            {
                                '文件路径': './plugin/data/ChanceCustom/上限.json',
                                '写入值': str(lastCount + 1),
                                '...': [
                                    str(bot_hash),
                                    str(time.strftime('%Y-%m/%W', time.localtime(nowTime))),
                                    str(replyKey)
                                ]
                            }
                        )
                    else:
                        res = False
        if not flagSkip:
            res_re = re.match('【一天上限(\d+)】', replyValue)
            if res_re != None:
                flagSkip = True
                res_re_list = res_re.groups()
                if len(res_re_list) >= 1 and type(res_re_list[0]) == str:
                    setCount = int(res_re_list[0])
                    if setCount <= 0:
                        setCount = 1
                    lastCount = ChanceCustom.replyJson.jsonGetFunTemp()({})(
                        {
                            '文件路径': './plugin/data/ChanceCustom/上限.json',
                            '默认值': '0',
                            '...': [
                                str(bot_hash),
                                str(time.strftime('%Y-%m-%d', time.localtime(nowTime))),
                                str(replyKey)
                            ]
                        }
                    )
                    lastCount = str2int(lastCount)
                    if lastCount < setCount:
                        res = True
                        ChanceCustom.replyJson.jsonSetFunTemp(flagValType = 'default')({})(
                            {
                                '文件路径': './plugin/data/ChanceCustom/上限.json',
                                '写入值': str(lastCount + 1),
                                '...': [
                                    str(bot_hash),
                                    str(time.strftime('%Y-%m-%d', time.localtime(nowTime))),
                                    str(replyKey)
                                ]
                            }
                        )
                    else:
                        res = False
    except:
        pass

    ChanceCustom.replyFilter.gPreFilterLock.release()

    return res

def str2int(value:str):
    res = 0
    try:
        res = int(value)
    except:
        res = 0
    return res

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
