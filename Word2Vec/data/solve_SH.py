#-*- coding: gbk -*-
# ========================================================
#   Copyright (C) 2014 All rights reserved.
#   
#   filename : solve_SH.py
#   author   : chendian@baidu.com
#   date     : 2016-01-22
#   desc     : Transform JSON data into Corpus_Type
# ======================================================== 

import os
import sys
import json
import common.Wordseg as Wordseg

#filename = "ReportList_sh10jqka"
filename = "Stock_Research_Report_shSinaF"
page = [line.strip() for line in file(filename)]
WriteX = open("Corpus_sh","a")
for each in page:
    contents = json.loads(each)
    #url = contents['url'].encode('utf-8')
    #title = contents['title'].encode('utf-8')
    #label = contents['rank'].encode('utf-8')
    corpuX = Wordseg.String_make_corpus(contents['Maintext'].encode('utf-8'))
    WriteX.write(corpuX + " ")
    
    #WriteX.write(url + '\t' + label + '\n')