# coding = utf8
# ========================================================
#   Copyright (C) 2016 All rights reserved.
#   
#   filename : checkout.py
#   author   : okcd00 / chendian@baidu.com
#   feat     : Creative Original
#   date     : 2015-05-11
#   desc     : find diff
# ======================================================== 

import os
import sys
import time

target = "z014" # "z008" / "z011" / "z014"
dict = {}


def findDiff():
    with open("Traintext_s" + target, "r") as ft:
        with open("Trainlabel_s" + target, "r") as fl:
            while True:
                a = ft.readline().split('\t')
                b = fl.readline().split('\t')
                if a[0] != b[0]:
                    print a[0],a[1], '\n', b[0],b[1]
                    a = ft.readline().split('\t')
                    b = fl.readline().split('\t')
                    print a[0],a[1], '\n', b[0],b[1]
                    break                   

def getRank():
    f = open('labels', 'r')
    for line in f.readlines(): 
        segs = line.split('\t')
        id = segs[0].strip()
        rank = segs[1].strip()
        dict[id] = rank
        
                    
def fileAnalysis(filename):
    signNum = filename.replace("Traintext_s", "")
    traintext  = "Traintext_s"  + signNum
    trainlabel = "Trainlabel_s" + signNum 
    outtext = "./s/text_s"  + signNum
    outlabel = "./s/label_s" + signNum
    with open(traintext, "r") as it:
        with open(trainlabel, "r") as il:
            with open(outtext, "w") as ot:
                with open(outlabel, "w") as ol:
                    while True:
                        linet = it.readline()
                        linel = il.readline()
                        if linet == "": break
                        irank = linel.replace(linel.split('\t')[0]+'\t', "").strip()
                        if dict.has_key(irank) and len(linet.strip().split('\t')) == 3 :
                            ot.write(linet)
                            ol.write(linel.replace(irank, dict[irank]))
                    
if __name__ == '__main__':
    getRank()
    for _, _, files in os.walk("./") :
        for filename in sorted(files) :
            if filename.startswith('Traintext_s'):
                fileAnalysis(filename)
                    