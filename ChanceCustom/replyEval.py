import OlivOS
import ChanceCustom

import re
from string import digits
import operator
import hashlib
import random
import requests

OPERATORS = {}
PRIORITY = {}

def addOperator(*names_and_prios):
    def add(fn):
        for name, priority in names_and_prios:
            OPERATORS[name] = fn
            PRIORITY[name] = priority
        return fn
    return add

@addOperator(('+', 10))
def operatorAdd(x, y):
    return operator.add(x, y)

@addOperator(('-', 10))
def operatorSub(x, y):
    return operator.sub(x, y)

@addOperator(('/', 11), ('÷', 11))
def operatorDiv(x, y):
    try:
        return operator.truediv(x, y)
    except ZeroDivisionError:
        return float('inf')

@addOperator(('*', 11), ('×', 11))
def operatorMul(x, y):
    return operator.mul(x, y)

@addOperator(('%', 11))
def operatorMod(x, y):
    return divmod(x, y)[1]

@addOperator(('<', 9))
def operatorSLB(x, y):
    x, y = int(x), int(y)
    return operator.lshift(x, y)

@addOperator(('>', 9))
def operatorSRB(x, y):
    x, y = int(x), int(y)
    return operator.rshift(x, y)

@addOperator(('&', 8))
def operatorAnd(x, y):
    return operator.and_(x, y)

@addOperator(('|', 6))
def operatorOr(x, y):
    return operator.or_(x, y)

@addOperator(('⊕', 7))
def operatorXor(x, y):
    return operator.xor(x, y)

@addOperator(('^', 13))
def operatorPow(x, y):
    return operator.pow(x, y)

@addOperator(('\\', 11))
def operatorQuotient(x, y):
    return divmod(x, y)[0]

@addOperator(('@', 11))
def operatorRound(x, y):
    if y <= 0:
        return round(round(x, y))
    else:
        return round(x, y)

class Symbol:
    _BINARY_OPERATOR = set('+-*×/÷%\^@&|⊕<>')
    _WHITESPACE = set(' \t\n\r')
    _NUMERAL_START = set(digits) | set('.')
    _NUMERAL_END = set(digits)
    _SINGLE_CHAR_TOKENS = set('(),（），') | _BINARY_OPERATOR
    _VALID_CHAR = (_BINARY_OPERATOR | _NUMERAL_START | _NUMERAL_END)

class Lexer:
    def __init__(self, string:str):
        self.string = self.preprocess(string)

    def preprocess(self, string):
        return '(' + string.replace(' ', '').replace('<<', '<').replace('>>', '>') \
            .replace('and', '&').replace('xor', '⊕').replace('or', '|') + ')'
    
    def tokenGenerator(self):
        k = 0
        def getNextToken():
            nonlocal k
            minus = False
            while k < len(self.string):
                c = self.string[k]
                if c in Symbol._WHITESPACE:
                    k += 1
                elif c == '-' and self.string[k-1] in Symbol._BINARY_OPERATOR | set('(（'):
                    minus = True
                    k += 1
                elif c in Symbol._SINGLE_CHAR_TOKENS:
                    k += 1
                    return c
                else:
                    i = k
                    number= False
                    while i < len(self.string):
                        char = self.string[i]
                        if not number and char in Symbol._NUMERAL_START:
                            number = True
                            i += 1
                        elif number and char in (Symbol._SINGLE_CHAR_TOKENS | Symbol._WHITESPACE):
                            number = False
                            token = self.string[k:i]
                            if '.' in token:
                                token = float(token)
                            else:
                                token = int(token)
                            k = i
                            if minus:
                                minus = False
                                return -token
                            else:
                                return token
                        else:
                            i += 1
        return getNextToken

def customEval(get_one_token):
    operator_stack = []
    operand_stack = []
    token = get_one_token()
    while token or (type(token) == int and token == 0):
        if isinstance(token, (int, float)):
            operand_stack.append(token)
        elif token in Symbol._BINARY_OPERATOR:
            if not len(operator_stack):
                operator_stack.append(token)
            else:
                operator = operator_stack.pop()
                if PRIORITY[token] > PRIORITY[operator]:
                    right = get_one_token()
                    if right in set('(（'):
                        right = customEval(get_one_token)
                    left = operand_stack.pop()
                    operand_stack.append(OPERATORS[token](left, right))
                    operator_stack.append(operator)
                else:
                    right = operand_stack.pop()
                    left = operand_stack.pop()
                    operand_stack.append(OPERATORS[operator](left, right))
                    operator_stack.append(token)        
        elif token in set('(（'):
            operand_stack.append(customEval(get_one_token))
        elif token in set(')）'):
            if not operator_stack and len(operand_stack) == 1:
                return operand_stack[0]
            operator = operator_stack.pop()
            right = operand_stack.pop()
            left = operand_stack.pop()
            return OPERATORS[operator](left, right)
        elif token in ',，':
            operator = operator_stack.pop()
            right = operand_stack.pop()
            left = operand_stack.pop()
            operand_stack.append(OPERATORS[operator](left, right))
        token = get_one_token()
    if not operator_stack and len(operand_stack) == 1:
        return operand_stack[0]
    operator = operator_stack.pop()
    right = operand_stack.pop()
    left = operand_stack.pop()
    return OPERATORS[operator](left, right)

