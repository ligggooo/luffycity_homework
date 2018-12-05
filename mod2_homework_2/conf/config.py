#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   config.py
@Time    :   2018/11/26 11:11
@Desc    :
'''
import os

_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_data_dir = _base_dir+'/data'
_log_dir = _base_dir+'/log'

root_file = _data_dir+'/root.dat'

user_file = _data_dir+'/user.dat'  # 用户账户信息
mall_file = _data_dir+'/goods.dat'  # 商城商品信息

cart_file = _data_dir+'/cart.dat'  # 购物车列表文件

account_file = _data_dir+'/accounts.dat'

sys_log = _log_dir+'/system_log/sys_log.log'  # 系统日志目录
atm_log = _log_dir + '/atm_log/atm_log.log'  # atm记录目录
mall_log = _log_dir + '/mall_log/mall_log.log'  # 消费记录目录

