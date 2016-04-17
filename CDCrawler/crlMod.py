#-*- coding: gbk -*-

from bs4 import BeautifulSoup
from multiprocessing import Pool
import os
import sys
import time
import json
import cPickle
import urllib2
import logging 

class crlMod:

    Log = "./log/crlLog.txt"
    Data =  "./data/crlData.txt"
    LastDate = "Last Recorded Date"
    LastTime = 0
    CurrentDate = "Current Date"
    CurrentTime = -1
    dictStore = {} # dict from last time, updated by 'tmp'
    Storetmp = {} # tmp for this time
    proxylist = []
    infile = ""

    logger=logging.getLogger()
    handler=logging.FileHandler(Log)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)

    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    UrlHead = "http://data.eastmoney.com/report/"
    MainUrl = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?\
    type=SR&sty=GGSR&js=var%20qjEEjLvR={%22data%22:[(x)],%22pages%22:%22(pc)%22,\
    %22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p=pagesites&mkt=0&stat=0&cmd=2&code=&rt=47941243"

    def __init__(self):
        LastTime = time.localtime(time.time())
        self.LastDate = str(time.strftime('%m%d',time.localtime(time.time())))
        self.infile = open(self.Data.replace('.txt','%s.txt' % self.LastDate),"a")
    
    
    def setProxy(self, list):
        self.proxylist = list
    
    
    def GetDesc(self, pagesite) :
        value = "NULL"
        try :
            html_doc = urllib2.urlopen(pagesite) 
        except :
            self.logger.info("[ERROR]:" + str(pagesite))
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
            print pagesite
        except:
            self.logger.info("[ERROR]:" + str(link))
            return "NULL"
        return pagesite
    
    
    def GetContent(self, soup) :
        for link in soup['data'] :
            #print link
            pagesite, value = "", ""
            pagesite = self.MergeUrl(link)
            key = "%s\t%s\t%s" % (link['secuFullCode'],link['title'],link['author'])
            if (not self.dictStore.has_key(key)) or self.dictStore[key] != pagesite :
                #print "%s\t%s\t%s\t%s\t%s" % (ncp[0], ncp[1], pagesite, info, value)       
                self.Storetmp[key] = pagesite
            else :
                return 1
            value = self.GetDesc(pagesite)
            self.infile.write( "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
            % (link['secuFullCode'], link['secuName'], link['companyCode'], link['rate'], link['change'],\
            link['sratingName'], link['insName'], link['author'], pagesite, link['title'], value) ) 
        return 0
    
    
    def GetMainUrl(self, url, pxy) : 
        value = -1
        tmp = pxy.split(':');
        ip = tmp[0];
        port = tmp[1];
        try :
            proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
            opener = urllib2.build_opener(proxy_handler);
            urllib2.install_opener(opener);
            request = urllib2.Request(url);  
            request.add_header('User-Agent', 'fake-client');  
            html_doc = urllib2.urlopen(request)
        except Exception, e:
            self.logger.info("[Urlopen_ERROR]:" + str(url) + str(e))
            return value
        the_page = html_doc.read()
        page = "".join(the_page.split("=")[1:])
        contents = json.loads(page)
        return self.GetContent(contents)
    
    
    def CrawlPage(self, pxy, page) :
        ret = 0
        #self.proxylist = pxy
        url = self.MainUrl.replace("pagesites", str(page))
        ret = self.GetMainUrl(url, pxy)
        if ret == 1: # If Store Changed
            self.dictStore = self.Storetmp
        return ret