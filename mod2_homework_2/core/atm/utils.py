#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils.py
@Time    :   2018/11/27 9:10
@Desc    :
'''
import json

from core.auth import auth_passwd,login,isRoot
from core.auth import get_user_name
from conf.config import account_file

_FEE_RATE = 0.05

@auth_passwd
def transfer():
	print('转账')
	from_user_name = get_user_name()
	amount_avail = check_account()['balance']
	while 1:
		to_user_name = input('请输入要转帐的账户名:').strip()
		if to_user_name not in acc:
			print('目标账户不存在')
			continue
		else:
			while 1:
				amount = input('请输入要转帐的金额：').strip()
				if not amount.isdigit():
					print('金额格式错误请重输')
				elif float(amount)>amount_avail:
					print('余额不足，请重输')
				else:
					_atm_transfer(amount,from_user_name,to_user_name)


@auth_passwd
def withdraw():
	amount_avail = check_account()['balance']
	while 1:
		amount = input('请输入要转帐的金额：').strip()
		if not amount.isdigit():
			print('金额格式错误请重输')
		else:
			amount = float(amount)
			fee = amount*_FEE_RATE
			amount_in_total = amount+fee
			if amount_in_total > amount_avail:
				print('余额不足，请重输')
			else:
				_atm_cut(amount_in_total)
				print('取款%s，手续费%s'%(amount,fee))

@login
def repay():
	print('还款')
	import time
	print('.....')
	time.sleep(3)
	print('...经过一番操作，还款10000元')
	_atm_deposit(10000,get_user_name())

@login
def check_account():
	print('查账')
	acc=_load_accounts()
	user_name = get_user_name()
	if user_name in acc:
		res = acc[user_name]
		return res
	else:
		print('账户错误')
		return {'balance':0}


# ----------------------------------下面都是不对用户直接开放的底层接口
@auth_passwd
def atm_pay(amount): # 商城付款接口
	from_user_name = get_user_name() #todo
	to_user_name = 'mall'
	return _atm_transfer(amount,from_user_name,to_user_name)

def _atm_cut(amount,from_user_name = get_user_name()): # 扣款接口
	# 扣款的默认发起方是当前登陆用户，root账户有权指定发起方为任意用户
	acc = _load_accounts()
	amount_avail = acc[from_user_name]['balance']
	if float(amount) > amount_avail:
		print('余额不足扣款失败')
		return False
	else:
		acc[from_user_name]['balance'] -= amount
		_save_accounts(acc)
		return True

def _atm_deposit(amount,to_user_name): # 存款接口
	acc = _load_accounts()
	acc[to_user_name]['balance'] -= amount
	_save_accounts(acc)
	return True

def _atm_transfer(amount,from_user_name,to_user_name):  # 划账
	acc = _load_accounts()
	if from_user_name in acc and to_user_name in acc:
		c = _atm_cut(amount,from_user_name)
		d = _atm_deposit(amount,to_user_name)
		if c and d:
			return True
		else:
			print('转账失败')
			_save_accounts(acc)  # 记录回退
			return False
	else:
		print('账户名称错误，转账失败')
		return False

def _load_accounts():
	accounts = json.loads(open(account_file).read())
	return accounts

def _save_accounts(accounts):
	open(account_file,'w').write(json.dumps(accounts, indent=' '))




if __name__ == '__main__':
	print('----------------testing------------', __file__)
	acc = _load_accounts()
	print(acc)
	acc.pop('xx')
	_save_accounts(acc)

