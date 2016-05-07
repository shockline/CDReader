#-*- coding: gbk -*-
# ========================================================
#   Copyright (C) 2014 All rights reserved.
#   
#   filename : solve_SZ.py
#   author   : chendian@baidu.com
#   date     : 2016-01-22
#   desc     : Transform JSON data into Corpus_Type
# ======================================================== 

import os
import sys
import json
import common.Wordseg as Wordseg

#filename = "ReportList_sz10jqka"
filename = "Stock_Research_Report_szSinaF"
page = [line.strip() for line in file(filename)]
WriteX = open("Corpus_sz","a")
for each in page:
    contents = json.loads(each)
    #url = contents['url'].encode('utf-8')
    #title = contents['title'].encode('utf-8')
    #label = contents['rank'].encode('utf-8')
    corpuX = Wordseg.String_make_corpus(contents['Maintext'].encode('utf-8'))
    WriteX.write(corpuX + " ")
    
    #WriteX.write(url + '\t' + label + '\n')