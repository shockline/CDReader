#-*- coding: gbk -*-
import crlMod
import random
import cPickle

if __name__ == '__main__' :
    c = crlMod.crlMod()
    print c.GetDesc_goose("http://data.eastmoney.com/report/20151027/APPGPfMnqWcLASearchReport.html")