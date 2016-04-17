#-*- coding: gbk -*-
import os
import sys
import json
import time
import crlMod # Crawl Module as crlMod.py
import prxMod # Proxy Module as prxMod.py
import logMod # Logger Module as LogMod.py
import random
import cPickle
import urllib2
import ConfigParser

pxylist = []
LastTime = -1
CurrentTime = -1
LastDate = "Last Recorded Date"
p = prxMod.prxMod()
c = crlMod.crlMod()
l = logMod.logMod()

config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 
# CONFIG SET
path_dict = config.get("path", "path_dict")
path_pxylist = config.get("path", "path_pxylist")
exec_cyctime = config.getint("para", "EXEC_CYCLETIME")

def init(): # Run Once at First_time
    LastTime = time.time()
    if os.path.exists(path_dict):
        d = open(path_dict)
        c.dictStore = cPickle.load(d)
    if os.path.exists(path_pxylist):
        f = open(path_pxylist)
        pxylist = cPickle.load(f)
    if p.Getpxylist():
        pxylist.extend(p.proxylist)
        c.SetProxy(pxylist)
        c.Storepxy() # For test
    
def DailyMT(): # Daily Maintenance
    try :
        if c.dictStore:
            c.DumpDict()
        if p.Getpxylist():
            pxylist = p.proxylist
            c.SetProxy(pxylist)
    except Exception,ex:
        l.Warning("%s's DMT Failed <%s" % (str(LastDate),str(ex)))
        

if __name__ == '__main__' :
    try :
        init() # Noted "./new.txt" should be existed
    except Exception,ex:
        l.Fatal( "Initial Failed %s" % str(ex) )
    while True:
        CurrentTime = time.time()
        CurrentDate = str(time.strftime('%m%d',time.localtime(time.time())))
        if (CurrentDate != LastDate): 
            LastDate = CurrentDate
            try :
                DailyMT()
            except Exception,ex:
                l.Warning("Daily Maintenance Failed %s at %s" % (str(ex),str(CurrentDate)))
        elif (CurrentTime - LastTime > exec_cyctime):
            try :
                LastTime = CurrentTime
                status = c.CrawlPage(1)
                if status < 0:
                    l.Warning("This Crawl Failed, return %d" % status)
            except Exception,ex:
                l.Notice("Main_Crawl Failed %s" % str(ex))
        # DailyMT() # For Test