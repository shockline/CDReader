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
sys.setdefaultencoding('gb18030')

Url = "http://quote.eastmoney.com/stocklist.html"

def GetDesc(pagesite) :
    value = []
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
    for link in soup.find_all('li') :
        if link.find('a') and link.a['target'] == "_blank" and link.a.string[-1]==')': 
            value.append(link.a.string.decode('gb18030').encode('utf-8'))
    return value

def GetContent(pagesite) :
    #print "Now getting Desc\n"
    value = GetDesc(pagesite)
    #f.write("%s\t%s\t%s\n" % (link['title'], pagesite, value))
    f = open(Data,'a')
    for str in value :
        f.write("%s\n" % (str))
    f.close()
		
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
    GetContent(pagesite)
    return 0

	
if __name__ == '__main__' :
    ret = 0
    url = Url
    ret = GetMainUrl(url)
    if ret == -1 :
        print "no return at %s : %s" % (i,url)



