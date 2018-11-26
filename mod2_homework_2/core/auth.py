#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   auth.py
@Time    :   2018/11/26 9:18
@Desc    :   用户认证
'''
def login(func):
	def decorated(*args, **kwargs):
		'''
		用户认证代码
		'''
		print('认证通过了')
		return func(*args, **kwargs)
	return decorated

def auth_passwd(func):
	def decorated(*args, **kwargs):
		'''
		用户认证代码
		'''
		print('支付密码通过了')
		return func(*args, **kwargs)
	return decorated

if __name__ == '__main__':
	pass
