'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyJson.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re
import json

def jsonSetDataHandler(data:str, pathList:list, setVal:str, flagValType:str):
    json_data = {}
    try:
        json_data = json.loads(data)
    except:
        json_data = {}
    json_data_this = json_data
    count = 0
    try:
        for key_this in pathList:
            if count < len(pathList) - 1:
                if key_this not in json_data_this:
                    json_data_this[key_this] = {}
                if type(json_data_this[key_this]) != dict:
                    json_data_this[key_this] = {}
                json_data_this = json_data_this[key_this]
            elif count == len(pathList) - 1:
                data_in = None
                try:
                    if flagValType == 'str':
                        data_in = setVal
                    else:
                        data_in = json.loads(setVal)
                except:
                    data_in = setVal
                if type(data_in) not in [dict, list]:
                    if flagValType == 'default':
                        data_in = str(data_in)
                    elif flagValType == 'auto':
                        pass
                json_data_this[key_this] = data_in
            count += 1
    except:
        pass
    res = json.dumps(json_data, ensure_ascii = False, indent = 4)
    return res

def jsonSetFunTemp(flagValType:str = 'default'):
    def jsonSetFun(valDict):
        def jsonSet_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '文件路径', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '写入值', '', groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', None, groupDict)
            if None != resDict['...']:
                resDict['...'] = [
                    ChanceCustom.replyReg.replyValueRegTotal(
                        resData_this,
                        valDict = valDict
                    ) for resData_this in resDict['...']
                ]
            json_data = ''
            try:
                ChanceCustom.replyIO.releasePath(resDict['文件路径'])
                with open(resDict['文件路径'], 'r', encoding = 'utf-8') as json_f:
                    json_data = json_f.read()
            except:
                json_data = ''
            try:
                json_data_text = ChanceCustom.replyJson.jsonSetDataHandler(json_data, resDict['...'], resDict['写入值'], flagValType)
                with open(resDict['文件路径'], 'w', encoding = 'utf-8') as json_f:
                    json_f.write(json_data_text)
            except:
                pass
            return res
        return jsonSet_f
    return jsonSetFun

def jsonSetStrFunTemp(flagValType:str = 'default'):
    def jsonSetStrFun(valDict):
        def jsonSetStr_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '来源', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '写入值', '', groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', None, groupDict)
            if None != resDict['...']:
                resDict['...'] = [
                    ChanceCustom.replyReg.replyValueRegTotal(
                        resData_this,
                        valDict = valDict
                    ) for resData_this in resDict['...']
                ]
            json_data = resDict['来源']
            try:
                res = ChanceCustom.replyJson.jsonSetDataHandler(json_data, resDict['...'], resDict['写入值'], flagValType)
            except:
                pass
            return res
        return jsonSetStr_f
    return jsonSetStrFun

def jsonGetDataHandler(data:str, pathList:list, defaultVal:str):
    res = defaultVal
    json_data = {}
    try:
        json_data = json.loads(data)
    except:
        json_data = {}
    res_obj = defaultVal
    json_data_this = json_data
    count = 0
    try:
        res_obj = json_data_this
        for key_this in pathList:
            if type(json_data_this) == dict and key_this in json_data_this:
                json_data_this = json_data_this[key_this]
                res_obj = json_data_this
            elif type(json_data_this) == list and (
                int(key_this) >= -len(json_data_this)
            ) and (
                int(key_this) < len(json_data_this)
            ):
                json_data_this = json_data_this[int(key_this)]
                res_obj = json_data_this
            else:
                res_obj = defaultVal
                break
            count += 1
        if type(res_obj) in [dict, list]:
            res = json.dumps(res_obj, ensure_ascii = False, indent = 4)
        else:
            res = str(res_obj)
    except:
        res = defaultVal
    return res

def jsonGetFunTemp():
    def jsonGetFun(valDict):
        def jsonGet_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '文件路径', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '默认值', '', groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', [], groupDict)
            resDict['...'] = [
                ChanceCustom.replyReg.replyValueRegTotal(
                    resData_this,
                    valDict = valDict
                ) for resData_this in resDict['...']
            ]
            json_data = ''
            try:
                with open(resDict['文件路径'], 'r', encoding = 'utf-8') as json_f:
                    json_data = json_f.read()
            except:
                json_data = ''
            res = resDict['默认值']
            res = ChanceCustom.replyJson.jsonGetDataHandler(json_data, resDict['...'], resDict['默认值'])
            return res
        return jsonGet_f
    return jsonGetFun

