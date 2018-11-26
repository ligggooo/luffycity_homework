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
		print(command, ' 无效命令')


CONSOLE = False
if CONSOLE:
	while 1:
		print('请输入命令行或者q退出,DESC + 表名显示可用字段信息')
		command = input('>>>').strip()
		check_execute(command)
else:
	# 也可以以如下方式执行
	execute('desc staff_table')
	input('next')
	execute('find name,age from staff_table where age > 22')
	input('next')
	execute('find name,age from staff_table where (age >= 23 and dept=\'IT\') or name = \'Alex Li\'')
	input('next')
	execute('UPDATE staff_table SET age=25,name=Ding Dong WHERE name = "Alex Li"')
	input('next')
	execute('UPDATE staff_table SET age=25,dep=W.C. WHERE name = "Alex Li"')
	input('next')
	execute('del from staff_table where staff_id=3')
	input('next')
	execute('add staff_table with Alex Li,25,134435344,IT,2015‐10‐29')
	input('next')