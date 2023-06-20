'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyOlivaDice.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re
import hashlib
import time

def drawFunTemp():
    def drawFun(valDict):
        def draw(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                import OlivaDiceCore
                resDict = {}
                ChanceCustom.replyBase.getCharRegTotal(resDict, '牌堆名', '', groupDict, valDict)
                ChanceCustom.replyBase.getNumRegTotal(resDict, '牌数', '1', groupDict, valDict)
                if resDict['牌数'] > 10:
                    resDict['牌数'] = 10
                if resDict['牌数'] < 1:
                    resDict['牌数'] = 1
                ChanceCustom.replyBase.getBoolRegTotal(resDict, '是否放回', '真', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTotal(resDict, '分隔符', '\n', groupDict, valDict)
                res_list = []
                plugin_event = None
                if 'plugin_event' in valDict['innerVal']:
                    plugin_event = valDict['innerVal']['plugin_event']
                for i in range(resDict['牌数']):
                    res_draw = OlivaDiceCore.drawCard.draw(
                        key_str = resDict['牌堆名'],
                        bot_hash = valDict['innerVal']['bot_hash_self'],
                        flag_need_give_back = resDict['是否放回'],
                        plugin_event = plugin_event
                    )
                    if res_draw != None:
                        for key_this in ChanceCustom.replyReg.listRegTotalEscape:
                            res_draw = res_draw.replace(key_this[0], key_this[1])
                        res_list.append(res_draw)
                if len(res_list):
                    res = resDict['分隔符'].join(res_list)
            return res
        return draw
    return drawFun

def RDFunTemp():
    def RDFun(valDict):
        def RD_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                import OlivaDiceCore
                resDict = {}
                ChanceCustom.replyBase.getCharRegTotal(resDict, '表达式', '', groupDict, valDict)

                rd_para_str = resDict['表达式']
                tmp_template_customDefault = None
                tmp_hagID = None
                if 'innerVal' in valDict and 'hag_id' in valDict['innerVal']:
                    tmp_hagID = valDict['innerVal']['hag_id']
                tmp_pc_id = valDict['innerVal']['user_id']
                tmp_pc_platform = valDict['innerVal']['platform']['platform']
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                skill_valueTable = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId = tmp_hagID)
                tmp_pcName = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, hagId = tmp_hagID)
                if tmp_pcName != None:
                    tmp_template_name = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pcName)
                    tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
                    if tmp_template != None:
                        if 'customDefault' in tmp_template:
                            tmp_template_customDefault = tmp_template['customDefault']
                rd_para = OlivaDiceCore.onedice.RD(rd_para_str, tmp_template_customDefault, valueTable = skill_valueTable)
                rd_para.roll()
                if rd_para.resError == None:
                    res = str(rd_para.resInt)
            return res
        return RD_f
    return RDFun

def JRRPFunTemp(mode = 'jrrp'):
    def JRRPFun(valDict):
        def JRRP_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            if 'OlivaDiceJoy' in ChanceCustom.load.listPlugin:
                hash_tmp = hashlib.new('md5')
                if mode == 'jrrp':
                    hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime())).encode(encoding='UTF-8'))
                elif mode == 'zrrp':
                    hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.localtime())) - 24 * 60 * 60))).encode(encoding='UTF-8'))
                elif mode == 'mrrp':
                    hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.localtime())) + 24 * 60 * 60))).encode(encoding='UTF-8'))
                hash_tmp.update(str(valDict['innerVal']['user_id']).encode(encoding='UTF-8'))
                tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
                res = str(tmp_jrrp_int)
            return res
        return JRRP_f
    return JRRPFun

def PcNameGetFunTemp():
    def PcNameGetFun(valDict):
        def PcNameGet_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                import OlivaDiceCore

                tmp_hagID = None
                if 'innerVal' in valDict and 'hag_id' in valDict['innerVal']:
                    tmp_hagID = valDict['innerVal']['hag_id']
                tmp_pc_id = valDict['innerVal']['user_id']
                tmp_pc_platform = valDict['innerVal']['platform']['platform']
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                defaultName = ChanceCustom.replyBase.getDefaultValFunTemp('发送者昵称')(valDict)({})
                if defaultName == '':
                    defaultName = '人物卡'
                res = OlivaDiceCore.pcCard.getPcNameAPI(
                    pcHash = tmp_pcHash,
                    hagId = tmp_hagID,
                    defaultName = defaultName
                )
                if res == None:
                    res = ''

            return res
        return PcNameGet_f
    return PcNameGetFun

