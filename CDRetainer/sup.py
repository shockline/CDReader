#-*- coding: gbk -*-

import os
import sys
import time
import logMod
import commands
import ConfigParser

l = logMod.logMod()
config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 
exec_cyctime = config.getint("para", "EXEC_CYCLETIME")

if __name__ == '__main__':
    LastTime = -1   
    while True:
        CurrentTime = time.time()
        if (CurrentTime - LastTime > exec_cyctime):
            LastTime = CurrentTime
            # os.system('nohup python CDRetainer.py &')
            (status, output) = commands.getstatusoutput('nohup python CDRetainer.py \&')
            l.Notice("Sup_Process Start. Loading CDRetainer...")
            l.Notice("Status: %s\nOutput: %s" % (str(status), str(output)))