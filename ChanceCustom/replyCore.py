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

globalValDict = {}

def unity_reply(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow, event_name:str):
    reply_runtime(
        plugin_event = plugin_event,
        Proc = Proc,
        event_name = event_name
    )

def getValDictUnity(valDict:dict):
    global globalValDict
    if 'funcValRawGData' in globalValDict:
        valDict['funcValRawGData'] = globalValDict['funcValRawGData'].copy()
    if 'valRawGData' in globalValDict:
        valDict['valRawGData'] = globalValDict['valRawGData'].copy()
    if 'valGData' in globalValDict:
        valDict['valGData'] = globalValDict['valGData'].copy()
    if 'innerVal' in valDict and 'bot_hash' in valDict['innerVal']:
        bot_hash = valDict['innerVal']['bot_hash']
        if 'valRawGOData' in globalValDict and bot_hash in globalValDict['valRawGOData']:
            valDict['valRawGOData'] = globalValDict['valRawGOData'][bot_hash].copy()
        if 'valGOData' in globalValDict and bot_hash in globalValDict['valGOData']:
            valDict['valGOData'] = globalValDict['valGOData'][bot_hash].copy()

def setValDictUnity(valDict:dict):
    global globalValDict
    if 'funcValRawGData' in valDict:
        globalValDict['funcValRawGData'] = valDict['funcValRawGData'].copy()
    if 'valRawGData' in valDict:
        globalValDict['valRawGData'] = valDict['valRawGData'].copy()
    if 'valGData' in valDict:
        globalValDict['valGData'] = valDict['valGData'].copy()
    if 'innerVal' in valDict and 'bot_hash' in valDict['innerVal']:
        bot_hash = valDict['innerVal']['bot_hash']
        if 'valRawGOData' not in globalValDict:
            globalValDict['valRawGOData'] = {}
        if 'valRawGOData' in valDict:
            globalValDict['valRawGOData'][bot_hash] = valDict['valRawGOData'].copy()
        if 'valGOData' not in globalValDict:
            globalValDict['valGOData'] = {}
        if 'valGOData' in valDict:
            globalValDict['valGOData'][bot_hash] = valDict['valGOData'].copy()

def getFakePluginEvent(valDict:dict, plugin_event:OlivOS.API.Event, event_name:str, message:str):
    if 'poke_private' == event_name:
        valDict['innerVal']['plugin_event'] = ChanceCustom.replyEvent.getReRxEvent_private_message(
            src = plugin_event,
            message = message
        )
    elif 'poke_group' == event_name:
        valDict['innerVal']['plugin_event'] = ChanceCustom.replyEvent.getReRxEvent_group_message(
            src = plugin_event,
            message = message
        )

