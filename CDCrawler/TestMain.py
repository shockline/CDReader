#-*- coding: gbk -*-
import os
import time
import crlMod
import prxMod
import random
import cPickle

if __name__ == '__main__' :
    p = prxMod.prxMod()
    print p.Getpxylist()
    
    c = crlMod.crlMod()
    if os.path.exists('./pxylist.txt'):
        f = open(r"./pxylist.txt")
    pxylist = cPickle.load(f)
    pos = random.randrange(0, len(pxylist), 1)
    status = c.CrawlPage(pxylist[pos],1)
    if status == 0:
        print "OK"
    elif status == -1:
        print pxylist[pos]