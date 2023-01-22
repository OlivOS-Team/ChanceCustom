'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   GUI.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import ChanceCustom

import tkinter
from tkinter import ttk
from tkinter import messagebox
try:
    from tkinter import filedialog
except:
    pass
import os
import shutil
import json
import zipfile
import configparser

dictColorContext = {
    'color_001': '#00A0EA',
    'color_002': '#BBE9FF',
    'color_003': '#40C3FF',
    'color_004': '#FFFFFF',
    'color_005': '#000000',
    'color_006': '#80D7FF'
}

dictSLMap = {
    'matchTypeList': [
        '完全匹配',
        '模糊匹配',
        '前缀匹配',
        '正则匹配'
    ],
    'matchTypeList_loadMap': {
        'full': '完全匹配',
        'contain': '模糊匹配',
        'perfix': '前缀匹配',
        'reg': '正则匹配'
    },
    'matchTypeList_saveMap': {
        '完全匹配': 'full',
        '模糊匹配': 'contain',
        '前缀匹配': 'perfix',
        '正则匹配': 'reg'
    },
    'matchPlaceList': [
        '群聊触发',
        '私聊触发',
        '群/私聊触发'
    ],
    'matchPlaceList_loadMap': {
        '1': '群聊触发',
        '2': '私聊触发',
        '3': '群/私聊触发'
    },
    'matchPlaceList_saveMap': {
        '群聊触发': '1',
        '私聊触发': '2',
        '群/私聊触发': '3'
    }
}

