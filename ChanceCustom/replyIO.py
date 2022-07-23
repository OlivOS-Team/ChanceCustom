'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyIO.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re
import configparser

def iniSetFunTemp():
    def iniSetFun(valDict):
        def iniSet_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ini = configparser.ConfigParser()
            ChanceCustom.replyBase.getCharRegTatol(resDict, '文件路径', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '配置节', None, groupDict, valDict)
            if None != resDict['配置节']:
                ChanceCustom.replyBase.getCharRegTatol(resDict, '配置项', None, groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTatol(resDict, '写入值', None, groupDict, valDict)
                try:
                    ini.read(resDict['文件路径'], encoding = 'utf-8')
                    if None != resDict['配置项']:
                        if resDict['配置节'] not in ini.sections():
                            ini.add_section(resDict['配置节'])
                        if None != resDict['写入值']:
                            ini.set(resDict['配置节'], resDict['配置项'], resDict['写入值'])
                        else:
                            ini.remove_option(resDict['配置节'], resDict['配置项'])
                    else:
                        ini.remove_section(resDict['配置节'])
                    with open(resDict['文件路径'], 'w', encoding = 'utf-8') as ini_f:
                        ini.write(ini_f, space_around_delimiters = False)
                except:
                    pass
            return res
        return iniSet_f
    return iniSetFun

def iniGetFunTemp():
    def iniGetFun(valDict):
        def iniGet_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ini = configparser.ConfigParser()
            ChanceCustom.replyBase.getCharRegTatol(resDict, '文件路径', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '配置节', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '配置项', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '默认值', '', groupDict, valDict)
            try:
                ini.read(resDict['文件路径'], encoding = 'utf-8')
                res = ini.get(resDict['配置节'], resDict['配置项'], fallback = resDict['默认值'])
            except:
                res = resDict['默认值']
            return res
        return iniGet_f
    return iniGetFun

def iniGetOptionsFunTemp():
    def iniGetOptionsFun(valDict):
        def iniGetOptions_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ini = configparser.ConfigParser()
            ChanceCustom.replyBase.getCharRegTatol(resDict, '文件路径', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '配置节', None, groupDict, valDict)
            try:
                ini.read(resDict['文件路径'], encoding = 'utf-8')
                if None != resDict['配置节']:
                    optionList = ini.items(resDict['配置节'])
                    res = '\n'.join([('%s=%s' % optionThis) for optionThis in optionList if 2 == len(optionThis)])
            except:
                pass
            return res
        return iniGetOptions_f
    return iniGetOptionsFun

def iniGetSectionFunTemp():
    def iniGetSectionFun(valDict):
        def iniGetSection_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ini = configparser.ConfigParser()
            ChanceCustom.replyBase.getCharRegTatol(resDict, '文件路径', None, groupDict, valDict)
            try:
                ini.read(resDict['文件路径'], encoding = 'utf-8')
                res = '\n'.join(ini.sections())
            except:
                pass
            return res
        return iniGetSection_f
    return iniGetSectionFun

def fileReadFunTemp():
    def fileReadFun(valDict):
        def fileRead_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTatol(resDict, '文件路径', None, groupDict, valDict)
            try:
                with open(resDict['文件路径'], 'r', encoding = 'utf-8') as file_f:
                    res = file_f.read()
            except:
                pass
            return res
        return fileRead_f
    return fileReadFun

def fileWriteFunTemp():
    def fileWriteFun(valDict):
        def fileWrite_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTatol(resDict, '欲写内容', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '文件路径', None, groupDict, valDict)
            try:
                with open(resDict['文件路径'], 'w', encoding = 'utf-8') as file_f:
                    file_f.write(resDict['欲写内容'])
            except:
                pass
            return res
        return fileWrite_f
    return fileWriteFun

