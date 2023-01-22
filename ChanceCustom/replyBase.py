'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyBase.py
@Author    :   lunzhiPenxil仑质、Amber-Keter
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom
import os
import sys

import re

def getDataRaw(resDict:dict, calKey, default, groupDict):
    # resDict.setdefault(calKey, groupDict.get(calKey,default))
    resDict[calKey] = default
    if calKey in groupDict:
        resDict[calKey] = groupDict[calKey]

def getCharRaw(resDict, calKey, default, groupDict):
    resDict[calKey] = default
    if calKey in groupDict:
        resDict[calKey] = groupDict[calKey]

def getCharRegTotal(resDict:dict, calKey, default, groupDict, valDict):
    # resDict.setdefault(calKey,
    #         ChanceCustom.replyReg.replyValueRegTotal(
    #             groupDict[calKey],
    #             valDict = valDict
    #         ) if groupDict.get(calKey) else default)
    resDict[calKey] = default
    if calKey in groupDict:
        if len(groupDict[calKey]):
            resDict[calKey] = ChanceCustom.replyReg.replyValueRegTotal(
                groupDict[calKey],
                valDict = valDict
            )

def getNumRegTotal(resDict, calKey, default, groupDict, valDict):
    getCharRegTotal(resDict, calKey, default, groupDict, valDict)
    try:
        resDict[calKey] = int(resDict[calKey])
    except:
        try:
            resDict[calKey] = int(default)
        except:
            resDict[calKey] = 0

def getBoolRegTotal(resDict, calKey, default, groupDict, valDict, defaultBool = ['真', True]):
    getCharRegTotal(resDict, calKey, default, groupDict, valDict)
    if resDict[calKey] == defaultBool[0]:
        resDict[calKey] = defaultBool[1]
    else:
        resDict[calKey] = not defaultBool[1]

def getGroupDictInit(matched:'re.Match|dict'):
    res = {}
    if type(matched) == re.Match:
        res = matched.groupdict()
    if type(matched) == dict:
        res = matched
    return res

def setLFFunTemp():
    def setLFFun(valDict):
        def setLF_f(matched:'re.Match|dict'):
            res = '\n'
            return res
        return setLF_f
    return setLFFun

def ifFunTemp():
    def ifFun(valDict):
        def if_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getBoolRegTotal(resDict, '逻辑值', '真', groupDict, valDict)
            if resDict['逻辑值']:
                getCharRegTotal(resDict, '为真返回', '', groupDict, valDict)
                res = resDict['为真返回']
            else:
                getCharRegTotal(resDict, '否则返回', '', groupDict, valDict)
                res = resDict['否则返回']
            return res
        return if_f
    return ifFun

def ifEmptyFunTemp():
    def ifEmptyFun(valDict):
        def ifEmpty_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRegTotal(resDict, '被判断文本', '', groupDict, valDict)
            if resDict['被判断文本'] == '':
                getCharRegTotal(resDict, '为空替换文本', '', groupDict, valDict)
                res = resDict['为空替换文本']
            else:
                res = resDict['被判断文本']
            return res
        return ifEmpty_f
    return ifEmptyFun

def ifIsFunTemp():
    def ifIsFun(valDict):
        def ifIs_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRegTotal(resDict, '被比较文本', '', groupDict, valDict)
            getCharRegTotal(resDict, '比较文本', '', groupDict, valDict)
            if resDict['被比较文本'] == resDict['比较文本']:
                getCharRegTotal(resDict, '相同返回文本', '', groupDict, valDict)
                res = resDict['相同返回文本']
            else:
                getCharRegTotal(resDict, '不相同返回文本', '', groupDict, valDict)
                res = resDict['不相同返回文本']
            return res
        return ifIs_f
    return ifIsFun

def ifMoreFunTemp():
    def ifMoreFun(valDict):
        def ifMore_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getNumRegTotal(resDict, '被比较数值', '0', groupDict, valDict)
            getNumRegTotal(resDict, '比较数值', '0', groupDict, valDict)
            if resDict['被比较数值'] > resDict['比较数值']:
                getCharRegTotal(resDict, '前者大返回', '', groupDict, valDict)
                res = resDict['前者大返回']
            else:
                getCharRegTotal(resDict, '否则返回', '', groupDict, valDict)
                res = resDict['否则返回']
            return res
        return ifMore_f
    return ifMoreFun

