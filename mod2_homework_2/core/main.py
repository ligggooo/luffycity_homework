#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   main.py
@Time    :   2018/11/26 9:12
@Desc    :   主函数
'''
from core.mall import mall
from core.atm import atm
from core.menu import menu_loader
from core.auth import login,auth_passwd
import core.global_keeper as global_keeper


global_keeper._init() # 全局变量，标记用户状态
global_keeper.set_value('user_name', '')
global_keeper.set_value('login_status', False)

@login
def welcome():
	print('Welcome',global_keeper.get_value('user_name'))

menu = {
	'tag': '主界面',
	'msg': '输入S或A选择其中一项，q 退出程序:',
	'functions': [welcome],
	'sub': {
		'S': {
			'tag': '商城',
			'msg': '输入b退回主界面，q退出程序：',
			'functions': [mall,],
			'sub':{}
		},
		'A': {
			'tag': '取款机',
			'msg': '输入b退回主界面，q退出程序：',
			'functions': [atm,],
			'sub':{}
		}
	}
}

if __name__ == '__main__':
	menu_loader(menu)


