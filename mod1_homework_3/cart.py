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

user_file = 'status.dat'  # 用户状态文件，保存密码和锁定状态
record_file = './record.dat' # 消费记录文件
# users = [['luffy', '12345'], ['zoro', '12341'], ['chopper', '321'], ['robin', 'absd']]  # 账户名和密码


record = load_record(record_file)  # 载入消费记录文件
user = user_auth(user_file)  # 用户验证，是作业一的函数封装
if user: # 通过验证后会返回用户名，否则会退出
    if user not in record:  #若未查询到该用户的消费记录，则由用户输入工资，且初始化该用户的消费记录为空字典
        while 1:
            user_input = input('无消费记录，请输入你的工资：')
            if user_input.isdigit():
                money = float(user_input)
                break
            else:
                print('无效输入，请重新输入你的工资：')
        shopping_log = {}  # 初始化消费记录
    else:    # 若查询到该用户的消费记录，则载入其余额和消费记录信息，且将其之前的消费记录和余额打印出来
        money = record[user]['money']
        shopping_log = record[user]['goods_bought']
        print('查到消费记录')
        print_log(shopping_log, money)
    while 1:   # 购物
        print('商品')
        show_goods(goods)
        select = input('您当前的余额为%s,输入商品序号购买，或者q退出：'%money)
        if select == 'q':              # 若用户选择退出，则打印其消费记录，且保存期消费记录
            print_log(shopping_log,money)
            save_record(record_file,record,user,money,shopping_log)
            exit('退出程序')
        elif select.isdigit() and int(select) >=0 and int(select) <len(goods):  # 若用户选择退出，则更新余额和购物篮信息，且输出关键信息
            money = buy_goods(goods,int(select),money,shopping_log)
        else:
            print('无效输入，请重输：')




