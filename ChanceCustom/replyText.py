'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyText.py
@Author    :   Fitz161
@Contact   :   
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re
import random
from math import ceil

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
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被取文本', '', groupDict, valDict)
            if type == 'order':
                ChanceCustom.replyBase.getCharRegTotal(resDict, '开始位置', '1', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTotal(resDict, '取出长度', '0', groupDict, valDict)
                beginIdex = max(str2int(resDict['开始位置']) - 1, 0)
                endIndex = beginIdex + str2int(resDict['取出长度'])
                res = resDict['被取文本'][beginIdex:endIndex]
            elif type == 'replace':
                ChanceCustom.replyBase.getCharRegTotal(resDict, '右边文本', '', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTotal(resDict, '左边文本', '', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTotal(resDict, '替换文本', '', groupDict, valDict)
                text = resDict['被取文本']
                leftIndex = text.find(resDict['左边文本'])
                rightIndex = text.find(resDict['右边文本']) + len(resDict['右边文本'])
                res = text[:leftIndex] + resDict['替换文本'] + text[rightIndex:]
            elif type == 'reverse':
                ChanceCustom.replyBase.getCharRegTotal(resDict, '右边文本', '', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTotal(resDict, '左边文本', '', groupDict, valDict)
                text = resDict['被取文本']
                leftIndex = text.find(resDict['左边文本'])
                rightIndex = text.find(resDict['右边文本']) + len(resDict['右边文本'])
                res = text[leftIndex:rightIndex][::-1]
            elif type == 'len':
                res = str(len(resDict['被取文本']))
            elif type == 'left':
                ChanceCustom.replyBase.getCharRegTotal(resDict, '取出长度', '0', groupDict, valDict)
                res = resDict['被取文本'][:str2int(resDict['取出长度'])]
            elif type == 'right':
                ChanceCustom.replyBase.getCharRegTotal(resDict, '取出长度', '0', groupDict, valDict)
                res = resDict['被取文本'][-str2int(resDict['取出长度']):]
            elif type == 'searchL':
                ChanceCustom.replyBase.getCharRegTotal(resDict, '被寻内容', '', groupDict, valDict)
                text = resDict['被取文本']
                index = text.find(resDict['被寻内容'])
                if index == -1:
                    res = '未找到指定内容'
                else:
                    res = text[:index]
            elif type == 'searchR':
                ChanceCustom.replyBase.getCharRegTotal(resDict, '被寻内容', '', groupDict, valDict)
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
            ChanceCustom.replyBase.getCharRegTotal(resDict, '转换文本', '', groupDict, valDict)
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
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被寻文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '欲寻内容', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '开始位置', '1', groupDict, valDict)
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
            ChanceCustom.replyBase.getCharRegTotal(resDict, '反转文本', '', groupDict, valDict)
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
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被替文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '开始位置', '1', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换长度', '0', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换文本', '', groupDict, valDict)
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
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被删文本', '', groupDict, valDict)
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

def deleteLineFunTemp(type):
    def deleteLineFun(valDict):
        def deleteLine_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被删文本', '', groupDict, valDict)
            
            if type == 'blank':
                str.isspace()
                lines = resDict['被删文本'].split('\n')
                res = '\n'.join(filter(lambda line: line != '' and not line.isspace(), lines))
            elif type == 'repeat':
                lines = resDict['被删文本'].split('\n')
                visitedLines = []
                for line in lines:
                    if line in visitedLines:
                        continue
                    visitedLines.append(line)
                res = '\n'.join(visitedLines)
            elif type == 'fix':
                ChanceCustom.replyBase.getCharRegTotal(resDict, '开头行序', '-1', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTotal(resDict, '结尾行序', '-1', groupDict, valDict)
                lines = resDict['被删文本'].split('\n')
                startIndex = max(str2int(resDict['开头行序'], 1) - 1, 0)
                endIndex = min(str2int(resDict['结尾行序'], 1) - 1, len(lines) - 1)
                del lines[startIndex:endIndex+1]
                res = '\n'.join(lines)
            return res
        return deleteLine_f
    return deleteLineFun

def lineStripFunTemp():
    def lineStripFun(valDict):
        def lineStrip_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被删文本', '', groupDict, valDict)
            text = resDict['被删文本']
            if text.startswith('-'):
                type = resDict['被删文本'][1]
                text = resDict['被删文本'][2:]
                if type == '首':
                    res = '\n'.join(map(str.lstrip, text.split('\n')))
                elif type == '尾':
                    res = '\n'.join(map(str.rstrip, text.split('\n')))
            else:
                res = '\n'.join(map(str.strip, text.split('\n')))
            return res
        return lineStrip_f
    return lineStripFun

def replaceLineFunTemp():
    def replaceLineFun(valDict):
        def replaceLine_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被替文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '开头行序', '1', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '结尾行序', '1', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换文本', '', groupDict, valDict)
            
            lines = resDict['被替文本'].split('\n')
            startIndex = max(str2int(resDict['开头行序'], 1) - 1, 0)
            endIndex = min(str2int(resDict['结尾行序'], 1) - 1, len(lines) - 1)
            lines[startIndex:endIndex+1] = resDict['替换文本'].split('\n')
            res = '\n'.join(lines)
            return res
        return replaceLine_f
    return replaceLineFun

def insertTextFunTemp():
    def insertTextFun(valDict):
        def insertText_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被插文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '插入内容', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '行数', '1', groupDict, valDict)
            if resDict['行数'].isdigit():
                pos = int(resDict['行数']) - 1
                lines = resDict['被插文本'].split('\n')
                lines.insert(pos, resDict['插入内容'])
                res = '\n'.join(lines)
            else:
                res = resDict['被插文本']
            return res
        return insertText_f
    return insertTextFun

def splitTextByLengthFunTemp():
    def splitTextByLengthFun(valDict):
        def splitTextByLength_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被拆文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '每行字数', '1', groupDict, valDict)
            if resDict['每行字数'].isdigit():
                lines = []
                limit = int(resDict['每行字数'])
                text = resDict['被拆文本']
                for i in range(ceil(len(text) // limit)):
                    lines.append(text[limit*i:limit*(i+1)])
                res = '\n'.join(lines)
            else:
                res = resDict['被拆文本']
            return res
        return splitTextByLength_f
    return splitTextByLengthFun

def concatTextFunTemp():
    def concatTextFun(valDict):
        def concatText_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被连文本1', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被连文本2', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '连接字符', ' ', groupDict, valDict)
            symbol = resDict['连接字符']
            lines1 = resDict['被连文本1'].split('\n')
            lines2 = resDict['被连文本2'].split('\n')

            concatedLines = [f'{line1}{symbol}{line2}' for line1, line2 in zip(lines1, lines2)]
            if len(concatedLines) < len(lines1):
                concatedLines.extend(lines1[len(concatedLines):])
            elif len(concatedLines) < len(lines2):
                concatedLines.extend(lines2[len(concatedLines):])
            res = '\n'.join(concatedLines)
            return res
        return concatText_f
    return concatTextFun

def sortByFirstLetterFunTemp():
    def sortByFirstLetterFun(valDict):
        def sortByFirstLetter_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被排文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '排序顺逆', '', groupDict, valDict)
            lines = resDict['被排文本'].split('\n')
            if resDict['排序顺逆'] == '逆序':
                lines.sort(reverse=True)
            else:
                lines.sort()
            res = '\n'.join(lines)
            return res
        return sortByFirstLetter_f
    return sortByFirstLetterFun

def reverseContentFunTemp(type):
    def reverseContentFun(valDict):
        def reverseContent_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被转文本', '', groupDict, valDict)
            lines = resDict['被转文本'].split('\n')
            if type == 'char':
                lines = list(map(''.join, map(reversed, lines)))
            elif type == 'line':
                lines.reverse()
            res = '\n'.join(lines)
            return res
        return reverseContent_f
    return reverseContentFun

def splitTextByLinesFunTemp():
    def splitTextByLinesFun(valDict):
        def splitTextByLines_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被分页文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '每页行数', '1', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '分页', '[分页]', groupDict, valDict)
            lines = resDict['被分页文本'].split('\n')
            lineNumPerPage = int(resDict['每页行数']) if resDict['每页行数'].isdigit() else 1
            page = []
            pages = []
            for index, line in enumerate(lines):
                if index % lineNumPerPage == 0 and index != 0:
                    pages.append('\n'.join(page))
                    page = [line]
                else:
                    page.append(line) 
            pages.append('\n'.join(page))
            res = resDict['分页'].join(pages)
            return res
        return splitTextByLines_f
    return splitTextByLinesFun

