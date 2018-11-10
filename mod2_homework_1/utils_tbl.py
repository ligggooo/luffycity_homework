#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils_tbl.py
@Time    :   2018/11/10 9:14
@Desc    :   员工信息增删改查程序—基础函数  表文件操作函数
'''
import json
import os


def check_record(tbl_name,record): # ToDO
	'''
	检查要添加的记录是否符合标准： 表是否存在 主键是否重复 各个字段有无超长
	:param tbl_name:  表名
	:param record:
	:return:
	'''
	return True

def table_exist(tbl_name): # ToDO
	return True

def get_max_id(tbl_name):
	tbl_info = json.loads(open('./data/%s.aux'%tbl_name,encoding='utf-8').read())
	return tbl_info['max_id']

def set_max_id(tbl_name,id):
	tbl_info = json.loads(open('./data/%s.aux' % tbl_name, encoding='utf-8').read())
	tbl_info['max_id'] = id
	open('./data/%s.aux' % tbl_name,'w', encoding='utf-8').write(json.dumps(tbl_info,indent='\t'))

if __name__ == '__main__':
	pass
