#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author: Goodwillie
# datetime: 2018/11/9 15:14
# project: Luffycity_homework
# description: 员工信息增删改查程序

from utils import *


def check_execute(command):
	if command == 'Q':
		exit('退出')
	if execute(command) != 0:
		print(command, ' Not valid !')


while 1:
	print('请输入命令行或者q退出')
	command = input('>>>').strip() # 掐头去尾，大写
	check_execute(command)