#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import sys
import json
import time
import cPickle
import logging 

Log = "./log/Log.txt"
Data =  "./data/Stock.txt"

logger=logging.getLogger()
handler=logging.FileHandler(Log)
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

reload(sys)
sys.setdefaultencoding('utf-8')

UrlHead = "http://vip.stock.finance.sina.com.cn/q/go.php/vReport_List/kind/search/index.phtml?symbol=#stockcode#&t1=all&p="

posi = -1               # Which stockcode is being crawling in this cycle
update_Flag = False     # Whether Update the dictData
stocklist = []          # Store name-code pair
dictStore = {}          # Store Info-_Url pair


def Getsoup(pagesite) :
    value = "NULL"
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
    req = urllib2.Request(url = pagesite, headers = headers)
    #print "%s\t" % (req)
    try :
        html_doc = urllib2.urlopen(req)
    except Exception, e:
        logger.info("[Urlopen_ERROR]:" + str(pagesite) + "\t" + str(e))
        return value
    soup = BeautifulSoup(html_doc)
    #print len(soup)
    return soup

    
def Getsoup_pxy(url, ip, port) : # If use this, Add call in Getsoup() with proxy_Addr
    try :
        proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
        opener = urllib2.build_opener(proxy_handler);
        urllib2.install_opener(opener);
        request = urllib2.Request(url);  
        request.add_header('User-Agent', 'fake-client');  
        html_doc = urllib2.urlopen(request)
    except Exception, e:
        logger.info("[Urlopen_ERROR]:" + str(url) + str(e))
        return value
    soup = BeautifulSoup(html_doc)
    return soup

    
def GetDesc(pagesite) : #Get Maintext on src
    value = "NULL"
    soup = Getsoup(pagesite)
    if soup == "NULL":
        return value
        
    #print "I'm going to get Maintext\n"
    for blk in soup.find_all('div') :
        if blk.get('class') and blk.get('class')[0]=="main" and blk.get('class')[1]=="clearfix" :
            for div in blk.find_all('div', 'blk_container') :
                # Gain Maintext
                if div.text != "":
                    value = div.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','').encode('utf-8') 
    return value

    
def GetNext(soup) : # find all Maintext_Entrance
    value = []
    #print "I'm going to find hrefs\n"
    for tab in soup.find_all('table','tb_01') :
        trpos = 0
        for tr in tab.find_all('tr') :
            trpos = trpos + 1
            if trpos > 2 :
                pos = 0
                ret = []    # attrs container
                info = []   # pair of (url, attrs)
                for td in tr.find_all('td') :
                    pos = pos + 1
                    if pos > 1 :
                        if pos == 2 :
                            for ahref in td.find_all('a') :
                                if ahref.get('href') and ahref.get('href')[0] != "" :
                                    info.append(td.a['href']) # get info[0]: url
                                    textV = td.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','').encode('utf-8')
                                    ret.append(textV)
                        else :
                            if td.get_text() == "" :
                                ret.append("NULL")
                            else :
                                textV = td.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','').encode('utf-8')
                                ret.append(textV)
                info.append('\t'.join(ret)) # get info[1]: attrs
                value.append(info)
    return value  

    
def GetContent(soup, ncp) : 
    for pair in soup :
        if len(pair) == 2 : # For Exception 'IndexError'
            link = pair[0]
            info = pair[1]
            key = info.decode('utf-8')
            pagesite, value = "", ""
            if link != "NULL" and link != "":
                pagesite = link
                #print "Now getting Desc\n"
                value = GetDesc(pagesite)
                if value != "" and value !="\t" :
                    if (not dictStore.has_key(key)) or dictStore[key] != pagesite :
                        print "%s\t%s\t%s\t%s\t%s" % (ncp[0], ncp[1], pagesite, info, value)
                        print key, dictStore[key]
                        sys.stdout.flush()
                        dictStore[info] = pagesite
                else :
                    logger.info("[NoContent_ERROR]:" + str(link))
            else:
                logger.info("[GetContent_ERROR]:" + str(link))
        else :
            logger.info("[InfoMiss_ERROR]: on " + ncp[0] + " " + ncp[1])

            
def GetMainUrl(pagesite, ncp) : #Crawl Maintext pagelist <on this page>
    soup = Getsoup(pagesite)
    #print soup
    if soup == "NULL" or soup == "" :
        return -1
    else :
        # Get Content of Next-level link_list
        url_list = GetNext(soup)
        GetContent(url_list, ncp)
        return 0

    
def CheckEnd(pagesite) : #Check whether this url has nextPage
    soup = Getsoup(pagesite)
    if soup == "NULL" or len(soup) < 5 :
        return True # White means End
    
    #Check Whether it has "Next"
    for link in soup.find_all('div','pagebox') :
        for tl in link.find_all('span') :
            #print tl.get('class')[0]
            if tl.get('class') and tl.get('class')[0] == "pagebox_next" :
                return False
            if tl.get('class') and tl.get('class')[0] == "pagebox_next_nolink" :
                return True
    logger.info("[log] %s Get the End" % pagesite[-2:])
    return True


def Get_stock_in_file() :
    try :
        infile = open("name-code.txt","r")
        line = infile.readline()
        while line:
            ncpair = line.replace(' ','').replace('\r','').replace('\n','').replace('\b','').replace('/','\t').split('\t')
            stocklist.append(ncpair)
            line = infile.readline()
        infile.close()
        cPickle.dump(stocklist, open("listData","w"))
    except :
        logger.info("[Warning]: NCpair-File Not Exist")

        
def Get_stock() : # Use Func_infile to init
    sl = []
    try :
        sl = cPickle.load(open("listData","r"))
    except :
        logger.info("[Warning]: NCpair-File Not Exist")
    return sl
    
    
def Get_posi() : # Get the position of present crawling
    ret = -1
    try :
        ret = cPickle.load(open("posi","r"))
    except :
        logger.info("[Warning]: Posi-File Not Exist")
    return ret
    
    
def Dump_file(date) :
    try :
        if update_Flag == True :
            cPickle.dump(dictStore, open("dictData","w"))
            cPickle.dump(posi, open("posi","w"))
    except Exception, e:
        logger.info("[Dump_Error]: " + str(e))
            
    
if __name__ == '__main__' : #Main for Stock_code_loop

    #init
    posi = Get_posi()
    stocklist = Get_stock()
    CurrentTime = time.strftime('%m-%d %H:%M:%S',time.localtime(time.time())) #Start
    
    #for posi in xrange(0,2599) : # sz-1259 sh-1341 lines in 2600 lines
    while True :
        posi = (posi + 1 + 2600) % 2600
        ret = 0
        page = 1
        update_Flag = False
        head = UrlHead.replace("#stockcode#", stocklist[posi][1])
        if posi % 20 == 0 :
            CurrentTime = time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
            logger.info("[Log] %s on %s" % (CurrentTime, stocklist[posi][1]))
        #print "Now go to %s" % stocklist[posi][1]
        while True:
            url = head + str(page) # Get the nextPage's url
            ret = GetMainUrl(url, stocklist[posi]) # Jump into the netpage
            if ret == -1 :
                logger.info("[GetUrl_ERROR]:" + url)
            if CheckEnd(url) == True :
                break
            page = page + 1
        # Dump Present_Status into file
        if update_Flag == True :
            Dump_file(CurrentTime)

