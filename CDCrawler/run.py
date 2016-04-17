#-*- coding: gbk -*-
import os
import sys
import json
import time
import random
import cPickle
import urllib2
import ConfigParser   
import crlMod # Crawl Module as crlMod.py
import prxMod # Proxy Module as prxMod.py
import logMod # Logger Module as LogMod.py

import common.Wordseg as Wordseg
import lr.LR_model as LR_model
import liblinear.Liblinear_model as Liblinear_model

pxylist = []
LastTime = -1
CurrentTime = -1
LastDate = "Last Recorded Date"
p = prxMod.prxMod()
c = crlMod.crlMod()
l = logMod.logMod()
lr = LR_model.LR_model()
liblinear = Liblinear_model.Liblinear_model()

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
        
    
def DailyMT(): # Daily Maintenance
    try :
        if c.dictStore: # Dump dictStore
            c.DumpDict()
        if p.proxylist: # Dump proxylist
            c.SetProxy(p.proxylist)
            c.Storepxy()
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
        if (CurrentTime - LastTime > exec_cyctime): # Crawl when 'exec_cyctime' later
            try :
                LastTime = CurrentTime
                status = c.CrawlPage(1)
                if status >= 0:
                    result = c.crawllist
                    for idx in xrange(0,len(result)) :
                        corpus = Wordseg.String_make_corpus()
                        label1 = lr.Predict(corpus)
                        label2 = liblinear.Predict(corpus)
                        result[idx] = result[idx] + ( "\t%s\t%s" % (label1, label2) )
                    result.reverse()
                    c.WriteInFile(result)
            except Exception,ex:
                l.Fatal("Main_Crawl Failed %s" % str(ex))
            c.Storepxy() # Open For Testing proxylists
        if (CurrentDate != LastDate): # Daily Maintenance
            LastDate = CurrentDate
            try :
                DailyMT()
            except Exception,ex:
                l.Warning("Daily Maintenance Failed %s at %s" % (str(ex),str(CurrentDate)))