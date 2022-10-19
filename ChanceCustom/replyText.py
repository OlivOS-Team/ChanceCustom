import OlivOS
import ChanceCustom

import re


def str2int(intStr, default=0):
    try:
        return int(intStr)
    except:
        return default

def extractCharFunTemp(type):
    def extractCharFun(valDict):
        def extractChar_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTatol(resDict, '被取文本', '', groupDict, valDict)
            if type == 'order':
                ChanceCustom.replyBase.getCharRegTatol(resDict, '开始位置', '1', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTatol(resDict, '取出长度', '0', groupDict, valDict)
                beginIdex = max(str2int(resDict['开始位置']) - 1, 0)
                endIndex = beginIdex + str2int(resDict['取出长度'])
                res = resDict['被取文本'][beginIdex:endIndex]
            elif type == 'replace':
                ChanceCustom.replyBase.getCharRegTatol(resDict, '右边文本', '', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTatol(resDict, '左边文本', '', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTatol(resDict, '替换文本', '', groupDict, valDict)
                text = resDict['被取文本']
                leftIndex = text.find(resDict['左边文本'])
                rightIndex = text.find(resDict['右边文本']) + len(resDict['右边文本'])
                res = text[:leftIndex] + resDict['替换文本'] + text[rightIndex:]
            elif type == 'reverse':
                ChanceCustom.replyBase.getCharRegTatol(resDict, '右边文本', '', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTatol(resDict, '左边文本', '', groupDict, valDict)
                text = resDict['被取文本']
                leftIndex = text.find(resDict['左边文本'])
                rightIndex = text.find(resDict['右边文本']) + len(resDict['右边文本'])
                res = text[leftIndex:rightIndex][::-1]
            elif type == 'len':
                res = str(len(resDict['被取文本']))
            elif type == 'left':
                ChanceCustom.replyBase.getCharRegTatol(resDict, '取出长度', '0', groupDict, valDict)
                res = resDict['被取文本'][:str2int(resDict['取出长度'])]
            elif type == 'right':
                ChanceCustom.replyBase.getCharRegTatol(resDict, '取出长度', '0', groupDict, valDict)
                res = resDict['被取文本'][-str2int(resDict['取出长度']):]
            elif type == 'searchL':
                ChanceCustom.replyBase.getCharRegTatol(resDict, '被寻内容', '', groupDict, valDict)
                text = resDict['被取文本']
                index = text.find(resDict['被寻内容'])
                if index == -1:
                    res = '未找到指定内容'
                else:
                    res = text[:index]
            elif type == 'searchR':
                ChanceCustom.replyBase.getCharRegTatol(resDict, '被寻内容', '', groupDict, valDict)
                text = resDict['被取文本']
                index = text.find(resDict['被寻内容']) + len(resDict['被寻内容'])
                if text.find(resDict['被寻内容']) == -1:
                    res = '未找到指定内容'
                else:
                    res = text[:index]
            return res
        return extractChar_f
    return extractCharFun

def toggleCaseFunTemp(type):
    def toggleCaseFun(valDict):
        def toggleCase_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTatol(resDict, '转换文本', '', groupDict, valDict)
            if type == 'upper':
                res = resDict['转换文本'].upper()
            elif type == 'lower':
                res = resDict['转换文本'].lower()
            return res
        return toggleCase_f
    return toggleCaseFun

def searchTextFunTemp(reversed=False):
    def searchTextFun(valDict):
        def searchText_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTatol(resDict, '被寻文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '欲寻内容', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '开始位置', '1', groupDict, valDict)
            text = resDict['被寻文本']
            if not reversed:
                res = str(text[str2int(resDict['开始位置']) - 1:].find(resDict['欲寻内容']) + 1)
            else:
                res = str(text[::-1][str2int(resDict['开始位置']) - 1:].find(resDict['欲寻内容'][::-1]) + 1)
            if res == '0':
                res = '未找到指定内容'
            return res
        return searchText_f
    return searchTextFun

def reverseTextFunTemp():
    def reverseTextFun(valDict):
        def reverseText_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTatol(resDict, '反转文本', '', groupDict, valDict)
            res = resDict['反转文本'][::-1]
            return res
        return reverseText_f
    return reverseTextFun

def replaceTextFunTemp():
    def replaceTextFun(valDict):
        def replaceText_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTatol(resDict, '被替文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '开始位置', '1', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '替换长度', '0', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTatol(resDict, '替换文本', '', groupDict, valDict)
            text = resDict['被替文本']
            startIndex = max(str2int(resDict['开始位置']) - 1, 0)
            endIndex = startIndex + str2int(resDict['替换长度'])
            res = text[:startIndex] + resDict['替换文本'] + text[endIndex:]
            return res
        return replaceText_f
    return replaceTextFun


def textStripFunTemp():
    def textStripFun(valDict):
        def textStrip_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTatol(resDict, '被删文本', '', groupDict, valDict)
            text = resDict['被删文本']
            if text.startswith('-'):
                type = resDict['被删文本'][1]
                text = resDict['被删文本'][2:]
                if type == '首':
                    res = text.lstrip()
                elif type == '尾':
                    res = text.rstrip()
            else:
                res = text.strip()
            return res
        return textStrip_f
    return textStripFun
