#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   log_conf.py
@Time    :   2018/11/27 21:00
@Desc    :   配置日志模块
'''

import logging
import logging.handlers
from conf.config import atm_log,mall_log,sys_log

log_sys = logging.getLogger('log_sys')
log_sys.setLevel(logging.DEBUG)
log_atm = logging.getLogger('log_atm')
log_atm.setLevel(logging.DEBUG)
log_mall = logging.getLogger('log_mall')
log_mall.setLevel(logging.DEBUG)

#file handler
fh_sys = logging.handlers.TimedRotatingFileHandler(sys_log, when='D', interval=1,backupCount=7)
fh_sys.setLevel(logging.DEBUG)

fh_atm = logging.handlers.TimedRotatingFileHandler(atm_log, when='D', interval=1,backupCount=0)
fh_atm.setLevel(logging.DEBUG)

fh_mall = logging.handlers.TimedRotatingFileHandler(mall_log, when='D', interval=1,backupCount=30)
fh_mall.setLevel(logging.DEBUG)

#formatter
formatter = logging.Formatter('%(asctime)s - %(message)s')
formatter_sys = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

#bind formatter to handler
fh_sys.setFormatter(formatter_sys)
fh_atm.setFormatter(formatter)
fh_mall.setFormatter(formatter)


# #add handler   to logger instance
log_sys.addHandler(fh_sys)
log_atm.addHandler(fh_atm)
log_mall.addHandler(fh_mall)


if __name__ == '__main__':
	import time
	# while 1:
	# 	time.sleep(1)
	# 	log_sys.info('-------------')
