#-*- coding: gbk -*-

from bs4 import BeautifulSoup
import urllib2
import sys
import logging 
import json

Log = "./log/Log.txt"
Data =  "./data/text.txt"

logger=logging.getLogger()
handler=logging.FileHandler(Log)
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

reload(sys)
sys.setdefaultencoding('utf-8')

UrlHead = "http://blog.csdn.net"
MainUrl = "http://blog.csdn.net/okcd00/article/list/pagesites"


def GetDesc(pagesite) :
    value = "NULL"
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
    req = urllib2.Request(url = pagesite, headers = headers)
    #print "%s\t" % (req)
    try :
        html_doc = urllib2.urlopen(req)
    except :
        logger.info("[ERROR]:" + pagesite)
        return value
    soup = BeautifulSoup(html_doc)
    #print "I'm going to get Maintext\n"
    for link in soup.find_all('div') :
        if link.get('class') and link.get('class')[0] == 'article_content' :
            value = link.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','').encode('utf-8')
    return value

    
def GetNext(html_doc) :
    value = []
    soup = BeautifulSoup(html_doc)
    #print "I'm going to find hrefs\n"
    for link in soup.find_all('h1') :
        if link.find('a') :
            value.append(link.a['href'])
            #print "%s\n%s\n" % (link.a.string,link.a['href'])
    return value  

	
def MergeUrl(link) :
    try:
        mid = link
        pagesite = UrlHead + mid
        #print "now go to the url: %s" % pagesite
    except:
        logger.info("[ERROR]:" + link)
        return "NULL"
    #print "Now I'm going to request %s \n" % pagesite
    return pagesite


def GetContent(soup) :
    for link in soup :
        #print link
        pagesite, value = "", ""
        if MergeUrl(link) != "NULL":
            pagesite = MergeUrl(link)
            #print "Now getting Desc\n"
            value = GetDesc(pagesite)
            #f.write("%s\t%s\t%s\n" % (link['title'], pagesite, value))
            f = open(Data,'a')
            f.write("%s\t%s\n" % (pagesite, value))
            f.close()
        else:
            print "%s\t Nothing here\n" % pagesite 

		
def GetMainUrl(pagesite) :
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
    try:
        req = urllib2.Request(url = pagesite, headers = headers)
        #print "%s\t" % (req)
        html_doc = urllib2.urlopen(req)
        #print "%s\t" % (html_doc)
        #the_page = html_doc.read()
        #print "%s\t" % (the_page)
    except:
        logger.info("[ERROR]:" + pagesite)
        return -1
    url_list = GetNext(html_doc)
    GetContent(url_list)
    return 0

	
if __name__ == '__main__' :
    for i in xrange(1,10) :
        ret = 0
        url = MainUrl.replace("pagesites", str(i))
        ret = GetMainUrl(url)
        if ret == -1 :
            print "no return at %s : %s" % (i,url)
            continue