def jsonGetStrFunTemp():
    def jsonGetStrFun(valDict):
        def jsonGetStr_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '来源', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '默认值', '', groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', [], groupDict)
            resDict['...'] = [
                ChanceCustom.replyReg.replyValueRegTotal(
                    resData_this,
                    valDict = valDict
                ) for resData_this in resDict['...']
            ]
            json_data = resDict['来源']
            res = ChanceCustom.replyJson.jsonGetDataHandler(json_data, resDict['...'], resDict['默认值'])
            return res
        return jsonGetStr_f
    return jsonGetStrFun

def jsonDelDataHandler(data:str, pathList:list):
    json_data = {}
    try:
        json_data = json.loads(data)
    except:
        json_data = {}
    json_data_this = json_data
    count = 0
    try:
        for key_this in pathList:
            if count < len(pathList) - 1:
                if type(json_data_this) == dict and key_this in json_data_this:
                    json_data_this = json_data_this[key_this]
                elif type(json_data_this) == list and (
                    int(key_this) >= -len(json_data_this)
                ) and (
                    int(key_this) < len(json_data_this)
                ):
                    json_data_this = json_data_this[int(key_this)]
                else:
                    break
            elif count == len(pathList) - 1:
                if type(json_data_this) == dict:
                    if key_this in json_data_this:
                        json_data_this.pop(key_this)
                elif type(json_data_this) == list:
                    if (
                        int(key_this) >= -len(json_data_this)
                    ) and (
                        int(key_this) < len(json_data_this)
                    ):
                        json_data_this.pop(int(key_this))
            count += 1
    except:
        pass
    res = json.dumps(json_data, ensure_ascii = False, indent = 4)
    return res

def jsonDelFunTemp():
    def jsonDelFun(valDict):
        def jsonDel_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '文件路径', None, groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', None, groupDict)
            if None != resDict['...']:
                resDict['...'] = [
                    ChanceCustom.replyReg.replyValueRegTotal(
                        resData_this,
                        valDict = valDict
                    ) for resData_this in resDict['...']
                ]
            json_data = ''
            try:
                with open(resDict['文件路径'], 'r', encoding = 'utf-8') as json_f:
                    json_data = json_f.read()
            except:
                json_data = ''
            try:
                json_data_text = ChanceCustom.replyJson.jsonDelDataHandler(json_data, resDict['...'])
                with open(resDict['文件路径'], 'w', encoding = 'utf-8') as json_f:
                    json_f.write(json_data_text)
            except:
                pass
            return res
        return jsonDel_f
    return jsonDelFun

def jsonDelStrFunTemp():
    def jsonDelStrFun(valDict):
        def jsonDelStr_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '来源', None, groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', None, groupDict)
            if None != resDict['...']:
                resDict['...'] = [
                    ChanceCustom.replyReg.replyValueRegTotal(
                        resData_this,
                        valDict = valDict
                    ) for resData_this in resDict['...']
                ]
            json_data = resDict['来源']
            try:
                res = ChanceCustom.replyJson.jsonDelDataHandler(json_data, resDict['...'])
            except:
                pass
            return res
        return jsonDelStr_f
    return jsonDelStrFun

def jsonAppendDataHandler(data:str, pathList:list, setVal:str, flagValType:str):
    json_data = None
    try:
        json_data = json.loads(data)
    except:
        json_data = None
    count = 0
    try:
        if json_data == None:
            if len(pathList) > 0:
                json_data = {}
            else:
                json_data = []
        json_data_this = json_data
        for key_this in pathList:
            if count < len(pathList):
                if key_this not in json_data_this:
                    if count == len(pathList) - 1:
                        json_data_this[key_this] = []
                    else:
                        json_data_this[key_this] = {}
                else:
                    if count == len(pathList) - 1 and type(json_data_this[key_this]) != list:
                        json_data_this[key_this] = []
                    elif count != len(pathList) - 1 and type(json_data_this[key_this]) != dict:
                        json_data_this[key_this] = {}
                if type(json_data_this) == dict and key_this in json_data_this:
                    json_data_this = json_data_this[key_this]
                elif type(json_data_this) == list and (
                    int(key_this) >= -len(json_data_this)
                ) and (
                    int(key_this) < len(json_data_this)
                ):
                    json_data_this = json_data_this[int(key_this)]
                else:
                    break
            count += 1
        data_in = None
        try:
            if flagValType == 'str':
                data_in = setVal
            else:
                data_in = json.loads(setVal)
        except:
            data_in = setVal
        if type(data_in) not in [dict, list]:
            if flagValType == 'default':
                data_in = str(data_in)
            elif flagValType == 'auto':
                pass
        json_data_this.append(data_in)
    except:
        pass
    res = json.dumps(json_data, ensure_ascii = False, indent = 4)
    return res

