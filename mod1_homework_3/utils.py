#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   utils.py
@Time    :   2018/11/3 0:14
@Desc    :
'''
import json

def user_auth(user_file):
    user_status = json.loads(open(user_file).read())  # 读取用户数据文件
    try_left = 3
    while try_left > 0:
        user_name = input('请输入用户名： ')
        if user_name in user_status:  # 若账户在user-file中，验证其锁定状态
            status = user_status[user_name]['status']
            if status == 'locked':
                exit('此账户已被锁定，无法使用')  # 若账户处于锁定状态，则直接退出程序             # 1 退出--》
            else:  # 否则，进入密码验证环节
                user_passwd_recored = user_status[user_name]['passwd']
                user_passwd = input('请输入密码： ')
                if user_passwd == user_passwd_recored:  # 若密码验证通过，则进入欢迎界面
                    print('Welcome,', user_name, '!')
                    return user_name                                                           # 2 返回 --》
                else:  # 否则try_left减1
                    try_left -= 1
                    print('密码错误,还有%s次机会' % try_left)                                   # 3 进入下一循环
        else:  # 若账户不在user_file中，try_left减1
            try_left -= 1
            print('无此账户,还有%s次机会' % try_left)                                           # 4 进入下一循环

    print('三次错误')  # 到了这里说明三次尝试都没有通过密码验证，需要锁定一个账户
    if user_name in user_status:
        user_status[user_name]['status'] = 'locked'
        open(user_file, 'w').write(json.dumps(user_status, indent='  '))
        print(user_name, '已被锁定')                                                      # 5 锁定最后一次输入的账户
    else:
        print('无法确定锁定对象')                                                         # 6 最后一次输入的账户无效，无法锁定

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
            shopping_log[item['name']]+=1
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
            tokens = line.split('\t')
            name,money = tokens[:2]
            record[name] = {}
            record[name]['goods_bought'] = json.loads(tokens[2])
            record[name]['money'] = float(money)
    return record

def save_record(record_file,record,username,money,shopping_log):
    record[username] = {
        'money' : money,
        'goods_bought': shopping_log
    }
    f= open(record_file,'w')
    for username in record:
        line = username+'\t'+str(record[username]['money'])+'\t'+json.dumps(record[username]['goods_bought'])+'\n'
        f.write(line)
    f.close()