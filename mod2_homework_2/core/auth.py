#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   auth.py
@Time    :   2018/11/26 9:18
@Desc    :   用户认证
'''
# 认证状态需要一个跨模块的全局变量来保存
# login会检查这个全局变量，通过之后会对其赋值，
# 配合一个logout，会清空这个全局变量

import core.global_keeper as global_keeper

def login(func):
	def decorated(*args, **kwargs):
		'''
		用户认证代码
		'''
		print('登陆成功',global_keeper.get_value('user'))
		return func(*args, **kwargs)
	return decorated

def auth_passwd(func):
	def decorated(*args, **kwargs):
		'''
		用户认证代码
		'''
		print('支付密码通过了',)
		return func(*args, **kwargs)
	return decorated

if __name__ == '__main__':
	pass
