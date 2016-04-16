# -*- coding: gbk -*-

from bs4 import BeautifulSoup
from multiprocessing import Pool

import os
import sys
import time
import logMod
import random
import cPickle
import urllib2
import ConfigParser

l = logMod.logMod()
config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 
path_home = config.get("path", "path_home")
path_list = config.get("path", "path_list")
prxswitch = config.getint("para", "USE_PROXY")
exec_cyctime = config.getint("para", "EXEC_CYCLETIME")

cachepxy = []

filepath = [line.strip().split('@')[0] for line in file(path_list) ]
TestPassUrl = [line.strip().split('@')[1] for line in file(path_list) ]

def test_proxy(ip, port, target):
    try:
        time1= time.time();
        proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
        opener = urllib2.build_opener(proxy_handler);
        urllib2.install_opener(opener);
        request = urllib2.Request(TestPassUrl[target]);  
        request.add_header('User-Agent', 'fake-client');  
        response = urllib2.urlopen(request,timeout = 10);  
        text = response.read(); 
        #print "Text: %s" % len(text)
        if len(text) > 10:
            time2 = time.time();
            if time2 - time1 < 10:
                fobj = open("%s/%s" % (str(path_home), filepath[target]), "a");
                current_proxy = str(ip) + ":" + str(port)
                fobj.write('%s\n' % current_proxy );
                if prxswitch != 0 and len(cachepxy) < 20 and not(current_proxy in cachepxy) :
                    cachepxy.append( current_proxy )
                fobj.close();
                l.Notice("%s:%s Passed [Target %s]" % (str(ip), str(port), str(target))) 
                return True
        else:
            raise 'error';
    except Exception,ex:
        l.Notice("%s:%s Failed, %s" % (str(ip), str(port), str(ex))) 
        return False

def Getdoc_proxy(url, pxy) :
    __tmp = pxy.split(':');
    ip,port = __tmp[0],__tmp[1];
    proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
    opener = urllib2.build_opener(proxy_handler);
    urllib2.install_opener(opener);
    request = urllib2.Request(url);  
    request.add_header('User-Agent', 'fake-client');  
    html_doc = urllib2.urlopen(request, timeout = 10)
    return html_doc

def Getdoc_direct(url) :
    request = urllib2.Request(url);  
    request.add_header('User-Agent', 'fake-client');  
    html_doc = urllib2.urlopen(request, timeout = 10)
    return html_doc

def Getdoc(url) :
    if prxswitch == 0 :
        doc = Getdoc_direct(url)
        return doc
    else :
        try :
            doc = Getdoc_direct(url)
            return doc
        except Exception,ex :
            l.Warning( "Direct Crawl Failed at %s : %s\n" % (str(url), str(ex)) )
            while len(cachepxy) > 3 :
                idx = random.randrange(0, len(cachepxy), 1)
                Cur_proxy = cachepxy[idx]
                l.Notice("%s Proxy_Crawling... " % str(Cur_proxy) ) 
                try :
                    doc = Getdoc_proxy(url, Cur_proxy)
                    return doc
                except Exception,ex :
                    l.Warning("Proxy Crawl Failed at %s, Remove [%s] for %s" % (str(url), str(Cur_proxy), str(ex)) )
                    cachepxy.remove(Cur_proxy)
                    continue
            return Getdoc_direct(url)

                    
def GetSoup_html(html_doc, lang) :
    readinto = html_doc.read()
    soup = BeautifulSoup(readinto.decode(lang), "html.parser")
    return soup
    
def GetSoup(html_doc) :
    readinto = html_doc.read()
    soup = BeautifulSoup(readinto, "lxml")
    return soup
    
def Get_XICI():
    url = [ "http://www.xicidaili.com/nn/", "http://www.xicidaili.com/nt/", \
            "http://www.xicidaili.com/wn/", "http://www.xicidaili.com/wt/"]
    retlist = []
    for idx in xrange(0,4):
        doc = Getdoc(url[idx])
        soup = GetSoup(doc)
        for table in soup.find_all('table') :
            if table.find('tr') :
                for tr in table.find_all('tr') :
                    if tr.find('td'):
                        ip = tr.find_all('td')[2].get_text()
                        port = tr.find_all('td')[3].get_text()
                        pxy = ip.strip() + ":" + port.strip()
                        retlist.append(pxy)
    return retlist
                        
                        
