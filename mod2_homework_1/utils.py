#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Goodwillie
# datetime: 2018/11/9 15:24
# project: Luffycity_homework
# description: 员工信息增删改查程序—基础函数

import os
import json
import traceback
from utils_tbl import *

# 一个操作命令由关键字key_word和限定段command__spec两部分构成
key_words = ['FIND','ADD','DEL','UPDATE','FROM','WHERE','SET','WITH','DESC']  # 关键字列表
command_specs = ['AREA','TBL_NAME','CONDITION','TO_SET','RECORD'] # 语句限定段列表

# 下面的模板序列定义了各种类型的命令,command_parser会根据模板将一个实际的命令拆分成若干段
FIND_TEMPLATE = ['CONDITION', 'WHERE', 'TBL_NAME', 'FROM', 'AREA', 'FIND']  # 定义find的操作顺序，每次pop一个出来
ADD_TEMPLATE = ['RECORD','WITH', 'TBL_NAME', 'ADD']
DEL_TEMPLATE = ['CONDITION', 'WHERE', 'TBL_NAME', 'FROM', 'DEL']
UPDATE_TEMPLATE = ['CONDITION', 'WHERE', 'TO_SET', 'SET', 'TBL_NAME', 'UPDATE']
DESC_TEMPLATE = ['TBL_NAME','DESC']

# 读取表结构信息
# tbl_structure_position = {'STAFF_ID': 0, 'NAME': 1, 'AGE': 2, 'PHONE': 3, 'DEPT': 4, 'ENROLL_DATE': 5}  # 表结构 列名位置索引
# tbl_structure_type = {'STAFF_ID': 'int', 'NAME': 'str', 'AGE': 'int', 'PHONE':'int', 'DEPT': 'str', 'ENROLL_DATE': 'str'}  # 表结构 列类型索引
# # tbl_structure_length = {'STAFF_ID': 10, 'NAME': 20, 'AGE': 4, 'PHONE':20, 'DEPT': 20, 'ENROLL_DATE': 15} # 限定每一字段的占位数，便于精确读写,（此功能未完成
# tbl_structure = [tbl_structure_position,tbl_structure_type]
# primary_key = 'PHONE'  # 主键

tbl_structure,primary_key = load_table_info('staff_table')


def command_parser(command_pieces, command_template):
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
				val = val + command_pieces[index] + ' '
				index += 1
				if index >= len_command_pieces:
					break
			output[name] = val.strip()
		else:  # 模板必须由key_words和command_specs构成，否则模板有错误
			print('模板错误')
			return -1
	return output


def condition_parser(CONDITION):
	'''
	where语句的解析
	:return:
	'''
	# 解析逻辑运算表达式难度太高，改用字符替换 + eval实现一个check_condition
	CONDITION = CONDITION.strip()
	return CONDITION.replace('=', '==').replace('AND','and').replace('OR','or').replace('<==','<=').replace('>==','>=')


def check_condition(data_line, tbl_structure, condition):
	try:
		[tbl_structure_position, tbl_structure_type] = tbl_structure
		for val_name in tbl_structure_position: # 用一行数据给每一个变量赋值
			if tbl_structure_type[val_name] == 'str':
				exec('%s = \'%s\''%(val_name,data_line[tbl_structure_position[val_name]].upper()))
			else:
				exec('%s = %s' % (val_name, data_line[tbl_structure_position[val_name]]))
		return eval(condition) # 执行验证条件
	except:
		traceback.print_exc()
		return False


def set_parser(TO_SET):
	'''
	set 赋值语句的解析
	:return: {'字段名0':'待赋值0','字段名1':'待赋值1', ...}
	'''
	out_put = {}
	TO_SET = TO_SET.strip()
	for expr in TO_SET.split(','):
		area, value = expr.split('=')
		out_put[area] = value
	return out_put


def area_parser(AREA,tbl_structure):
	'''
	解析命令行的AREA关键段，返回列索引列表 output
	:param AREA:
	:param tbl_structure:
	:return:
	'''
	tbl_structure_position = tbl_structure[0]
	output=[]
	AREA = AREA.strip()
	if AREA == '*':
		return list(range(len(tbl_structure[0])))
	else:
		for name in AREA.split(','):
			if name not in tbl_structure_position:
				print('指定了不存在的字段')
				return -1
			output.append(tbl_structure_position[name])
		return output