def retrieveTextByLineIndexFunTemp():
    def retrieveTextByLineIndexFun(valDict):
        def retrieveTextByLineIndex_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被取文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '开头行序', '1', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '结尾行序', '1', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '取出类型', '', groupDict, valDict)
            
            lines = resDict['被取文本'].split('\n')
            startIndex = max(str2int(resDict['开头行序'], 1) - 1, 0)
            endIndex = min(str2int(resDict['结尾行序'], 1), len(lines) - 1)
            retrieveType = resDict['取出类型']
            if  retrieveType == '[取出所有]':
                res = '\n'.join(lines[startIndex:endIndex])
            elif retrieveType.startswith('[随机取'):
                if retrieveType[4:] == '出]':
                    res = random.choice(lines)
                else:
                    res = '\n'.join(random.sample(lines, str2int(retrieveType[4:-1], 1)))
            elif retrieveType[3] == '前':
                res = '\n'.join(lines[startIndex:startIndex + str2int(retrieveType[4:-1], 0)])
            elif retrieveType[3] == '后':
                res = '\n'.join(lines[endIndex - str2int(retrieveType[4:-1], 0):endIndex])    
            return res
        return retrieveTextByLineIndex_f
    return retrieveTextByLineIndexFun

def addTextForEachLineFunTemp():
    def insertIntoStrHelperFun(pattern, text, type):
        def insertIntoStr(string):
            if type == 'asc':
                index = string.find(pattern)
                if index == -1:
                    return string
            elif type == 'des':
                index = string.find(pattern)
                if index == -1:
                    return string
                else:
                    index += len(pattern)
            else:
                index = str2int(pattern, 1) - 1
            return string[:index] + text + string[index:]
        return insertIntoStr
    def addTextForEachLineFun(valDict):
        def addTextForEachLine_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被添文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '添加类型', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '添加参数', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '添加文本', '', groupDict, valDict)
            lines = resDict['被添文本'].split('\n')
            addType = resDict['添加类型']

            if addType == '[文本之前]':
                pattern = resDict['添加参数']
                res = '\n'.join(map(insertIntoStrHelperFun(pattern, resDict['添加文本'], 'asc'), lines))
            elif addType == '[文本之后]':
                pattern = resDict['添加参数']
                res = '\n'.join(map(insertIntoStrHelperFun(pattern, resDict['添加文本'], 'des'), lines))
            elif addType == '[某位置前]':
                pattern = resDict['添加参数']
                res = '\n'.join(map(insertIntoStrHelperFun(pattern, resDict['添加文本'], 'order'), lines))  
            return res
        return addTextForEachLine_f
    return addTextForEachLineFun

