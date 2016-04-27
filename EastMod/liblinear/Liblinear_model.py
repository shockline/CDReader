import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import codecs

import math
import numpy
from scipy import sparse
from liblinearutil import *
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("./conf/liblinear.conf")

model_path = config.get('path','model_path')
vocab_path = config.get('path','vocab_path')
stocklist_path = config.get('path','stocklist_path')
top = config.get('para','top')

class Liblinear_model:

    __vocab = {}
    __idf = []
    __stocklist = {}
    __top = 5

    def __init__(self):
        self.Loadmodel(model_path,vocab_path,stocklist_path)
        self.__top = int(top)


    def Loadmodel(self,modelfile,vocabfile,stockfile):
        infile = codecs.open(vocabfile,'rb','utf-8')
        for line in infile:
            line = line.strip().split(' ')
            self.__vocab[line[1]] = int(line[0])
            self.__idf.append(float(line[2]))
        infile.close()
        infile = open(stockfile,'rb')
        for line in infile:
            line = line.strip().split(' ')
            self.__stocklist[line[0]] = line[1]
        infile.close()
        self.__model = load_model(modelfile)


    def Predict(self, text):
        text = text.decode('utf-8')
        from sklearn.feature_extraction.text import CountVectorizer
    
        countV = CountVectorizer(vocabulary=self.__vocab)
        tf = countV.transform([text])
        tf = sparse.csr_matrix(tf.multiply(numpy.asarray(self.__idf)))
        tfidf = sparse.csr_matrix(tf/(numpy.sqrt((tf.multiply(tf)).sum(1))))
        x = {tfidf.indices[i]+1:j for i,j in enumerate(tfidf.data)}
        p_labels,p_acc,p_val = predict([0],[x],self.__model,'-b 1')
        labellist = self.__model.get_labels()
        prob = p_val[0]
        index = sorted(range(0,len(prob)), key=lambda i: prob[i],reverse=True)
        prob_5 = [str(prob[i]) for i in index[0:self.__top]]
        label_5 = [self.__stocklist['0'*(6-len(str(labellist[i])))+str(labellist[i])] for i in index[0:self.__top]]
        label_prob = [0] * self.__top * 2
        label_prob[0::2] = label_5
        label_prob[1::2] = prob_5
        return ' '.join(label_prob)


