#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: Goodwillie
# datetime: 2018/11/2 14:42
# project: Luffycity_homework

# 作业题目：编写登陆认证程序
# 作业需求:
# 	1 让用户输入用户名密码
# 	2 认证成功后显示欢迎信息
# 	3 输错三次后退出程序
# 	4 可以支持多个用户登录 (提示，通过列表存多个账户信息)
# 	5 用户3次认证失败后，退出程序，再次启动程序尝试登录时，还是锁定状态（提示:需把用户锁定的状态存到文件里）

status_file = 'status.dat'  # 文件中写入1，则登录可用，否则登录不可用
users = [['luffy', '12345'], ['zoro', '12341'], ['chopper', '321'], ['robin', 'absd']]  # 账户名和密码

status = open(status_file).read()
if status == '1':
    try_left = 3
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
                    exit()
                break
        try_left -= 1
        if not user_exist:
            print('无此账户,还有%s次机会' % try_left)
        else:
            print('密码错误,还有%s次机会' % try_left)
    print('三次错误，锁定')
    open(status_file, 'w').write('0')
else:
    print('登录锁定，无法使用')
