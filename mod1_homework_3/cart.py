#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   cart.py
@Time    :   2018/11/2 23:57
@Desc    :   Luffycity homework 3
'''
# 作业题目：购物车程序
# 功能要求：
# 1、启动程序后，输入用户名密码后，让用户输入工资，然后打印商品列表
# 2、允许用户根据商品编号购买商品
# 3、用户选择商品后，检测余额是否够，够就直接扣款，不够就提醒
# 4、可随时退出，退出时，打印已购买商品和余额
# 5、在用户使用过程中， 关键输出，如余额，商品已加入购物车等消息，需高亮显示
# 6、用户下一次登录后，输入用户名密码，直接回到上次的状态，即上次消费的余额什么的还是那些，再次登录可继续购买
# 7、允许查询之前的消费记录
from utils import load_record,save_record,user_auth,show_goods,buy_goods,print_log

goods = [
{"name": "电脑", "price": 1999},
{"name": "鼠标", "price": 10},
{"name": "游艇", "price": 20},
{"name": "美女", "price": 998},
]

status_file = 'status.dat'  # 文件中写入1，则登录可用，否则登录不可用
record_file = './record.dat' # 用于记录余额,若某个用户有消费记录，则程序不会提示输入工资
users = [['luffy', '12345'], ['zoro', '12341'], ['chopper', '321'], ['robin', 'absd']]  # 账户名和密码


record = load_record(record_file)
user = user_auth(users,status_file)
if user:
    if user not in record:
        while 1:
            user_input = input('无消费记录，请输入你的工资：')
            if user_input.isdigit():
                money = float(user_input)
                break
            else:
                print('无效输入，请重新输入你的工资：')
    else:
        money = record[user]
        print('查到消费记录，你的余额为%s'%money)
    shopping_log = {}
    while 1:
        print('商品')
        show_goods(goods)
        select = input('您当前的余额为%s,输入商品序号购买，或者q退出：'%money)
        if select == 'q':
            print_log(shopping_log,money)
            save_record(record_file,record,user,money)
            exit('退出')
        elif select.isdigit() and int(select) >=0 and int(select) <len(goods):
            money = buy_goods(goods,int(select),money,shopping_log)
        else:
            print('无效输入')