def evalExprFunTemp():
    def evalExprFun(valDict):
        def evalExpr_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '计算公式', '0', groupDict, valDict)
            expr = resDict['计算公式']
            try:
                res = str(customEval(Lexer(expr).tokenGenerator()))
            except:
                res = str(float('nan'))
            return res
        return evalExpr_f
    return evalExprFun

def baseConvFunTmp():
    def encode(num, base):
        base_table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/'
        result = []
        while num > 0:
            result.append(base_table[num%base])
            num //= base
        return ''.join(reversed(result))
    def decode(num_str, base):
        num_str = num_str.replace('-', '+').replace('_', '/')
        base_table = {
            "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15, "g": 16,
            "h": 17, "i": 18, "j": 19, "k": 20, "l": 21, "m": 22, "n": 23,
            "o": 24, "p": 25, "q": 26, "r": 27, "s": 28, "t": 29, "u": 30,
            "v": 31, "w": 32, "x": 33, "y": 34, "z": 35,
            "A": 36, "B": 37, "C": 38, "D": 39, "E": 40, "F": 41, "G": 42,
            "H": 43, "I": 44, "J": 45, "K": 46, "L": 47, "M": 48, "N": 49,
            "O": 50, "P": 51, "Q": 52, "R": 53, "S": 54, "T": 55, "U": 56,
            "V": 57, "W": 58, "X": 59, "Y": 60, "Z": 61,
            "+": 62, "/": 63
        }
        result = 0
        for i in range(len(num_str)):
            result = result * base + base_table[num_str[i]]
        return result
    def baseConvFun(valDict):
        def baseConv_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '待转化数值', '0', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '原数值进制', '10', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '目标进制', '10', groupDict, valDict)
            table = {'二': 2, '四': 4, '八': 8, '十': 10, '十六': 16, '三十二': 32, '六十四': 64}
            src_base = resDict['原数值进制']
            dst_base = resDict['目标进制']
            src_base = int(src_base) if src_base.isdigit() else table.get(src_base, 10)
            dst_base = int(dst_base) if dst_base.isdigit() else table.get(dst_base, 10)
            res = encode(decode(resDict['待转化数值'], src_base), dst_base)
            return res
        return baseConv_f
    return baseConvFun

