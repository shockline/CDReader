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

class prxMod:

    Log = "./log/PrxLog.txt"
    Data =  "./data/PrxData.txt"
    LastDate = "Last Recorded Date"
    LastTime = 0
    CurrentDate = "Current Date"
    CurrentTime = -1
    proxylist = [] # Serviceability-unknown prxlist to Service-Avaliable List

    logger=logging.getLogger()
    handler=logging.FileHandler(Log)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)

    reload(sys)
    sys.setdefaultencoding('utf-8')

        
    def test_proxy(self,ip,port):
        #print ip,port,'miao'
        try:
            time1= time.time();
            proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
            opener = urllib2.build_opener(proxy_handler);
            urllib2.install_opener(opener);
            request = urllib2.Request('http://data.eastmoney.com/');  
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
            self.logger.info("[check]:" + str(ex))   
            
            
    def check_proxy(self):
        lines = []
        if (os.path.exists('./new.txt')):
            lines = [line.strip().split('@')[0] for line in file('new.txt')];
            for l in lines:
                tmp = l.split(':');
                ip = tmp[0]; 
                port = tmp[1];
                self.test_proxy(ip,port);
            os.remove('./new.txt')
            return True
        elif os.path.exists('./pxylist.txt'):
            if self.proxylist :
                return True
            else :
                f = open(r"./pxylist.txt")
                self.proxylist = cPickle.load(f)
                return True
        else:
            self.logger.info("[ERROR]: prx_new fail at " + str(self.LastDate))
        return False

        
    def Getpxylist(self):
        Status = self.check_proxy()
        self.LastDate = str(time.strftime('%m%d',time.localtime(time.time())))
        if (os.path.exists('./proxy_inuse.txt')):
            self.proxylist = [line.strip().split('@')[0] for line in file('proxy_inuse.txt')];  
            os.remove('./proxy_inuse.txt') # Delete tmpFile
            self.StoreFile()
        elif Status == False:
            self.logger.info("[ERROR]: Getlist fail at " + str(self.LastDate))
        return Status # If return true, list can be available as "proxylist"


    def StoreFile(self):
        cPickle.dump(self.proxylist, open("pxylist.txt", "w"))
        
    def RefreshList(self):
        if self.proxylist:
            fobj = open('proxy_inuse.txt','a');
            for each in self.proxylist:
                fobj.write("%s" % str(each));
            fobj.close();
        else :
            self.logger.info("[TIP]: Empty pxylist at " + str(self.LastDate))
