#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author: Goodwillie
# datetime: 2018/11/2 16:09
# project: Luffycity_homework

# 作业题目：三级菜单
# 需求：
# 	可依次选择进入各子菜单
# 	可从任意一层往回退到上一层
# 	可从任意一层退出程序

menu = {
    '北京':{
        '海淀':{
            '五道口':{
                'soho':{},
                '网易':{},
                'google':{}
            },
            '中关村':{
                '爱奇艺':{},
                '汽车之家':{},
                'youku':{},
            },
            '上地':{
                '百度':{},
            },
        },
        '昌平':{
            '沙河':{
                '老男孩':{},
                '北航':{},
            },
            '天通苑':{},
            '回龙观':{},
        },
        '朝阳':{},
        '东城':{},
    },
    '上海':{
        '闵行':{
            "人民广场":{
                '炸鸡店':{}
            }
        },
        '闸北':{
            '火车站':{
                '携程':{}
            }
        },
        '浦东':{},
    },
    '山东':{},
}

route,level= [menu],0
while 1:
	command = input('Menu ' + ' '.join(route[-1].keys()) +' 输入选择其中一项, q 退出程序, b 返回上一级菜单: ')
	if command == 'b' and level > 0:
		level,route = level-1,route[:-1]
	elif command == 'q':
		exit()
	elif command in route[-1] and len(route[-1][command])>0:
		level, route = level + 1, route + [route[-1][command]]   # 10
	elif command == 'b' and level == 0:
		print('Error 已经到了根目录，无法后退')
	else:
		print('Error 无此选项，或此选项无下一级菜单')