def replaceTextForEachLineFunTemp():
    def replaceStrHelperFun(patternL, patternR, text, type):
        def replaceStr(string):
            if type == 'mid':
                if string.find(patternL) == -1 or string.find(patternR) == -1:
                    return string
                leftIndex = string.find(patternL) + len(patternL)
                rightIndex = string.find(patternR)
            elif type == 'edge':
                if patternL == '[文本之前]':
                    if string.find(patternR) == -1:
                        return string
                    leftIndex = 0
                    rightIndex = string.find(patternR)
                elif patternL == '[文本之后]':
                    if string.find(patternR) == -1:
                        return string
                    leftIndex = string.find(patternR) + len(patternR)
                    rightIndex = len(string)
            else:
                leftIndex = max(str2int(patternL, 1), 0)
                rightIndex = str2int(patternR, 1) - 1
            return string[:leftIndex] + text + string[rightIndex:]
        return replaceStr
    def replaceTextForEachLineFun(valDict):
        def replaceTextForEachLine_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被替文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换类型', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换参数1', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换参数2', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换文本', '', groupDict, valDict)
            lines = resDict['被替文本'].split('\n')
            addType = resDict['替换类型']
            patternLeft = resDict['替换参数1']
            patternRight = resDict['替换参数2']
            if addType == '[文本之间]':
                res = '\n'.join(map(replaceStrHelperFun(patternLeft, patternRight, resDict['替换文本'], 'mid'), lines))
            elif addType == '[位置之间]':
                res = '\n'.join(map(replaceStrHelperFun(patternLeft, patternRight, resDict['替换文本'], 'index'), lines))
            elif addType == '[文本前后]':
                res = '\n'.join(map(replaceStrHelperFun(patternLeft, patternRight, resDict['替换文本'], 'edge'), lines))
            return res
        return replaceTextForEachLine_f
    return replaceTextForEachLineFun

