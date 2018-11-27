#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   admin.py
@Time    :   2018/11/27 14:07
@Desc    :   提供管理接口，包括添加账户、用户额度，冻结账户等
'''

from core.menu import menu_loader,go_back
from core.auth import isRoot
import core.global_keeper as global_keeper
from core.admin.utils import add_account,set_limit,freeze_account,edit_account

menu = {
	'tag': '管理员界面',
	'msg': '输入 选择其中一项，b 返回主界面，q 退出程序:',
	'functions': [],
	'sub': {
		'A': {
			'tag': '添加账户',
			'msg': '输入b退回ATM主界面，q退出程序：',
			'functions': [add_account,go_back],
			'sub':{}
		},
		'S': {
			'tag': '设置用户额度',
			'msg': '输入b退回ATM主界面，q退出程序：',
			'functions': [set_limit,go_back],
			'sub':{}
		},
		'F': {
			'tag': '冻结账户',
			'msg': '输入b退回ATM主界面，q退出程序：',
			'functions': [freeze_account,go_back],
			'sub':{}
		},
		'E': {
			'tag': '设置账户',
			'msg': '输入b退回ATM主界面，q退出程序：',
			'functions': [edit_account,go_back,],
			'sub':{}
		}
	}
}

@isRoot
def admin():
	menu_loader(menu,is_root_tree=False)


if __name__ == '__main__':
	global_keeper._init()  # 全局变量，标记用户状态
	global_keeper.set_value('user_name', 'root')
	global_keeper.set_value('login_status', True)
	admin()
