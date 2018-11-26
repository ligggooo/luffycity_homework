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
import conf.config as conf
import json

user_file = conf.user_file

def login(func): # 这个装饰器用于登陆认证，三次错误锁定账户
	def decorated(*args, **kwargs):
		if not global_keeper.get_value('login_status'):
			# 用户认证
			user_name = check_login()
			global_keeper.set_value('username', user_name)
			global_keeper.set_value('login_status', True)
		else:
			print('已经登陆')
		return func(*args, **kwargs)
	return decorated

def auth_passwd(func): # 这个装饰器用于支付认证，五次错误锁定账户
	def decorated(*args, **kwargs):
		if not global_keeper.get_value('login_status'): # 先确保用户已经登陆，未登陆要求登陆，已登陆跳过
			# 用户认证
			user_name = check_login()
			global_keeper.set_value('username', user_name)
			global_keeper.set_value('login_status', True)
		else:
			pass
		# 支付密码验证
		user_name=global_keeper.get_value('username')
		if check_passwd(user_name): # 如果密码验证不通过会直接退出程序并被冻结
			print('支付密码通过了',)
		else:
			print('') # 实际上不会循环到这里来
		return func(*args, **kwargs)
	return decorated

def check_login(user_file=user_file):
	user_status = json.loads(open(user_file).read())  # 读取用户数据文件
	try_left = 3
	while try_left > 0:
		user_name = input('请输入用户名： ')
		if user_name in user_status:  # 若账户在user-file中，验证其锁定状态
			status = user_status[user_name]['status']
			if status == 'locked':
				exit('此账户已被锁定，无法使用')  # 若账户处于锁定状态，则直接退出程序             # 1 退出--》
			else:  # 否则，进入密码验证环节
				user_passwd_recored = user_status[user_name]['passwd']
				user_passwd = input('请输入密码： ')
				if user_passwd == user_passwd_recored:  # 若密码验证通过，则进入欢迎界面
					print('Welcome,', user_name, '!')
					return user_name                                                           # 2 返回 --》
				else:  # 否则try_left减1
					try_left -= 1
					print('密码错误,还有%s次机会' % try_left)                                   # 3 进入下一循环
		else:  # 若账户不在user_file中，try_left减1
			try_left -= 1
			print('无此账户,还有%s次机会' % try_left)                                           # 4 进入下一循环

	print('三次错误')  # 到了这里说明三次尝试都没有通过密码验证，需要锁定一个账户
	if user_name in user_status:
		user_status[user_name]['status'] = 'locked'
		open(user_file, 'w').write(json.dumps(user_status, indent='  '))
		print(user_name, '已被锁定')# 5 锁定最后一次输入的账户
	else:
		print('无法确定锁定对象')
	exit('退出程序')  # 6 除了#2 的另一个出口

def check_passwd(user_name,user_file=user_file):
	user_status = json.loads(open(user_file).read())  # 读取用户数据文件
	user_passwd_recored = user_status[user_name]['passwd'] # 获取用户密码

	try_left = 5
	while try_left > 0:
		user_passwd = input('请输入支付密码： ')
		if user_passwd == user_passwd_recored:  # 若密码验证通过，则返回True
			return True  # 2 返回 --》
		else:  # 否则try_left减1
			try_left -= 1
			print('密码错误,还有%s次机会' % try_left)
	print('超过尝试次数限定')
	if user_name in user_status:
		user_status[user_name]['status'] = 'locked'
		open(user_file, 'w').write(json.dumps(user_status, indent='  '))
		print(user_name, '已被锁定')  # 5 锁定最后一次输入的账户
	else:
		print('无法确定锁定对象')
	exit('退出程序')  # 6 除了#2 的另一个出口

if __name__ == '__main__':
	pass
