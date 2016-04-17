#-*- coding: gbk -*-
import crlMod
import random
import cPickle

if __name__ == '__main__' :
    p = crlMod.crlMod()
    f = open(r"./pxylist.txt")
    pxylist = cPickle.load(f)
    pos = random.randrange(0, len(pxylist), 1)
    status = p.CrawlPage(pxylist[pos],1)
    if status == 0:
        print "OK"
    elif status == -1:
        print pxylist[pos]