def getValDict(valDict:dict, plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow, event_name:str):
    #内置变量，用于内部调用
    valDict['innerVal'] = {}
    valDict['innerVal']['plugin_event'] = plugin_event
    valDict['innerVal']['Proc'] = Proc
    valDict['innerVal']['platform'] = plugin_event.platform
    valDict['innerVal']['event_name'] = event_name
    valDict['innerVal']['bot_hash'] = 'unity'
    valDict['innerVal']['chat_id'] = ''
    valDict['innerVal']['replaceReply'] = None
    if 'group_message' == event_name:
        valDict['innerVal']['bot_hash'] = plugin_event.bot_info.hash
        valDict['innerVal']['host_id'] = plugin_event.data.host_id
        valDict['innerVal']['group_id'] = plugin_event.data.group_id
        valDict['innerVal']['hag_id'] = plugin_event.data.group_id
        if plugin_event.data.host_id != None:
            valDict['innerVal']['hag_id'] = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
        valDict['innerVal']['user_id'] = plugin_event.data.user_id
        valDict['innerVal']['chat_id'] = 'GROUP:%s' % str(valDict['innerVal']['hag_id'])
    elif 'private_message' == event_name:
        valDict['innerVal']['bot_hash'] = plugin_event.bot_info.hash
        valDict['innerVal']['user_id'] = plugin_event.data.user_id
        valDict['innerVal']['chat_id'] = 'USER:%s' % str(valDict['innerVal']['user_id'])
    elif 'poke_private' == event_name:
        valDict['innerVal']['bot_hash'] = plugin_event.bot_info.hash
        valDict['innerVal']['user_id'] = str(plugin_event.data.target_id)
        valDict['innerVal']['event_name'] = 'private_message'
        valDict['innerVal']['chat_id'] = 'USER:%s' % str(valDict['innerVal']['user_id'])
    elif 'poke_group' == event_name:
        valDict['innerVal']['bot_hash'] = plugin_event.bot_info.hash
        valDict['innerVal']['user_id'] = str(plugin_event.data.target_id)
        valDict['innerVal']['event_name'] = 'group_message'
        valDict['innerVal']['host_id'] = None
        valDict['innerVal']['group_id'] = plugin_event.data.group_id
        valDict['innerVal']['hag_id'] = plugin_event.data.group_id
        valDict['innerVal']['chat_id'] = 'GROUP:%s' % str(valDict['innerVal']['hag_id'])
    elif 'init' == event_name:
        valDict['innerVal']['user_id'] = str(88888888)
        valDict['innerVal']['event_name'] = 'group_message'
        valDict['innerVal']['host_id'] = None
        valDict['innerVal']['group_id'] = str(88888888)
        valDict['innerVal']['hag_id'] = str(88888888)
        valDict['innerVal']['chat_id'] = 'GROUP:%s' % str(valDict['innerVal']['hag_id'])

    #预设变量，用于供外部调用
    valDict['defaultVal'] = {}
    valDict['defaultVal']['当前群号'] = ''
    valDict['defaultVal']['当前频道号'] = ''
    valDict['defaultVal']['发送者QQ'] = ''
    valDict['defaultVal']['发送者ID'] = ''
    valDict['defaultVal']['艾特'] = ''
    if event_name in ['init']:
        valDict['defaultVal']['发送者QQ'] = str(88888888)
        valDict['defaultVal']['发送者ID'] = str(88888888)
        valDict['defaultVal']['艾特'] = '[CQ:at,qq=%s]' % str(88888888)
    else:
        valDict['defaultVal']['发送者QQ'] = str(plugin_event.data.user_id)
        valDict['defaultVal']['发送者ID'] = str(plugin_event.data.user_id)
        valDict['defaultVal']['艾特'] = '[CQ:at,qq=%s]' % str(plugin_event.data.user_id)
    valDict['defaultVal']['发送者昵称'] = ''
    if event_name in ['poke_group', 'poke_private']:
        resObj = plugin_event.get_stranger_info(plugin_event.data.user_id)
        if resObj != None and resObj['active']:
            valDict['defaultVal']['发送者昵称'] = resObj['data']['name']
    elif event_name in ['init']:
        pass
    else:
        if 'name' in plugin_event.data.sender:
            valDict['defaultVal']['发送者昵称'] = plugin_event.data.sender['name']
    valDict['defaultVal']['机器人QQ'] = str(plugin_event.bot_info.id)
    valDict['defaultVal']['机器人ID'] = str(plugin_event.bot_info.id)
    if event_name in ['group_message', 'poke_group']:
        valDict['defaultVal']['当前群号'] = plugin_event.data.group_id
    elif event_name in ['init']:
        valDict['defaultVal']['当前群号'] = str(88888888)


