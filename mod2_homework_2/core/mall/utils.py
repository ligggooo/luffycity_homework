#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils.py
@Time    :   2018/11/3 0:14
@Desc    :   mall的支持模块
'''
import json
from conf.config import mall_file
import shutil

goods = json.loads(open(mall_file,encoding='utf-8').read()) # 载入商品信息为全局变量

def show_goods():
	for i,item in enumerate(goods):
		print('%s. %s, price:%s'%(i,item['name'],item['price']))
	return len(goods)

def add_cart(select,cart_list):
	item = goods[select]
	if item['name'] in cart_list:
		cart_list[item['name']] += 1
	else:
		cart_list[item['name']] = 1
	print("\033[1;31;40m %s 已经加入购物车.\033[0m" % item['name'])
	return cart_list

def check_cart(cart_list): # 展示购物车内物品
	sum = 0
	for key in cart_list: # 效率低
		amount = cart_list[key]
		for item in goods:
			if item['name'] == key:
				sum += item['price'] * amount
	print(cart_list,sum)
	return sum


def print_log(log,money):
	print('购物记录:')
	if len(log)==0:
		print('未购买任何物品，余额为%s'%money)
	else:
		for item in log:
			print("\033[1;31;40m您购买了%s * %s.\033[0m" % (item, log[item]))
		print('你的余额为%s' % money)

def load_cart(cart_file,user_name): # todo
	cart = {}
	for line in open(cart_file).readlines():
		line = line.strip()
		if len(line) > 0:
			tokens = line.split('\t')
			name = tokens[0]
			if name == user_name:
				cart = json.loads(tokens[1])
			else:
				pass
		else:
			pass
	return cart

def save_cart(cart_file, cart_list,user_name): #todo
	f_in  = open(cart_file,'r')
	f_out = open(cart_file+'.bak','w')
	for line in f_in.readlines():
		line_s = line.strip()
		if len(line_s) > 0:
			tokens = line_s.split('\t')
			name = tokens[0]
			if name == user_name:
				line = name+'\t'+json.dumps(cart_list)+'\n'
		f_out.write(line)
	f_in.close()
	f_out.close()
	shutil.move(cart_file+'.bak', cart_file)

if __name__ == '__main__':
	show_goods()
	import conf.config as cc

	# z = load_cart(cc.cart_file+'.bak','luffy')
	# print(z)
	c_l = {'电脑': 3, '鼠标': 2, '游艇': 3,'月饼':30}
	#save_cart(cc.cart_file,c_l,'luffy')
	print(check_cart(cart_list=c_l))