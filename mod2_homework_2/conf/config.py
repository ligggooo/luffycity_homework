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

user_file = _data_dir+'/user.dat' # 用户账户信息
mall_file = _data_dir+'/goods.dat' # 商城商品信息

record_file = _data_dir+'/record.dat' #消费记录文件
cart_file = _data_dir+'/cart.dat' #购物车列表文件

account_file = _data_dir+'/accounts.dat'
