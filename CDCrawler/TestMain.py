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

pxylist = []
LastTime = -1
CurrentTime = -1
LastDate = "Last Recorded Date"
p = prxMod.prxMod()
c = crlMod.crlMod()
l = logMod.logMod()

def init(): # Run Once at First_time
    LastTime = time.time()
    if os.path.exists('./dictStore.txt'):
        d = open(r"./dictStore.txt")
        c.dictStore = cPickle.load(d)
    if os.path.exists('./pxylist.txt'):
        f = open(r"./pxylist.txt")
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
                l.Warning("[ERROR]Daily Maintenance Failed %s at %s" % (str(ex),str(CurrentDate)))
        elif (CurrentTime - LastTime > 6 * 60):
            try :
                LastTime = CurrentTime
                status = c.CrawlPage(1)
            except Exception,ex:
                l.Notice("Main_Crawl Failed %s" % str(ex))
        # DailyMT() # For Test