def hideResultFunTemp():
    def hideResultFun(valDict):
        def hideResult_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            return res
        return hideResult_f
    return hideResultFun

def splitAndSelectFunTemp():
    def splitAndSelectFun(valDict):
        def splitAndSelect_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被分割文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '分隔符', '\n', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '取出序号', '0', groupDict, valDict)
            delimiter = resDict['分隔符']
            splited_text = resDict['被分割文本'].split(delimiter)
            selectType = str2int(resDict['取出序号'])
            if selectType == 0:
                res = random.choice(splited_text)
            elif selectType > 0:
                res = splited_text[min(selectType, len(splited_text)) - 1]
            else:
                res = splited_text[max(selectType, -len(splited_text))]
            return res
        return splitAndSelect_f
    return splitAndSelectFun

def roundNumberFunTemp():
    def str2float(floatStr, default=.0):
        try:
            return float(floatStr)
        except:
            return default
    def roundNumberFun(valDict):
        def roundNumber_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '数值', '0', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '下界', None, groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '上界', None, groupDict, valDict)
            upperBound = str2float(resDict['上界'], float('inf'))
            lowerBound = str2float(resDict['下界'], -float('inf'))
            val = max(min(str2float(resDict['数值']), upperBound), lowerBound)
            res = str(int(val)) if val == int(val) else str(val)
            return res
        return roundNumber_f
    return roundNumberFun

def filterNumberFunTemp():
    def filterNumberFun(valDict):
        def filterNumber_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被取文本', '', groupDict, valDict)
            numbers = []
            for c in resDict['被取文本']:
                if c.isdigit():
                    numbers.append(c)
            res = ''.join(numbers)
            return res
        return filterNumber_f
    return filterNumberFun

def selectMiddleFunTemp():
    def selectMiddleFun(valDict):
        def selectMiddle_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            
            ChanceCustom.replyBase.getCharRegTotal(resDict, 'XX1', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, 'XX2', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, 'XX3', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, 'XX4', '', groupDict, valDict)
            text = resDict['XX1']
            leftText = resDict['XX2']
            rightText = resDict['XX3']
            selectType = resDict['XX4']

            pattern = leftText + '(.*?)' + rightText
            candidates = re.findall(pattern, text)

            if selectType == '':
                if candidates is []:
                    candidates.append('')
                res = random.choice(candidates)
            elif selectType.isdigit():
                res = candidates[min(len(candidates), str2int(selectType)) - 1]
            elif selectType.startswith('all'):
                delimeter = selectType[3:]
                if delimeter is '':
                    for i, candidate in enumerate(candidates):
                        res += f'{i+1}.{candidate} '
                    res = res[:-1]
                else:
                    res = delimeter.join(candidates)
            elif selectType.startswith('top'):
                limit = str2int(selectType[3:], 1)
                res = ' '.join(candidates[:limit])
            elif selectType.startswith('bot'):
                limit = str2int(selectType[3:], 1)
                res = ' '.join(candidates[-limit:]) 
            return res
        return selectMiddle_f
    return selectMiddleFun

def regExpRefactorFunTemp():
    def regExpRefactorFun(valDict):
        def regExpRefactor_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '重构文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '表达式', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '重构格式', '', groupDict, valDict)
            pattern = resDict['表达式']
            text = resDict['重构文本']
            match = re.search(pattern, text)

            if match is None:
                res = ''
            elif resDict['重构格式'].startswith('匹配') and len(resDict['重构格式']) > 2:
                selectType = str2int(resDict['重构格式'][2:]) - 1
                sub_matches = re.search(pattern, text).groups()
                if 0 < selectType < len(sub_matches) + 1:
                    res = sub_matches[selectType - 1]
            else:
                res = match.group()
            return res
        return regExpRefactor_f
    return regExpRefactorFun

