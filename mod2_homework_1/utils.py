#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author: Goodwillie
# datetime: 2018/11/9 15:24
# project: Luffycity_homework
# description: 员工信息增删改查程序—基础函数

position = {'staff_id':0,'name':1,'age':2,'phone':3,'dept':4,'eroll_date':5} # 表结构
primary_key = 3 # 主键

# 一个操作命令由关键字key_word和限定段command__spec两部分构成
key_words = ['FIND','ADD','DEL','UPDATE','FROM','WHERE','SET'] # 关键字列表
command_specs = ['AREA','TBL_NAME','CONDITION','TO_SET'] # 语句限定段列表

# 下面的模板序列定义了各种类型的命令,command_parser会根据模板将一个实际的命令拆分成段
FIND_TEMPLATE = ['CONDITION','WHERE','TBL_NAME','FROM','AREA','FIND'] # 定义find的操作顺序，每次pop一个出来
ADD_TEMPLATE = ['RECORD','TBL_NAME','ADD']
DEL_TEMPLATE = ['CONDITION','WHERE','TBL_NAME','DEL']
UPDATE_TEMPLATE = ['CONDITION','WHERE','TO_SET','SET','TBL_NAME','UPDATE']

def command_parser(command_pieces,command_template):
	'''
	这个函数会根据预先定义好的模板去解析一个命令，输出一个便于函数读取的参数字典
	:param command_pieces: 命令字符串
	:param command_template: 预定义的模板
	:return:
	'''
	# if len(command_pieces) != len(command_template):
	# 	return -1 # 模板长度和命令长度不符
	output = {}
	index = 0
	len_command_pieces = len(command_pieces)
	while len(command_template)>0:
		part = command_template.pop()
		if part in key_words: # 根据模板，命令的下一个字符串应该是一个关键字
			if command_pieces[index] == part: # 命令的下一个关键字与模板吻合
				index += 1 # Jump over this keyword
			else: # 命令的下一个关键字与模板不吻合，命令有错，退出
				return -1
		elif part in command_specs: # 根据模板，命令的下一个字符串应该是一个限定段
			name = part # 将这个段按照模板要求的进行命名
			val = ''
			while command_pieces[index] not in key_words: # 下一个关键字之前的所有部分都属于这个限定段
				val +=command_pieces[index]
				index += 1
				if index >= len_command_pieces:
					break
			output[name] = val
		else:  # 模板必须由key_words和command_specs构成，否则模板有错误
			print('模板错误')
			return -1
	return output



def execute(command):
	command = command.upper()
	command_pieces = command.split(' ')

	if len(command_pieces) <2:
		return -1  # 太短一定是错的
	else:
		command_type = command_pieces[0] # 命令行的第一个词决定了命令的类型
	if command_type == 'FIND': # 分开执行，遇到不能识别的命令会返回-1
		return find(command_pieces)
	elif command_type == 'ADD':
		return add(command_pieces)
	elif command_type == 'DEL':
		return delete(command_pieces)
	elif command_type == 'UPDATE':
		return update(command_pieces)
	else:
		return -1


def find(command_pieces):
	args = command_parser(command_pieces,FIND_TEMPLATE[:])
	print(args)
	return 0

def add(command_pieces):
	print(command_pieces)
	return 0

def delete(command_pieces):
	print(command_pieces)
	return 0

def update(command_pieces):
	print(command_pieces)
	return 0



if __name__ == '__main__':
	execute('find name,age from staff_table where age > 22')
	execute('find name,age from staff_table where age > 22')
	execute('find name,age from staff_table where age > 22')
	execute('find name,age from staff_table where age > 22')