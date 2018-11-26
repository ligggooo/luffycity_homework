#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   menu.py
@Time    :   2018/11/26 9:55
@Desc    :
'''
def menu_loader(menu):
	route, level = [menu], 0
	while 1:
		for key in menu['sub']:
			print(menu['sub'][key]['tag'],key) # todo 加颜色
		command = input(menu['msg'])
		if command == 'b' and level > 0:
			level, route = level - 1, route[:-1]
		elif command == 'q':
			exit()
		elif command in route[-1] and len(route[-1][command]) > 0:
			level, route = level + 1, route + [route[-1][command]]  # 10
		elif command == 'b' and level == 0:
			print("\033[1;31;40m Error 已经到了根目录，无法后退\033[0m")
		else:
			print("\033[1;31;40m Error 无此选项，或此选项无下一级菜单\033[0m")

if __name__ == '__main__':
	pass
