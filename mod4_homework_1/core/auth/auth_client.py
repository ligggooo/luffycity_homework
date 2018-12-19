#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   auth.py
@Time    :   2018/12/9 16:58
@Desc    :   认证模块 用户端  打包认证数据
'''

def login(func):  # 将这个装饰器绑定在client的run方法上
	def login_decorated(*args,**kwargs):   # 每次建立连接的时候调用一次这部分认证代码
		client = args[0]  # self
		username = input('>>>请输入账户名：')
		passwd = input('>>>请输入密码：')
		if check_auth(username,passwd):
			res = client.send_auth(username,passwd) # 如果认证没通过，服务器会主动断开此次连接
			print(res['msg'])
			if not res['status']:
				client.socket.close()
			else:
				try:
					func(*args,**kwargs)
				except ConnectionResetError:
					print('连接被服务器中断')
	return login_decorated


def check_auth(usrname,passwd): # 可以增加一些约束条件
	print('check', usrname, passwd)
	return True
