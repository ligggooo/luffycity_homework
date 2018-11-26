#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   mall.py
@Time    :   2018/11/26 9:20
@Desc    :   商城
'''
from core.auth import login_status,auth_passwd,get_user_name
import core.global_keeper as global_keeper
import conf.config as conf
from core.mall.utils import load_cart,show_goods,save_cart,add_cart,show_cart

record_file = conf.record_file
cart_file = conf.cart_file

def mall():
	# 允许用户在未登录状态下浏览和添加购物车
	# 仅仅在付款的时候会被要求确认登陆状态，并确认支付密码
	if login_status():
		cart_list = load_cart(cart_file,get_user_name()) #若用户已经登陆，载入购物车历史# 若未登陆，生成空购物车
	else:
		cart_list = {}

	while 1:  # 购物 加车
		print('商品')
		num_goods = show_goods() # 展示商品

		select = input('输入商品序号加入购物车，c进入购物车，b返回，q退出：')
		if select == 'b':  # 若用户选择返回，则打印其消费记录，且保存期消费记录
			if login_status():
				save_cart(cart_file, cart_list, get_user_name())
			else:
				pass
			return 0
		if select == 'q':  # 若用户选择退出，则打印其消费记录，且保存期消费记录
			if login_status():
				save_cart(cart_file, cart_list, get_user_name())
			else:
				pass
			exit('退出程序')
		elif select.isdigit() and int(select) >= 0 and int(select) < num_goods:  # 若用户选择退出，则更新余额和购物篮信息，且输出关键信息
			cart_list = add_cart(int(select),cart_list)
		elif select=='c':
			cart_list = cart(cart_list) # 进入购物车
		else:
			print('无效输入，请重输：')


def cart(cart_list):
	print('进入购物车')
	while 1:  # 购物 加车
		show_cart(cart_list)
		select = input('输入p付款，输入b返回商城')
		if select =='p':
			pay_status = pay(cart_list)
			if pay_status:
				cart_list = {}
			break
		elif select=='b':
			break
		else:
			print('无效输入，请重输：')
	return cart_list

@auth_passwd
def pay(): # 未登录状态下加入购物车会在登陆之后与已有记录合并
	# 若购物车内物品价格小于账户余额，则完成扣款
	return True

if __name__ == '__main__':
	global_keeper._init()  # 全局变量，标记用户状态
	global_keeper.set_value('user_name', 'luffy')
	global_keeper.set_value('login_status', True)
	mall()