def execute(command):
	try:
		command = command.upper()
		command_pieces = command.split(' ')

		if len(command_pieces) < 2:
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
		elif command_type == 'DESC':
			return desc(command_pieces)
		else:
			return -1
	except Exception as e:
		traceback.print_exc()
		return -1

def desc(command_pieces):
	command_dict = command_parser(command_pieces, DESC_TEMPLATE[:])
	print(command_dict)
	tbl_name = command_dict['TBL_NAME']
	if not table_exist(tbl_name):
		print('表不存在')
		return -1
	print_info(tbl_name)
	return 0

def find(command_pieces):
	command_dict = command_parser(command_pieces, FIND_TEMPLATE[:])
	print(command_dict)
	area = command_dict['AREA']
	tbl_name = command_dict['TBL_NAME']
	if not table_exist(tbl_name):
		print('表不存在')
		return -1
	condition = condition_parser(command_dict['CONDITION'])
	col_find = area_parser(area, tbl_structure)
	if col_find == -1: # 说明字段解析错误
		print('字段解析错误')
		return  -1
	# print(area_parser(area,tbl_structure))
	for line in open('./data/%s.data'%tbl_name, encoding='utf-8'):
		data_line = line.strip().split(',')
		if check_condition(data_line, tbl_structure, condition):
			out_line = []
			for i in col_find:
				out_line.append(data_line[i])
			print('\t'.join(out_line))
	return 0


def add(command_pieces):
	command_dict = command_parser(command_pieces, ADD_TEMPLATE[:])
	print(command_dict)
	tbl_name = command_dict['TBL_NAME']
	if not table_exist(tbl_name):
		print('表不存在')
		return -1
	record = command_dict['RECORD']
	if check_record(tbl_name,record): # 检查要添加的记录是否符合标准
		id = get_max_id(tbl_name)+1 # 获取新纪录的id
		data_file_name = './data/%s.data' % tbl_name
		f= open(data_file_name,'a',encoding='utf-8')
		line = str(id)+','+record+'\n'
		f.write(line)
		f.close()
		set_max_id(tbl_name,id)
		return 0
	else:
		return -1


def delete(command_pieces):
	command_dict = command_parser(command_pieces, DEL_TEMPLATE[:])
	print(command_dict)
	tbl_name = command_dict['TBL_NAME']
	if not table_exist(tbl_name):
		print('表不存在')
		return -1
	condition = condition_parser(command_dict['CONDITION'])
	data_file_name = './data/%s.data' % tbl_name
	data_file_name_new = './data/%s.data.new' % tbl_name
	file_new = open(data_file_name_new, 'w', encoding='utf-8')
	for line in open(data_file_name, encoding='utf-8'):
		data_line = line.strip().split(',')
		if not check_condition(data_line, tbl_structure, condition):
			file_new.write(line)
		else:
			print('删除',line)
	file_new.close()
	os.remove(data_file_name)
	os.rename(data_file_name_new, data_file_name)
	return 0

def update(command_pieces):
	command_dict = command_parser(command_pieces, UPDATE_TEMPLATE[:])
	print(command_dict)
	tbl_name = command_dict['TBL_NAME']
	if not table_exist(tbl_name):
		print('表不存在')
		return -1
	condition = condition_parser(command_dict['CONDITION'])
	to_set = set_parser(command_dict['TO_SET'])
	print(to_set)
	data_file_name = './data/%s.data'%tbl_name
	data_file_name_new = './data/%s.data.new'%tbl_name
	file_new = open(data_file_name_new, 'w',encoding='utf-8')
	for line in open(data_file_name, encoding='utf-8'):
		data_line = line.strip().split(',')
		if check_condition(data_line, tbl_structure, condition):
			print('old line',line)
			for key in to_set:
				index = tbl_structure[0][key]
				value = to_set[key]
				data_line[index]=value
			line = ','.join(data_line)+'\n'
			print('new line', line)
		file_new.write(line)
	file_new.close()
	os.remove(data_file_name)
	os.rename(data_file_name_new, data_file_name)
	return 0




if __name__ == '__main__':
	# execute('find name,age from staff_table where age > 22')
	# execute('find name,age from staff_table where (age >= 23 and dept=\'IT\') or name = \'Alex Li\'')
	# execute('UPDATE staff_table SET age=25,name=Ding Dong WHERE name = "Alex Li"')
	# execute('UPDATE staff_table SET age=25,dep=W.C. WHERE name = "Alex Li"')
	# execute('del from staff_table where staff_id=3')
	# execute('add staff_table with Alex Li,25,134435344,IT,2015‐10‐29')
	pass