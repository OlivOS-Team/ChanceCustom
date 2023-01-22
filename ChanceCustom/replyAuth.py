'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyContent.py
@Author    :   Linnest
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

from typing import Optional,Callable



def CurryTemp(func:Callable):
    def reciveStatus(key:Optional[str]=None,*,
                    valLife:Optional[str]=None,
                    flagGlobal:Optional[bool]=None,**anyothers
                    ):
        def reciveValDict(valDict:Optional[dict]=None):
            def TempExcute(*args,**kwargs):
                return func(*args,
                        key=key,
                        valLife=valLife,
                        flagGlobal=flagGlobal,
                        valDict=valDict,**anyothers,
                        **kwargs)
            return TempExcute
        return reciveValDict
    return reciveStatus

def set_group_ban(plugin_event:OlivOS.API.Event, 
    group_id: 'str|int', user_id: 'str|int', 
    host_id: 'str|int|None' = None,duration: int = 1800):
    plugin_event.set_group_ban(group_id, user_id,host_id, duration=duration)

@CurryTemp
def set_group_ban_matcher(matched:'re.Match|dict',**kwargs):
    valDict = kwargs["valDict"]
    groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
    resDict = {}

    ChanceCustom.replyBase.getNumRegTotal(resDict, '时间', 300, groupDict, valDict)
    ChanceCustom.replyBase.getNumRegTotal(resDict, 'QQ', valDict['defaultVal']['发送者QQ'], groupDict, valDict)

    try:
        set_group_ban(plugin_event=valDict['innerVal']['plugin_event'],
            group_id=valDict['defaultVal']['当前群号'],
            user_id=resDict['QQ'],
            duration=resDict['时间'])
    except:
        print("？",flush=True)
    return ""