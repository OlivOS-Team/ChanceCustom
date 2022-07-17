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
            res = 0
            resDict = {}
            ChanceCustom.replyBase.getCharRaw(resDict, 'X', '0', groupDict)
            ChanceCustom.replyBase.getCharRaw(resDict, 'Y', None, groupDict)
            if resDict['Y'] == None:
                if '-' in resDict['X']:
                    try:
                        tmp = resDict['X'].split('-')
                        x = int(tmp[0])
                        y = int(tmp[1])
                    except:
                        x = 0
                        y = 0
                else:
                    x = 0
                    y = 0
            else:
                ChanceCustom.replyBase.getNumRegTatol(resDict, 'X', '0', groupDict, valDict)
                ChanceCustom.replyBase.getNumRegTatol(resDict, 'Y', '0', groupDict, valDict)
                x = resDict['X']
                y = resDict['Y']
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
