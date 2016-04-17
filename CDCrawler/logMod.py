#-*- coding: gbk -*-

import os
import sys
import time
import urllib2
import logging 
import ConfigParser

config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 
# CONFIG SET
path_log = config.get("path", "path_log")

class logMod:

    Log = path_log
    LastTime = 0
    LastDate = "Last Recorded Date"
    CurrentDate = "Current Date"

    logger=logging.getLogger()
    handler=logging.FileHandler(Log)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)

    reload(sys)
    sys.setdefaultencoding('utf-8')

    def __init__(self):
        self.LastTime = time.localtime(time.time())
    
    def getTime(self):
        return str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time())))
    
    def Warning(self, tstring):
        self.logger.info("[Warning] %s " % str(tstring) + self.getTime())
        
    def Fatal(self, tstring):
        self.logger.info("[Fatal] %s " % str(tstring) + self.getTime())
        
    def Notice(self, tstring):
        self.logger.info("[Notice] %s " % str(tstring) + self.getTime())
        
    def CheckLog(self):
        if os.path.exists(Log):
            return True
        else :
            return False