class ConfigUI(object):
    def __init__(self, Model_name, logger_proc = None):
        self.Model_name = Model_name
        self.UIObject = {}
        self.UIData = {}
        self.UIConfig = {}
        self.logger_proc = logger_proc
        self.UIData['flag_open'] = False
        self.UIData['click_record'] = {}
        self.UIConfig.update(dictColorContext)

    def start(self):
        self.UIObject['root'] = tkinter.Toplevel()
        self.UIObject['root'].title('程心自定义')
        self.UIObject['root'].geometry('518x400')
        self.UIObject['root'].resizable(
            width = False,
            height = False
        )
        self.UIObject['root'].configure(bg = self.UIConfig['color_001'])

        self.UIData['hash_now'] = 'unity'
        self.init_notebook()
        self.tree_init()

        self.tree_UI_Combobox_init(
            obj_root = 'root',
            obj_name = 'root_hash',
            str_name = 'root_hash_StringVar',
            x = 50,
            y = 20,
            width_t = 35,
            width = 140,
            height = 24,
            action = None,
            title = '账号'
        )
        self.UIData['hash_default'] = 'unity'
        self.UIData['hash_default_key'] = '全局'
        self.UIData['hash_find'] = {
            self.UIData['hash_default_key']: self.UIData['hash_default']
        }
        self.UIData['hash_list'] = [self.UIData['hash_default_key']]
        for hash_this in ChanceCustom.load.dictBotInfo:
            key_info = '%s | %s' % (
                ChanceCustom.load.dictBotInfo[hash_this].platform['platform'],
                ChanceCustom.load.dictBotInfo[hash_this].id
            )
            self.UIData['hash_list'].append(key_info)
            self.UIData['hash_find'][key_info] = hash_this
        self.UIObject['root_hash']['value'] = tuple(self.UIData['hash_list'])
        self.UIObject['root_hash'].current(
            self.UIData['hash_list'].index(
                self.UIData['hash_default_key']
            )
        )

        self.tree_UI_Button_init(
            name = 'root_Button_IMPORT',
            text = '导入...',
            command = lambda : self.ccpk_read(),
            x = 240,
            y = 15,
            width = 80,
            height = 34
        )

        self.tree_UI_Button_init(
            name = 'root_Button_PACK',
            text = '打包...',
            command = lambda : self.ccpk_pack(),
            x = 330,
            y = 15,
            width = 80,
            height = 34
        )

        self.tree_UI_Button_init(
            name = 'root_Button_SAVE',
            text = '保存',
            command = lambda : self.tree_save(),
            x = 420,
            y = 15,
            width = 80,
            height = 34
        )

        self.UIObject['root'].iconbitmap('./resource/tmp_favoricon.ico')
        self.UIObject['root'].mainloop()
        #ChanceCustom.load.flag_open = False


    def init_notebook(self):
        self.UIData['style'] = ttk.Style(self.UIObject['root'])
        try:
            self.UIData['style'].element_create('Plain.Notebook.tab', "from", 'default')
        except:
            pass
        self.UIData['style'].layout(
            "TNotebook.Tab",
            [('Plain.Notebook.tab', {'children':
                [('Notebook.padding', {'side': 'top', 'children':
                    [('Notebook.focus', {'side': 'top', 'children':
                        [('Notebook.label', {'side': 'top', 'sticky': ''})],
                    'sticky': 'nswe'})],
                'sticky': 'nswe'})],
            'sticky': 'nswe'})])
        self.UIData['style'].configure(
            "TNotebook",
            background = self.UIConfig['color_001'],
            borderwidth = 0,
            relief = tkinter.FLAT,
            padding = [-1, 1, -3, -3],
            tabmargins = [5, 5, 0, 0]
        )
        self.UIData['style'].configure(
            "TNotebook.Tab",
            background = self.UIConfig['color_006'],
            foreground = self.UIConfig['color_001'],
            padding = 4,
            borderwidth = 0,
            font = ('等线', 12, 'bold')
        )
        self.UIData['style'].map(
            "TNotebook.Tab",
            background = [
                ('selected', self.UIConfig['color_004']),
                ('!selected', self.UIConfig['color_003'])
            ],
            foreground = [
                ('selected', self.UIConfig['color_003']),
                ('!selected', self.UIConfig['color_004'])
            ]
        )

        self.UIObject['Notebook_root'] = ttk.Notebook(self.UIObject['root'], style = 'TNotebook')
        self.UIObject['Notebook_root'].place(x = 15, y = 64, width = 488, height = 321)
        self.UIObject['Notebook_root'].grid_rowconfigure(0, weight = 15)
        self.UIObject['Notebook_root'].grid_columnconfigure(0, weight = 15)

    def tree_init(self):
        self.UIObject['frame_key_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_key_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_key_root'].grid(
            row = 0,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['frame_key_root'].grid_rowconfigure(0, weight = 15)
        self.UIObject['frame_key_root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['frame_key_root'].grid_columnconfigure(1, weight = 1)
        self.UIObject['tree'] = ttk.Treeview(self.UIObject['frame_key_root'])
        self.UIObject['tree']['show'] = 'headings'
        self.UIObject['tree']['columns'] = ('KEY', 'MATCHTYPE', 'MATCHPLACE', 'VALUE', 'PRIORITY')
        self.UIObject['tree'].column('KEY', width = 90)
        self.UIObject['tree'].column('MATCHTYPE', width = 90)
        self.UIObject['tree'].column('MATCHPLACE', width = 90)
        self.UIObject['tree'].column('VALUE', width = 140)
        self.UIObject['tree'].column('PRIORITY', width = 50)
        self.UIObject['tree'].heading('KEY', text = '关键词')
        self.UIObject['tree'].heading('MATCHTYPE', text = '匹配类型')
        self.UIObject['tree'].heading('MATCHPLACE', text = '触发方式')
        self.UIObject['tree'].heading('VALUE', text = '回复')
        self.UIObject['tree'].heading('PRIORITY', text = '优先级')
        self.UIObject['tree']['selectmode'] = 'browse'
        self.UIObject['tree_rightkey_menu'] = tkinter.Menu(self.UIObject['frame_key_root'], tearoff = False)
        #self.UIObject['tree'].bind('<<TreeviewSelect>>', lambda x : self.treeSelect('tree', x))
        self.UIObject['tree'].grid(
            row = 0,
            column = 0,
            sticky = "nswe",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['tree'].bind('<Button-3>', lambda x : self.tree_rightKey(x))
        self.UIObject['tree_yscroll'] = ttk.Scrollbar(
            self.UIObject['frame_key_root'],
            orient = "vertical",
            command = self.UIObject['tree'].yview
        )
        self.UIObject['tree'].configure(
            yscrollcommand = self.UIObject['tree_yscroll'].set
        )
        self.UIObject['tree_yscroll'].grid(
            row = 0,
            column = 1,
            sticky = "nse",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['frame_ccpk_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_ccpk_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_ccpk_root'].grid(
            row = 0,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['frame_ccpk_root'].grid_rowconfigure(0, weight = 15)
        self.UIObject['frame_ccpk_root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['frame_ccpk_root'].grid_columnconfigure(1, weight = 1)
        self.UIObject['tree_ccpk'] = ttk.Treeview(self.UIObject['frame_ccpk_root'])
        self.UIObject['tree_ccpk']['show'] = 'headings'
        self.UIObject['tree_ccpk']['columns'] = ('NAME', 'AUTHOR', 'VERSION', 'INFO')
        self.UIObject['tree_ccpk'].column('NAME', width = 90)
        self.UIObject['tree_ccpk'].column('AUTHOR', width = 90)
        self.UIObject['tree_ccpk'].column('VERSION', width = 90)
        self.UIObject['tree_ccpk'].column('INFO', width = 190)
        self.UIObject['tree_ccpk'].heading('NAME', text = '包名')
        self.UIObject['tree_ccpk'].heading('AUTHOR', text = '作者')
        self.UIObject['tree_ccpk'].heading('VERSION', text = '版本')
        self.UIObject['tree_ccpk'].heading('INFO', text = '说明')
        self.UIObject['tree_ccpk']['selectmode'] = 'browse'
        self.UIObject['tree_ccpk_rightkey_menu'] = tkinter.Menu(self.UIObject['frame_ccpk_root'], tearoff = False)
        #self.UIObject['tree_ccpk'].bind('<<TreeviewSelect>>', lambda x : self.treeSelect('tree_ccpk', x))
        self.UIObject['tree_ccpk'].grid(
            row = 0,
            column = 0,
            sticky = "nswe",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['tree_ccpk'].bind('<Button-3>', lambda x : self.tree_rightKey(x, 'ccpk'))
        self.UIObject['tree_ccpk_yscroll'] = ttk.Scrollbar(
            self.UIObject['frame_ccpk_root'],
            orient = "vertical",
            command = self.UIObject['tree_ccpk'].yview
        )
        self.UIObject['tree_ccpk'].configure(
            yscrollcommand = self.UIObject['tree_ccpk_yscroll'].set
        )
        self.UIObject['tree_ccpk_yscroll'].grid(
            row = 0,
            column = 1,
            sticky = "nse",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['frame_default_reply_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_default_reply_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_default_reply_root'].configure(bg = self.UIConfig['color_001'])
        self.UIObject['frame_default_reply_root'].grid(
            row = 0,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['frame_default_reply_root'].grid_rowconfigure(0, weight = 15)
        self.UIObject['frame_default_reply_root'].grid_rowconfigure(1, weight = 15)
        self.UIObject['frame_default_reply_root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['frame_default_reply_root'].grid_columnconfigure(1, weight = 1)

        self.tree_UI_singal_Label_Entry_init(
            obj_root='frame_default_reply_root',
            obj_name='default_reply_day',
            title='达到每日上限后的默认回复',
            str_name='default_reply_day_StringVar',
            count=0,
            mode='NONE'
        )

        self.tree_UI_singal_Label_Entry_init(
            obj_root='frame_default_reply_root',
            obj_name='default_reply_week',
            title='达到每周上限后的默认回复',
            str_name='default_reply_week_StringVar',
            count=1,
            mode='NONE'
        )

        self.tree_UI_singal_Label_Entry_init(
            obj_root='frame_default_reply_root',
            obj_name='default_reply_month',
            title='达到每月上限后的默认回复',
            str_name='default_reply_month_StringVar',
            count=2,
            mode='NONE'
        )

        self.tree_UI_singal_Label_Entry_init(
            obj_root='frame_default_reply_root',
            obj_name='default_reply_once',
            title='达到一次间隔后的默认回复',
            str_name='default_reply_once_StringVar',
            count=3,
            mode='NONE'
        )

        self.tree_UI_singal_Label_Entry_init(
            obj_root='frame_default_reply_root',
            obj_name='default_reply_reply',
            title='触发回复间隔冷却后的默认回复',
            str_name='default_reply_reply_StringVar',
            count=4,
            mode='NONE'
        )

        self.tree_UI_singal_Label_Entry_init(
            obj_root='frame_default_reply_root',
            obj_name='default_reply_role',
            title='权限不足时的默认回复',
            str_name='default_reply_role_StringVar',
            count=5,
            mode='NONE'
        )

        self.UIObject['Notebook_root'].add(self.UIObject['frame_key_root'], text="关键词")
        self.UIObject['Notebook_root'].add(self.UIObject['frame_ccpk_root'], text="导入包")
        self.UIObject['Notebook_root'].add(self.UIObject['frame_default_reply_root'], text="默认回复")

        self.tree_load()

    def tree_UI_singal_Label_Entry_init(
        self,
        obj_root:str,
        obj_name:str,
        title:str,
        str_name:str,
        count:int,
        mode:str='NONE'
    ):
        tmp_span_len = 4
        tmp_both_width_len = 400
        tmp_label_height_len = 20
        tmp_entry_height_len = 20
        self.tree_UI_singal_Label_init(
            obj_root,
            obj_name,
            title
        )
        self.UIData[str_name] = tkinter.StringVar()
        self.tree_UI_singal_Entry_init(
            obj_root,
            obj_name,
            str_name,
            mode
        )
        self.UIObject[obj_name + '=Label'].place(
            x=tmp_span_len,
            y=tmp_span_len * (count * 2 + 1) + tmp_label_height_len * (count) + tmp_entry_height_len * (count),
            width=tmp_both_width_len,
            height=tmp_label_height_len
        )
        self.UIObject[obj_name + '=Entry'].place(
            x=tmp_span_len,
            y=tmp_span_len * (count * 2 + 2) + tmp_label_height_len * (count + 1) + tmp_entry_height_len * (count),
            width=tmp_both_width_len,
            height=tmp_entry_height_len
        )

    def tree_UI_singal_Label_init(self, obj_root, obj_name, title=''):
        self.UIObject[obj_name + '=Label'] = tkinter.Label(
            self.UIObject[obj_root],
            text=title
        )
        self.UIObject[obj_name + '=Label'].configure(
            bg=self.UIConfig['color_001'],
            fg=self.UIConfig['color_004'],
            justify='left',
            anchor='nw'
        )

    def tree_UI_singal_Entry_init(self, obj_root, obj_name, str_name, mode='NONE'):
        self.UIObject[obj_name + '=Entry'] = tkinter.Entry(
            self.UIObject[obj_root],
            textvariable=self.UIData[str_name]
        )
        self.UIObject[obj_name + '=Entry'].configure(
            bg=self.UIConfig['color_004'],
            fg=self.UIConfig['color_005'],
            bd=0
        )
        if mode == 'SAFE':
            self.UIObject[obj_name].configure(
                show='●'
            )

    def tree_UI_Entry_init(self, obj_root, obj_name, str_name, x, y, width, height, action, title='', mode='NONE'):
        self.UIObject[obj_name + '=Label'] = tkinter.Label(
            self.UIObject[obj_root],
            text=title
        )
        self.UIObject[obj_name + '=Label'].configure(
            bg=self.UIConfig['color_001'],
            fg=self.UIConfig['color_004']
        )
        self.UIObject[obj_name + '=Label'].place(
            x=x - 100,
            y=y,
            width=100,
            height=height
        )
        self.UIObject[obj_name] = tkinter.Entry(
            self.UIObject[obj_root],
            textvariable=self.UIData[str_name]
        )
        self.UIObject[obj_name].configure(
            bg=self.UIConfig['color_004'],
            fg=self.UIConfig['color_005'],
            bd=0
        )
        if mode == 'SAFE':
            self.UIObject[obj_name].configure(
                show='●'
            )
        self.UIObject[obj_name].place(
            x=x,
            y=y,
            width=width,
            height=height
        )

    def tree_UI_Combobox_init(self, obj_root, obj_name, str_name, x, y, width_t, width, height, action, title = ''):
        self.UIObject[obj_name + '=Label'] = tkinter.Label(
            self.UIObject[obj_root],
            text = title
        )
        self.UIObject[obj_name + '=Label'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004']
        )
        self.UIObject[obj_name + '=Label'].place(
            x = x - width_t,
            y = y,
            width = width_t,
            height = height
        )
        self.UIData[str_name] = tkinter.StringVar()
        self.UIObject[obj_name] = ttk.Combobox(
            self.UIObject[obj_root],
            textvariable = self.UIData[str_name]
        )
        self.UIObject[obj_name].place(
            x = x,
            y = y,
            width = width,
            height = height
        )
        self.UIObject[obj_name].configure(state='readonly')
        self.UIObject[obj_name].bind('<<ComboboxSelected>>', lambda x : self.tree_UI_Combobox_ComboboxSelected(x, action, obj_name))

    def tree_UI_Combobox_ComboboxSelected(self, action, event, target):
        if target == 'root_hash':
            self.UIData['hash_now'] = self.UIData['hash_find'][self.UIData['root_hash_StringVar'].get()]
            self.tree_load()

    def tree_UI_Button_init(self, name, text, command, x, y, width, height):
        self.UIObject[name] = tkinter.Button(
            self.UIObject['root'],
            text = text,
            command = command,
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove'
        )
        self.UIObject[name].bind('<Enter>', lambda x : self.buttom_action(name, '<Enter>'))
        self.UIObject[name].bind('<Leave>', lambda x : self.buttom_action(name, '<Leave>'))
        self.UIObject[name].bind('<Button-1>', lambda x : self.clickRecord(name, x))
        self.UIObject[name].place(
            x = x,
            y = y,
            width = width,
            height = height
        )

    def buttom_action(self, name, action):
        if name in self.UIObject:
            if action == '<Enter>':
                self.UIObject[name].configure(bg = self.UIConfig['color_006'])
            if action == '<Leave>':
                self.UIObject[name].configure(bg = self.UIConfig['color_003'])

    def clickRecord(self, name, event):
        self.UIData['click_record'][name] = event

    def tree_load(self):
        tmp_dictCustomData = ChanceCustom.load.dictCustomData
        tmp_hashSelection = self.UIData['hash_now']
        tmp_tree_item_children = self.UIObject['tree'].get_children()
        for tmp_tree_item_this in tmp_tree_item_children:
            self.UIObject['tree'].delete(tmp_tree_item_this)
        it_list_tmp_dictCustomData = ChanceCustom.load.getCustomDataSortKeyList(
            data = tmp_dictCustomData['data'][tmp_hashSelection],
            reverse = True
        )
        for tmp_dictCustomData_this in it_list_tmp_dictCustomData:
            try:
                self.UIObject['tree'].insert(
                    '',
                    0,
                    text = tmp_dictCustomData_this,
                    values=(
                        tmp_dictCustomData['data'][tmp_hashSelection][tmp_dictCustomData_this]['key'],
                        dictSLMap['matchTypeList_loadMap'][
                            tmp_dictCustomData['data'][tmp_hashSelection][tmp_dictCustomData_this]['matchType']
                        ],
                        dictSLMap['matchPlaceList_loadMap'][
                            tmp_dictCustomData['data'][tmp_hashSelection][tmp_dictCustomData_this]['matchPlace']
                        ],
                        tmp_dictCustomData['data'][tmp_hashSelection][tmp_dictCustomData_this]['value'].replace('\n', ''),
                        str(tmp_dictCustomData['data'][tmp_hashSelection][tmp_dictCustomData_this]['priority'])
                    )
                )
            except:
                pass # 能不能为所有excepetion打日志？
        tmp_tree_item_children = self.UIObject['tree_ccpk'].get_children()
        for tmp_tree_item_this in tmp_tree_item_children:
            self.UIObject['tree_ccpk'].delete(tmp_tree_item_this)
        for tmp_dictCustomData_this in tmp_dictCustomData['ccpkList'][tmp_hashSelection]:
            try:
                self.UIObject['tree_ccpk'].insert(
                    '',
                    0,
                    text = tmp_dictCustomData_this,
                    values=(
                        tmp_dictCustomData['ccpkList'][tmp_hashSelection][tmp_dictCustomData_this]['info']['name'],
                        tmp_dictCustomData['ccpkList'][tmp_hashSelection][tmp_dictCustomData_this]['info']['author'],
                        tmp_dictCustomData['ccpkList'][tmp_hashSelection][tmp_dictCustomData_this]['info']['version'],
                        tmp_dictCustomData['ccpkList'][tmp_hashSelection][tmp_dictCustomData_this]['info']['info'],
                    )
                )
            except:
                pass
        try:
            self.UIData['default_reply_day_StringVar'].set(tmp_dictCustomData['defaultVar'][tmp_hashSelection]['一天上限'])
            self.UIData['default_reply_week_StringVar'].set(tmp_dictCustomData['defaultVar'][tmp_hashSelection]['一周上限'])
            self.UIData['default_reply_month_StringVar'].set(tmp_dictCustomData['defaultVar'][tmp_hashSelection]['一月上限'])
            self.UIData['default_reply_once_StringVar'].set(tmp_dictCustomData['defaultVar'][tmp_hashSelection]['一次间隔'])
            self.UIData['default_reply_reply_StringVar'].set(tmp_dictCustomData['defaultVar'][tmp_hashSelection]['回复间隔'])
            self.UIData['default_reply_role_StringVar'].set(tmp_dictCustomData['defaultVar'][tmp_hashSelection]['权限限制'])
        except:
            pass

    def tree_save(self):
        try:
            tmp_dictCustomData = ChanceCustom.load.dictCustomData
            tmp_hashSelection = self.UIData['hash_now']
            tmp_dictCustomData['defaultVar'][tmp_hashSelection]['一天上限'] = self.UIData['default_reply_day_StringVar'].get()
            tmp_dictCustomData['defaultVar'][tmp_hashSelection]['一周上限'] = self.UIData['default_reply_week_StringVar'].get()
            tmp_dictCustomData['defaultVar'][tmp_hashSelection]['一月上限'] = self.UIData['default_reply_month_StringVar'].get()
            tmp_dictCustomData['defaultVar'][tmp_hashSelection]['一次间隔'] = self.UIData['default_reply_once_StringVar'].get()
            tmp_dictCustomData['defaultVar'][tmp_hashSelection]['回复间隔'] = self.UIData['default_reply_reply_StringVar'].get()
            tmp_dictCustomData['defaultVar'][tmp_hashSelection]['权限限制'] = self.UIData['default_reply_role_StringVar'].get()
        except:
            pass
        ChanceCustom.load.saveCustomData()

    def ccpk_read(self):
        tmp_dictCustomData = ChanceCustom.load.dictCustomData
        tmp_hashSelection = self.UIData['hash_now']
        ccpk_load_path_list = []
        try:
            ccpk_load_path_list = filedialog.askopenfilenames(
                title = '导入...',
                filetypes = [
                    ("程心包", "*.ccpk"),
                    ("铃心包", "*.epk")
                ]
            )
        except:
            tkinter.messagebox.showwarning('运行失败', '你需要使用最新版OlivOS才能使用此功能')
        for ccpk_load_path in ccpk_load_path_list:
            try:
                releaseDir('./plugin')
                releaseDir('./plugin/data')
                releaseDir('./plugin/data/ChanceCustom')
                removeDir('./plugin/data/ChanceCustom/tmp')
                releaseDir('./plugin/data/ChanceCustom/tmp')
                if ccpk_load_path.endswith('.ccpk'):
                    with zipfile.ZipFile(ccpk_load_path, 'r', zipfile.ZIP_DEFLATED) as z:
                        z.extractall('./plugin/data/ChanceCustom/tmp')
                        with open('./plugin/data/ChanceCustom/tmp/data.json', 'r', encoding = 'utf-8') as f:
                            ccpk_data = json.loads(f.read())
                            if 'type' in ccpk_data and ccpk_data['type'] == 'ccpk':
                                if 'dataVersion' in ccpk_data and ccpk_data['dataVersion'] == 2:
                                    for key_this in ccpk_data['data']:
                                        tmp_dictCustomData['data'][tmp_hashSelection][key_this] = ccpk_data['data'][key_this]
                                    tmp_dictCustomData['ccpkList'][tmp_hashSelection][ccpk_data['info']['name']] = ccpk_data
                elif ccpk_load_path.endswith('.epk'):
                    with support_gbk(zipfile.ZipFile(ccpk_load_path, 'r', zipfile.ZIP_DEFLATED)) as z:
                        z.extractall('./plugin/data/ChanceCustom/tmp')
                        ini = configparser.ConfigParser()
                        ini.read('./plugin/data/ChanceCustom/tmp/配置.ini', encoding = 'gbk')
                        dataAll = {
                            'type': 'ccpk',
                            'dataVersion' : ChanceCustom.load.dataVersion,
                            'info': {
                                'name': ccpk_load_path.rstrip('.epk').split('/')[-1],
                                'author': '铃心自定义',
                                'version': '0',
                                'info': ''
                            },
                            'data': {}
                        }
                        with open('./plugin/data/ChanceCustom/tmp/说明.txt', encoding = 'gbk') as f:
                            dataAll['info']['info'] = f.read()
                        for key_this in ini:
                            data_this = {
                                "key": key_this,
                                "division":"1",
                                "matchType": "full",
                                "matchPlace": "1",
                                "priority": 0,
                                "value": ""
                            }
                            if key_this not in ['DEFAULT']:
                                if '回复' in ini[key_this]:
                                    data_this['value'] = ini[key_this]['回复'].replace('【分隔】', '\n')
                                if '分群' in ini[key_this]:
                                    data_this['division'] = str(ini[key_this]['分群'])
                                if '优先级' in ini[key_this]:
                                    data_this['priority'] = int(ini[key_this]['优先级'])
                                if '匹配方式' in ini[key_this]:
                                    if ini[key_this]['匹配方式'] == '完全匹配':
                                        data_this['matchType'] = 'full'
                                    elif ini[key_this]['匹配方式'] == '模糊匹配':
                                        data_this['matchType'] = 'contain'
                                    elif ini[key_this]['匹配方式'] == '前缀匹配':
                                        data_this['matchType'] = 'perfix'
                                    elif ini[key_this]['匹配方式'] == '正则匹配':
                                        data_this['matchType'] = 'reg'
                                    else:
                                        continue
                                if '触发方式' in ini[key_this]:
                                    if ini[key_this]['触发方式'] == '群聊触发':
                                        data_this['matchPlace'] = '1'
                                    elif ini[key_this]['触发方式'] == '私聊触发':
                                        data_this['matchPlace'] = '2'
                                    else:
                                        data_this['matchPlace'] = '3'
                                dataAll['data'][key_this] = data_this
                        for key_this in dataAll['data']:
                            tmp_dictCustomData['data'][tmp_hashSelection][key_this] = dataAll['data'][key_this]
                        tmp_dictCustomData['ccpkList'][tmp_hashSelection][dataAll['info']['name']] = dataAll
                    removeDir('./plugin/data/ChanceCustom/tmp')
            except:
                tkinter.messagebox.showwarning('导入失败', '导入 %s 时失败' % ccpk_load_path)
        self.tree_save()
        self.tree_load()

    def ccpk_pack(self):
        bot_hash_now = self.UIData['hash_now']
        PackUpUI(
            action = 'create',
            key = None,
            bot_hash = bot_hash_now,
            edit_commit_callback = None,
            root = self
        ).start()

    def tree_rightKey(self, event, name = 'key'):
        if name == 'key':
            self.UIObject['tree_rightkey_menu'].delete(0, tkinter.END)
            self.UIObject['tree_rightkey_menu'].add_command(label = '添加', command = lambda : self.tree_edit('create'))
            self.UIObject['tree_rightkey_menu'].add_command(label = '编辑', command = lambda : self.tree_edit('update'))
            self.UIObject['tree_rightkey_menu'].add_command(label = '删除', command = lambda : self.tree_edit('delete'))
            self.UIObject['tree_rightkey_menu'].post(event.x_root, event.y_root)
        elif name == 'ccpk':
            self.UIObject['tree_ccpk_rightkey_menu'].delete(0, tkinter.END)
            self.UIObject['tree_ccpk_rightkey_menu'].add_command(label = '卸载', command = lambda : self.ccpk_remove(flagDelete = True))
            self.UIObject['tree_ccpk_rightkey_menu'].add_command(label = '解绑(不删关键词)', command = lambda : self.ccpk_remove(flagDelete = False))
            self.UIObject['tree_ccpk_rightkey_menu'].add_command(label = '重新安装', command = lambda : self.ccpk_reinstall())
            self.UIObject['tree_ccpk_rightkey_menu'].post(event.x_root, event.y_root)

    def ccpk_remove(self, flagDelete = True):
        tmp_dictCustomData = ChanceCustom.load.dictCustomData
        key_now = None
        bot_hash_now = self.UIData['hash_now']
        key_now = get_tree_force(self.UIObject['tree_ccpk'])['text']
        if key_now == '':
            key_now = None
        if key_now != None:
            if key_now in tmp_dictCustomData['ccpkList'][bot_hash_now]:
                if flagDelete:
                    for key_this in tmp_dictCustomData['ccpkList'][bot_hash_now][key_now]['data']:
                        if key_this in tmp_dictCustomData['data'][bot_hash_now]:
                            tmp_dictCustomData['data'][bot_hash_now].pop(key_this)
                tmp_dictCustomData['ccpkList'][bot_hash_now].pop(key_now)
            self.tree_save()
            self.tree_load()

    def ccpk_reinstall(self):
        tmp_dictCustomData = ChanceCustom.load.dictCustomData
        key_now = None
        bot_hash_now = self.UIData['hash_now']
        key_now = get_tree_force(self.UIObject['tree_ccpk'])['text']
        if key_now == '':
            key_now = None
        if key_now != None:
            if key_now in tmp_dictCustomData['ccpkList'][bot_hash_now]:
                for key_this in tmp_dictCustomData['ccpkList'][bot_hash_now][key_now]['data']:
                    if key_this not in tmp_dictCustomData['data'][bot_hash_now]:
                        tmp_dictCustomData['data'][bot_hash_now][key_this] = tmp_dictCustomData['ccpkList'][bot_hash_now][key_now]['data'][key_this]
            self.tree_save()
            self.tree_load()

    def tree_edit(self, action):
        key_now = None
        bot_hash_now = self.UIData['hash_now']
        if action == 'update' or action == 'delete':
            key_now = get_tree_force(self.UIObject['tree'])['text']
            if key_now == '':
                action = 'create'
        if action == 'delete':
            ChanceCustom.load.dictCustomData['data'][bot_hash_now].pop(key_now)
            self.tree_load()
        else:
            if not self.UIData['flag_open']:
                self.UIData['flag_open'] = True
                edit_action = TreeEditUI(
                    action = action,
                    key = key_now,
                    bot_hash = bot_hash_now,
                    edit_commit_callback = None,
                    root = self
                )
                edit_action.start()


def support_gbk(zip_file: zipfile.ZipFile):
    name_to_info = zip_file.NameToInfo
    # copy map first
    for name, info in name_to_info.copy().items():
        real_name = name.encode('cp437').decode('gbk')
        if real_name != name:
            info.filename = real_name
            del name_to_info[name]
            name_to_info[real_name] = info
    return zip_file


class TreeEditUI(object):
    def __init__(self, action, key = None, bot_hash = 'unity', edit_commit_callback = None, root = None):
        self.root = root
        self.key = key
        self.action = action
        self.bot_hash = bot_hash
        self.edit_commit_callback = edit_commit_callback
        self.UIObject = {}
        self.UIConfig = {}
        self.UIConfig.update(dictColorContext)
        self.UIData = {}

    def start(self):
        self.UIObject['edit_root'] = tkinter.Toplevel()
        self.UIObject['edit_root'].title('编辑')
        if 'create' == self.action:
            self.UIObject['edit_root'].title('添加')
        elif 'update' == self.action:
            self.UIObject['edit_root'].title('编辑')
        self.UIObject['edit_root'].geometry('550x350')
        self.UIObject['edit_root'].resizable(
            width = False,
            height = False
        )
        self.UIObject['edit_root'].configure(bg = self.UIConfig['color_001'])

        self.UIObject['edit_root'].protocol("WM_DELETE_WINDOW", self.tree_edit_data_save)

        self.tree_edit_UI_Entry_init(
            obj_root = 'edit_root',
            obj_name = 'edit_root_key',
            str_name = 'edit_root_key_StringVar',
            x = 70,
            y = 15,
            width_t = 70,
            width = 550 - 70 - 15,
            height = 24,
            action = self.action,
            title = '关键词'
        )

        self.tree_edit_UI_Entry_init(
            obj_root = 'edit_root',
            obj_name = 'edit_root_division',
            str_name = 'edit_root_division_StringVar',
            x = 70,
            y = 60,
            width_t = 70,
            width = 550 - 70 - 15,
            height = 24,
            action = self.action,
            title = '分群/分人'
        )

        self.tree_edit_UI_Combobox_init(
            obj_root = 'edit_root',
            obj_name = 'edit_root_matchType',
            str_name = 'edit_root_matchType_StringVar',
            x = 70,
            y = 60 +45,
            width_t = 70,
            width = 100,
            height = 24,
            action = self.action,
            title = '匹配方式'
        )

        self.tree_edit_UI_Combobox_init(
            obj_root = 'edit_root',
            obj_name = 'edit_root_matchPlace',
            str_name = 'edit_root_matchPlace_StringVar',
            x = 280,
            y = 60 +45,
            width_t = 70,
            width = 100,
            height = 24,
            action = self.action,
            title = '触发方式'
        )

        self.tree_edit_UI_Entry_init(
            obj_root = 'edit_root',
            obj_name = 'edit_root_priority',
            str_name = 'edit_root_priority_StringVar',
            x = 550 - 15 - 70,
            y = 60 + 45,
            width_t = 50,
            width = 70,
            height = 24,
            action = self.action,
            title = '优先级'
        )

        self.tree_edit_UI_Text_init(
            obj_root = 'edit_root',
            obj_name = 'edit_root_value',
            str_name = 'edit_root_value_StringVar',
            x = 15,
            y = 100 + 45,
            width_t = 0,
            width = 550 - 15 * 2 - 18,
            height = 30 * 8,
            action = self.action,
            title = '回复'
        )

        self.UIObject['edit_root_value_yscroll'] = ttk.Scrollbar(
            self.UIObject['edit_root'],
            orient = "vertical",
            command = self.UIObject['edit_root_value'].yview
        )
        self.UIObject['edit_root_value_yscroll'].place(
            x = 550 - 18 - 15,
            y = 100,
            width = 18,
            height = 30 * 8
        )
        self.UIObject['edit_root_value'].configure(
            yscrollcommand = self.UIObject['edit_root_value_yscroll'].set
        )

        self.tree_edit_data_init()

        self.UIObject['edit_root'].iconbitmap('./resource/tmp_favoricon.ico')
        self.UIObject['edit_root'].mainloop()

    def tree_edit_UI_Combobox_init(self, obj_root, obj_name, str_name, x, y, width_t, width, height, action, title = ''):
        self.UIObject[obj_name + '=Label'] = tkinter.Label(
            self.UIObject[obj_root],
            text = title
        )
        self.UIObject[obj_name + '=Label'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004']
        )
        self.UIObject[obj_name + '=Label'].place(
            x = x - width_t,
            y = y,
            width = width_t,
            height = height
        )
        self.UIData[str_name] = tkinter.StringVar()
        self.UIObject[obj_name] = ttk.Combobox(
            self.UIObject[obj_root],
            textvariable = self.UIData[str_name]
        )
        self.UIObject[obj_name].place(
            x = x,
            y = y,
            width = width,
            height = height
        )
        self.UIObject[obj_name].configure(state='readonly')
        #self.UIObject[obj_name].bind('<<ComboboxSelected>>', lambda x : self.tree_edit_UI_Combobox_ComboboxSelected(x, action, obj_name))

    def tree_edit_UI_Entry_init(self, obj_root, obj_name, str_name, x, y, width_t, width, height, action, title = '', mode = 'NONE'):
        self.UIObject[obj_name + '=Label'] = tkinter.Label(
            self.UIObject[obj_root],
            text = title
        )
        self.UIObject[obj_name + '=Label'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004']
        )
        self.UIObject[obj_name + '=Label'].place(
            x = x - width_t,
            y = y,
            width = width_t,
            height = height
        )
        self.UIData[str_name] = tkinter.StringVar()
        self.UIObject[obj_name] = tkinter.Entry(
            self.UIObject[obj_root],
            textvariable = self.UIData[str_name]
        )
        self.UIObject[obj_name].configure(
            bg = self.UIConfig['color_004'],
            fg = self.UIConfig['color_005'],
            bd = 0
        )
        if mode == 'SAFE':
            self.UIObject[obj_name].configure(
                show = '●'
            )
        self.UIObject[obj_name].place(
            x = x,
            y = y,
            width = width,
            height = height
        )

    def tree_edit_UI_Text_init(self, obj_root, obj_name, str_name, x, y, width_t, width, height, action, title = '', mode = 'NONE'):
        self.UIObject[obj_name + '=Label'] = tkinter.Label(
            self.UIObject[obj_root],
            text = title
        )
        self.UIObject[obj_name + '=Label'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004']
        )
        self.UIObject[obj_name + '=Label'].place(
            x = x - width_t,
            y = y,
            width = width_t,
            height = height
        )
        self.UIData[str_name] = tkinter.StringVar()
        self.UIObject[obj_name] = tkinter.Text(
            self.UIObject[obj_root],
            wrap = tkinter.WORD
        )
        self.UIObject[obj_name].configure(
            bg = self.UIConfig['color_004'],
            fg = self.UIConfig['color_005'],
            bd = 0
        )
        self.UIObject[obj_name].place(
            x = x,
            y = y,
            width = width,
            height = height
        )

    def tree_edit_UI_Combobox_ComboboxSelected(self, action, event, target):
        pass

    def tree_edit_data_init(self):
        self.UIObject['edit_root_matchType']['value'] = tuple(dictSLMap['matchTypeList'])
        self.UIObject['edit_root_matchPlace']['value'] = tuple(dictSLMap['matchPlaceList'])
        if self.action == 'create':
            self.UIData['edit_root_division_StringVar'].set(str(1))
            self.UIObject['edit_root_matchType'].current(0)
            self.UIObject['edit_root_matchPlace'].current(0)
            self.UIData['edit_root_priority_StringVar'].set(str(0))
        elif self.action == 'update':
            tmp_data_this = ChanceCustom.load.dictCustomData['data'][self.bot_hash][self.key]
            self.UIData['edit_root_key_StringVar'].set(str(tmp_data_this['key']))
            self.UIData["edit_root_division_StringVar"].set(str(tmp_data_this.get("division","1")))
            self.UIObject['edit_root_matchType'].current(
                dictSLMap['matchTypeList'].index(
                    dictSLMap['matchTypeList_loadMap'][
                        tmp_data_this['matchType']
                    ]
                )
            )
            self.UIObject['edit_root_matchPlace'].current(
                dictSLMap['matchPlaceList'].index(
                    dictSLMap['matchPlaceList_loadMap'][
                        tmp_data_this['matchPlace']
                    ]
                )
            )
            self.UIData['edit_root_priority_StringVar'].set(str(tmp_data_this['priority']))
            self.UIObject['edit_root_value'].insert('1.0', tmp_data_this['value'])

    def tree_edit_data_save(self):
        tmp_key = self.UIData['edit_root_key_StringVar'].get()
        tmp_division = self.UIData.get("edit_root_division_StringVar","1")
        if tmp_division != "1":
            tmp_division = tmp_division.get()
        tmp_matchType = self.UIObject['edit_root_matchType'].get()
        tmp_matchPlace = self.UIObject['edit_root_matchPlace'].get()
        tmp_priority = self.UIData['edit_root_priority_StringVar'].get()
        try:
            tmp_priority = int(tmp_priority)
        except:
            tmp_priority = 0
        tmp_value = self.UIObject['edit_root_value'].get('1.0', tkinter.END)
        if len(tmp_key) > 0:
            try:
                if self.action == 'update':
                    ChanceCustom.load.dictCustomData['data'][self.bot_hash].pop(self.key)
                ChanceCustom.load.dictCustomData['data'][self.bot_hash][tmp_key] = {
                    'key': tmp_key,
                    "division": tmp_division,
                    'matchType': dictSLMap['matchTypeList_saveMap'][tmp_matchType],
                    'matchPlace': dictSLMap['matchPlaceList_saveMap'][tmp_matchPlace],
                    'priority': tmp_priority,
                    'value': tmp_value[:-1]
                }
            except:
                pass
        if self.root != None:
            self.root.tree_load()
            self.root.tree_save()
            self.root.UIData['flag_open'] = False
        self.UIObject['edit_root'].destroy()

def get_tree_force(tree_obj):
    return tree_obj.item(tree_obj.focus())


class PackUpUI(object):
    def __init__(self, action, key = None, bot_hash = 'unity', edit_commit_callback = None, root = None):
        self.root = root
        self.key = key
        self.action = action
        self.bot_hash = bot_hash
        self.edit_commit_callback = edit_commit_callback
        self.UIObject = {}
        self.UIConfig = {}
        self.UIConfig.update(dictColorContext)
        self.UIData = {}
        self.UIData['click_record'] = {}

    def start(self):
        self.UIObject['edit_root'] = tkinter.Toplevel()
        self.UIObject['edit_root'].title('打包...')
        self.UIObject['edit_root'].geometry('600x400')
        self.UIObject['edit_root'].resizable(
            width = False,
            height = False
        )
        self.UIObject['edit_root'].configure(bg = self.UIConfig['color_001'])

        self.UIObject['label_info'] = tkinter.Label(
            self.UIObject['edit_root'],
            text = '从左侧列表中选择需要打包的回复词',
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004']
        )
        self.UIObject['label_info'].place(
            x = 15,
            y = 15,
            width = 600 - 15 * 2,
            height = 24
        )

        self.UIObject['listbox_L_StringVar'] = tkinter.StringVar()
        self.UIObject['listbox_L'] = tkinter.Listbox(self.UIObject['edit_root'])
        self.UIObject['listbox_L'].configure(
            listvariable = self.UIObject['listbox_L_StringVar']
        )
        self.UIObject['listbox_L'].place(x = 45, y = 45, width = 250 - 18, height = 200)
        self.UIObject['listbox_L_yscroll'] = ttk.Scrollbar(
            self.UIObject['edit_root'],
            orient = "vertical",
            command = self.UIObject['listbox_L'].yview
        )
        self.UIObject['listbox_L_yscroll'].place(
            x = 45 + 250 - 18,
            y = 45,
            width = 18,
            height = 200
        )
        self.UIObject['listbox_L'].configure(
            yscrollcommand = self.UIObject['listbox_L_yscroll'].set
        )
        self.UIObject['listbox_L'].bind('<<ListboxSelect>>', lambda x : self.listbox_selected(x, 'listbox_L', 'listbox_R'))

        self.UIObject['listbox_R_StringVar'] = tkinter.StringVar()
        self.UIObject['listbox_R'] = tkinter.Listbox(self.UIObject['edit_root'])
        self.UIObject['listbox_R'].configure(
            listvariable = self.UIObject['listbox_R_StringVar']
        )
        self.UIObject['listbox_R'].place(x = 600 - (250 + 45), y = 45, width = 250 - 18, height = 200)
        self.UIObject['listbox_R_yscroll'] = ttk.Scrollbar(
            self.UIObject['edit_root'],
            orient = "vertical",
            command = self.UIObject['listbox_R'].yview
        )
        self.UIObject['listbox_R_yscroll'].place(
            x = 600 - 45 - 18,
            y = 45,
            width = 18,
            height = 200
        )
        self.UIObject['listbox_R'].configure(
            yscrollcommand = self.UIObject['listbox_R_yscroll'].set
        )
        self.UIObject['listbox_R'].bind('<<ListboxSelect>>', lambda x : self.listbox_selected(x, 'listbox_R', 'listbox_L'))

        self.init_data()
        self.load_data()

        self.tree_edit_UI_Entry_init(
            obj_root = 'edit_root',
            obj_name = 'entry_NAME',
            str_name = 'entry_NAME_StringVar',
            x = 65,
            y = 260,
            width_t = 50,
            width = 150,
            height = 26,
            action = None,
            title = '名称'
        )

        self.tree_edit_UI_Entry_init(
            obj_root = 'edit_root',
            obj_name = 'entry_AUTHOR',
            str_name = 'entry_AUTHOR_StringVar',
            x = 255,
            y = 260,
            width_t = 50,
            width = 150,
            height = 26,
            action = None,
            title = '作者'
        )

        self.tree_edit_UI_Entry_init(
            obj_root = 'edit_root',
            obj_name = 'entry_VERSION',
            str_name = 'entry_VERSION_StringVar',
            x = 455,
            y = 260,
            width_t = 50,
            width = 100,
            height = 26,
            action = None,
            title = '版本'
        )

        self.tree_edit_UI_Entry_init(
            obj_root = 'edit_root',
            obj_name = 'entry_INFO',
            str_name = 'entry_INFO_StringVar',
            x = 65,
            y = 300,
            width_t = 50,
            width = 600 - 65 - 45,
            height = 26,
            action = None,
            title = '说明'
        )

        self.tree_UI_Button_init(
            name = 'button_PACK_SAVE',
            text = '打包并保存至...',
            command = lambda : self.pack_save(),
            x = 45,
            y = 340,
            width = 600 - 45 * 2,
            height = 34
        )

        self.UIObject['edit_root'].iconbitmap('./resource/tmp_favoricon.ico')
        self.UIObject['edit_root'].mainloop()

    def tree_UI_Button_init(self, name, text, command, x, y, width, height):
        self.UIObject[name] = tkinter.Button(
            self.UIObject['edit_root'],
            text = text,
            command = command,
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove'
        )
        self.UIObject[name].bind('<Enter>', lambda x : self.buttom_action(name, '<Enter>'))
        self.UIObject[name].bind('<Leave>', lambda x : self.buttom_action(name, '<Leave>'))
        self.UIObject[name].bind('<Button-1>', lambda x : self.clickRecord(name, x))
        self.UIObject[name].place(
            x = x,
            y = y,
            width = width,
            height = height
        )

    def buttom_action(self, name, action):
        if name in self.UIObject:
            if action == '<Enter>':
                self.UIObject[name].configure(bg = self.UIConfig['color_006'])
            if action == '<Leave>':
                self.UIObject[name].configure(bg = self.UIConfig['color_003'])

    def clickRecord(self, name, event):
        self.UIData['click_record'][name] = event

    def tree_edit_UI_Entry_init(self, obj_root, obj_name, str_name, x, y, width_t, width, height, action, title = '', mode = 'NONE'):
        self.UIObject[obj_name + '=Label'] = tkinter.Label(
            self.UIObject[obj_root],
            text = title
        )
        self.UIObject[obj_name + '=Label'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004']
        )
        self.UIObject[obj_name + '=Label'].place(
            x = x - width_t,
            y = y,
            width = width_t,
            height = height
        )
        self.UIData[str_name] = tkinter.StringVar()
        self.UIObject[obj_name] = tkinter.Entry(
            self.UIObject[obj_root],
            textvariable = self.UIData[str_name]
        )
        self.UIObject[obj_name].configure(
            bg = self.UIConfig['color_004'],
            fg = self.UIConfig['color_005'],
            bd = 0
        )
        if mode == 'SAFE':
            self.UIObject[obj_name].configure(
                show = '●'
            )
        self.UIObject[obj_name].place(
            x = x,
            y = y,
            width = width,
            height = height
        )

    def init_data(self):
        tmp_dictCustomData = ChanceCustom.load.dictCustomData
        tmp_hashSelection = self.bot_hash
        self.UIData['list_listbox_L'] = ChanceCustom.load.getCustomDataSortKeyList(
            data = tmp_dictCustomData['data'][tmp_hashSelection],
            reverse = True
        )
        self.UIData['list_listbox_R'] = []

    def load_data(self):
        self.UIObject['listbox_L_StringVar'].set(value = self.UIData['list_listbox_L'])
        self.UIObject['listbox_R_StringVar'].set(value = self.UIData['list_listbox_R'])

    def listbox_selected(self, event, name, name_to):
        selected_indices = self.UIObject[name].curselection()
        selected_langs = [self.UIObject[name].get(i) for i in selected_indices]
        list_this_new:list = []
        list_to_this_new:list = self.UIData['list_%s' % name_to]
        for list_it in self.UIData['list_%s' % name]:
            if list_it in selected_langs:
                list_to_this_new.append(list_it)
            else:
                list_this_new.append(list_it)
        self.UIData['list_%s' % name] = list_this_new
        self.UIObject[name].select_clear(0,None)
        self.load_data()

    def pack_save(self):
        tmp_dictCustomData = ChanceCustom.load.dictCustomData
        tmp_hashSelection = self.bot_hash
        ccpk_name = self.UIData['entry_NAME_StringVar'].get()
        ccpk_author = self.UIData['entry_AUTHOR_StringVar'].get()
        ccpk_version = self.UIData['entry_VERSION_StringVar'].get()
        ccpk_info = self.UIData['entry_INFO_StringVar'].get()
        ccpk_key_list = self.UIData['list_listbox_R']
        if ccpk_name == '':
            return
        ccpk_save_path = ''
        try:
            ccpk_save_path = filedialog.asksaveasfilename(title = '保存至...', filetypes=[("程心包", "*.ccpk")])
        except:
            tkinter.messagebox.showwarning('运行失败', '你需要使用最新版OlivOS才能使用此功能')
        if ccpk_save_path == '':
            return
        else:
            ccpk_save_path += '.ccpk'
        ccpk_data = {
            'type': 'ccpk',
            'dataVersion' : ChanceCustom.load.dataVersion,
            'info': {
                'name': ccpk_name,
                'author': ccpk_author,
                'version': ccpk_version,
                'info': ccpk_info
            },
            'data': {}
        }
        for ccpk_key_this in ccpk_key_list:
            if ccpk_key_this in tmp_dictCustomData['data'][tmp_hashSelection]:
                ccpk_data['data'][ccpk_key_this] = tmp_dictCustomData['data'][tmp_hashSelection][ccpk_key_this]
        releaseDir('./plugin')
        releaseDir('./plugin/data')
        releaseDir('./plugin/data/ChanceCustom')
        releaseDir('./plugin/data/ChanceCustom/pack')
        removeDir('./plugin/data/ChanceCustom/pack/tmp')
        removeDir('./plugin/data/ChanceCustom/pack/tmp.ccpk')
        releaseDir('./plugin/data/ChanceCustom/pack/tmp')
        ccpk_tmp_dir_path = './plugin/data/ChanceCustom/pack/tmp'
        ccpk_tmp_path = ccpk_tmp_dir_path + '/data.json'
        with open(ccpk_tmp_path, 'w', encoding = 'utf-8') as ccpk_tmp_path_f:
            ccpk_tmp_path_f.write(json.dumps(ccpk_data, ensure_ascii = False, indent = 4))
        ccpk_tmp_path = './plugin/data/ChanceCustom/pack/tmp.ccpk'
        with zipfile.ZipFile(ccpk_tmp_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for dirpath, dirnames, filenames in os.walk(ccpk_tmp_dir_path):
                for filename in filenames:
                    fpath = dirpath.replace(ccpk_tmp_dir_path, '')
                    for filename in filenames:
                        z.write(os.path.join(dirpath, filename), os.path.join(fpath, filename))
        copyFile(ccpk_tmp_path, ccpk_save_path)
        removeDir(ccpk_tmp_dir_path)
        removeDir(ccpk_tmp_path)
        tkinter.messagebox.showinfo('完成打包', '程心导入包已保存至 %s' % ccpk_save_path)

def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def removeDir(dir_path):
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
    except:
        try:
            if os.path.exists(dir_path):
                os.remove(dir_path) 
        except:
            pass

def copyFile(src, dst):
    try:
        shutil.copyfile(src = src, dst = dst)
    except:
        pass
