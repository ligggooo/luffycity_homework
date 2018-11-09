#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author: Goodwillie
# datetime: 2018/11/9 15:24
# project: Luffycity_homework
# description: 员工信息增删改查程序—基础函数

def execute(command):
	command_pieces = command.split(' ')
	if len(command_pieces) <2:
		return -1  # 太短一定是错的
	else:
		command_type = command_pieces[0] # 命令行的第一个词决定了命令的类型
	if command_type == 'find': # 分开执行，遇到不能识别的命令会返回-1
		return find(command_pieces)
	elif command_type == 'add':
		return add(command_pieces)
	elif command_type == 'del':
		return delete(command_pieces)
	elif command_type == 'update':
		return update(command_pieces)
	else:
		return -1

position = {'staff_id':0,'name':1,'age':2,'phone':3,'dept':4,'eroll_date':5}
def find(command_left):
	print(command_left)
	to_find = command_left[0].split(',')
	return 0

def add(command_left):
	print(command_left)
	return 0

def delete(command_left):
	print(command_left)
	return 0

def update(command_left):
	print(command_left)
	return 0



if __name__ == '__main__':
	execute('find name,age from staff_table where age > 22')
	execute('find name,age from staff_table where age > 22')
	execute('find name,age from staff_table where age > 22')
	execute('find name,age from staff_table where age > 22')