def regExpReplaceFunTemp():
    def regExpReplaceFun(valDict):
        def regExpReplace_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '表达式', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被搜索的文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '序次', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换文本', None, groupDict, valDict)
            text = resDict['被搜索的文本']
            pattern = re.compile(resDict['表达式'])
            matched_items = pattern.findall(text)
            new_exp = resDict['替换文本']
            selectType = resDict['序次']

            if new_exp is None: 
                if len(matched_items) == 0:
                    res = ''
                elif selectType == '':
                    res = random.choice(matched_items)
                elif selectType.isdigit():
                    res = matched_items[min(len(matched_items), str2int(selectType)) - 1]
                elif selectType.startswith('all'):
                    delimeter = selectType[3:]
                    if delimeter is '':
                        for i, item in enumerate(matched_items):
                            res += f'{i+1}.{item} '
                        res = res[:-1]
                    else:
                        res = delimeter.join(matched_items)
                elif selectType.startswith('top'):
                    limit = str2int(selectType[3:], 1)
                    res = ' '.join(matched_items[:limit])
                elif selectType.startswith('bot'):
                    limit = str2int(selectType[3:], 1)
                    res = ' '.join(matched_items[-limit:])
            else:
                res = re.sub(pattern, new_exp, text, count=max(0, str2int(resDict['序次'])))
            return res
        return regExpReplace_f
    return regExpReplaceFun

def subRegExpFunTemp():
    def subRegExpFun(valDict):
        def subRegExp_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '表达式', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被搜索的文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '序次', '1', groupDict, valDict)
            text = resDict['被搜索的文本']
            pattern = re.compile(resDict['表达式'])
            match = re.search(pattern, text)
            selectType = str2int(resDict['序次'])

            if match is None:
                res = ''
            elif selectType == 0:
                res = match.group()
            else:
                sub_matches = match.groups()
                if 0 < selectType < len(sub_matches) + 1:
                    res = sub_matches[selectType - 1]
                else:
                    res = sub_matches[0]
            return res
        return subRegExp_f
    return subRegExpFun

def deleteTextFunTemp():
    def deleteTextFun(valDict):
        def deleteText_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '欲被删除文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '删除文本开头', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '删除文本结尾', '', groupDict, valDict)
            text = resDict['欲被删除文本']
            pattern = re.compile(resDict['删除文本开头'] + '.*?' + resDict['删除文本结尾'])
            res = re.sub(pattern, '', text, count=0)
            return res
        return deleteText_f
    return deleteTextFun

def switchAndReturnFunTemp():
    def switchAndReturnFun(valDict):
        def switchAndReturn_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '序号或逻辑组', None, groupDict, valDict)
            ChanceCustom.replyBase.getDataRaw(resDict, '...', None, groupDict)
            case = resDict['序号或逻辑组']
            cases = resDict['...']
            if None == case or None == cases or 0 == len(cases):
                res = ''
            elif case.find('||') != -1:
                logic_exps = case.split('||')
                flag = False
                for i, logic_exp in enumerate(logic_exps):
                    if logic_exp == '真':
                        res = cases[i] if len(cases) > i else ''
                        flag = True
                        break
                if not flag:
                    res = cases[-1] if len(cases) > 0 else ''
            else:
                res = cases[max(min(str2int(case) - 1, len(cases)), 0)]
            return res
        return switchAndReturn_f
    return switchAndReturnFun

def replaceFunTemp():
    def replaceFun(valDict):
        def replace_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被替换内容', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被替换文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '替换次数', '-1', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '并列替换', '', groupDict, valDict)
            text = resDict['被替换内容']
            count = str2int(resDict['替换次数'])
            pattern = resDict['被替换文本']
            repl = resDict['替换文本']
            if resDict['并列替换'] != '[并列]':
                res = text.replace(pattern, repl, count)
            else:
                patterns = pattern.split('||')
                replaces = repl.split('||')
                if len(patterns) != len(replaces):
                    res = text.replace(pattern, repl, count)
                else:
                    for pattern, repl in zip(patterns, replaces):
                        text = text.replace(pattern, repl, count)
                    res = text
            return res
        return replace_f
    return replaceFun
