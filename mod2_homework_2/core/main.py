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

@auth
def welcome():
	print('wel',user)

menu = {
	'tag': '主界面',
	'msg': '输入S或A选择其中一项，q 退出程序:',
	'functions': [welcome],
	'sub': {
		'S': {
			'tag': '商城',
			'msg': '输入b退回主界面，q退出程序：',
			'functions': [cart,],
			'sub':{}
		},
		'A': {
			'tag': '取款机',
			'msg': '输入b退回主界面，q退出程序：',
			'functions': [account,],
			'sub':{}
		}
	}
}

if __name__ == '__main__':
	menu_loader(menu)


