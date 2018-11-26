#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   main.py
@Time    :   2018/11/26 9:12
@Desc    :   主函数
'''
from core.mall import cart
from core.atm import account
from core.menu import menu_loader

user = {'name':'na','login':'False'} #全局变量，标记用户状态

menu = {
	'tag': '主界面',
	'msg': '输入S或A选择其中一项，q 退出程序:',
	'todo': [],
	'sub': {
		'S': {
			'tag': '商城',
			'msg': '进入商城',
			'todo': [cart]
		},
		'A': {
			'tag': '取款机',
			'msg': '进入ATM',
			'todo': [account]
		}
	}
}

if __name__ == '__main__':
	menu_loader(menu)


