# -*- coding: utf-8 -*-
# ========================================================
#   Copyright (C) 2016 All rights reserved.
#   
#   filename : knoweagebleClassifyFlattenedLazy
#   author   : Ganbin Zhou @ ICS_ICT
#   feat     : okcd00 / chendian@baidu.com
#   date     : 2016-02-12
#   desc     : CorpusReader Demo Modules
# ======================================================== 

import os
import codecs
import string
import theano
import cPickle
import numpy as np
from codecs import decode

import ConfigParser
config = ConfigParser.ConfigParser()  
config.read("./conf/Basic.conf") 

# CONFIG SET
path_w2v = config.get("path", "path_w2v")
path_word2vec = config.get("path", "path_word2vec")
path_stopword = config.get("path", "path_stopword")
path_cdpickle = config.get("path", "path_cdpickle")

import logMod
l = logMod.logMod()

class CorpusReader:
    def __init__(self, minDocSentenceNum, minSentenceWordNum, dataset=None, labelset=None):
        self.minDocSentenceNum = minDocSentenceNum
        self.minSentenceWordNum = minSentenceWordNum
        
        """
        self.__pos_vectors = dict()
        for pos, index in self.__posDict.items():
            tmp = [0] * len(self.__posDict)
            tmp[index] = 1
            self.__pos_vectors[pos] = tmp
        """
        
        # Load labels
        if(labelset is not None):
            self.labels, self.labelsList = loadLabels(labelset)
            l.Notice("%d Labels Loaded " % len(self.labels) )
        else:
            self.labels = None
            
        # Load documents
        if(dataset is not None):
            self.docs, self.docIdList = loadDocuments(dataset, "utf-8")
            l.Notice("%d Documents Loaded " % len(self.docs) )
        else:
            self.docs = None
            l.Warning("Load Documents ERROR")
        
        # Load stop words
        if CorpusReader.stopwords is None:
            CorpusReader.stopwords = loadStopwords(path_stopword, "utf-8")
            l.Notice("%d Stop-Words Loaded " % len(self.stopwords) )
        
        # Load w2v model data from file
        if CorpusReader.w2vDict is None:
            CorpusReader.w2vDict = loadW2vModel(path_w2v)
            l.Notice("w2v model Loaded, contains: %d elements" % len(self.w2vDict) )
        
    docs      = None 
    labels    = None
    w2vDict   = None
    stopwords = None

    minDocSentenceNum  = 0
    minSentenceWordNum = 0
    __wordDim = 200
    __zeroWordVector = [0] * __wordDim
    
    __posDict = {
        "Ag":0,     "Bg":1,     "Dg":2,     "Mg":3,     "Ng":4,     "Qg":5,     "Rg":6,     
        "Tg":7,     "Vg":8,     "Yg":9,     "a":10,     "ad":11,    "an":12,    "b":13,     
        "c":14,     "d":15,     "e":16,     "email":17, "f":18,     "h":19,     "i":20,     
        "j":21,     "k":22,     "l":23,     "m":24,     "n":25,     "nr":26,    "nrf":27,   
        "nrg":28,   "ns":29,    "nt":30,    "nx":31,    "nz":32,    "o":33,     "p":34,     
        "q":35,     "r":36,     "s":37,     "t":38,     "tele":39,  "u":40,     "v":41,     
        "vd":42,    "vn":43,    "w":44,     "www":45,   "x":46,     "y":47,     "z":48    
    }
    
    def getDocNum(self):
        if self.labels is None: return len(self.docs)
        else:                   return len(self.labels)
    
    def getDim(self):
        return self.__wordDim
    
    def getVec(self, word):
        if self.w2vDict.has_key(word):
            return self.w2vDict[word]
        else : return self.w2vDict["UNK"]
    
    def __sentence2Matrix(self, wordList):
        
        sentenceMatrix = map(lambda word: (self.getVec(word[0]), word[0]) if (word[0] in self.w2vDict) else None, wordList)
        
        sentenceMatrix = filter(lambda item: not item is None, sentenceMatrix)
        
        sentenceWordNum = len(sentenceMatrix)
        if(sentenceWordNum < self.minSentenceWordNum): return None
        
        sentenceMatrix, wordList = zip(*sentenceMatrix)
        
        sentenceMatrix = list(sentenceMatrix)
        wordList       = list(wordList)

        return (sentenceMatrix, sentenceWordNum, wordList)
    
    def __doc2Matrix(self, e):
        (docIdStr, label) = e
        wordList = self.docs[docIdStr]
        mapL = lambda e: e[1] if (u"\u3000" in e[0] or u"。" in e[0] or u"，" in e[0] or u"." in e[0] or u"," in e[0]) else None
        t = map(mapL, zip(wordList, range(len(wordList))))
        t = [-1] + filter(None, t) + [len(wordList)]
        m = map(lambda i:  self.__sentence2Matrix(wordList[i[0] + 1:i[1]]) if(i[1] - i[0] > self.minSentenceWordNum + 1) else None , zip(t[:-1], t[1:]))
        m = filter(lambda item: not item is None, m)
        
        if(len(m) == 0): 
            l.Notice("Length of map is Zero")
            return None
        docMatrix, sentenceWordNum, wordListList = zip(*m)
        docMatrix = list(docMatrix)
        sentenceWordNum = list(sentenceWordNum)
        wordListList = list(wordListList)
        
        docSentenceNum = len(docMatrix)
        if(docSentenceNum < self.minDocSentenceNum): 
            l.Notice("docSentenceNum < self.minDocSentenceNum value at %s/%s" % (str(docSentenceNum), str(self.minDocSentenceNum)) )
            return None
        
        # Merge the sentence embedding into a holistic list.
        docMatrix = reduce(add, docMatrix, [])
        
        return (docMatrix, docSentenceNum, sentenceWordNum, docIdStr, label, wordListList)
    
    def __getDataMatrix(self, scope):
        scope[1] = np.min([scope[1], len(self.labels)])
        if(scope[0] < 0 or scope[0] >= scope[1]): return None
