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
import hashlib
import traceback

user_file = conf.user_file
root_file = conf.root_file

def login_status():
	return global_keeper.get_value('login_status')

def get_user_name():
	return global_keeper.get_value('user_name')

def login(func): # 这个装饰器用于登陆认证，三次错误锁定账户
	def decorated(*args, **kwargs):
		if not global_keeper.get_value('login_status'):
			# 用户认证
			user_name = _check_login()
			global_keeper.set_value('user_name', user_name)
			global_keeper.set_value('login_status', True)
		else:
			print('已经登陆')
		return func(*args, **kwargs)
	return decorated

def auth_passwd(func): # 这个装饰器用于支付认证，五次错误锁定账户
	def decorated(*args, **kwargs):
		if not global_keeper.get_value('login_status'): # 先确保用户已经登陆，未登陆要求登陆，已登陆跳过
			# 用户认证
			user_name = _check_login()
			global_keeper.set_value('user_name', user_name)
			global_keeper.set_value('login_status', True)
		else:
			pass
		# 支付密码验证
		user_name=global_keeper.get_value('user_name')
		if _check_passwd(user_name): # 如果密码验证不通过会直接退出程序并被冻结
			print('支付密码通过了',)
		else:
			print('') # 实际上不会循环到这里来
		return func(*args, **kwargs)
	return decorated

def isRoot(func): # 这个装饰器用于检验超级用户
	@login # 使用login做一次保护，要求用户名是root，
	def decorated(*args, **kwargs):
		if login_status() and get_user_name()=='root': #
			pw = input('请输入root用户隐藏密码:') # 使用隐藏密码做第二次保护
			h = hashlib.sha256(pw.encode('utf-8'))
			h_pw = h.hexdigest()
			if h_pw == _get_root_pass_wd():
				return func(*args, **kwargs)
		else:
			print('你不是超级用户')
			return None
	return decorated

# --------------------- 以下为底层函数      -----------------

def _get_root_pass_wd():
	root_data = json.loads(open(root_file).read())['root']
	h = hashlib.sha256(root_data['secret_passwd'].encode('utf-8'))
	h_pw = h.hexdigest()
	return h_pw



def _check_login(user_file=user_file):
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
					print('登陆成功', user_name, '!')
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

def _check_passwd(user_name,user_file=user_file):
	user_status = json.loads(open(user_file).read())  # 读取用户数据文件
	user_pay_passwd_recored = user_status[user_name]['pay_passwd'] # 获取支付密码

	if user_name in user_status:  # 若账户在user-file中，验证其锁定状态
		status = user_status[user_name]['status']
		if status == 'locked':
			exit('此账户已被锁定，无法使用')

	try_left = 5
	while try_left > 0:
		user_passwd = input('请输入支付密码： ')
		if user_passwd == user_pay_passwd_recored:  # 若密码验证通过，则返回True
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

def _load_users():
	accounts = json.loads(open(user_file).read())
	return accounts

def _save_users(users):
	try:
		open(user_file, 'w').write(json.dumps(users, indent=' '))
		return True
	except Exception as e:
		traceback.print_exc()
		return False

if __name__ == '__main__':
	pass
