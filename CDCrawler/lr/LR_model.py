import numpy,os
import sys

class LR_model:

    def __init__(self):
        self.__tfidfvectorizer = numpy.load('./model/LR_tfidfvectorizer')
        self.__lr = numpy.load('./model/LR_model')

    def Make_feature(self, corpus):
        tfidf = self.__tfidfvectorizer.transform(corpus)
        feature = tfidf.toarray()
        return feature

    def Predict(self, text):
        corpus = []
        corpus.append(text)
        feature = self.Make_feature(corpus)
        predict_noeng = self.__lr.predict(feature)
        probs_noeng = self.__lr.predict_proba(feature)
        probs_noeng = numpy.array(probs_noeng)
        #print 'probs ', probs_noeng
        for i in [5]:
            predict_noeng = 1 * (probs_noeng[:,1] >= i/10.)
            return str(predict_noeng).replace("[","").replace("]","")
            print 'i = ', i
            print 'predict ', predict_noeng
        print 'probs_noeng ', probs_noeng


