'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyBase.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom
import random

import re

def RangeNumFunTemp(flagPadding:bool = False):
    def RangeNumFun(valDict):
        def RangeNum_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            x = 0
            y = 0
            flagRight = True
            ChanceCustom.replyBase.getCharRaw(resDict, 'X', '0', groupDict)
            ChanceCustom.replyBase.getCharRaw(resDict, 'Y', None, groupDict)
            resDict['X'] = ChanceCustom.replyReg.replyValueRegTotal(
                resDict['X'],
                valDict = valDict
            )
            if resDict['Y'] == None:
                if '-' in resDict['X']:
                    try:
                        tmp = resDict['X'].split('-')
                        x = int(tmp[0])
                        y = int(tmp[1])
                    except:
                        flagRight = False
                else:
                    flagRight = False
            else:
                resDict['Y'] = ChanceCustom.replyReg.replyValueRegTotal(
                    resDict['Y'],
                    valDict = valDict
                )
                try:
                    x = int(resDict['X'])
                    y = int(resDict['Y'])
                except:
                    flagRight = False
            if flagRight:
                res = str(random.randint(x,y))
                if flagPadding:
                    res = res.zfill(len(str(y)))
            return res
        return RangeNum_f
    return RangeNumFun

def RangeCharFunTemp():
    def RangeCharFun(valDict):
        def RangeChar_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            alphabet = 'AaBbCcDdEdFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
            res = random.choice(alphabet)
            return res
        return RangeChar_f
    return RangeCharFun
