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
        '前缀匹配',
        '正则匹配'
    ],
    'matchTypeList_loadMap': {
        'full': '完全匹配',
        'perfix': '前缀匹配',
        'reg': '正则匹配'
    },
    'matchTypeList_saveMap': {
        '完全匹配': 'full',
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
        self.UIObject['root'] = tkinter.Tk()
        self.UIObject['root'].title('程心自定义')
        self.UIObject['root'].geometry('518x400')
        self.UIObject['root'].resizable(
            width = False,
            height = False
        )
        self.UIObject['root'].configure(bg = self.UIConfig['color_001'])

        self.UIData['hash_now'] = 'unity'
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
            name = 'root_Button_SAVE',
            text = '保存',
            command = lambda : self.tree_save(),
            x = 380,
            y = 15,
            width = 120,
            height = 34
        )

        self.UIObject['root'].iconbitmap('./resource/tmp_favoricon.ico')
        self.UIObject['root'].mainloop()
        ChanceCustom.load.flag_open = False

    def tree_init(self):
        self.UIObject['tree'] = ttk.Treeview(self.UIObject['root'])
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
        self.UIObject['tree_rightkey_menu'] = tkinter.Menu(self.UIObject['root'], tearoff = False)
        #self.UIObject['tree'].bind('<<TreeviewSelect>>', lambda x : self.treeSelect('tree', x))
        self.tree_load()
        self.UIObject['tree'].place(x = 15, y = 64, width = 488 - 18, height = 321)
        self.UIObject['tree'].bind('<Button-3>', lambda x : self.tree_rightKey(x))
        self.UIObject['tree_yscroll'] = ttk.Scrollbar(
            self.UIObject['root'],
            orient = "vertical",
            command = self.UIObject['tree'].yview
        )
        self.UIObject['tree_yscroll'].place(
            x = 15 + 488 - 18,
            y = 64,
            width = 18,
            height = 321
        )
        self.UIObject['tree'].configure(
            yscrollcommand = self.UIObject['tree_yscroll'].set
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
                pass

    def tree_save(self):
        ChanceCustom.load.saveCustomData()

    def tree_rightKey(self, event):
        self.UIObject['tree_rightkey_menu'].delete(0, tkinter.END)
        self.UIObject['tree_rightkey_menu'].add_command(label = '添加', command = lambda : self.tree_edit('create'))
        self.UIObject['tree_rightkey_menu'].add_command(label = '编辑', command = lambda : self.tree_edit('update'))
        self.UIObject['tree_rightkey_menu'].add_command(label = '删除', command = lambda : self.tree_edit('delete'))
        self.UIObject['tree_rightkey_menu'].post(event.x_root, event.y_root)

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

        self.tree_edit_UI_Combobox_init(
            obj_root = 'edit_root',
            obj_name = 'edit_root_matchType',
            str_name = 'edit_root_matchType_StringVar',
            x = 70,
            y = 60,
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
            y = 60,
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
            y = 60,
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
            y = 100,
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
            self.UIObject['edit_root_matchType'].current(0)
            self.UIObject['edit_root_matchPlace'].current(0)
            self.UIData['edit_root_priority_StringVar'].set(str(0))
        elif self.action == 'update':
            tmp_data_this = ChanceCustom.load.dictCustomData['data'][self.bot_hash][self.key]
            self.UIData['edit_root_key_StringVar'].set(str(tmp_data_this['key']))
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
