#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   menu.py
@Time    :   2018/11/26 9:55
@Desc    :   模板化的菜单设计，似乎，很明显地，极其有可能提高代码可扩展性
'''

def menu_loader(menu,is_root_tree=True):
	route, level = [menu], 0
	jump_back = False
	for func in menu['functions']: # 菜单等级变化之后要把这一级的functions任务都完成
		func()
	while 1:
		if jump_back:
			command = 'b'
			jump_back = False
		else:
			for key in route[-1]['sub']:
				print(menu['sub'][key]['tag'],key) #  todo 加颜色
			command = input(route[-1]['msg'])
		if command == 'b' and level > 0:
			level, route = level - 1, route[:-1]
			for func in route[-1]['functions']:
				func()
		elif command == 'q':
			exit()
		elif command in route[-1]['sub'] and len(route[-1]['sub'][command]) > 0:
			level, route = level + 1, route + [route[-1]['sub'][command]]  # 10
			for func in route[-1]['functions']:
				if func() == 'go_back':
					jump_back = True
					break
		elif command == 'b' and level == 0:
			if is_root_tree:
				print("\033[1;31;40m Error 已经到了根目录，无法后退\033[0m")
			else:
				return 0 # 如果菜单树是一株子树，则return 0，返回到母树
		else:
			print("\033[1;31;40m Error 无此选项，或此选项无下一级菜单\033[0m")

def go_back():
	return 'go_back'


if __name__ == '__main__':
	pass
