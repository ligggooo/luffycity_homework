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

menu = {
	'tag': 'ATM机',
	'msg': '输入S或A选择其中一项，q 退出程序:',
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
	menu_loader(menu)


if __name__ == '__main__':
	pass
