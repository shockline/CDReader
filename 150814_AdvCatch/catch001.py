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

UrlHead = "http://search.10jqka.com.cn/"
MainUrl = "http://search.10jqka.com.cn/search?preParams=&ts=1&f=1&qs=1&querytype=&tid=report&bgid=&sdate=&edate=&tid=report&w=#stockcode#"

label = ["20","机构","评级","分析","研报","页数"] #时间,机构,评级,分析师,研报类型,页数
stocklist = []

def GetDesc(pagesite) : #Get Maintext on src
    info = []
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
    
    #print "I'm going to get Title\n"
    for link in soup.find_all('div') :
        #print "%s\n" % link
        if link.get('class') and link.get('class')[0] == 'kuaizhaolefttitle' and link.text != "":
            # Gain Title
            titleInfo = link.h2.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','').encode('utf-8') 
            info.append(titleInfo)
            
    #print "I'm going to get Maintext\n"
    for link in soup.find_all('div') :
        #print "%s\n" % link
        if link.get('class') and link.get('class')[0] == 'kuaizhao_contant' and link.text != "":
            # Gain Maintext
            textInfo = link.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','').encode('utf-8') 
            info.append(textInfo)
            
    return '\t'.join(info)

    
def GetNext(html_doc) : # find all Maintext_Entrance
    value = []
    soup = BeautifulSoup(html_doc)
    #print "I'm going to find hrefs\n"
    for div in soup.find_all('div','s_r_box') :
        info = []
        for link in div.find_all('h2') :
            for t in link.find_all('a','reportPreview') :
                info.append(t['href'])
                # print "%s\n" % (t['href']) # Check url
        for attr in div.find_all('p','s_r_attr') :
            a = attr.get_text().replace(' ','').replace('\t','').replace('\r','').replace('\n','').replace('\b','').replace('/','\t')
            crack = a.split('\t')
            #print crack
            pos = 0
            ret = []
            lim = len(crack)
            for i in xrange(0,6) :
                if pos < lim and len(crack[pos])>2 and crack[pos][0:2] == label[i]:
                    ret.append(crack[pos])
                    pos = pos + 1
                else :
                    ret.append("NULL")
                    if pos > lim :
                        logger.info("[Div_ERROR]:" + crack[pos])
            info.append('\t'.join(ret))
        value.append(info)
    return value  

    
def MergeUrl(link) : # Add href with UrlHead
    try:
        pagesite = UrlHead + link
    except:
        logger.info("[Merge_ERROR]:" + link)
        return "NULL"
    #print "Now I'm going to request %s \n" % pagesite
    return pagesite


def GetContent(soup, ncp) : 
    for pair in soup :
        link = pair[0]
        info = pair[1]
        pagesite, value = "", ""
        if MergeUrl(link) != "NULL":
            pagesite = MergeUrl(link)
            #print "Now getting Desc\n"
            value = GetDesc(pagesite)
            if value != "" and value !="\t" :
                print "%s\t%s\t%s\t%s\t%s" % (ncp[0], ncp[1], pagesite, info, value)
                sys.stdout.flush()
            else :
                logger.info("[NoContent_ERROR]:" + link)
        else:
            logger.info("[GetContent_ERROR]:" + link)

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
    ret = "NULL"
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
    try:
        req = urllib2.Request(url = pagesite, headers = headers)
        html_doc = urllib2.urlopen(req)
    except:
        logger.info("[CheckEnd_ERROR]:" + pagesite)
        return -1
    soup = BeautifulSoup(html_doc)
    for link in soup.find_all('div','grayr') :
        for tl in link.find_all('a') :
            #print "%s\t%s\n" % (tl.string, tl.text)
            if tl.text == "下一页" :
                ret = UrlHead + "search" + tl['href']
    return ret
    

    
if __name__ == '__main__' : #Main for Stock_code_loop

    infile = open("name-code.txt","r")
    line = infile.readline()
    while line:
        ncpair = line.replace(' ','').replace('\r','').replace('\n','').replace('\b','').replace('/','\t').split('\t')
        stocklist.append(ncpair)
        line = infile.readline()
    infile.close()

    for i in xrange(0,2599) : # 2600lines
        ret = 0
        url = MainUrl.replace("#stockcode#", stocklist[i][1])
        if i%20 == 0 :
            CurrentTime = time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
            logger.info("[Log] %s on %s" % (CurrentTime, stocklist[i][1]))
        #print "Now go to %s" % stocklist[i][1]
        while True:
            ret = GetMainUrl(url, stocklist[i]) # Jump into the netpage
            if ret == -1 :
                logger.info("[GetUrl_ERROR]:" + url)
            nextPage = CheckEnd(url) # null if no nextPage, otherwise return nextPage's Url
            if nextPage == "NULL" :
                break
            url = nextPage # Get the nextPage's url