def Get_KUAI():
    urlhead = "http://www.kuaidaili.com/proxylist/pagesites/"
    retlist = []
    for idx in xrange(1,11):
        url = urlhead.replace('pagesites',str(idx))
        doc = Getdoc(url)
        soup = GetSoup(doc)
        for table in soup.find_all('table') :
            if table.find('tr') :
                for tr in table.find_all('tr') :
                    if tr.find('td'):
                        ip = tr.find_all('td')[0].get_text()
                        port = tr.find_all('td')[1].get_text()
                        pxy = ip.strip() + ":" + port.strip()
                        retlist.append(pxy)
    return retlist
        
        
def Get_P360():
    url = "http://www.proxy360.cn/Proxy"
    doc = Getdoc(url)
    soup = GetSoup(doc)
    retlist = []
    for table in soup.find_all('table') :
        for div in table.find_all('div', 'proxylistitem') :
            if div.find('span'):
                ip = div.find_all('span')[0].get_text()
                port = div.find_all('span')[1].get_text()
                pxy = ip.strip() + ":" + port.strip()
                retlist.append(pxy)
    return retlist
    
    
def Get_YDLN(): # Broken Soup
    url = ""
    head = "http://www.youdaili.net/Daili/guonei/"
    docu = Getdoc(head)
    soup = GetSoup(docu)
    for ul in soup.find_all('ul', 'newslist_line'):
        if ul.find('li'):
            url = str(ul.find_all('li')[0].a['href'])
            break
    doc = Getdoc(url)
    soup = GetSoup_html(doc, "Unicode")
    # print soup # May be some Block
    for list in soup.find_all('div', 'content_newslist') :
        for div in soup.find_all('div', 'cont_font') :
            if div.find('p'):
                print div.find_all('p')[0].get_text().strip()
    
    
def Get_CZ88():
    url = "http://www.cz88.net/proxy/"
    doc = Getdoc(url)
    soup = GetSoup(doc)
    retlist = []
    for d in soup.find_all('div') :
        if d.get('id') and d['id'] == 'boxright' :
            Flag = True
            for li in d.find_all('li'):
                if Flag :
                    Flag = False
                    continue
                else :
                    ip = li.find_all('div')[0].get_text().strip()
                    port = li.find_all('div')[1].get_text().strip()
                    pxy = ip.strip() + ":" + port.strip()
                    retlist.append(pxy)
    return retlist


def test_Vars():
    print filepath, TestPassUrl
    
if __name__ == '__main__':
    # test_Vars()
    pxylist = []
    try : # www.xicidaili.com
        pxylist.extend(Get_XICI())
        l.Notice("XICI Finished.")
    except Exception,ex :
        l.Warning("XICI Failed for %s" % str(ex))
    try : # www.kuaidaili.com
        pxylist.extend(Get_KUAI())
        l.Notice("KUAI Finished.")
    except Exception,ex :
        l.Warning("KUAI Failed for %s" % str(ex))
    try : # www.proxy360.cn
        pxylist.extend(Get_P360())
        l.Notice("P360 Finished.")
    except Exception,ex :
        l.Warning("P360 Failed for %s" % str(ex))   
    try : # www.cz88.net
        pxylist.extend(Get_CZ88())
        l.Notice("CZ88 Finished.")
    except Exception,ex :
        l.Warning("CZ88 Failed for %s" % str(ex))  
    
    cnt = {}
    lenT,lenP = len(TestPassUrl), len(pxylist)
    for idx in xrange(0, lenT):
        cnt[idx] = 0
    for each in pxylist:
        tmp = each.split(':');
        ip,port = tmp[0],tmp[1]; 
        for idx in xrange(0, lenT):
            if test_proxy(ip, port, idx):
                cnt[idx] += 1
    l.Notice("Crawl Finished, Result Below:")
    for idx in xrange(0, lenT):
        Rst = lenP
        l.Notice("[Target %s] (%s/%s) Passed %s\n" % (str(idx), str(cnt[idx]), str(Rst), TestPassUrl[idx] ))        
        