'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyCore.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re

def unity_reply(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow, event_name:str):
    reply_runtime(
        plugin_event = plugin_event,
        Proc = Proc,
        event_name = event_name
    )

def reply_runtime(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow, event_name:str):
    tmp_dictCustomData = ChanceCustom.load.dictCustomData
    tmp_hash_list = ['unity', plugin_event.bot_info.hash]
    tmp_message = plugin_event.data.message
    falg_matchPlace_target = 0
    valDict = {}
    valDict['platform'] = plugin_event.platform
    if 'group_message' == event_name:
        falg_matchPlace_target |= 1
        valDict['host_id'] = plugin_event.data.host_id
        valDict['group_id'] = plugin_event.data.group_id
        valDict['hag_id'] = plugin_event.data.group_id
        if plugin_event.data.host_id != None:
            valDict['hag_id'] = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
        valDict['user_id'] = plugin_event.data.user_id
    if 'private_message' == event_name:
        falg_matchPlace_target |= 2
        valDict['user_id'] = plugin_event.data.user_id
    for tmp_hash_list_this in tmp_hash_list:
        valDict['bot_hash'] = tmp_hash_list_this
        valDict['bot_hash_self'] = plugin_event.bot_info.hash
        if tmp_hash_list_this in tmp_dictCustomData['data']:
            tmp_dictCustomData_this = tmp_dictCustomData['data'][tmp_hash_list_this]
            it_list_tmp_dictCustomData = ChanceCustom.load.getCustomDataSortKeyList(
                data = tmp_dictCustomData_this,
                reverse = False
            )
            for key_this in it_list_tmp_dictCustomData:
                falg_matchPlace = int(tmp_dictCustomData_this[key_this]['matchPlace'])
                if (falg_matchPlace_target & falg_matchPlace) != 0:
                    if 'full' == tmp_dictCustomData_this[key_this]['matchType']:
                        if tmp_message == tmp_dictCustomData_this[key_this]['key']:
                            reply(
                                plugin_event,
                                ChanceCustom.replyReg.replyValueRegTotal(
                                    tmp_dictCustomData_this[key_this]['value'],
                                    valDict
                                )
                            )
                            break
                    elif 'perfix' == tmp_dictCustomData_this[key_this]['matchType']:
                        if tmp_message.startswith(tmp_dictCustomData_this[key_this]['key']):
                            valDict['内容1'] = tmp_message[len(tmp_dictCustomData_this[key_this]['key']):]
                            reply(
                                plugin_event,
                                ChanceCustom.replyReg.replyValueRegTotal(
                                    tmp_dictCustomData_this[key_this]['value'],
                                    valDict
                                )
                            )
                            break
                    elif 'reg' == tmp_dictCustomData_this[key_this]['matchType']:
                        res_re = re.match(tmp_dictCustomData_this[key_this]['key'], tmp_message)
                        if res_re != None:
                            res_re_list = res_re.groups()
                            count = 1
                            for res_re_list_this in res_re_list:
                                key = '内容%s' % str(count)
                                value = ''
                                if type(res_re_list_this) == str:
                                    value = res_re_list_this
                                elif res_re_list_this != None:
                                    value = ''
                                valDict[key] = value
                                count += 1
                            reply(
                                plugin_event,
                                ChanceCustom.replyReg.replyValueRegTotal(
                                    tmp_dictCustomData_this[key_this]['value'],
                                    valDict
                                )
                            )
                            break

def reply(plugin_event:OlivOS.API.Event, message:str):
    plugin_event.reply(message)

def send(plugin_event:OlivOS.API.Event, send_type:str, target_id:str, message:str, host_id:'str|None' = None):
    plugin_event.send(send_type, target_id, message, host_id = host_id)
