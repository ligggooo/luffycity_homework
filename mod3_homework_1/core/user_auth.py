#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   user_auth.py
@Time    :   2018/12/6 14:58
@Desc    :
'''
from conf.config import user_info

def login():
	name = input('username : ')
	passwd = input('password : ')
	with open(user_info,encoding='utf-8') as f:
		for line in f:
			usr,pwd,identify = line.strip().split('|')
			if usr == name and passwd == pwd:
				return {'result':True,'name':name,'id':identify}
		else:
			return {'result':False,'name':name}

def write_user_info(name,passwd,id):
	with open(user_info,'a', encoding='utf-8') as f:
		f.write('\n%s|%s|%s'%(name,passwd,id))