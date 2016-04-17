#-*- coding: gbk -*-

import os
import sys
import json
import time
import random
import cPickle
import urllib2
import ConfigParser
import crlMod # Crawl Module as crlMod.py
import prxMod # Proxy Module as prxMod.py
import logMod # Logger Module as LogMod.py

import common.Wordseg as Wordseg
import lr.LR_model as LR_model
import liblinear.Liblinear_model as Liblinear_model
import MysqlMod # MySQL Module as Mysql.py


# Global_Vars
pxylist = []
posWlist = []
negWlist = []
LastTime = -1
LastDate = "Last Recorded Date"

# Initial_Objects
s = MysqlMod.MysqlMod()
p = prxMod.prxMod()
c = crlMod.crlMod()
l = logMod.logMod()

# CONFIG SET
config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 
path_dict = config.get("path", "path_dict")
path_pxylist = config.get("path", "path_pxylist")
path_Positive = config.get("path", "path_Positive")
path_Negative = config.get("path", "path_Negative")
exec_cyctime = config.getint("para", "EXEC_CYCLETIME")

posWlist = [line.strip() for line in file(path_Positive) ]
negWlist = [line.strip() for line in file(path_Negative) ]
content = [line.strip().encode("utf-8") for line in file("./case") ]

corpuX = Wordseg.String_make_corpus(content[0])
_content = corpuX.split(' ')
label3 = Wordseg.dealWithContent(_content, posWlist, negWlist)

print "corpuX: ", corpuX
print "split: ", _content
print "label: [%s]" % label3