def splitSortFunTemp(type="sort"):
    def splitSortFun(valDict):
        def splitSort_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            splited_text = []
            ChanceCustom.replyBase.getCharRegTotal(resDict, '排序文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '分割符号', '\n', groupDict, valDict)
            delimiter = resDict['分割符号']
            if type == 'shuffle':
                splited_text = resDict['排序文本'].split(delimiter)
                random.shuffle(splited_text)
                res = ' '.join(splited_text)
            elif type == 'sort':
                text = resDict['排序文本']
                if text.startswith('-数字'):
                    try:
                        splited_text = map(int, text[3:].split(delimiter))
                    except:
                        splited_text = text[3:].split(delimiter)
                else:
                    splited_text = text.split(delimiter)
                ChanceCustom.replyBase.getCharRegTotal(resDict, '排序正逆', '正序', groupDict, valDict)
                if resDict['排序正逆'] == '正序':
                    res = ' '.join(map(str, sorted(splited_text)))
                else:
                    res = ' '.join(map(str, sorted(splited_text, reverse=True)))
            elif type == 'split':
                ChanceCustom.replyBase.getCharRegTotal(resDict, '依据序号', '1', groupDict, valDict)
                ChanceCustom.replyBase.getCharRegTotal(resDict, '排序正逆', '正序', groupDict, valDict)
                if resDict['排序文本'].startswith('-数字'):
                    sortByValFlag = True
                    lines = resDict['排序文本'][3:].split('\n')
                    dataTable = [line.split(delimiter) for line in lines]
                else:
                    sortByValFlag = False
                    lines = resDict['排序文本'].split('\n')
                    dataTable = [line.split(delimiter) for line in lines]
                length = len(dataTable[0])
                indexNum = int(resDict['依据序号']) if resDict['依据序号'].isdigit() else 1
                reverseFlag = True if resDict['排序正逆'] == '逆序' else False

                if length < indexNum:
                    res = '依据序号大于数据个数'
                elif any(length != len(row) for row in dataTable):
                    res = '每行数据个数不一致'
                else:
                    dataMap = {row[indexNum - 1]: line for row, line in zip(dataTable, lines)}
                    if sortByValFlag:
                        try:
                            sortedDataList = sorted(dataMap.items(), key=lambda x: int(x[0]), reverse=reverseFlag)
                        except:
                            sortedDataList = sorted(dataMap.items(), key=lambda x: x[0], reverse=reverseFlag)
                    else:
                        sortedDataList = sorted(dataMap.items(), key=lambda x: x[0], reverse=reverseFlag)
                    res = '\n'.join(map(lambda x: x[1], sortedDataList))
            return res
        return splitSort_f
    return splitSortFun

def wordCountFunTemp():
    def wordCountFun(valDict):
        def wordCount_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被统计文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '统计出现的文本', '', groupDict, valDict)
            pattern = resDict['统计出现的文本']
            if not pattern:
                res = '0'
            else:
                res = str(resDict['被统计文本'].count(pattern))
            return res
        return wordCount_f
    return wordCountFun

def getMD5FunTemp():
    def readFile(path):
        try:
            with open(path, 'rb') as f:
                return f.read()
        except:
            return ''
    def readOnlineFile(url):
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                return res.content
            else:
                raise
        except:
            return ''
    def getMD5Fun(valDict):
        def getMD5_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '被取目标', '', groupDict, valDict)
            ChanceCustom.replyBase.getNumRegTotal(resDict, 'MD5位数', 32, groupDict, valDict)
            CQ_code_pattern = r'^\[CQ:[a-z]+(?P<file>,file=.*?)?(?P<url>,url=.*?)?(,.*)?\]$'
            url_pattern = r'^(https?:\/\/)?(\w+\.)+\w{3}(:\d+)?(\/\w+)*(\.\w+)?$'
            file_pattern = r'^([A-Z]:)?\.?((\/|\\)\w+)+(\.\w+)?$'
            context = resDict['被取目标']
            content = ''
            if re.match(CQ_code_pattern, context):
                file_or_url = re.match( CQ_code_pattern, context).groupdict()
                file, url = file_or_url['file'], file_or_url['url']
                if file[6:13] == 'file://' and re.match(file_pattern, file[13:]):
                    content = readFile(file[13:])
                elif file and re.match(url_pattern, file[6:]):
                    content = readOnlineFile(file[6:])
                elif url and re.match(url_pattern, url[5:]):
                    content = readOnlineFile(url[5:])
            elif re.match(file_pattern, context):
                content = readFile(context)
            elif re.match(url_pattern, context):
                content = readOnlineFile(context)
            else:
                content = context    
            md = hashlib.md5()
            try:
                if not content:
                    res = '出现错误'
                elif isinstance(content, bytes):
                    md.update(content)
                    res = md.hexdigest()[:resDict['MD5位数']].upper()
                else:
                    md.update(content.encode('utf-8'))
                    res += md.hexdigest()[:resDict['MD5位数']].upper()
            except:
                res = '出现错误'
            return res
        return getMD5_f
    return getMD5Fun


def charPaddingFunTemp():
    def charPaddingFun(valDict):
        def charPadding_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '待补位文本', '', groupDict, valDict)
            ChanceCustom.replyBase.getCharRegTotal(resDict, '结尾/开头', '', groupDict, valDict)
            ChanceCustom.replyBase.getNumRegTotal(resDict, '结果长度', 0, groupDict, valDict)
            ChanceCustom.replyBase.getCharRaw(resDict, '补位字符', ' ', groupDict)
            text = resDict['待补位文本']
            dst_text_length = resDict['结果长度']
            char = resDict['补位字符']
            offset = dst_text_length - len(text)
            if offset < 0:
                res = text
            else:
                
                if resDict['结尾/开头'] == '开头':
                    res = (char * offset)[:offset] + text
                elif resDict['结尾/开头'] == '结尾':
                    res =  text + (char * offset)[:offset]
                else:
                    res = text
            return res
        return charPadding_f
    return charPaddingFun