#         batch = self.labelsList[scope[0]:scope[1]]
        batch   = self.labels.items()[scope[0]:scope[1]]
        docInfo = map(self.__doc2Matrix, batch)
        
        if(len(docInfo) == 0):
            l.Notice( "Lost doc: " + str(self.labels.items()[scope[0]:scope[1]]) )
            return None
        
        try : 
            # print docInfo
            docInfo = filter(None, docInfo)
            # print docInfo
        except Exception,e : l.Warning("filter ERROR for %s" % str(e))
        
        if(len(docInfo) == 0): 
            return None
        
        docMatrixes, docSentenceNums, sentenceWordNums, ids, labels, wordListList = zip(*docInfo)
        
        # Merge the sentence embedding into a holistic list.
        docMatrixes      = reduce(add, docMatrixes,      [])
        wordListList     = reduce(add, wordListList,     [])
        sentenceWordNums = reduce(add, sentenceWordNums, [])
        
        docSentenceNums  = [0] + list(docSentenceNums)
        sentenceWordNums = [0] + sentenceWordNums
        
        docSentenceNums  = np.cumsum(docSentenceNums)
        sentenceWordNums = np.cumsum(sentenceWordNums)
        
        #   print docSentenceNums
        #   print sentenceWordNums
        return (docMatrixes, docSentenceNums, sentenceWordNums, ids, labels, wordListList)
    
    def __getDataMatrixNoLabel(self, scope):
        scope[1] = np.min([scope[1], len(self.docs)])
        if(scope[0] < 0 or scope[0] >= scope[1]): return None
        
        ids = self.docIdList[scope[0]:scope[1]]
        batch = zip(ids, ids) # zip(A,B) = {(Ai,Bi)}
        docInfo = map(self.__doc2Matrix, batch)
        
        if(len(docInfo) == 0):
            l.Notice("Lost doc: " + str(self.labels.items()[scope[0]:scope[1]]))
            return None
        
        docInfo = filter(None, docInfo)
        if(len(docInfo) == 0): 
            return None
        
        docMatrixes, docSentenceNums, sentenceWordNums, ids, _, wordListList = zip(*docInfo)
        # docMatrixes, docSentenceNums, sentenceWordNums, ids, _, wordListList = zip(*docInfo)
        
        # Merge the sentence embedding into a holistic list.
        docMatrixes = reduce(add, docMatrixes, [])
        sentenceWordNums = reduce(add, sentenceWordNums, [])
        wordListList = reduce(add, wordListList, [])
        
        l.Notice("Already Merged the sentence embedding into a holistic list.")
        
        docSentenceNums  = [0] + list(docSentenceNums)
        sentenceWordNums = [0] + sentenceWordNums
        
        docSentenceNums  = np.cumsum(docSentenceNums)
        sentenceWordNums = np.cumsum(sentenceWordNums)
        
        return (docMatrixes, docSentenceNums, sentenceWordNums, ids, wordListList)
    
    def __findBoarder(self, docSentenceCount, sentenceWordCount):
        maxDocSentenceNum  = np.max(docSentenceCount)
        maxSentenceWordNum = np.max(np.max(sentenceWordCount))
        return maxDocSentenceNum, maxSentenceWordNum
    
    # Only positive scope numbers are legal.
    def getCorpus(self, scope):
        # docMatrixes, docSentenceNums, sentenceWordNums, labels = self.__getDataMatrix(scope)
        if(self.labels is not None):
            corpusInfo = self.__getDataMatrix(scope)
            l.Notice("getCorpus at getDataMatrix()")
        else:
            corpusInfo = self.__getDataMatrixNoLabel(scope)
            l.Notice("getCorpus at getDataMatrixNoLabel()")
        return corpusInfo

