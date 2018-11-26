#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils_tbl.py
@Time    :   2018/11/10 9:14
@Desc    :   员工信息增删改查程序——文件操作相关
'''
import json
import os


def check_record(tbl_name,record):
	'''
	检查要添加的记录是否符合标准： 表是否存在 主键是否重复 各个字段有无超长
	:param tbl_name:  表名
	:param record:
	:return:
	'''
	P_KEY = load_P_KEY(tbl_name)
	table_info = json.loads(open('./data/%s.aux'%tbl_name,encoding='utf-8').read())
	tbl_structure_position = table_info['tbl_structure_position']

	p_key_name = table_info['primary_key']
	p_key_ind = table_info['tbl_structure_position'][p_key_name]
	record = record.strip().split(',')
	if len(tbl_structure_position) != len(record)+1:
		print('字段缺失')
		return False
	elif record[p_key_ind-1] in P_KEY:
		print('主键冲突')
		return False
	else:  # 还可以检测各个插入字段是否符合类型定义，是否符合预设的长度限制条件
		return True

def table_exist(tbl_name):
	if os.path.exists('./data/%s.aux' % tbl_name) and os.path.exists('./data/%s.data' % tbl_name):
		return True
	else:
		return False

def get_max_id(tbl_name):
	tbl_info = json.loads(open('./data/%s.aux'%tbl_name,encoding='utf-8').read())
	return tbl_info['max_id']

def set_max_id(tbl_name,id):
	tbl_info = json.loads(open('./data/%s.aux' % tbl_name, encoding='utf-8').read())
	tbl_info['max_id'] = id
	open('./data/%s.aux' % tbl_name,'w', encoding='utf-8').write(json.dumps(tbl_info,indent='\t'))

def load_P_KEY(tbl_name):
	tbl_name = tbl_name.upper()
	table_info = json.loads(open('./data/%s.aux' % tbl_name, encoding='utf-8').read())
	p_key_name = table_info['primary_key']
	p_key_ind = table_info['tbl_structure_position'][p_key_name]
	p_keys = []
	if not table_exist(tbl_name):
		print('表不存在')
		return -1
	for line in open('./data/%s.data' % tbl_name, encoding='utf-8'):
		p_keys.append(line.strip().split(',')[p_key_ind])
	return p_keys

def print_info(tbl_name):
	table_info = json.loads(open('./data/%s.aux' % tbl_name, encoding='utf-8').read())
	if not table_exist(tbl_name):
		print('表不存在')
		return -1
	else:
		print('可选字段',' '.join(table_info['tbl_structure_detail']))

def load_table_info(tbl_name):
	table_info = json.loads(open('./data/%s.aux' % tbl_name, encoding='utf-8').read())
	tbl_structure_position = table_info['tbl_structure_position']
	tbl_structure_type = table_info['tbl_structure_type']
	tbl_structure = [tbl_structure_position,tbl_structure_type]
	primary_key = table_info['primary_key']
	return tbl_structure, primary_key



if __name__ == '__main__':
	pass
