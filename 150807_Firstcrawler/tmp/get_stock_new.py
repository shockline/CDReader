#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import sys
import logging 
import json

Log = "./log/Log.txt"
Data =  "./data/stock.txt"

logger=logging.getLogger()
handler=logging.FileHandler(Log)
logger.addHandler(handler)
logger.setLevel(logging.NOTSET)

reload(sys)
sys.setdefaultencoding('utf-8')

UrlHead = "http://data.eastmoney.com/report/"
MainUrl = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20qjEEjLvR={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p=pagesites&mkt=0&stat=0&cmd=2&code=&rt=47941243"


def GetDesc(pagesite) :
    value = "NULL"
    try :
        html_doc = urllib2.urlopen(pagesite) 
    except :
        logger.info("[ERROR]:" + pagesite)
        return value
    soup = BeautifulSoup(html_doc)
    for link in soup.find_all('div') :
        if link.get('class') and link.get('class')[0] == 'newsContent' :
            value = link.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','').encode('utf-8')
    return value
    
    
def PrintResult(ConList):
    file_object = open(Data, 'a')
    fields = '\t'.join(ConList) + '\n'
    file_object.write(fields)
    file_object.close()


def MergeUrl(link) :
    try:
        mid = "".join((link['datetime'].split("T")[0]).split("-"))
        last = link['infoCode']
        pagesite = UrlHead + mid + '/' + last + '.html'
    except:
        logger.info("[ERROR]:" + link)
        return "NULL"
    return pagesite


def GetContent(soup) :
    for link in soup['data'] :
        #print link
        pagesite, value = "", ""
        pagesite = MergeUrl(link)
        value = GetDesc(pagesite)
        #print link['secuFullCode'],link['companyCode']
        f = open(Data,'a')
        f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (link['secuFullCode'], link['secuName'], link['companyCode'], link['rate'], link['change'], link['sratingName'], link['insName'], link['author'], pagesite, link['title'], value))
        f.close()

def GetMainUrl(pagesite) :
    try:
        req = urllib2.Request(pagesite) # Send Request
        html_doc = urllib2.urlopen(req) # Get Documents
        the_page = html_doc.read()
    except:
        logger.info("[ERROR]:" + pagesite)
        return -1
    page = "".join(the_page.split("=")[1:]) 
    contents = json.loads(page)
    GetContent(contents)
    return 0

if __name__ == '__main__' :
    for i in xrange(1,2) :
        ret = 0
        url = MainUrl.replace("pagesites", str(i)) #Replace differences in Mainurl to find destination
        ret = GetMainUrl(url)



