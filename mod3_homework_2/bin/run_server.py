#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   run_server.py
@Time    :   2018/12/10 9:22
@Desc    :
'''

import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from conf.config_server import ADDR,PORT
from core.server.FTPServer import MYTCPServer
tcpserver1=MYTCPServer((ADDR,PORT))

tcpserver1.run()