def reply_runtime(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow, event_name:str):
    global globalValDict
    tmp_dictCustomData = ChanceCustom.load.dictCustomData
    tmp_hash_list = ['unity', plugin_event.bot_info.hash]
    tmp_message = ''
    if event_name in ['poke']:
        tmp_message = '[戳一戳]'
    elif event_name in ['init']:
        tmp_message = '[初始化]'
    else:
        tmp_message = plugin_event.data.message
    flag_matchPlace_target = 0
    valDict = {}

    flag_fetch = False
    if 'group_message' == event_name:
        flag_matchPlace_target |= 0b01
    elif 'private_message' == event_name:
        flag_matchPlace_target |= 0b10
    elif 'poke' == event_name:
        if str(plugin_event.data.target_id) == str(plugin_event.bot_info.id):
            if plugin_event.data.group_id in [-1, '-1', None]:
                flag_matchPlace_target |= 0b10
                event_name = 'poke_private'
            else:
                flag_matchPlace_target |= 0b01
                event_name = 'poke_group'
        else:
            return
    elif 'init' == event_name:
        flag_matchPlace_target |= 0b01
        flag_fetch = True

    getValDict(valDict, plugin_event, Proc, event_name)
    getFakePluginEvent(valDict, plugin_event, event_name, tmp_message)

    getValDictUnity(valDict)

    if not ChanceCustom.replyContent.contextRegTryHit(
        message = tmp_message,
        event_name = event_name,
        valDict = valDict,
        bot_hash = plugin_event.bot_info.hash
    ):
        return



    bot_hash_last = None
    for tmp_hash_list_this in tmp_hash_list:
        bot_hash_last = tmp_hash_list_this
        valDict['innerVal']['bot_hash'] = tmp_hash_list_this
        valDict['innerVal']['bot_hash_self'] = plugin_event.bot_info.hash
        # 应用重定向逻辑（对于非unity的hash，仅在OlivaDiceCore可用时）
        if tmp_hash_list_this != 'unity' and has_olivadicecore:
            try:
                redirected_hash = OlivaDiceCore.userConfig.getRedirectedBotHash(tmp_hash_list_this)
            except:
                redirected_hash = tmp_hash_list_this
        else:
            redirected_hash = tmp_hash_list_this
        
        if redirected_hash in tmp_dictCustomData['data']:
            tmp_dictCustomData_this = tmp_dictCustomData['data'][redirected_hash]
            it_list_tmp_dictCustomData = ChanceCustom.load.getCustomDataSortKeyList(
                data = tmp_dictCustomData_this,
                reverse = False
            )
            for key_this in it_list_tmp_dictCustomData:
                flag_matchPlace = int(tmp_dictCustomData_this[key_this]['matchPlace'])
                
                get_division = False

                if not tmp_dictCustomData_this[key_this].get("division") or \
                    str(tmp_dictCustomData_this[key_this]["division"]) == "0" or \
                    str(tmp_dictCustomData_this[key_this]["division"]) == "1":
                    get_division = True
                elif 'group_message' == event_name and str(plugin_event.data.group_id) in \
                    str(tmp_dictCustomData_this[key_this]["division"]).split("*"):
                    get_division = True
                elif 'private_message' == event_name and str(plugin_event.data.user_id) in \
                    str(tmp_dictCustomData_this[key_this]["division"]).split("*") and \
                    flag_matchPlace & 0b10 != 0:
                    get_division = True

                if (flag_matchPlace_target & flag_matchPlace) != 0 and get_division:
                    if flag_fetch:
                        res_re = None
                        if tmp_message == '[初始化]':
                            res_re = re.match(r'^\[初始化.*\]$', key_this)
                        if res_re != None:
                            tmp_value = random.choice(tmp_dictCustomData_this[key_this]['value'].split('*'))
                            for tmp_value_this in tmp_value.split('[分页]'):
                                msg = ChanceCustom.replyReg.replyValueRegTotal(
                                    tmp_value_this,
                                    valDict
                                )
                                if len(msg) > 0:
                                    reply(
                                        plugin_event,
                                        msg
                                    )
                            continue
                    elif 'full' == tmp_dictCustomData_this[key_this]['matchType']:
                        if tmp_message == tmp_dictCustomData_this[key_this]['key']:
                            if ChanceCustom.replyFilter.preFilter(
                                replyKey = tmp_dictCustomData_this[key_this]['key'],
                                replyValue = tmp_dictCustomData_this[key_this]['value'],
                                valDict = valDict
                            ):
                                tmp_value = random.choice(tmp_dictCustomData_this[key_this]['value'].split('*'))
                                for tmp_value_this in tmp_value.split('[分页]'):
                                    msg = ChanceCustom.replyReg.replyValueRegTotal(
                                        tmp_value_this,
                                        valDict
                                    )
                                    if len(msg) > 0:
                                        reply(
                                            plugin_event,
                                            msg
                                        )
                            break
                    elif 'contain' == tmp_dictCustomData_this[key_this]['matchType']:
                        if tmp_dictCustomData_this[key_this]['key'] != '' and tmp_dictCustomData_this[key_this]['key'] in tmp_message:
                            res_re_list = tmp_message.split(tmp_dictCustomData_this[key_this]['key'])
                            count = 1
                            for res_re_list_this in res_re_list:
                                key = '内容%s' % str(count)
                                value = ''
                                if type(res_re_list_this) == str:
                                    value = res_re_list_this
                                elif res_re_list_this != None:
                                    value = ''
                                valDict[key] = codeEscape(value)
                                count += 1
                            if ChanceCustom.replyFilter.preFilter(
                                replyKey = tmp_dictCustomData_this[key_this]['key'],
                                replyValue = tmp_dictCustomData_this[key_this]['value'],
                                valDict = valDict
                            ):
                                tmp_value = random.choice(tmp_dictCustomData_this[key_this]['value'].split('*'))
                                for tmp_value_this in tmp_value.split('[分页]'):
                                    msg = ChanceCustom.replyReg.replyValueRegTotal(
                                        tmp_value_this,
                                        valDict
                                    )
                                    if len(msg) > 0:
                                        reply(
                                            plugin_event,
                                            msg
                                        )
                            break
                    elif 'perfix' == tmp_dictCustomData_this[key_this]['matchType']:
                        if tmp_message.startswith(tmp_dictCustomData_this[key_this]['key']):
                            valDict['内容1'] = codeEscape(tmp_message[len(tmp_dictCustomData_this[key_this]['key']):])
                            if ChanceCustom.replyFilter.preFilter(
                                replyKey = tmp_dictCustomData_this[key_this]['key'],
                                replyValue = tmp_dictCustomData_this[key_this]['value'],
                                valDict = valDict
                            ):
                                tmp_value = random.choice(tmp_dictCustomData_this[key_this]['value'].split('*'))
                                for tmp_value_this in tmp_value.split('[分页]'):
                                    msg = ChanceCustom.replyReg.replyValueRegTotal(
                                        tmp_value_this,
                                        valDict
                                    )
                                    if len(msg) > 0:
                                        reply(
                                            plugin_event,
                                            msg
                                        )
                            break
                    elif 'reg' == tmp_dictCustomData_this[key_this]['matchType']:
                        res_re = re.match('^%s$' % tmp_dictCustomData_this[key_this]['key'], tmp_message)
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
                                valDict[key] = codeEscape(value)
                                count += 1
                            if ChanceCustom.replyFilter.preFilter(
                                replyKey = tmp_dictCustomData_this[key_this]['key'],
                                replyValue = tmp_dictCustomData_this[key_this]['value'],
                                valDict = valDict
                            ):
                                tmp_value = random.choice(tmp_dictCustomData_this[key_this]['value'].split('*'))
                                for tmp_value_this in tmp_value.split('[分页]'):
                                    msg = ChanceCustom.replyReg.replyValueRegTotal(
                                        tmp_value_this,
                                        valDict
                                    )
                                    if len(msg) > 0:
                                        reply(
                                            plugin_event,
                                            msg
                                        )
                            break

    if bot_hash_last != None and valDict['innerVal']['replaceReply'] != None:
        tmp_value = random.choice(valDict['innerVal']['replaceReply'].split('*'))
        for tmp_value_this in tmp_value.split('[分页]'):
            msg = ChanceCustom.replyReg.replyValueRegTotal(
                tmp_value_this,
                valDict
            )
            if len(msg) > 0:
                reply(
                    plugin_event,
                    msg
                )

    setValDictUnity(valDict)


def codeDisEscape(data):
    res = data
    for key_this in ChanceCustom.replyReg.listRegTotalDisEscape:
        res = res.replace(key_this[0], key_this[1])
    return res

def codeEscape(data):
    res = data
    for key_this in ChanceCustom.replyReg.listRegTotalEscape:
        res = res.replace(key_this[0], key_this[1])
    return res

def reply(plugin_event:OlivOS.API.Event, message:str):
    plugin_event.reply(message)

def send(plugin_event:OlivOS.API.Event, send_type:str, target_id:str, message:str, host_id:'str|None' = None):
    plugin_event.send(send_type, target_id, message, host_id = host_id)
