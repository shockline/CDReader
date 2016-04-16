#-*- coding: utf-8 -*-

import sys
import dict
import time
import logging 

Log = "./log/Log.txt"
logger=logging.getLogger()
handler=logging.FileHandler(Log)
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__' : #Main for Stock_code_loop