def ifInFunTemp():
    def ifInFun(valDict):
        def ifIn_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRegTotal(resDict, '被判断文本', '', groupDict, valDict)
            getCharRegTotal(resDict, '被包含文本', '', groupDict, valDict)
            if resDict['被包含文本'] in resDict['被判断文本']:
                getCharRegTotal(resDict, '包含返回', '', groupDict, valDict)
                res = resDict['包含返回']
            else:
                getCharRegTotal(resDict, '不包含返回', '', groupDict, valDict)
                res = resDict['不包含返回']
            return res
        return ifIn_f
    return ifInFun

def forRangeFunTemp():
    def forRangeFun(valDict):
        def forRange_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getNumRegTotal(resDict, '循环次数', '0', groupDict, valDict)
            getCharRaw(resDict, '循环体', '', groupDict)
            count = 0
            while count < resDict['循环次数']:
                context_this = resDict['循环体']
                context_this = context_this.replace('[序号]', str(count))
                context_this = ChanceCustom.replyReg.replyValueRegTotal(
                    context_this,
                    valDict = valDict
                )
                context_list_1 = context_this.split('[跳出]')
                context_list_2 = context_this.split('[继续]')
                context_this_1 = context_list_1[0]
                context_this_2 = context_list_2[0]
                if len(context_list_1) > 1 or len(context_list_2) > 1:
                    if context_this_1 < context_this_2:
                        if len(context_list_1) > 1:
                            res += context_this_1
                            break
                    else:
                        if len(context_list_2) > 1:
                            res += context_this_2
                            continue
                else:
                    res += context_this
                count += 1
            return res
        return forRange_f
    return forRangeFun

def forEachFunTemp():
    def forEachFun(valDict):
        def forEach_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRegTotal(resDict, '遍历文本', '', groupDict, valDict)
            getCharRegTotal(resDict, '分隔符', '|', groupDict, valDict)
            getCharRaw(resDict, '遍历体', '', groupDict)
            resList = resDict['遍历文本'].split(resDict['分隔符'])
            count = 0
            for resList_this in resList:
                context_this = resDict['遍历体']
                context_this = context_this.replace('[内容]', resList_this)
                context_this = context_this.replace('[序号]', str(count))
                context_this = ChanceCustom.replyReg.replyValueRegTotal(
                    context_this,
                    valDict = valDict
                )
                context_list_1 = context_this.split('[跳出]')
                context_list_2 = context_this.split('[继续]')
                context_this_1 = context_list_1[0]
                context_this_2 = context_list_2[0]
                if len(context_list_1) > 1 or len(context_list_2) > 1:
                    if context_this_1 < context_this_2:
                        if len(context_list_1) > 1:
                            res += context_this_1
                            break
                    else:
                        if len(context_list_2) > 1:
                            res += context_this_2
                            continue
                else:
                    res += context_this
                count += 1
            return res
        return forEach_f
    return forEachFun

def getContextFunTemp():
    def getContextFun(valDict):
        def getContext_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getNumRegTotal(resDict, 'x', '1', groupDict, valDict)
            key = '内容%s' % str(resDict['x'])
            if key in valDict:
                res = valDict[key]
            return res
        return getContext_f
    return getContextFun

def getDefaultValFunTemp(key):
    def getDefaultValFun(valDict):
        def getDefaultVal_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            if key in valDict['defaultVal']:
                if type(valDict['defaultVal'][key]) == str:
                    res = valDict['defaultVal'][key]
            return res
        return getDefaultVal_f
    return getDefaultValFun

