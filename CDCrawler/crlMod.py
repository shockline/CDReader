#-*- coding: gbk -*-

from bs4 import BeautifulSoup
from multiprocessing import Pool
import os
import sys
import time
import json
import random
import logMod
import cPickle
import urllib2
import ConfigParser

l = logMod.logMod()

config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 
# CONFIG SET
path_dict = config.get("path", "path_dict")
path_data = config.get("path", "path_data")
path_pxylist = config.get("path", "path_pxylist")
exec_runtime = config.getint("para","EXEC_CYCLETIME")
_URLHEAD = config.get("netpage","URLHEAD")
_MAINURL = config.get("netpage","MAINURL")

class crlMod:

    Data = path_data
    Dict = path_dict
    LastDate = "Last Recorded Date"
    LastTime = 0
    infile = ""
    CurrentDate = "Current Date"
    CurrentTime = -1
    Storetmp = {} # tmp for this time
    dictStore = {} # dict from last time, updated by 'tmp'
    proxylist = []
    
    UrlHead = _URLHEAD
    MainUrl = _MAINURL

    def __init__(self):
        self.LastTime = time.localtime(time.time())
        self.ChangeFile()
    
    
    def SetProxy(self, exlist):
        self.proxylist.extend(exlist)
        tmplist = []
        for each in self.proxylist :
            if each not in tmplist :
                tmplist.append(each)
        self.proxylist = tmplist # Unique
    
    
    def GetDesc(self, pagesite) :
        value = "NULL"
        try :
            html_doc = urllib2.urlopen(pagesite) 
        except :
            #l.Notice("Desc_Crawl fail " + str(pagesite))
            return value
        soup = BeautifulSoup(html_doc)
        for link in soup.find_all('div') :
            if link.get('class') and link.get('class')[0] == 'newsContent' :
                value = link.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','')
        return value
    
    
    def MergeUrl(self, link) :    
        pagesite = ""
        try:
            mid = "".join((link['datetime'].split("T")[0]).split("-"))
            last = link['infoCode']
            pagesite = "%s%s/%s.html" % (self.UrlHead, str(mid), str(last))
        except:
            l.Warning("Get pagesite failed: " + str(link))
            return "NULL"
        return pagesite
    
    
    def GetContent(self, soup) :
        if soup :
            for link in soup['data'] : # 'link': json-info-group
                pagesite, value = "", ""
                pagesite = self.MergeUrl(link)
                if pagesite == "NULL":
                    return -3 # Retry
                key = "%s$%s$%s" % (link['secuFullCode'],link['title'],link['author'])
                value = self.GetDesc(pagesite)
                if value == "NULL":
                    l.Notice("Get NULL Desc from %s" % str(pagesite).replace(self.UrlHead, ""))
                    return -3 # Retry
                if (not self.dictStore.has_key(key)) or self.dictStore[key] != pagesite :
                    self.infile.write( "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
                    % (link['secuFullCode'], link['secuName'], link['companyCode'], link['rate'], link['change'],\
                    link['sratingName'], link['insName'], link['author'], pagesite, link['title'], value) ) 
                    self.Storetmp[key] = pagesite
                else :
                    return 1 # This one has been crawled
            return 0
        else :
            return -2
    
    
    def Getdoc(self, url, pxy) :
        tmp = pxy.split(':');
        ip = tmp[0];
        port = tmp[1];
        proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
        opener = urllib2.build_opener(proxy_handler);
        urllib2.install_opener(opener);
        request = urllib2.Request(url);  
        request.add_header('User-Agent', 'fake-client');  
        html_doc = urllib2.urlopen(request)
        return html_doc
            
            
    def GetMainUrl(self, url, pxy) : 
        try :
            html_doc = self.Getdoc(url, pxy)
            # Get info from doc
            the_page = html_doc.read()
            page = "".join(the_page.split("=")[1:])
            contents = json.loads(page)
        except Exception, e:
            l.Warning("GetMainURL failed: %s %s" % (str(url), str(e)))
            self.proxylist.remove(pxy)
            if self.proxylist:
                newpxy = self.proxylist[random.randrange(0, len(self.proxylist), 1)]
                return self.GetMainUrl(url,newpxy)
            else :
                return -1 # Pxylist is Empty
        return self.GetContent(contents)

    
    def ChangeFile(self):
        self.LastDate = str(time.strftime('%m%d',time.localtime(time.time())))
        self.infile = open(self.Data.replace('.txt','%s.txt' % self.LastDate),"a")
    
    
    def DumpDict(self): # Dump dictStore
        if self.dictStore:
            cPickle.dump(self.dictStore, open(Dict, "w"))
    
    
    def Storepxy(self): # Make a back-up
        if self.proxylist :
            cPickle.dump(self.proxylist, open(path_pxylist, "w"))
    
    
    def CrawlPage(self, page) :
        self.ChangeFile()
        pos = random.randrange(0, len(self.proxylist), 1)
        url = self.MainUrl.replace("pagesites", str(page))
        ret = self.GetMainUrl(url, self.proxylist[pos])
        if ret == 1: # If Store Changed
            if self.Storetmp:
                l.Notice("Something New Existed")
        elif ret == -1: # Gain Failed
            l.Fatal("Proxylist has been empty")
        elif ret <= -2: # NoContentError (Soup.size is 0 or Desc is empty)
            l.Warning("GetSoup Failed")
        elif ret == 0: # Crawl until Page_end
            l.Notice("Initial Finish")
        if self.Storetmp : # If No news then return 'Empty'
            self.dictStore = self.Storetmp
            self.Storetmp = []
        return ret