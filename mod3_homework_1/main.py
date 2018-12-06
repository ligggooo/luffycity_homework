#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   main.py
@Time    :   2018/12/6 18:15
@Desc    :
'''
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(base_dir)

from core.views import main_view

if __name__ == '__main__':
	main_view()
