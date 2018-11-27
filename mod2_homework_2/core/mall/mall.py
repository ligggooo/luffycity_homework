#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   mall.py
@Time    :   2018/11/26 9:20
@Desc    :   商城
'''
from core.auth import login,login_status,auth_passwd,get_user_name
import core.global_keeper as global_keeper
import conf.config as conf
from core.mall.utils import load_cart,show_goods,save_cart,add_cart,check_cart
from core.atm.utils import atm_pay
from conf.log_conf import log_mall

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

		select = input('输入商品序号加入购物车，x清空购物车，c进入购物车，b返回，q退出：')
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
		if select == 'x':
			cart_list = {}
			if login_status():
				save_cart(cart_file, cart_list, get_user_name())
			else:
				pass
		elif select.isdigit() and int(select) >= 0 and int(select) < num_goods:  # 若用户选择退出，则更新余额和购物篮信息，且输出关键信息
			cart_list = add_cart(int(select),cart_list)
		elif select=='c':
			cart_list = cart(cart_list) # 进入购物车
		else:
			print('无效输入，请重输：')


def cart(cart_list):
	print('进入购物车')
	while 1:  # 购物 加车
		check_cart(cart_list)
		select = input('输入p付款，输入b返回商城')
		if select =='p':
			s = login_status() # 记录此刻的登陆状态，pay会强制未登录用户登陆，这种情况下需要merge登陆前后的购物车列表
			pay_status = pay(cart_list,s)
			if pay_status:
				log_mall.info(str(cart_list))  # 成功支付会清空购物车，此时将购物车内容记录到商城log里面
				cart_list = {}
				save_cart(cart_file,cart_list,get_user_name())
				break
			else:
				break
		elif select=='b':
			break
		else:
			print('无效输入，请重输：')
	return cart_list

@login
def pay(cart_list,was_logged_in):
	if not was_logged_in:
		merge_cart(cart_list)  # 未登录状态下加入购物车的商品会在登陆之后与历史购物车合并
	sum_money = check_cart(cart_list)
	if sum_money <= 0:
		return False
	pay_res = atm_pay(sum_money)
	if not pay_res:
		print('扣款失败')
	return pay_res

def merge_cart(cart_list): #
	# 用户有时会在非登陆状态下将一些商品加车，而支付函数会强制用户登陆
	# 这个merge函数用于合并非登陆状态下加车商品列表与历史购物车列表
	cart_list_2 = load_cart(cart_file,get_user_name()) # 能到这里，一定通过登陆验证了
	# 合并cart_list_2和cart_list
	for key in cart_list:
		if key in cart_list_2:
			cart_list[key] += cart_list_2[key]
			cart_list_2.pop(key)
	for key in cart_list_2:
		cart_list[key] = cart_list_2[key]
	save_cart(cart_file, cart_list, get_user_name())


if __name__ == '__main__':
	global_keeper._init()  # 全局变量，标记用户状态
	global_keeper.set_value('user_name', 'luffy')
	global_keeper.set_value('login_status', True)
	mall()
