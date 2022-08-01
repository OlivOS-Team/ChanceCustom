import OlivOS
import ChanceCustom

import re
from string import digits
import operator

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
                elif c == '-' and self.string[k-1] in Symbol._BINARY_OPERATOR:
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
    while token:
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
            ChanceCustom.replyBase.getCharRegTatol(resDict, '计算公式', '0', groupDict, valDict)
            expr = resDict['计算公式']
            try:
                res = str(customEval(Lexer(expr).tokenGenerator()))
            except:
                res = str(float('nan'))
            return res
        return evalExpr_f
    return evalExprFun
