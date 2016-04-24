#*- coding: gbk -*-

from goose import Goose
from bs4 import BeautifulSoup
from multiprocessing import Pool
from goose.text import StopWordsChinese

import os
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
_URLHEAD = config.get("netpage","URLHEAD")
_MAINURL = config.get("netpage","MAINURL")

class crlMod:

    LastDate = "Last Recorded Date"
    LastTime = 0
    infile = ""
    CurrentDate = "Current Date"
    CurrentTime = -1
    Storetmp = {} # tmp for this time
    dictStore = {} # dict from last time, updated by 'tmp'
    proxylist = []
    crawllist = []
    currentpxy = ""
    
    UrlHead = _URLHEAD
    MainUrl = _MAINURL
    
    # Varieties Getter and Setter
    def Get_crawllist(self):
        return self.crawllist
    
    def Set_crawllist(self, exlist):
        try :
            self.crawllist = exlist
            return True
        except Exception, ex:
            l.Warning("Setter Error on Crawllist %s" % str(ex))
            return False
    
    def Get_dictStore(self):
        return self.dictStore
    
    def Set_dictStore(self, exStore):
        try :
            self.dictStore = exStore
            return True
        except Exception, ex:
            l.Warning("Setter Error on dictStore %s" % str(ex))
            return False
    
    def Get_Storetmp(self):
        return self.Storetmp
    
    def Set_Storetmp(self, exStore):
        try :
            self.Storetmp = exStore
            return True
        except Exception, ex:
            l.Warning("Setter Error on Storetmp %s" % str(ex))
            return False
    
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
        soup = BeautifulSoup(html_doc, "lxml")
        for link in soup.find_all('div') :
            if link.get('class') and link.get('class')[0] == 'newsContent' :
                value = link.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','').replace('\"','\'')
                return value
        if value == "NULL" or len(value) < 20:
            self.proxylist.remove(pxy)
        return value
    
    
    def GetDesc_goose(self, curl) :
        article = "NULL"
        try :
            g = Goose( {'stopwords_class': StopWordsChinese} )
            article = g.extract(url = curl)
        except Exception, ex:
            l.Warning("Goose_Crawl Failed %s" % str(ex))
        return str(article.cleaned_text).replace('\t','').replace('\r','').replace('\n','').replace('\b','').replace('"',"'")
    
    
    def MergeUrl(self, link) :    
        pagesite = ""
        try:
            mid = "".join((link['datetime'].split("T")[0]).split("-"))
            last = link['infoCode']
            pagesite = "%s%s/%s.html" % (str(self.UrlHead), str(mid), str(last))
        except:
            l.Warning("Get pagesite failed: " + str(link))
            return "NULL"
        return pagesite
    
    
    def GetContent(self, soup) :
        if not soup :
            return -2 # soup is Empty
        
        for link in soup['data'] : # 'link': json-info-group
            pagesite, value = "", ""
            pagesite = self.MergeUrl(link)
            if pagesite == "NULL":
                return -3 # Retry For Url
            key = "%s\x01%s\x01%s" % ( str(link['secuFullCode']), str(link['title']), str(link['author']) )
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
                    thistime = time.localtime(time.time())
                    self.crawllist.append( "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
                    (sourceName, link['secuFullCode'][:6], link['secuName'], link['companyCode'], link['rate'], \
                     link['change'], link['sratingName'], link['insName'], link['author'], pagesite, link['title'], \
                     value, str(time.strftime('%Y%m%d', thistime)), str(time.strftime('%H:%M', thistime)) ) ) 
                    self.Storetmp[key] = pagesite
            else :
                return 1 # This one has been crawled
        return 0 # Page_end
    
    
    def Getdoc(self, url, pxy) :
        __tmp = pxy.split(':');
        ip,port = __tmp[0],__tmp[1];
        proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
        opener = urllib2.build_opener(proxy_handler);
        urllib2.install_opener(opener);
        request = urllib2.Request(url);  
        request.add_header('User-Agent', 'fake-client');  
        html_doc = urllib2.urlopen(request,timeout = wait_runtime)
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
            if self.proxylist:
                return self.GetMainUrl(url, self.Getpxy())
            else :
                return -1 # Pxylist is Empty

    
    def ChangeFile(self): # Achieve current infile [Ignore]
        self.LastDate = str(time.strftime('%m%d',time.localtime(time.time())))
        self.infile = open(str(path_data).replace('.txt','%s.txt' % self.LastDate),"a")
    
    def WriteInFile(self, pList): # Write list in reverse_mode
        NowX = str(time.strftime('%m%d',time.localtime(time.time())))
        WriteX = open(str(path_data).replace('.txt','%s.txt' % NowX),"a")
        for _each in pList :
            WriteX.write(_each + '\n')
        
    def StoreDict(self): # Dump dictStore
        __store = self.Get_dictStore()
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
        url = self.MainUrl.replace("pagesites", str(page))
        ret = self.GetMainUrl(url, self.Getpxy())
        if ret == 0: # Crawl till Page_end
            if self.Storetmp :
                if page == 1 :
                    self.Set_dictStore(self.Get_Storetmp())
                    l.Notice("InsertSQL & Initial Finished")
                    return 2
        elif ret == 1: # If Store Changed
            if self.Storetmp: # If No news, return 'Empty'
                # l.Notice("Something New Existed")
                # If want to test ProxyPool you can Remove this branch
                self.Set_dictStore(self.Get_Storetmp())
        elif ret == -1: # Gain Failed, This time's Crawl_list will be cleared.
            l.Fatal("Proxylist has been empty.") 
        elif ret <= -2: # NoContentError (Soup.size is 0 or Desc is empty)
            l.Notice("GetSoup Failed.")
        __Refreshdict = {}
        self.Set_Storetmp(__Refreshdict)
        return ret
