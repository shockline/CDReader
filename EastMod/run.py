# -*- coding: gbk -*-

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
import cnntext.cnn as ctext_model
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
dict_capacity = config.getint("para", "DICT_CAPACITY")

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
ct = ctext_model.cnn()
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
        if p.Getpxylist():
            pxylist.extend(p.proxylist)
            c.SetProxy(pxylist)
            c.Storepxy()
        cdict = c.dictStore
        if cdict: 
            c.StoreDict() # Dump dictStore
            tlist = cdict.keys() # Dequeue
            if tlist:
                tlist.sort()
                for each in tlist:
                    if len(tlist) < dict_capacity :
                        break
                    else: 
                        cdict.pop(each)
                        tlist.remove(each)
                c.dictStore = cdict
    except Exception,ex:
        l.Warning("%s's DMT Failed %s" % (str(LastDate), str(ex)))
        
        
def AddLabels():
    try :
        result = c.crawllist
        _len = len(result) - 1
        if result and _len >= 0:
            l.Notice("AddLabels Started, %s objects this time" % len(result))
        else :
            l.Notice("Nothing New, skip SQL-Module")
            return False
        s.Create()
        for _idx in xrange(0, _len + 1) :
            idx = _len - _idx # Reverse idx
            _slices = result[idx].split('\t')
            corpuX = Wordseg.String_make_corpus(_slices[11].encode('utf-8'))
            _content = corpuX.split(' ')
            thistime = time.localtime(time.time())
            try :
                mark,label1 = 0, lr.Predict(corpuX)
                mark,label2 = 1, liblinear.Predict(corpuX)
                mark,label3 = 2, Wordseg.dealWithContent(_content, posWlist, negWlist)
                mark,label4 = 3, ct.Predict(corpuX)
                mark,label5 = 4, str(time.strftime('%Y%m%d', thistime)) + "\t" + str(time.strftime('%H:%M', thistime)) # Means ALL Labels Get
                result[idx] =  "%s\t%s\t%s\t%s\t%s\t%s" % ( str(result[idx]), str(label1), str(label2), str(label3), str(label4), str(label5) )
                
                s.Insert("StockDataAL", result[idx])
            except Exception, ex:
                l.Warning("Corpus_Making Failed at %s [%s]%s" % (str(mark), str(ex), str(_slices[9])))
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
    c.crawllist = []
    while True :
        l.Notice("Now Start CrawlPage %s" % str(page))
        try :
            status = c.CrawlPage(page)
        except Exception,ex:
            c.Storetmp = {}
            c.crawllist = []
            if c.proxylist:
                l.Warning("Page[%s] Crawlpage Failed for %s, Retry" % (str(page), str(ex)))
                continue
            else :
                l.Warning("Page[%s] Crawlpage Failed for %s, ProxyPool is Empty, stop" % (str(page), str(ex)))
                break
        l.Notice("Crawl Finished. Status RET value is %s" % str(status))
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
                l.Notice("Page[%s] Finished, Empty Query" % str(page))
                break
            else :
                l.Notice("Page[%s] Finished, need continue" % str(page))
                page = page + 1
        elif status == -2: #pxy Failed
            c.crawllist = []
            l.Notice("Current Proxy Failed, Retry.")
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
                c.crawllist = []
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
