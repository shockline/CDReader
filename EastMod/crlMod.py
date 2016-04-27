# -*- coding: gbk -*-

from goose import Goose
from bs4 import BeautifulSoup
from multiprocessing import Pool
from goose.text import StopWordsChinese

import os
import re
import sys
import time
import json
import random
import logMod
import cPickle
import urllib2
import ConfigParser

sourceName = "EAST"
l = logMod.logMod()

config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 
# CONFIG SET
path_dict = config.get("path", "path_dict")
path_data = config.get("path", "path_data")
path_pxylist = config.get("path", "path_pxylist")
wait_runtime = config.getint("para","RUNTIME_WAITTIME")
EN_switch = config.getint("switch","EN_filter")

_URLHEAD = config.get("netpage","URLHEAD")
_MAINURL = config.get("netpage","MAINURL")

class crlMod:

    def __init__(self):
        self.LastDate = "Last Recorded Date"
        self.LastTime = 0
        self.infile = ""
        self.CurrentDate = "Current Date"
        self.CurrentTime = -1
        self.Storetmp = {} # tmp for this time
        self.dictStore = {} # dict from last time, updated by 'tmp'
        self.proxylist = []
        self.crawllist = []
        self.currentpxy = ""
        self.UrlHead = _URLHEAD
        self.MainUrl = _MAINURL
    
    
    def SetProxy(self, exlist):
        self.proxylist.extend(exlist)
        tmplist = []
        for each in self.proxylist :
            if each not in tmplist :
                tmplist.append(each)
        self.proxylist = tmplist # Unique
    
    
    # Crawl Module Functions
    def GetDesc(self, pagesite) :
        pxy = ""
        value = "NULL"
        try :
            pxy = self.Getpxy()
            html_doc = self.Getdoc(pagesite, pxy) # urllib2.urlopen(pagesite) 
        except Exception,ex:
            l.Notice("Remove %s for Desc_Crawl failed %s %s" % (str(pxy), str(pagesite).replace(self.UrlHead,""), str(ex)))
            return value
        soup = BeautifulSoup(html_doc.read().decode('gbk'), "html.parser") # html.parser 
        for link in soup.find_all('div') :
            if link.get('class') and link.get('class')[0] == 'newsContent' :
                value = link.get_text().replace('\t','').replace('\r','').replace('\b','').replace('\"','\'').encode('utf-8')
                return value
        if value == "NULL" or len(value) < 20:
            self.proxylist.remove(pxy)
        return value
    
    
    def GetDesc_goose(self, curl) :
        try :
            g = Goose( {'stopwords_class': StopWordsChinese} )
            article = g.extract(url = curl)
            return article.cleaned_text.encode('utf-8').replace('\t','').replace('\r','').replace('\b','').replace('"',"'")
        except Exception, ex:
            l.Warning("Goose_Crawl Failed %s" % str(ex))
            return "NULL"
    
    
    def MergeUrl(self, link) :    
        pagesite = ""
        try:
            mid = "".join((link['datetime'].split("T")[0]).split("-"))
            last = link['infoCode']
            pagesite = "%s%s/%s.html" % (str(self.UrlHead), str(mid), str(last))
        except:
            l.Warning("Get pagesite failed, link is: " + str(link))
            return "NULL"
        return pagesite
    
        
    def GetContent(self, soup) :
        if soup:
            __topCheck = 0
            l.Notice("Current Soup-list's size: [%s/%s]" % (str(len(soup)), str(len(soup['data']))))
            for link in soup['data'] : # 'link': json-info-group
                pagesite, value = "", ""
                pagesite = self.MergeUrl(link)
                if pagesite == "NULL":
                    return -3 # Retry For Url
                DateTime = str("".join((link['datetime'].split("T")[0]).split("-")))
                key = "%s\x01%s\x01%s" % ( DateTime, str(link['secuFullCode']), str(link['title']) )
                if __topCheck == 0 and self.dictStore.has_key(key) and self.dictStore[key] == pagesite :
                    l.Notice("The top %s has been crawlled, SKIP." % str(key))
                    return 1
                else :
                    __topCheck = 1
                # Regular Proxy Crawl
                for retry in xrange(0,3) :
                    value = self.GetDesc(pagesite)
                    if value == "NULL" or len(value) < 20 :
                        if self.proxylist :
                            continue
                        else :
                            break
                    else :
                        l.Notice("# Regular Crawl Finished. %s" % str(pagesite).replace(self.UrlHead,""))
                        break
                # Retry For Goose (Back-up / alternative)
                if value == "NULL" : 
                    l.Notice("Regular Crawl => Goose Retry %s" % str(pagesite).replace(self.UrlHead,"") )
                    for retry in xrange(0,3) :
                        value = self.GetDesc_goose(pagesite)
                        if value != "NULL" and len(value) >= 20 :
                            l.Notice("# Goose Crawl Finished.%s" % str(pagesite).replace(self.UrlHead,""))
                            break
                # Detect whether exists
                if (not self.dictStore.has_key(key)) or self.dictStore[key] != pagesite :
                    if len(value) > 4:
                        if DateTime == str(time.strftime('%Y%m%d', time.localtime(time.time()-3600))) or \
                           DateTime == str(time.strftime('%Y%m%d', time.localtime(time.time()+3600))):
                            self.crawllist.append( "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                           (sourceName, link['secuFullCode'][:6], link['secuName'], link['companyCode'], link['rate'], \
                           link['change'], link['sratingName'], link['insName'], link['author'], pagesite, link['title'], value ) ) 
                            self.Storetmp[key] = pagesite
                    else :
                        l.Notice("Insert into Blacklist: %s" % str(pagesite))
                        self.Storetmp[key] = pagesite
                else :
                    l.Notice("There's an Existed article. %s" % str(key))
                    return 1 # This one has been crawled
            return 0 # Page_end
        else :
            return -2 # soup is Empty

            
    def Getdoc(self, url, pxy) :
        __tmp = pxy.split(':');
        ip,port = __tmp[0],__tmp[1];
        proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
        opener = urllib2.build_opener(proxy_handler);
        urllib2.install_opener(opener);
        request = urllib2.Request(url);  
        request.add_header('User-Agent', 'fake-client');  
        html_doc = urllib2.urlopen(request,timeout = 2 * wait_runtime)
        return html_doc
            
            
    def GetMainUrl(self, url, pxy) : 
        try :
            html_doc = self.Getdoc(url, pxy)
            # Get info from doc
            the_page = html_doc.read()
            page = "".join(the_page.split("=")[1:])
            contents = json.loads(page)
            return self.GetContent(contents)
        except Exception, ex:
            l.Warning("%s GetMainUrl failed: %s" % (str(pxy), str(ex)))
            self.proxylist.remove(pxy)
            return -2

    
    def ChangeFile(self): # Achieve current infile [Ignore]
        self.LastDate = str(time.strftime('%m%d',time.localtime(time.time())))
        self.infile = open(str(path_data).replace('.txt','%s.txt' % self.LastDate),"a")
    
    def WriteInFile(self, pList): # Write list in reverse_mode
        NowX = str(time.strftime('%m%d',time.localtime(time.time())))
        WriteX = open(str(path_data).replace('.txt','%s.txt' % NowX),"a")
        for _each in pList :
            WriteX.write(_each + '\n')
        
    def StoreDict(self): # Dump dictStore
        __store = self.dictStore
        if __store:
            cPickle.dump(__store, open(str(path_dict), "w"))
    
    def Storepxy(self): # Make a back-up
        __store = self.proxylist
        if __store :
            cPickle.dump(__store, open(str(path_pxylist), "w"))
    
    def Getpxy(self): # Randomly-get a new proxy
        __pos = random.randrange(0, len(self.proxylist), 1)
        return self.proxylist[__pos]
    
    def CrawlPage(self, page) : # Crawl CurrentPage
        self.ChangeFile()
        __Refreshdict = {}
        __Refreshlist = []
        url = self.MainUrl.replace("pagesite", str(page))
        if len(self.proxylist) < 1 :
            ret = -1
        else :
            ret = self.GetMainUrl(url, self.Getpxy())
        if ret == 0: # Crawl till Page_end
            if self.dictStore : # Not Initial Mode
                self.dictStore.update(self.Storetmp) 
                self.Storetmp = __Refreshdict
                return 0
            elif page == 1 :
                self.dictStore.update(self.Storetmp)
                self.Storetmp = __Refreshdict
                l.Notice("InsertSQL & Initial Finished")
                return 2
        elif ret == 1: 
            if self.Storetmp: # If Store Changed
                # l.Notice("Something New Existed")
                # If want to test ProxyPool you can Remove this branch
                self.dictStore.update(self.Storetmp)
                self.Storetmp = __Refreshdict
                return 1
        elif ret == -1: # Gain Failed, This time's Crawl_list will be cleared.
            l.Fatal("Proxylist has been empty.") 
        elif ret <= -2: # NoContentError (Soup.size is 0 or Desc is empty)
            l.Notice("GetSoup Failed.")
        self.Storetmp = __Refreshdict
        self.crawllist = __Refreshlist
        l.Notice("Temp_dictStore Cleared, size is %s" % str(len(self.Storetmp)))
        return ret
