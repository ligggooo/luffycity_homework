#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils.py
@Time    :   2018/11/3 0:14
@Desc    :
'''


def user_auth(users,status_file):
    status = open(status_file).read().strip()
    if status == '1':
        try_left = 10
        while try_left > 0:
            user_exist = False
            user_name = input('请输入用户名： ')
            user_passwd = input('请输入密码： ')
            for user_recored in users:
                user_name_recored = user_recored[0]
                user_passwd_recored = user_recored[1]
                if user_name == user_name_recored:
                    user_exist = True
                    if user_passwd == user_passwd_recored:
                        print('Welcome,', user_name, '!')
                        return user_name
                    break
            try_left -= 1
            if not user_exist:
                print('无此账户,还有%s次机会' % try_left)
            else:
                print('密码错误,还有%s次机会' % try_left)
        print('三次错误，锁定')
        open(status_file, 'w').write('0')
        return 0
    else:
        print('登录锁定，无法使用')
        return 0

def show_goods(goods):
    for i,item in enumerate(goods):
        print('%s. %s, price:%s'%(i,item['name'],item['price']))

def buy_goods(goods,select,money,shopping_log):
    item = goods[select]
    price = item['price']
    if money >= price:
        money -= price
        print("\033[1;31;40m您购买了%s, 余额为%s.\033[0m"%(item['name'],money))
        if item['name'] in shopping_log:
            shopping_log[item['name'] ]+=1
        else:
            shopping_log[item['name']] = 1
    else:
        print("\033[1;31;40m余额不足，购买失败！\033[0m")
    return money

def print_log(log,money):
    print('购物记录:')
    if len(log)==0:
        print('未购买任何物品，余额为%s'%money)
    else:
        for item in log:
            print("\033[1;31;40m您购买了%s * %s.\033[0m" % (item, log[item]))
        print('你的余额为%s' % money)

def load_record(record_file):
    record = {}
    for line in open(record_file).readlines():
        line = line.strip()
        if len(line) > 0:
            name,money = line.split('\t')
            record[name] = float(money)
    return record

def save_record(record_file,record,user,money):
    record[user] = money
    f= open(record_file,'w')
    for user in record:
        line = user+'\t'+str(record[user])+'\n'
        f.write(line)
    f.close()