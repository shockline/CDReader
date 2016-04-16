#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import sys
import json
import time
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

stocklist = []

def GetDesc(pagesite) : #Get Maintext on src
    value = "NULL"
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
    req = urllib2.Request(url = pagesite, headers = headers)
    #print "%s\t" % (req)
    try :
        html_doc = urllib2.urlopen(req)
    except :
        logger.info("[Urlopen_ERROR]:" + pagesite)
        return value
    soup = BeautifulSoup(html_doc)
    
    #print "I'm going to get Maintext\n"
    for blk in soup.find_all('div') :
        if blk.get('class') and blk.get('class')[0]=="main" and blk.get('class')[1]=="clearfix" :
            for div in blk.find_all('div', 'blk_container') :
                # Gain Maintext
                if div.text != "":
                    value = div.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','').encode('utf-8') 
    return value

    
def GetNext(html_doc) : # find all Maintext_Entrance
    value = []
    soup = BeautifulSoup(html_doc)
    #print "I'm going to find hrefs\n"
    for tab in soup.find_all('table','tb_01') :
        trpos = 0
        for tr in tab.find_all('tr') :
            trpos = trpos + 1
            if trpos > 2 :
                pos = 0
                ret = []    # attrs container
                info = []   # pair of url & attrs 
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
        if len(pair) == 2 :
            link = pair[0]
            info = pair[1]
            pagesite, value = "", ""
            if link != "NULL" and link != "":
                pagesite = link
                #print "Now getting Desc\n"
                value = GetDesc(pagesite)
                if value != "" and value !="\t" :
                    print "%s\t%s\t%s\t%s\t%s" % (ncp[0], ncp[1], pagesite, info, value)
                    sys.stdout.flush()
                else :
                    logger.info("[NoContent_ERROR]:" + link)
            else:
                logger.info("[GetContent_ERROR]:" + link)
        else :
            logger.info("[InfoMiss_ERROR]: on " + ncp[0] + ncp[1])

            
def GetMainUrl(pagesite, ncp) : #Crawl Maintext pagelist <on this page>
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
    try:
        req = urllib2.Request(url = pagesite, headers = headers)
        #print "%s\t" % (req)
        html_doc = urllib2.urlopen(req)
        #print "%s\t" % (html_doc)
        #the_page = html_doc.read()
        #print "%s\t" % (the_page)
    except:
        logger.info("[GetUrl_ERROR]:" + pagesite)
        return -1
    
    # Get Content of Next-level link_list
    url_list = GetNext(html_doc)
    GetContent(url_list, ncp)
    
    return 0

def CheckEnd(pagesite) : #Check whether this url has nextPage
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
    try:
        req = urllib2.Request(url = pagesite, headers = headers)
        html_doc = urllib2.urlopen(req)
    except:
        logger.info("[CheckEnd_ERROR]:" + pagesite)
        return -1
    soup = BeautifulSoup(html_doc)
    #print pagesite,soup
    for link in soup.find_all('div','pagebox') :
        for tl in link.find_all('span') :
            #print tl.get('class')[0]
            if tl.get('class') and tl.get('class')[0] == "pagebox_next" :
                return False
            if tl.get('class') and tl.get('class')[0] == "pagebox_next_nolink" :
                return True
    logger.info("[log] %s Get the End" % pagesite[-2:])
    return True
    

    
if __name__ == '__main__' : #Main for Stock_code_loop

    infile = open("name-code.txt","r")
    line = infile.readline()
    while line:
        ncpair = line.replace(' ','').replace('\r','').replace('\n','').replace('\b','').replace('/','\t').split('\t')
        stocklist.append(ncpair)
        line = infile.readline()
    infile.close()
    for i in xrange(0,2599) : # 2600 lines
        ret = 0
        page = 1
        head = UrlHead.replace("#stockcode#", stocklist[i][1])
        if i % 20 == 0 :
            CurrentTime = time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
            logger.info("[Log] %s on %s" % (CurrentTime, stocklist[i][1]))
        #print "Now go to %s" % stocklist[i][1]
        while True:
            url = head + str(page) # Get the nextPage's url
            #print url
            ret = GetMainUrl(url, stocklist[i]) # Jump into the netpage
            if ret == -1 :
                logger.info("[GetUrl_ERROR]:" + url)
            if CheckEnd(url) == True :
                break
            page = page + 1


