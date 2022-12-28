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

def preFilter(replyValue:str, valDict:dict):
    res = True
    flagSkip = False
    releaseDir('./plugin')
    releaseDir('./plugin/data')
    releaseDir('./plugin/data/ChanceCustom')
    if not flagSkip:
        res_re = re.match('【回复间隔(\d+)】', replyValue)
        if res_re != None:
            flagSkip = True
            res_re_list = res_re.groups()
            if len(res_re_list) >= 1 and type(res_re_list[0]) == str:
                if 'platform' in valDict['innerVal']['platform'] and \
                    'sdk' in valDict['innerVal']['platform']:
                    setCount = int(res_re_list[0])
                    if setCount <= 0:
                        setCount = 1
                    nowTime = int(time.time())
                    lastTime = ChanceCustom.replyJson.jsonGetFunTemp()({})(
                        {
                            '文件路径': './plugin/data/ChanceCustom/冷却.json',
                            '默认值': '0',
                            '...': [
                                str(valDict['innerVal']['platform']['platform']),
                                str(valDict['innerVal']['platform']['sdk']),
                                str(valDict['innerVal']['user_id'])
                            ]
                        }
                    )
                    try:
                        lastTime = int(lastTime)
                    except:
                        lastTime = 0
                    if nowTime - lastTime > setCount * 60:
                        res = True
                        ChanceCustom.replyJson.jsonSetFunTemp(flagValType = 'default')({})(
                            {
                                '文件路径': './plugin/data/ChanceCustom/冷却.json',
                                '写入值': str(nowTime),
                                '...': [
                                    str(valDict['innerVal']['platform']['platform']),
                                    str(valDict['innerVal']['platform']['sdk']),
                                    str(valDict['innerVal']['user_id'])
                                ]
                            }
                        )
                    else:
                        res = False
    return res

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
