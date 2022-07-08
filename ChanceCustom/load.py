'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   load.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import os
import json

listPlugin = []

dictBotInfo = {}

dataVersion = 1

dictCustomData = {}

flag_open = False

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def initEmptyCustomData():
    global dictCustomData
    dictCustomData = {
        'dataVersion': dataVersion,
        'data': {}
    }

def initCheckCustomData():
    global dictCustomData
    res = True
    if 'data' not in dictCustomData:
        initEmptyCustomData()
    if 'dataVersion' not in dictCustomData:
        initEmptyCustomData()

def initCustomData(botInfo = None):
    global dictCustomData
    releaseDir('./plugin')
    releaseDir('./plugin/data')
    releaseDir('./plugin/data/ChanceCustom')
    dictCustomData_path = './plugin/data/ChanceCustom/custom.json'
    try:
        with open(dictCustomData_path, 'r', encoding = 'utf-8') as dictCustomData_f:
            dictCustomData = json.loads(dictCustomData_f.read())
    except:
        initEmptyCustomData()
    tmp_hash_list = ['unity']
    if botInfo != None:
        tmp_hash_list.extend(list(botInfo.keys()))
    for tmp_hash_list_this in tmp_hash_list:
        if tmp_hash_list_this not in dictCustomData['data']:
            dictCustomData['data'][tmp_hash_list_this] = {}

def getCustomDataSortKeyList(data, reverse = False):
    tmp_sort_list = []
    tmp_res_list = []
    tmp_dictCustomData_data = data
    for tmp_dictCustomData_data_this in tmp_dictCustomData_data:
        tmp_sort_list.append(
            [
                tmp_dictCustomData_data[tmp_dictCustomData_data_this]['key'],
                tmp_dictCustomData_data[tmp_dictCustomData_data_this]['priority']
            ]
        )
    tmp_sort_list.sort(key = lambda x : -x[1] if reverse else x[1])
    for tmp_sort_list_this in tmp_sort_list:
        tmp_res_list.append(tmp_sort_list_this[0])
    return tmp_res_list

def saveCustomData():
    global dictCustomData
    releaseDir('./plugin')
    releaseDir('./plugin/data')
    releaseDir('./plugin/data/ChanceCustom')
    dictCustomData_path = './plugin/data/ChanceCustom/custom.json'
    with open(dictCustomData_path, 'w', encoding = 'utf-8') as dictCustomData_f:
        dictCustomData_f.write(json.dumps(obj = dictCustomData, ensure_ascii = False, indent = 4))