def getDefaultValWithAPIFunTemp(key):
    def getDefaultValWithAPIFun(valDict):
        def getDefaultValWithAPI_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            if 'apiTemp' not in valDict:
                valDict['apiTemp'] = {}
            if key in ['机器人名字']:
                resObj = valDict['innerVal']['plugin_event'].get_stranger_info(valDict['innerVal']['plugin_event'].bot_info.id)
                if resObj != None and resObj['active']:
                    if key == '机器人名字':
                        res = resObj['data']['name']
            elif key in ['权限', '发送者名片', '发送者专属头衔']:
                if valDict['innerVal']['event_name'] == 'group_message':
                    resObj = valDict['innerVal']['plugin_event'].get_group_member_info(
                        group_id = valDict['innerVal']['group_id'],
                        user_id = valDict['innerVal']['user_id'],
                        host_id = valDict['innerVal']['host_id']
                    )
                    if resObj != None and resObj['active']:
                        if key == '权限':
                            if 'role' in resObj['data']:
                                if 'owner' == resObj['data']['role']:
                                    res = '群主'
                                elif 'admin' == resObj['data']['role']:
                                    res = '群管'
                                elif 'member' == resObj['data']['role']:
                                    res = '群员'
                                else:
                                    res = '群员'
                            else:
                                res = '群员'
                        elif key == '发送者名片':
                            if 'name' in resObj['data']:
                                res = resObj['data']['name']
                            if 'card' in resObj['data'] and resObj['data']['card'] != '':
                                res = resObj['data']['card']
                        elif key == '发送者专属头衔':
                            if 'title' in resObj['data']:
                                res = resObj['data']['title']
                else:
                    pass
            elif key in ['当前群名', '当前群人数', '当前群上限']:
                if valDict['innerVal']['event_name'] == 'group_message':
                    resObj = valDict['innerVal']['plugin_event'].get_group_info(
                        group_id = valDict['innerVal']['group_id'],
                        host_id = valDict['innerVal']['host_id']
                    )
                    if resObj != None and resObj['active']:
                        resObj['data']
                        if key == '当前群名':
                            if 'name' in resObj['data']:
                                res = resObj['data']['name']
                        elif key == '当前群人数':
                            if 'member_count' in resObj['data']:
                                res = str(resObj['data']['member_count'])
                        elif key == '当前群上限':
                            if 'max_member_count' in resObj['data']:
                                res = str(resObj['data']['max_member_count'])
                else:
                    pass
            return res
        return getDefaultValWithAPI_f
    return getDefaultValWithAPIFun

def getValFunTemp(valLife = 'local'):
    def getValFun(valDict):
        def getVal_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRegTotal(resDict, '自定义名称', '', groupDict, valDict)
            key = resDict['自定义名称']
            if valLife == 'local':
                if key in valDict:
                    if type(valDict[key]) == str:
                        res = valDict[key]
            elif valLife == 'global':
                if 'valGData' in valDict and key in valDict['valGData']:
                    if type(valDict['valGData'][key]) == str:
                        res = valDict['valGData'][key]
            elif valLife == 'globalOwned':
                if 'valGOData' in valDict and key in valDict['valGOData']:
                    if type(valDict['valGOData'][key]) == str:
                        res = valDict['valGOData'][key]
            return res
        return getVal_f
    return getValFun

def setValFunTemp(valLife = 'local'):
    def setValFun(valDict):
        def setVal_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRegTotal(resDict, '自定义名称', '', groupDict, valDict)
            getCharRegTotal(resDict, '赋值内容', '', groupDict, valDict)
            key = resDict['自定义名称']
            if valLife == 'local':
                if 'valRawData' not in valDict:
                    valDict['valRawData'] = {}
                valDict['valRawData'][key] = resDict['赋值内容']
                if key not in valDict or type(valDict[key]) == str:
                    valDict[key] = valDict['valRawData'][key]
            elif valLife == 'global':
                if 'valRawGData' not in valDict:
                    valDict['valRawGData'] = {}
                valDict['valRawGData'][key] = resDict['赋值内容']
                if 'valGData' not in valDict:
                    valDict['valGData'] = {}
                if key not in valDict['valGData'] or type(valDict['valGData'][key]) == str:
                    valDict['valGData'][key] = valDict['valRawGData'][key]
            elif valLife == 'globalOwned':
                if 'valRawGOData' not in valDict:
                    valDict['valRawGOData'] = {}
                valDict['valRawGOData'][key] = resDict['赋值内容']
                if 'valGOData' not in valDict:
                    valDict['valGOData'] = {}
                if key not in valDict['valGOData'] or type(valDict['valGOData'][key]) == str:
                    valDict['valGOData'][key] = valDict['valRawGOData'][key]
            return res
        return setVal_f
    return setValFun

def updateValFunTemp(valLife = 'local'):
    def updateValFun(valDict):
        def updateVal_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRegTotal(resDict, '自定义名称', '', groupDict, valDict)
            key = resDict['自定义名称']
            if valLife == 'local':
                if 'valRawData' not in valDict:
                    valDict['valRawData'] = {}
                if key in valDict['valRawData']:
                    if key not in valDict or type(valDict[key]) == str:
                        valDict[key] = valDict['valRawData'][key]
            elif valLife == 'global':
                if 'valRawGData' not in valDict:
                    valDict['valRawGData'] = {}
                if key in valDict['valRawGData']:
                    if key not in valDict['valGData'] or type(valDict['valGData'][key]) == str:
                        valDict['valGData'][key] = valDict['valRawGData'][key]
            elif valLife == 'globalOwned':
                if 'valRawGOData' not in valDict:
                    valDict['valRawGOData'] = {}
                if key in valDict['valRawGOData']:
                    if key not in valDict['valGOData'] or type(valDict['valGOData'][key]) == str:
                        valDict['valGOData'][key] = valDict['valRawGOData'][key]
            return res
        return updateVal_f
    return updateValFun

