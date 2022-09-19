'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyContent.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re
import time
import hashlib
import uuid

contextReg = {}

def flowInputFunTemp():
    def flowInputFun(valDict):
        def flowInput_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getNumRegTatol(resDict, '标识类型', '2', groupDict, valDict)
            ChanceCustom.replyBase.getNumRegTatol(resDict, '最大时间', '30', groupDict, valDict)
            ChanceCustom.replyBase.getNumRegTatol(resDict, '最大次数', '1', groupDict, valDict)
            ChanceCustom.replyBase.getNumRegTatol(resDict, '单Q次数', '0', groupDict, valDict)
            ChanceCustom.replyBase.getBoolRegTatol(resDict, '是否继续匹配', '假', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '回调函数', '', groupDict, valDict)
            contextRegName = None
            print(resDict)
            if resDict['标识类型'] == 1:
                if 'group_id' in valDict['innerVal'] and 'group_id' in valDict['innerVal']:
                    contextRegName =  contextRegHash([
                        str(valDict['innerVal']['host_id']),
                        str(valDict['innerVal']['group_id']),
                        str(None)
                    ])
                else:
                    contextRegName = None
            elif resDict['标识类型'] == 2:
                contextRegName = contextRegHash([
                    str(None),
                    str(None),
                    str(valDict['innerVal']['user_id'])
                ])
            elif resDict['标识类型'] == 3:
                if 'group_id' in valDict['innerVal'] and 'group_id' in valDict['innerVal']:
                    contextRegName =  contextRegHash([
                        str(valDict['innerVal']['host_id']),
                        str(valDict['innerVal']['group_id']),
                        str(valDict['innerVal']['user_id'])
                    ])
                else:
                    contextRegName = None
            bot_hash = None
            try:
                bot_hash = valDict['innerVal']['plugin_event'].bot_info.hash
            except:
                bot_hash = None
            count = resDict['最大时间'] * 2
            flagLoop = False
            if count == 0:
                flagLoop = True
            matchCount = resDict['最大次数']
            matchCountOne = resDict['单Q次数']
            matchContinue = resDict['是否继续匹配']
            token = str(uuid.uuid4())
            dataTmplate = None
            if bot_hash != None and contextRegName != None:
                if bot_hash not in ChanceCustom.replyContent.contextReg:
                    ChanceCustom.replyContent.contextReg[bot_hash] = {}
                dataTmplate = {
                    'type': resDict['标识类型'],
                    'data': None,
                    'dataQueue': [],
                    'flagLoop': flagLoop,
                    'count': count,
                    'matchCount': matchCount,
                    'matchCountOne': matchCountOne,
                    'matchContinue': matchContinue,
                    'token': token
                }
                ChanceCustom.replyContent.contextReg[bot_hash][contextRegName] = dataTmplate.copy()
                ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['dataQueue'] = []
            try:
                flagPop = True
                while flagLoop or count > 0:
                    count -= 1
                    if (
                        bot_hash in ChanceCustom.replyContent.contextReg
                    ) and (
                        contextRegName in ChanceCustom.replyContent.contextReg[bot_hash]
                    ) and (
                        'data' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]
                    ):
                        time.sleep(0.5)
                        if (
                            'token' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]
                        ) and (
                            ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['token'] != token
                        ):
                            flagPop = False
                            break
                        if resDict['回调函数'] != '' and 'dataQueue' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]:
                            dataQueueCount = len(ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['dataQueue'])
                            if dataQueueCount > 0:
                                dataQueueTmp = ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['dataQueue'][:dataQueueCount]
                                try:
                                    ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['dataQueue'] = ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['dataQueue'][dataQueueCount:]
                                except:
                                    ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['dataQueue'] = []
                                flagBreak = False
                                for dataQueueTmp_this in dataQueueTmp:
                                    res_this = ChanceCustom.replyReg.replyValueRegTotal(
                                        '【%s%s】' % (
                                            resDict['回调函数'],
                                            dataQueueTmp_this
                                        ),
                                        valDict = valDict
                                    )
                                    if res_this == str(1):
                                        ChanceCustom.replyContent.contextReg[bot_hash][contextRegName] = dataTmplate.copy()
                                        count = dataTmplate['count']
                                        ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['dataQueue'] = []
                                    elif res_this == str(-1):
                                        res = dataQueueTmp_this
                                        flagBreak = True
                                        break
                                if flagBreak:
                                    break
                        if ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['data'] != None:
                            res = str(ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['data'])
                            break
                        else:
                            ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['count'] = count
                    else:
                        break
                if flagPop and bot_hash != None and contextRegName != None:
                    if bot_hash in ChanceCustom.replyContent.contextReg and contextRegName in ChanceCustom.replyContent.contextReg[bot_hash]:
                        ChanceCustom.replyContent.contextReg[bot_hash].pop(contextRegName)
            except:
                res = ''
            return res
        return flowInput_f
    return flowInputFun

