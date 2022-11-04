'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   replyWeb.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import re
import requests

WebHeader = {
    'User-Agent': '%s/ChanceCustom' % ChanceCustom.main.version
}

def httpGetPageFunTemp(type = 'UTF'):
    def httpGetPageFun(valDict):
        def httpGetPage_f(matched:'re.Match|dict'):
            groupDict = ChanceCustom.replyBase.getGroupDictInit(matched)
            res = ''
            resDict = {}
            ChanceCustom.replyBase.getCharRegTotal(resDict, '网址', None, groupDict, valDict)
            try:
                if None != resDict['网址']:
                    request_res = requests.request("GET", resDict['网址'], headers = WebHeader)
                    res_type = 'utf-8'
                    if 'UTF' == type:
                        res_type = 'utf-8'
                    elif 'GBK' == type:
                        res_type = 'gbk'
                    res = request_res.content.decode(res_type, errors = 'replace')
            except:
                res = ''
            return res
        return httpGetPage_f
    return httpGetPageFun

