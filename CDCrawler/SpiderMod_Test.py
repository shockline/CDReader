#-*- coding: gbk -*-

from bs4 import BeautifulSoup
from multiprocessing import Pool
import sys
import time
import json
import cPickle
import urllib2
import logging 

Log = "./log/Log.txt"
Data =  "./data/stock.txt"
LastDate = "Last Recorded Date"
LastTime = 0
CurrentDate = "Current Date"
CurrentTime = -1
dictStore = {}
proxylist = []

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


def GetDesc(pagesite) :
    value = "NULL"
    try :
        html_doc = urllib2.urlopen(pagesite) 
    except :
        logger.info("[ERROR]:" + str(pagesite))
        return value
    soup = BeautifulSoup(html_doc)
    for link in soup.find_all('div') :
        if link.get('class') and link.get('class')[0] == 'newsContent' :
            value = link.get_text().replace('\t','').replace('\r','').replace('\n','').replace('\b','')
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
        logger.info("[ERROR]:" + str(link))
        return "NULL"
    return pagesite


def GetContent(soup) :
    for link in soup['data'] :
        #print link
        pagesite, value = "", ""
        pagesite = MergeUrl(link)
        key = "%s\t%s" % (link['secuFullCode'],link['title'])
        if (not dictStore.has_key(key)) or dictStore[key] != pagesite :
            #print "%s\t%s\t%s\t%s\t%s" % (ncp[0], ncp[1], pagesite, info, value)       
            dictStore[info] = pagesite
        else :
            return 1
        value = GetDesc(pagesite)
        infile.write( "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" \
        % (link['secuFullCode'], link['secuName'], link['companyCode'], link['rate'], link['change'],\
        link['sratingName'], link['insName'], link['author'], pagesite, link['title'], value) ) 
    return 0
        

def GetMainUrl(pagesite) :
    try:
        req = urllib2.Request(pagesite)
        html_doc = urllib2.urlopen(req)
        the_page = html_doc.read()
    except:
        logger.info("[ERROR]:" + str(pagesite))
        return -1
    page = "".join(the_page.split("=")[1:])
    contents = json.loads(page)
    return GetContent(contents)

    
def test_proxy(ip,port):
    print ip,port,'miao'
    try:
        time1= time.time();
        proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
        opener = urllib2.build_opener(proxy_handler);
        urllib2.install_opener(opener);
        request = urllib2.Request('http://www.baidu.com/');  
        request.add_header('User-Agent', 'fake-client');  
        response = urllib2.urlopen(request,timeout=3);  
        text = response.read(); 
        #print "%s" % text
        if len(text)>10:
            time2 = time.time();
            if time2 - time1 < 3:
                fobj = open('proxy_inuse.txt','a');
                fobj.write('%s:%s\n'%(ip,port));
                fobj.close();
                #print ip,port;
                #logger.info("[check]:" + str(ip) + ":" + str(port))
        else:
            raise 'error';
    except Exception,ex:
        logger.info("[check]:" + str(ex))   
        
        
def check_proxy():
    lines = [line.strip().split('@')[0] for line in file('new.txt')];
    for l in lines:
        tmp = l.split(':');
        ip = tmp[0];
        port = tmp[1];
        test_proxy(ip,port);
    
    
def CrawlPage(i) :
    ret = 0
    url = MainUrl.replace("pagesites", str(i))
    ret = GetMainUrl(url)
    return ret
    

def StoreData(CurrentDate) :
    #if ( HAS_NEW_PROXYLIST ):
    #   check_proxy()
    proxylist = [line.strip().split('@')[0] for line in file('proxy_inuse.txt')];   
    if len(dictStore) != 0:
        cPickle.dump(dictStore, open("dictData%s.txt" % CurrentDate, "w"))

    
if __name__ == '__main__' :

    infile = open("./data/Init.txt","a")
    #CurrentTime = time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
    while True :
        CurrentDate = time.strftime('%m%d',time.localtime(time.time()))
        CurrentTime = time.localtime(time.time())
        #print CurrentDate, CurrentTime
        DataPath = "./%s.txt" % CurrentDate
        if(CurrentDate != LastDate):
            StoreData(CurrentDate)
            infile.close()
            infile = open("./data/%s.txt" % CurrentDate, "a")
            LastDate = CurrentDate
        else :
            nowpage = 1
            while True:
                sta_code = CrawlPage(nowpage)
                if sta_code == 0:
                    nowpage = nowpage + 1
                else :
                    break
        time.sleep(5*60)