def add(a, b):
    return a + b

def loadDocuments(filename, charset="utf-8"):
    f = open(filename, "r")
    docList  = dict()
    docIdList = list()
    for line0 in f:
        try:
            line = decode(line0, charset, 'ignore')
        except: 
            l.Warning("Decode Error %s" % line)
            continue
        try:
            tokens  = line.strip().split("\t")
            idStr   = tokens[0]
            title   = tokens[1]
            content = tokens[2]
            wordData = getWords(title) + getWords(content)
        except Exception,e:
            l.Warning("[%s] Ignored for %s\n%s" % (str(idStr), str(e), str(line) ) )
            continue

        docList[idStr] = wordData
        docIdList.append(idStr)
    f.close()
    return (docList, docIdList)

def getWords(wordsStr):
    def dealword(word):
        word = word.strip()
        if(":" in word):
            return (word[:word.rfind(":")], word[word.rfind(":") + 1:])
        else:
            # print "Word %s has no POS." % word
            return (word)
    # t = filter(lambda word: len(word) > 1 and ":" in word and word.strip()[0] != ':', wordsStr.split(" "))
    t = filter(lambda word: len(word) > 1, wordsStr.split(" "))
    return map(dealword, t)

def loadLabels(filename, charset="utf-8"):
    f = codecs.open(filename, "r", charset, "ignore")
    labels = dict()
    labelsList = list()
    for line in f:
        if(not "\t" in line): continue
        (k, v) = line.strip().split("\t")
        labels[k] = string.atof(v)
        labelsList.append((k, v))
    f.close()
    return (labels, labelsList)

def loadStopwords(filename, charset="utf-8"):
    f = codecs.open(filename, "r", charset, "ignore")
    d = set()
    for line in f :
        d.add(line)
    f.close()
    return d

def loadW2vModel(filename, charset="utf-8"):
    d = dict()
    if os.path.exists(path_cdpickle):
        with open(path_cdpickle, 'rb+') as cf: 
            d = cPickle.load(cf)
        vec_unk = [0.0] * 200
        d["UNK"] = np.array(vec_unk, dtype = theano.config.floatX)
    else:
        f = codecs.open(filename, "r", charset)
        for line in f :
            try:
                data = line.strip().split(" ")
                word = data[0]
                #vec = [string.atof(s) for s in data[1:]]
                vec = []
                for s in data[1:]:
                    try : vec.append(string.atof(s))
                    except Exception,e : l.Warning("W2V Data-Error with [%s]%s" % ( str(word), str(s) ) )
                d[word] = np.array(vec, dtype = theano.config.floatX)
            except Exception,e:
                l.Warning("Loadw2v wrong with [%s]%s" % ( str(word), str(e) ) )
        f.close()
        with open(path_cdpickle, 'wb+') as cf: 
            cPickle.dump(d, cf, protocol = cPickle.HIGHEST_PROTOCOL)
    return d
