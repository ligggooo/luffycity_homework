#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils.py
@Time    :   2018/11/27 14:42
@Desc    :   admin的支持模块
'''

import re
import traceback

def add_account():
	print('添加账户')
	users = _load_users()
	accounts = _load_accounts()
	# print(users)
	# print(accounts)
	while 1:
		user_name = input('输入需要添加的账户名，b退回，q退出:')
		if user_name.lower() == 'q':
			exit('退出')
		elif user_name.lower() == 'b':
			return 0
		elif user_name in users or user_name in accounts:
			print('此账户已经存在,请重输')
		else:
			while 1:
				command = input('依次输入(密码)(支付密码)(账户额度),中间用空格隔开，b退回，q退出:').strip()
				if command.lower() == 'q':
					exit('退出')
				elif command.lower() == 'b':
					return 0
				else:
					s = re.search('^(\w+)\s+(\w+)\s+(\d+\.\d+|[1-9]\d*)$',command)
					if not s:
						print('输入格式有误')
					else:
						passwd,pay_passwd,balance = s.groups()
						try:
							balance = float(balance)
							if _add_account(user_name,passwd,pay_passwd,float(balance),users,accounts):
								print('添加成功')
							else:
								print('添加失败')
						except Exception as e:

							traceback.print_exc()
							print('输入金额有误')

def set_limit():
	users = _load_users()
	accounts = _load_accounts()
	while 1:
		user_name = input('输入需要设置额度的账户名，b退回，q退出:')
		if user_name.lower() == 'q':
			exit('退出')
		elif user_name.lower() == 'b':
			return 0
		elif user_name in users:
			if user_name in accounts:
				print('此账户下信用卡的信息%s' % str(accounts[user_name]))
				while 1:
					command = input('输入要设置的额度，b退回，q退出:').strip()
					if command.lower() == 'q':
						exit('退出')
					elif command.lower() == 'b':
						return 0
					else:
						if _set_limit(accounts, user_name, command):
							print('此账户下信用卡的信息%s' % str(accounts[user_name]))
						else:
							print('输入错误，设置失败')
							print('此账户下信用卡的信息%s' % str(accounts[user_name]))
			else:
				print('账户%s无信用卡' % user_name)
		else:
			print('账户%s不存在' % user_name)

def freeze_account():
	users = _load_users()
	accounts = _load_accounts()
	while 1:
		user_name = input('输入需要冻结的账户名，b退回，q退出:')
		if user_name.lower() == 'q':
			exit('退出')
		elif user_name.lower() == 'b':
			return 0
		elif user_name in users:
			print('此账户的信息%s' % str(users[user_name]))
			while 1:
				command = input('输入 Y 确认冻结，b退回，q退出:').strip()
				if command.lower() == 'q':
					exit('退出')
				elif command.lower() == 'b':
					return 0
				elif command.lower() == 'y':
					if _freeze_account(users, user_name):
						print('此账户的信息%s' % str(users[user_name]))
						break
					else:
						print('输入错误，修改失败')
						print('此账户的信息%s' % str(users[user_name]))
				else:
					print('取消')
					break
		else:
			print('账户%s不存在' % user_name)

def edit_account():
	# print('查看账户')
	users = _load_users()
	accounts = _load_accounts()
	# print(users)
	# print(accounts)
	while 1:
		user_name = input('输入需要编辑的账户名，b退回，q退出:')
		if user_name.lower() == 'q':
			exit('退出')
		elif user_name.lower() == 'b':
			return 0
		elif user_name in users:
			print('此账户的信息%s'%str(users[user_name]))
			if user_name in accounts:
				print('此账户下信用卡的信息%s' % str(accounts[user_name]))
				while 1:
					command = input('输入要修改的字段和要修改的值,中间用空格隔开，b退回，q退出:').strip()
					if command.lower() == 'q':
						exit('退出')
					elif command.lower() == 'b':
						return 0
					else:
						if _set_accounts_and_users(accounts,users,user_name,command):
							print('此账户的信息%s' % str(users[user_name]))
							print('此账户下信用卡的信息%s' % str(accounts[user_name]))
						else:
							print('输入错误，修改失败')
							print('此账户的信息%s' % str(users[user_name]))
							print('此账户下信用卡的信息%s' % str(accounts[user_name]))
			else:
				print('账户%s无信用卡' % user_name)
		else:
			print('账户%s不存在' % user_name)


# -------------下面的都是对用户隐藏的函数--------------

# 载入/写入信用卡账户信息
from core.atm.utils import _load_accounts,_save_accounts

# 载入/写入商城账户信息
from core.auth import _load_users,_save_users

def _add_account(user_name,passwd,pay_passwd,balance,users,accounts):
	new_user = {'status': 'free', 'passwd': passwd, 'pay_passwd': pay_passwd}
	new_account = {'balance': balance}
	users[user_name] = new_user
	accounts[user_name] = new_account
	u = _save_users(users)
	a = _save_accounts(accounts)
	if u and a:
		return True
	else:
		return False

def _set_limit(accounts, user_name, command):
	command = command.split(' ')
	if len(command) != 1:
		return False
	else:
		value = command[0]
		if _isaumber(value):
			accounts[user_name]['balance'] = float(value)
			_save_accounts(accounts)
			return True
		else:
			return False

def _freeze_account(users, user_name):
	users[user_name]['status'] = 'locked'
	return _save_users(users)

def _set_accounts_and_users(accounts,users,user_name,command):
	command = command.split(' ')
	if len(command) != 2:
		return False
	else:
		key,value = command
	if key in ['pay_passwd','passwd']:
		users[user_name][key] = value
		_save_users(users)
		return True
	elif key =='status' and value in ['locked','free']:
		users[user_name][key] = value
		_save_users(users)
		return True
	elif key =='balance' and _isaumber(value):
		accounts[user_name][key] = float(value)
		_save_accounts(accounts)
		return True
	else:
		return False


def _isaumber(string):
	try:
		float(string)
		return True
	except:
		return False




if __name__ == '__main__':
	import core.global_keeper as global_keeper
	global_keeper._init()  # 全局变量，标记用户状态
	global_keeper.set_value('user_name', 'root')
	global_keeper.set_value('login_status', True)
	#set_limit()
	freeze_account()