def jsonAppendFunTemp(flagValType:str = 'default'):
    def jsonAppendFun(valDict):
        def jsonAppend_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '文件路径', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '插入值', '', groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', [], groupDict)
            if None != resDict['...']:
                resDict['...'] = [
                    ChanceCustom.replyReg.replyValueRegTotal(
                        resData_this,
                        valDict = valDict
                    ) for resData_this in resDict['...']
                ]
            json_data = ''
            try:
                ChanceCustom.replyIO.releasePath(resDict['文件路径'])
                with open(resDict['文件路径'], 'r', encoding = 'utf-8') as json_f:
                    json_data = json_f.read()
            except:
                json_data = ''
            try:
                json_data_text = ChanceCustom.replyJson.jsonAppendDataHandler(json_data, resDict['...'], resDict['插入值'], flagValType)
                with open(resDict['文件路径'], 'w', encoding = 'utf-8') as json_f:
                    json_f.write(json_data_text)
            except:
                pass
            return res
        return jsonAppend_f
    return jsonAppendFun

def jsonAppendStrFunTemp(flagValType:str = 'default'):
    def jsonAppendStrFun(valDict):
        def jsonAppendStr_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '来源', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '插入值', '', groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', [], groupDict)
            if None != resDict['...']:
                resDict['...'] = [
                    ChanceCustom.replyReg.replyValueRegTotal(
                        resData_this,
                        valDict = valDict
                    ) for resData_this in resDict['...']
                ]
            json_data = resDict['来源']
            try:
                res = ChanceCustom.replyJson.jsonAppendDataHandler(json_data, resDict['...'], resDict['插入值'], flagValType)
            except:
                pass
            return res
        return jsonAppendStr_f
    return jsonAppendStrFun

def jsonGetListDataHandler(data:str, pathList:list, splitVal:str):
    defaultVal = ''
    res = defaultVal
    json_data = {}
    try:
        json_data = json.loads(data)
    except:
        json_data = {}
    json_data_this = json_data
    count = 0
    try:
        res_obj = json_data_this
        for key_this in pathList:
            if type(json_data_this) == dict and key_this in json_data_this:
                json_data_this = json_data_this[key_this]
                res_obj = json_data_this
            elif type(json_data_this) == list and (
                int(key_this) >= -len(json_data_this)
            ) and (
                int(key_this) < len(json_data_this)
            ):
                json_data_this = json_data_this[int(key_this)]
                res_obj = json_data_this
            else:
                res_obj = defaultVal
                break
            count += 1
        if type(res_obj) in [dict, list]:
            res = splitVal.join(
                [
                    str(
                        json.dumps(
                            res_obj_this,
                            ensure_ascii = False,
                            indent = 4
                        )
                    ) if type(res_obj_this) in [
                        dict,
                        list
                    ] else str(res_obj_this) for res_obj_this in res_obj
                ]
            )
        else:
            res = defaultVal
    except:
        res = defaultVal
    return res

def jsonGetListFunTemp():
    def jsonGetListFun(valDict):
        def jsonGetList_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '文件路径', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '分隔符', '', groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', [], groupDict)
            resDict['...'] = [
                ChanceCustom.replyReg.replyValueRegTotal(
                    resData_this,
                    valDict = valDict
                ) for resData_this in resDict['...']
            ]
            json_data = ''
            try:
                with open(resDict['文件路径'], 'r', encoding = 'utf-8') as json_f:
                    json_data = json_f.read()
            except:
                json_data = ''
            res = ChanceCustom.replyJson.jsonGetListDataHandler(json_data, resDict['...'], resDict['分隔符'])
            return res
        return jsonGetList_f
    return jsonGetListFun

def jsonGetListStrFunTemp():
    def jsonGetListStrFun(valDict):
        def jsonGetListStr_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '来源', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '分隔符', '', groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', [], groupDict)
            resDict['...'] = [
                ChanceCustom.replyReg.replyValueRegTotal(
                    resData_this,
                    valDict = valDict
                ) for resData_this in resDict['...']
            ]
            json_data = resDict['来源']
            res = ChanceCustom.replyJson.jsonGetListDataHandler(json_data, resDict['...'], resDict['分隔符'])
            return res
        return jsonGetListStr_f
    return jsonGetListStrFun
