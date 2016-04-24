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
import MysqlMod # MySQL Module as Mysql.py

# CONFIG SET
config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 
path_dict = config.get("path", "path_dict")
path_pxylist = config.get("path", "path_pxylist")
path_Positive = config.get("path", "path_Positive")
path_Negative = config.get("path", "path_Negative")
exec_cyctime = config.getint("para", "EXEC_CYCLETIME")

# Global_Vars
pxylist = []
LastTime = -1
posWlist = [line.strip() for line in file(path_Positive) ]
negWlist = [line.strip() for line in file(path_Negative) ]
LastDate = "Last Recorded Date"

# Initial_Objects
s = MysqlMod.MysqlMod()
p = prxMod.prxMod()
c = crlMod.crlMod()
l = logMod.logMod()
lr = LR_model.LR_model()
liblinear = Liblinear_model.Liblinear_model()


def init(): # Run Once at First time
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
        cdict = c.dictStore
        if cdict: # Dump dictStore
            c.StoreDict()
        plist = p.proxylist
        if plist: # Dump proxylist
            c.SetProxy(plist)
            c.Storepxy()
    except Exception,ex:
        l.Warning("%s's DMT Failed %s" % (str(LastDate), str(ex)))
        
    
def AddLabels():
    try :
        result = c.crawllist
        _len = len(result) - 1
        if result and _len > 0:
            l.Notice("AddLabels Started, %s objects this time" % len(result))
        else :
            l.Notice("Nothing New, skip SQL-Module")
            return False
        s.Create()
        for _idx in xrange(0, _len + 1) :
            idx = _len - _idx # Reverse idx
            _slices = result[idx].split('\t')
            corpuX = Wordseg.String_make_corpus(_slices[5].encode('utf-8'))
            _content = corpuX.split(' ')
            try :
                mark = 0
                label1 = lr.Predict(corpuX)
                mark = 1
                label2 = liblinear.Predict(corpuX)
                mark = 2
                label3 = Wordseg.dealWithContent(_content, posWlist, negWlist)
                mark = 3
                result[idx] =  "%s\t%s\t%s\t%s" % ( str(result[idx]), str(label1), str(label2), str(label3) )
                s.Insert("StockDataSina", result[idx])
            except Exception, ex:
                l.Warning("Corpus_Making Failed at %s [%s]%s" % (str(mark), str(ex), str(_slices[4])))
                result[idx] = "<Ignored> %s" % str(result[idx])
        s.Destroy()
        l.Notice("InsertSQL Finished")
        c.WriteInFile(result) # Use this can get a txt recording infolist
        del result[:]
        c.crawllist = []
        return True
    except Exception, ex:
        l.Fatal("Insert Failed %s" % str(ex))


def GoCrawl():
    c.ChangeFile()
    page = 1
    while True :
        l.Notice("Now Start CrawlPage %s" % str(page))
        status = c.CrawlPage(page)
        l.Notice("Status RET value is %s" % str(status))
        if status == 2: # Initial (Also Insert)
            AddLabels()
            c.crawllist = []
            l.Notice("Page[%s] Finished, Initial over" % str(page))
            break
        elif status == 1: # Has_new
            AddLabels()
            c.crawllist = []
            l.Notice("Page[%s] Finished, stop here" % str(page))
            break
        elif status == 0: # This Page Completed
            ALsta = AddLabels()
            c.crawllist = []
            if ALsta == False:
                break
            else :
                l.Notice("Page[%s] Finished, need continue" % str(page))
                page = page + 1
        else :
            l.Warning("Crawl Failed, Return %s" % str(status))
            break
    l.Notice("GoCrawl Over, Current Crawllist's size is %s" % str(len(c.crawllist)))

            
if __name__ == '__main__' :
    try :
        # LastTime = time.time()
        init() # Noted "./new.txt" should be existed
    except Exception,ex:
        l.Fatal( "Initial Failed %s" % str(ex) )
    while True:
        CurrentTime = time.time()
        CurrentDate = str(time.strftime('%y%m%d',time.localtime(time.time())))
        if (CurrentTime - LastTime > exec_cyctime): # Crawl when 'exec_cyctime' later
            l.Notice("News Detect Started >> "  )
            LastTime = CurrentTime
            try :
                GoCrawl()
            except Exception,ex:
                l.Notice("This_Crawl Failed %s" % str(ex))
                if str(ex).startswith("empty range for randrange()"):
                    LastDate = "Needs Maintenance"
            c.Storepxy() # Open For Testing proxylists
            c.StoreDict() # Open For Testing dictStores
        if ( CurrentDate != LastDate ): # Call function when Date Changes
            l.Notice("Daily Maintenance Started >> From %s to %s " % (str(LastDate),str(CurrentDate)) )
            LastDate = CurrentDate
            try :
                DailyMT() # Daily Maintenance
                l.Notice("Daily Maintenance Finished")
            except Exception,ex:
                l.Warning("Daily Maintenance Failed %s at %s" % (str(ex),str(CurrentDate)))