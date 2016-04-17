#-*- coding: gbk -*-

from bs4 import BeautifulSoup
from multiprocessing import Pool
import os
import sys
import time
import logMod
import cPickle
import urllib2
import ConfigParser

l = logMod.logMod()

config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 
# CONFIG SET
path_new = config.get("path", "path_new")
path_dict = config.get("path", "path_dict")
path_pxylist = config.get("path", "path_pxylist")
path_tmplist = config.get("path", "path_tmplist")
exec_runtime = config.getint("para","RUNTIME_WAITTIME")

class prxMod:

    LastDate = "Last Recorded Date"
    CurrentDate = "Current Date"
    proxylist = [] # Serviceability-unknown prxlist to Service-Avaliable List
    
    # Varieties Setter and Getter
    def Get_proxylist(self): # This means get the list of 'self'
        return self.proxylist
    
    
    def test_proxy(self,ip,port):
        #print ip,port,'miao'
        try:
            time1= time.time();
            proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(ip,port)});
            opener = urllib2.build_opener(proxy_handler);
            urllib2.install_opener(opener);
            request = urllib2.Request('http://data.eastmoney.com/');  
            request.add_header('User-Agent', 'fake-client');  
            response = urllib2.urlopen(request,timeout = exec_runtime);  
            text = response.read(); 
            #print "%s" % text
            if len(text) > 10:
                time2 = time.time();
                if time2 - time1 < exec_runtime:
                    fobj = open(path_tmplist, "a");
                    fobj.write('%s:%s\n'%(ip,port));
                    fobj.close();
            else:
                raise 'error';
        except Exception,ex:
            l.Notice("%s Failed, %s" % (str(ip), str(ex)))
            
            
    def check_proxy(self):
        lines = []
        if (os.path.exists(path_new)): # Format : <IPAddress>:<Port>@<Anything> per line
            lines = [line.strip().split('@')[0] for line in file(path_new)];
            for l in lines:
                tmp = l.split(':');
                ip = tmp[0]; 
                port = tmp[1];
                self.test_proxy(ip,port);
            os.remove(path_new)
            return True
        elif os.path.exists(path_pxylist):
            if self.proxylist :
                return True
            else :
                f = open(path_pxylist)
                self.proxylist = cPickle.load(f)
                return True
        else:
            l.Fatal("Please Add new Proxylist <" + str(self.LastDate))
        return False # Means there's no more new prx to add

        
    def Getpxylist(self): # This means get list by calculating from origin resource
        Status = self.check_proxy()
        self.LastDate = str(time.strftime('%m%d',time.localtime(time.time())))
        if (os.path.exists(path_tmplist)):
            self.proxylist = [line.strip().split('@')[0] for line in file(path_tmplist)];  
            os.remove(path_tmplist) # Delete tmpFile
            self.Storepxy()
        elif Status == False:
            l.Warning("Getlist fail at " + str(self.LastDate))
        return Status # If return true, list can be available as "proxylist"


    def Storepxy(self): # Make a back-up
        cPickle.dump(self.proxylist, open(path_pxylist, "w"))
        
        
    def DumpList(self): # For Refresh or Check
        if self.proxylist:
            fobj = open(path_tmplist, "a");
            for each in self.proxylist:
                fobj.write("%s" % str(each));
            fobj.close();
        else :
            l.Notice("Empty pxylist at " + str(self.LastDate))