def contextRegHash(data:list):
    res = None
    hash_tmp = hashlib.new('md5')
    for data_this in data:
        if type(data_this) == str:
            hash_tmp.update(str(data_this).encode(encoding='UTF-8'))
    res = hash_tmp.hexdigest()
    return res

def contextRegTryHit(message:str, event_name:str, valDict:dict, bot_hash:str):
    res = True
    contextRegName_list = []
    if event_name == 'group_message':
        contextRegName_list.append(contextRegHash([
            str(valDict['innerVal']['host_id']),
            str(valDict['innerVal']['group_id']),
            str(valDict['innerVal']['user_id'])
        ]))
        contextRegName_list.append(contextRegHash([
            str(None),
            str(None),
            str(valDict['innerVal']['user_id'])
        ]))
        contextRegName_list.append(contextRegHash([
            str(valDict['innerVal']['host_id']),
            str(valDict['innerVal']['group_id']),
            str(None)
        ]))
    elif event_name == 'private_message':
        contextRegName_list.append(contextRegHash([
            str(None),
            str(None),
            str(valDict['innerVal']['user_id'])
        ]))
    for contextRegName in contextRegName_list:
        flagMatch = False
        flagBlock = False
        if (
            contextRegName != None
        ) and (
            bot_hash in ChanceCustom.replyContent.contextReg
        ) and (
            contextRegName in ChanceCustom.replyContent.contextReg[bot_hash]
        ) and (
            'data' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]
        ) and (
            None == ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['data']
        ) and (((
                'count' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]
            ) and (
                ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['count'] > 0
            )
        ) or ((
                'flagLoop' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]
            ) and (
                ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['flagLoop']
            )
        )):
            if 'matchCount' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]:
                if ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCount'] > 0:
                    if 'matchCount_count' not in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]:
                        ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCount_count'] = 0
                    ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCount_count'] += 1
                    if ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCount_count'] == ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCount']:
                        flagMatch = True
                    elif 'matchCount_count' not in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]:
                        ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCount_count'] = 1
                else:
                    flagMatch = True
            if (
                'type' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]
            ) and (
                ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['type'] == 1
            ):
                if 'matchCountOne' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]:
                    if ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCountOne'] > 0:
                        if 'matchCountOne_count' not in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]:
                            ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCountOne_count'] = {}
                        contextRegNameOne = contextRegHash([
                            str(None),
                            str(None),
                            str(valDict['innerVal']['user_id'])
                        ])
                        if contextRegNameOne not in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCountOne_count']:
                            ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCountOne_count'][contextRegNameOne] = 0
                        ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCountOne_count'][contextRegNameOne] += 1
                        if ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCountOne_count'][contextRegNameOne] == ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchCountOne']:
                            flagMatch = True
            if 'dataQueue' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]:
                ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['dataQueue'].append(message)
            if flagMatch:
                ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['data'] = message
            res = False
            if 'matchContinue' in ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]:
                if ChanceCustom.replyContent.contextReg[bot_hash][contextRegName]['matchContinue'] == True:
                    res = True
    return res

def flowOutputFunTemp():
    def flowOutputFun(valDict):
        def flowOutput_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTatol(resDict, '加入文本', '', groupDict, valDict)
            msg = resDict['加入文本']
            valDict['innerVal']['plugin_event'].reply(
                message = msg
            )
            return res
        return flowOutput_f
    return flowOutputFun

def flowSleepFunTemp():
    def flowSleepFun(valDict):
        def flowSleep_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getNumRegTatol(resDict, '秒', 0, groupDict, valDict)
            time.sleep(resDict['秒'])
            return res
        return flowSleep_f
    return flowSleepFun