def PcSwitchSetFunTemp():
    def PcSwitchSetFun(valDict):
        def PcSwitchSet_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                import OlivaDiceCore
                resDict = {}
                ChanceCustom.replyBase.getCharRegTotal(resDict, '目标人物卡名', '', groupDict, valDict)
                switchName = resDict['目标人物卡名']

                tmp_hagID = None
                if 'innerVal' in valDict and 'hag_id' in valDict['innerVal']:
                    tmp_hagID = valDict['innerVal']['hag_id']
                tmp_pc_id = valDict['innerVal']['user_id']
                tmp_pc_platform = valDict['innerVal']['platform']['platform']
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                OlivaDiceCore.pcCard.setPcSwitchAPI(
                    pcHash = tmp_pcHash,
                    hagId = tmp_hagID,
                    switchName = switchName
                )

            return res
        return PcSwitchSet_f
    return PcSwitchSetFun

def PcLockSetFunTemp(action = 'lock'):
    def PcLockSetFun(valDict):
        def PcLockSet_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                import OlivaDiceCore

                tmp_hagID = None
                if 'innerVal' in valDict and 'hag_id' in valDict['innerVal']:
                    tmp_hagID = valDict['innerVal']['hag_id']
                tmp_pc_id = valDict['innerVal']['user_id']
                tmp_pc_platform = valDict['innerVal']['platform']['platform']
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                defaultName = ChanceCustom.replyBase.getDefaultValFunTemp('发送者昵称')(valDict)({})
                if defaultName == '':
                    defaultName = '人物卡'
                setFlag = True
                if action == 'lock':
                    setFlag = True
                elif action == 'unlock':
                    setFlag = False
                OlivaDiceCore.pcCard.setPcLockAPI(
                    pcHash = tmp_pcHash,
                    hagId = tmp_hagID,
                    setFlag = setFlag,
                    pcName = defaultName
                )

            return res
        return PcLockSet_f
    return PcLockSetFun

def PcSkillGetFunTemp(action = 'get'):
    def PcSkillGetFun(valDict):
        def PcSkillGet_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                import OlivaDiceCore
                resDict = {}
                ChanceCustom.replyBase.getCharRegTotal(resDict, '技能名', '', groupDict, valDict)
                skillName = resDict['技能名']
                skillValue = None

                tmp_hagID = None
                if 'innerVal' in valDict and 'hag_id' in valDict['innerVal']:
                    tmp_hagID = valDict['innerVal']['hag_id']
                tmp_pc_id = valDict['innerVal']['user_id']
                tmp_pc_platform = valDict['innerVal']['platform']['platform']
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                    tmp_pc_id,
                    tmp_pc_platform
                )
                defaultName = ChanceCustom.replyBase.getDefaultValFunTemp('发送者昵称')(valDict)({})
                if defaultName == '':
                    defaultName = '人物卡'
                if action == 'get':
                    res = OlivaDiceCore.pcCard.getPcSkillAPI(
                        pcHash = tmp_pcHash,
                        skillName = skillName,
                        hagId = tmp_hagID,
                        defaultName = defaultName
                    )
                elif action == 'set':
                    ChanceCustom.replyBase.getNumRegTotal(resDict, '技能值', '0', groupDict, valDict)
                    skillValue = resDict['技能值']
                    OlivaDiceCore.pcCard.setPcSkillAPI(
                        pcHash = tmp_pcHash,
                        skillName = skillName,
                        skillValue = skillValue,
                        hagId = tmp_hagID,
                        defaultName = defaultName
                    )
                    res = ''
                if res == None:
                    res = ''
                elif type(res) == int:
                    res = str(res)

            return res
        return PcSkillGet_f
    return PcSkillGetFun

def CommandRegFunTemp():
    def CommandRegFun(valDict):
        def CommandReg_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                import OlivaDiceCore
                resDict = {}
                ChanceCustom.replyBase.getCharRegTotal(resDict, '指令前缀', '', groupDict, valDict)
                commandPrefix = resDict['指令前缀']

                if 'replyContextFliter' in OlivaDiceCore.crossHook.dictHookList \
                and len(commandPrefix) > 0:
                    OlivaDiceCore.crossHook.dictHookList['replyContextFliter'].append(commandPrefix)

            return res
        return CommandReg_f
    return CommandRegFun

def PrefixRegFunTemp():
    def PrefixRegFun(valDict):
        def PrefixReg_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            if 'OlivaDiceCore' in ChanceCustom.load.listPlugin:
                import OlivaDiceCore
                resDict = {}
                ChanceCustom.replyBase.getCharRegTotal(resDict, '屏蔽前缀', '', groupDict, valDict)
                commandPrefix = resDict['屏蔽前缀']

                if 'replyContextFliter' in OlivaDiceCore.crossHook.dictHookList \
                and len(commandPrefix) > 0:
                    OlivaDiceCore.crossHook.dictHookList['replyContextPrefixFliter'].append(commandPrefix)

            return res
        return PrefixReg_f
    return PrefixRegFun
