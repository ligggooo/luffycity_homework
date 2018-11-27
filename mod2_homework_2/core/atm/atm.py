#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   atm.py
@Time    :   2018/11/26 9:20
@Desc    :   取款机
'''
from core.auth import login,auth_passwd
from core.menu import menu_loader
from core.atm.utils import check_account,repay,transfer,withdraw
import core.global_keeper as global_keeper

menu = {
	'tag': 'ATM机',
	'msg': '输入T、C、W、R选择其中一项，b 返回主界面，q 退出程序:',
	'functions': [],
	'sub': {
		'C': {
			'tag': '查询',
			'msg': '输入b退回ATM主界面，q退出程序：',
			'functions': [check_account,],
			'sub':{}
		},
		'R': {
			'tag': '还款',
			'msg': '输入b退回ATM主界面，q退出程序：',
			'functions': [repay,],
			'sub':{}
		},
		'T': {
			'tag': '转账',
			'msg': '输入b退回ATM主界面，q退出程序：',
			'functions': [transfer,],
			'sub':{}
		},
		'W': {
			'tag': '提现',
			'msg': '输入b退回ATM主界面，q退出程序：',
			'functions': [withdraw,],
			'sub':{}
		}
	}
}

@login
def atm():
	menu_loader(menu,is_root=False)

if __name__ == '__main__':
	global_keeper._init()  # 全局变量，标记用户状态
	global_keeper.set_value('user_name', 'luffy')
	global_keeper.set_value('login_status', True)
	atm()
