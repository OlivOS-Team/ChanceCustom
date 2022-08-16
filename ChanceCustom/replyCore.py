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
import random

def unity_reply(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow, event_name:str):
    reply_runtime(
        plugin_event = plugin_event,
        Proc = Proc,
        event_name = event_name
    )

def getValDict(valDict:dict, plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow, event_name:str):
    #内置变量，用于内部调用
    valDict['innerVal'] = {}
    valDict['innerVal']['plugin_event'] = plugin_event
    valDict['innerVal']['Proc'] = Proc
    valDict['innerVal']['platform'] = plugin_event.platform
    valDict['innerVal']['event_name'] = event_name
    if 'group_message' == event_name:
        valDict['innerVal']['host_id'] = plugin_event.data.host_id
        valDict['innerVal']['group_id'] = plugin_event.data.group_id
        valDict['innerVal']['hag_id'] = plugin_event.data.group_id
        if plugin_event.data.host_id != None:
            valDict['innerVal']['hag_id'] = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
        valDict['innerVal']['user_id'] = plugin_event.data.user_id
    elif 'private_message' == event_name:
        valDict['innerVal']['user_id'] = plugin_event.data.user_id
    elif 'poke_private' == event_name:
        valDict['innerVal']['user_id'] = str(plugin_event.data.target_id)
        valDict['innerVal']['event_name'] = 'private_message'
    elif 'poke_group' == event_name:
        valDict['innerVal']['user_id'] = str(plugin_event.data.target_id)
        valDict['innerVal']['event_name'] = 'group_message'
        valDict['innerVal']['host_id'] = None
        valDict['innerVal']['group_id'] = plugin_event.data.group_id
        valDict['innerVal']['hag_id'] = plugin_event.data.group_id

    #预设变量，用于供外部调用
    valDict['defaultVal'] = {}
    valDict['defaultVal']['当前群号'] = ''
    valDict['defaultVal']['当前频道号'] = ''
    valDict['defaultVal']['发送者QQ'] = str(plugin_event.data.user_id)
    valDict['defaultVal']['发送者ID'] = str(plugin_event.data.user_id)
    valDict['defaultVal']['艾特'] = '[CQ:at,qq=%s]' % str(plugin_event.data.user_id)
    valDict['defaultVal']['发送者昵称'] = ''
    if event_name in ['poke_group', 'poke_private']:
        resObj = plugin_event.get_stranger_info(plugin_event.data.user_id)
        if resObj != None and resObj['active']:
            valDict['defaultVal']['发送者昵称'] = resObj['data']['name']
    else:
        if 'name' in plugin_event.data.sender:
            valDict['defaultVal']['发送者昵称'] = plugin_event.data.sender['name']
    valDict['defaultVal']['机器人QQ'] = str(plugin_event.bot_info.id)
    valDict['defaultVal']['机器人ID'] = str(plugin_event.bot_info.id)
    if event_name in ['group_message', 'poke_group']:
        valDict['defaultVal']['当前群号'] = plugin_event.data.group_id


def reply_runtime(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow, event_name:str):
    tmp_dictCustomData = ChanceCustom.load.dictCustomData
    tmp_hash_list = ['unity', plugin_event.bot_info.hash]
    tmp_message = ''
    if event_name in ['poke']:
        tmp_message = '[戳一戳]'
    else:
        tmp_message = plugin_event.data.message
    falg_matchPlace_target = 0
    valDict = {}

    if 'group_message' == event_name:
        falg_matchPlace_target |= 1
    elif 'private_message' == event_name:
        falg_matchPlace_target |= 2
    elif 'poke' == event_name:
        if str(plugin_event.data.target_id) == str(plugin_event.bot_info.id):
            if plugin_event.data.group_id in [-1, None]:
                falg_matchPlace_target |= 2
                event_name = 'poke_private'
            else:
                falg_matchPlace_target |= 1
                event_name = 'poke_group'
        else:
            return

    getValDict(valDict, plugin_event, Proc, event_name)

    for tmp_hash_list_this in tmp_hash_list:
        valDict['innerVal']['bot_hash'] = tmp_hash_list_this
        valDict['innerVal']['bot_hash_self'] = plugin_event.bot_info.hash
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
                            tmp_value = random.choice(tmp_dictCustomData_this[key_this]['value'].split('*'))
                            reply(
                                plugin_event,
                                ChanceCustom.replyReg.replyValueRegTotal(
                                    tmp_value,
                                    valDict
                                )
                            )
                            break
                    elif 'perfix' == tmp_dictCustomData_this[key_this]['matchType']:
                        if tmp_message.startswith(tmp_dictCustomData_this[key_this]['key']):
                            valDict['内容1'] = tmp_message[len(tmp_dictCustomData_this[key_this]['key']):]
                            tmp_value = random.choice(tmp_dictCustomData_this[key_this]['value'].split('*'))
                            reply(
                                plugin_event,
                                ChanceCustom.replyReg.replyValueRegTotal(
                                    tmp_value,
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
                            tmp_value = random.choice(tmp_dictCustomData_this[key_this]['value'].split('*'))
                            reply(
                                plugin_event,
                                ChanceCustom.replyReg.replyValueRegTotal(
                                    tmp_value,
                                    valDict
                                )
                            )
                            break

def reply(plugin_event:OlivOS.API.Event, message:str):
    plugin_event.reply(message)

def send(plugin_event:OlivOS.API.Event, send_type:str, target_id:str, message:str, host_id:'str|None' = None):
    plugin_event.send(send_type, target_id, message, host_id = host_id)
