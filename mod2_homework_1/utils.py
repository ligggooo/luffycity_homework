#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Goodwillie
# datetime: 2018/11/9 15:24
# project: Luffycity_homework
# description: 员工信息增删改查程序—基础函数

tbl_structure_position = {'STAFF_ID': 0, 'NAME': 1, 'AGE': 2, 'PHONE': 3, 'DEPT': 4, 'ENROLL_DATE': 5}  # 表结构 列名位置索引
tbl_structure_type = {'STAFF_ID': int, 'NAME': str, 'AGE': int, 'PHONE':int, 'DEPT': str, 'ENROLL_DATE': str}  # 表结构 列类型索引
tbl_structure = [tbl_structure_position,tbl_structure_type]
primary_key = 3  # 主键

# 一个操作命令由关键字key_word和限定段command__spec两部分构成
key_words = ['FIND','ADD','DEL','UPDATE','FROM','WHERE','SET']  # 关键字列表
command_specs = ['AREA','TBL_NAME','CONDITION','TO_SET'] # 语句限定段列表

# 下面的模板序列定义了各种类型的命令,command_parser会根据模板将一个实际的命令拆分成若干段
FIND_TEMPLATE = ['CONDITION', 'WHERE', 'TBL_NAME', 'FROM', 'AREA', 'FIND']  # 定义find的操作顺序，每次pop一个出来
ADD_TEMPLATE = ['RECORD', 'TBL_NAME', 'ADD']
DEL_TEMPLATE = ['CONDITION', 'WHERE', 'TBL_NAME', 'DEL']
UPDATE_TEMPLATE = ['CONDITION', 'WHERE', 'TO_SET', 'SET', 'TBL_NAME', 'UPDATE']


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
				val = val + command_pieces[index] + ' '
				index += 1
				if index >= len_command_pieces:
					break
			output[name] = val
		else:  # 模板必须由key_words和command_specs构成，否则模板有错误
			print('模板错误')
			return -1
	return output


def condition_parser(CONDITION):
	'''
	where语句的解析
	:return:
	'''
	# 解析表达式太难，改用字符替换 + eval实现一个check_condition
	CONDITION = CONDITION.strip()
	return CONDITION.replace('=', '==').replace('AND','and').replace('OR','or').replace('<==','<=').replace('>==','>=')


def check_condition(data_line,tbl_structure,condition):
	[tbl_structure_position, tbl_structure_type] = tbl_structure
	for val_name in tbl_structure_position: # 用一行数据给每一个变量赋值
		if tbl_structure_type[val_name] == str:
			exec('%s = \'%s\''%(val_name,data_line[tbl_structure_position[val_name]].upper()))
		else:
			exec('%s = %s' % (val_name, data_line[tbl_structure_position[val_name]]))
	return eval(condition) # 执行验证条件


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
			output.append(tbl_structure_position[name])
		return output


def execute(command):
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
	else:
		return -1


def find(command_pieces):
	command_dict = command_parser(command_pieces, FIND_TEMPLATE[:])
	print(command_dict)
	area = command_dict['AREA']
	tbl_name = command_dict['TBL_NAME']
	condition = condition_parser(command_dict['CONDITION'])
	col_find = area_parser(area, tbl_structure)
	# print(area_parser(area,tbl_structure))
	for line in open('./data/STAFF_TABLE.data',encoding='utf-8'):
		data_line = line.strip().split(',')
		if check_condition(data_line, tbl_structure, condition):
			out_line = []
			for i in col_find:
				out_line.append(data_line[i])
			print('\t'.join(out_line))
	return 0


def add(command_pieces):
	print(command_pieces)
	return 0

def delete(command_pieces):
	print(command_pieces)
	return 0

def update(command_pieces):
	args = command_parser(command_pieces, UPDATE_TEMPLATE[:])
	print(args)
	print(set_parser(args['TO_SET']))
	return 0



if __name__ == '__main__':
	# execute('find name,age from staff_table where age > 22')
	execute('find name,age from staff_table where (age >= 23 and dept=\'IT\') or name = \'Alex Li\'')
	# execute('UPDATE staff_table SET age=25 WHERE name = "Alex Li"')
	# execute('UPDATE staff_table SET age=25,dep=W.C. WHERE name = "Alex Li"')

