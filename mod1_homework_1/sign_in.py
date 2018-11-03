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

import json
user_file = 'status.dat'  # 文件以json格式保存一个字典，每一个key是一个用户名，value是一个包含密码和锁定状态的字典
# user_passwd = [['luffy', '12345'], ['zoro', '12341'], ['chopper', '321'], ['robin', 'absd']]  # 账户名和密码

user_status = json.loads(open(user_file).read()) # 读取用户数据文件
try_left = 3
while try_left > 0:
    user_exist = False
    user_name = input('请输入用户名： ')
    if user_name in user_status:              # 若账户在user-file中，验证其锁定状态
        status = user_status[user_name]['status']
        if status == 'locked':
            exit('此账户已被锁定，无法使用')          # 若账户处于锁定状态，则直接退出程序   # 1 退出--》
        else:                                        # 否则，进入密码验证环节
            user_passwd_recored = user_status[user_name]['passwd']
            user_passwd = input('请输入密码： ')
            if user_passwd == user_passwd_recored:       # 若密码验证通过，则进入欢迎界面
                print('Welcome,', user_name, '!')
                exit()                                                                     # 2 退出 --》
            else:                                        # 否则try_left减1
                try_left -= 1
                print('密码错误,还有%s次机会' % try_left)                                   # 3 进入下一循环
    else:                                     # 若账户不在user_file中，try_left减1
        try_left -= 1
        print('无此账户,还有%s次机会' % try_left)                                           # 4 进入下一循环

print('三次错误')                                                                     # 到了这里说明三次尝试都没有通过密码验证，需要锁定一个账户
if user_name in user_status:
    user_status[user_name]['status'] = 'locked'
    open(user_file, 'w').write(json.dumps(user_status, indent='  '))
    print(user_name,'已被锁定')                                                            # 5 锁定最后一次输入的账户
else:
    print('无法确定锁定对象')                                                              # 6 最后一次输入的账户无效


