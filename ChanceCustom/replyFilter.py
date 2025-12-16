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
import hashlib

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
        bot_hash = 'unity'
        plugin_event:'OlivOS.API.Event|None' = None
        user_hash = None
        if 'plugin_event' in valDict['innerVal'] and valDict['innerVal']['plugin_event'] != None:
            bot_hash = valDict['innerVal']['plugin_event'].bot_info.hash
        if 'plugin_event' in valDict['innerVal']:
            plugin_event = valDict['innerVal']['plugin_event']
        if plugin_event != None:
            user_hash = getUserHash(
                plugin_event.data.user_id,
                'user',
                plugin_event.platform['platform']
            )
        if not flagSkip:
            if '【主人】' in replyValue and plugin_event != None:
                if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                    try:
                        import OlivaDiceCore
                        if not OlivaDiceCore.ordinaryInviteManager.isInMasterList(
                            bot_hash,
                            OlivaDiceCore.userConfig.getUserHash(
                                plugin_event.data.user_id,
                                'user',
                                plugin_event.platform['platform']
                            )
                        ):
                            getPreFilterReply('权限限制', valDict)
                            res = False
                            flagSkip = True
                    except:
                        pass
        if not flagSkip:
            if '【群管】' in replyValue and plugin_event != None:
                if 'role' in plugin_event.data.sender and \
                    plugin_event.data.sender['role'] not in ['admin', 'onwer']:
                        getPreFilterReply('权限限制', valDict)
                        res = False
                        flagSkip = True
        if not flagSkip:
            if '【管理】' in replyValue and plugin_event != None:
                if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                    try:
                        import OlivaDiceCore
                        if not OlivaDiceCore.ordinaryInviteManager.isInMasterList(
                            bot_hash,
                            OlivaDiceCore.userConfig.getUserHash(
                                plugin_event.data.user_id,
                                'user',
                                plugin_event.platform['platform']
                            )
                        ):
                            getPreFilterReply('权限限制', valDict)
                            res = False
                            flagSkip = True
                    except:
                        pass
                if 'role' in plugin_event.data.sender and \
                    plugin_event.data.sender['role'] not in ['admin', 'onwer']:
                        getPreFilterReply('权限限制', valDict)
                        res = False
                        flagSkip = True
        if not flagSkip:
            res_re = re.match('[\s\S]*【回复间隔(\d+)】', replyValue)
            if res_re != None and plugin_event != None:
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
                        flagSkip = True
                        getPreFilterReply('回复间隔', valDict)
        if not flagSkip:
            res_re = re.match('[\s\S]*【一次间隔(\d+)】', replyValue)
            if res_re != None and plugin_event != None:
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
                                str(valDict['innerVal']['chat_id']),
                                user_hash,
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
                                    str(valDict['innerVal']['chat_id']),
                                    user_hash,
                                    str(replyKey)
                                ]
                            }
                        )
                    else:
                        res = False
                        flagSkip = True
                        getPreFilterReply('一次间隔', valDict)
                        valDict['innerVal']['间隔'] = str(int((lastTime + setCount * 60 - nowTime) / 60) + 1)
        if not flagSkip:
            res_re = re.match('[\s\S]*【一月上限(\d+)】', replyValue)
            if res_re != None and plugin_event != None:
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
                                str(valDict['innerVal']['chat_id']),
                                user_hash,
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
                                    str(valDict['innerVal']['chat_id']),
                                    user_hash,
                                    str(replyKey)
                                ]
                            }
                        )
                    else:
                        res = False
                        flagSkip = True
                        getPreFilterReply('一月上限', valDict)
        if not flagSkip:
            res_re = re.match('[\s\S]*【一周上限(\d+)】', replyValue)
            if res_re != None and plugin_event != None:
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
                                str(time.strftime('%Y/%V', time.localtime(nowTime))),
                                str(valDict['innerVal']['chat_id']),
                                user_hash,
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
                                    str(time.strftime('%Y/%V', time.localtime(nowTime))),
                                    str(valDict['innerVal']['chat_id']),
                                    user_hash,
                                    str(replyKey)
                                ]
                            }
                        )
                    else:
                        res = False
                        flagSkip = True
                        getPreFilterReply('一周上限', valDict)
        if not flagSkip:
            res_re = re.match('[\s\S]*【一天上限(\d+)】', replyValue)
            if res_re != None and plugin_event != None:
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
                                str(valDict['innerVal']['chat_id']),
                                user_hash,
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
                                    str(valDict['innerVal']['chat_id']),
                                    user_hash,
                                    str(replyKey)
                                ]
                            }
                        )
                    else:
                        res = False
                        flagSkip = True
                        getPreFilterReply('一天上限', valDict)
    except:
        pass

    ChanceCustom.replyFilter.gPreFilterLock.release()

    return res

def getPreFilterReply(key:str, valDict:dict):
    bot_hash = 'unity'
    res = None
    if 'plugin_event' in valDict['innerVal'] and valDict['innerVal']['plugin_event'] != None:
        bot_hash = valDict['innerVal']['plugin_event'].bot_info.hash
    # 应用重定向逻辑（对于非unity的hash，仅在OlivaDiceCore可用时）
    if bot_hash != 'unity' and 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
        try:
            import OlivaDiceCore
            redirected_bot_hash = OlivaDiceCore.userConfig.getRedirectedBotHash(bot_hash)
        except:
            redirected_bot_hash = bot_hash
    else:
        redirected_bot_hash = bot_hash
    if key in ChanceCustom.load.dictCustomData['defaultVar']['unity']:
        res = ChanceCustom.load.dictCustomData['defaultVar']['unity'][key]
    if key in ChanceCustom.load.dictCustomData['defaultVar'][redirected_bot_hash]:
        if len(ChanceCustom.load.dictCustomData['defaultVar'][redirected_bot_hash][key]) > 0:
            res = ChanceCustom.load.dictCustomData['defaultVar'][redirected_bot_hash][key]
    valDict['innerVal']['replaceReply'] = res
    return res

def getPreFilterFunTemp(key:str):
    def getPreFilterFun(valDict):
        def getPreFilter_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            if 'innerVal' in valDict and key in valDict['innerVal'] and \
                valDict['innerVal'][key] != None:
                res = valDict['innerVal'][key]
            return res
        return getPreFilter_f
    return getPreFilterFun

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

def getUserHash(userId, userType, platform, subId = None):
    hash_tmp = hashlib.new('md5')
    if subId != None:
        tmp_strID = '%s|%s' % (str(subId), str(userId))
        hash_tmp.update(tmp_strID.encode(encoding='UTF-8'))
    else:
        hash_tmp.update(str(userId).encode(encoding='UTF-8'))
    hash_tmp.update(str(userType).encode(encoding='UTF-8'))
    hash_tmp.update(str(platform).encode(encoding='UTF-8'))
    if subId != None:
        hash_tmp.update(str(subId).encode(encoding='UTF-8'))
    return hash_tmp.hexdigest()
