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

import ChanceCustom

import re
import time

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