def RunDirectoryFunTemp():
    def RunDirectoryFun(valDict):
        def RunDirectory_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = os.path.split(os.path.realpath(sys.argv[0]))[0]
            return res
        return RunDirectory_f
    return RunDirectoryFun

def AppDirectoryFunTemp():
    def AppDirectoryFun(valDict):
        def AppDirectory_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = os.path.split(os.path.realpath(sys.argv[0]))[0]
            res += '/plugin/data/ChanceCustom/'
            return res
        return AppDirectory_f
    return AppDirectoryFun

def codeEscapeFunTemp():
    def codeEscapeFun(valDict):
        def codeEscape_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRaw(resDict, 'xxx', '', groupDict)
            res_tmp = resDict['xxx']
            for key_this in ChanceCustom.replyReg.listRegTotalEscape:
                res_tmp = res_tmp.replace(key_this[0], key_this[1])
            res = ChanceCustom.replyReg.replyValueRegTotal(
                res_tmp,
                valDict = valDict
            )
            return res
        return codeEscape_f
    return codeEscapeFun

def codeDisEscapeFunTemp():
    def codeDisEscapeFun(valDict):
        def codeDisEscape_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRaw(resDict, 'xxx', '', groupDict)
            res_tmp = resDict['xxx']
            res_tmp = ChanceCustom.replyReg.replyValueRegTotal(
                res_tmp,
                valDict = valDict
            )
            for key_this in ChanceCustom.replyReg.listRegTotalDisEscape:
                res_tmp = res_tmp.replace(key_this[0], key_this[1])
            res_tmp = ChanceCustom.replyReg.replyValueRegTotal(
                res_tmp,
                valDict = valDict
            )
            res = res_tmp
            return res
        return codeDisEscape_f
    return codeDisEscapeFun

def setFuncValFunTemp(flagGlobal = False):
    def setFuncValFun(valDict):
        def setFuncVal_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            getCharRegTotal(resDict, '函数名称', '', groupDict, valDict)
            getDataRaw(resDict, '代码体', None, groupDict)
            key = resDict['函数名称']
            if key != None:
                if 'funcValRawData' not in valDict:
                    valDict['funcValRawData'] = {}
                if 'funcValRawGData' not in valDict:
                    valDict['funcValRawGData'] = {}
                if flagGlobal:
                    valDict['funcValRawGData'][key] = resDict['代码体']
                else:
                    valDict['funcValRawData'][key] = resDict['代码体']
            return res
        return setFuncVal_f
    return setFuncValFun

def getFuncValFunTemp():
    def setFuncValFun(valDict):
        def setFuncVal_f(matched:'re.Match|dict'):
            groupDict = getGroupDictInit(matched)
            res = ''
            resDict = {}
            resValDict = {}
            getDataRaw(resDict, '...', None, groupDict)
            if None != resDict['...']:
                resDict['...'] = [
                    ChanceCustom.replyReg.replyValueRegTotal(
                        resData_this,
                        valDict = valDict
                    ) for resData_this in resDict['...']
                ]
                if len(resDict['...']) > 0:
                    keyRaw = resDict['...'][0]
                    keyHit = None
                    resRaw = ''
                    if keyHit == None and 'funcValRawData' in valDict:
                        for key in valDict['funcValRawData']:
                            if keyRaw.startswith(key):
                                keyHit = key
                                resRaw = valDict['funcValRawData'][key]
                                break
                    if keyHit == None and 'funcValRawGData' in valDict:
                        for key in valDict['funcValRawGData']:
                            if keyRaw.startswith(key):
                                keyHit = key
                                resRaw = valDict['funcValRawGData'][key]
                                break
                    if keyHit != None:
                        resValDict['参数1'] = keyRaw[len(key):]
                        count = 2
                        for resValDict_this in resDict['...'][1:]:
                            resValDict['参数%d' % count] = str(resValDict_this)
                            count += 1
                        for resValDict_this in resValDict:
                            resRaw = resRaw.replace('[%s]' % resValDict_this, resValDict[resValDict_this])
                        res = ChanceCustom.replyReg.replyValueRegTotal(
                            resRaw,
                            valDict = valDict
                        )
            return res
        return setFuncVal_f
    return setFuncValFun
