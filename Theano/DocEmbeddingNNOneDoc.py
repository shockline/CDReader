# coding = utf8
# ========================================================
#   Copyright (C) 2016 All rights reserved.
#   
#   filename : DocEmbeddingNNOneDoc.py
#   author   : okcd00 / chendian@baidu.com
#   feat     : Theano Inc. @ Github & Ganbin Zhou @ ICS_ICT
#   date     : 2016-01-25
#   desc     : Document Embedding Neural Networks For One Document
# ======================================================== 

import numpy
import theano
import theano.tensor.signal.downsample as downsample
import theano.tensor.signal.conv as conv
from theano import tensor as T, printing

class DocEmbeddingNNOneDoc:
    
    def __init__(
        self,
        corpus,
        sentenceWordCount,
        rng,
        wordEmbeddingDim,
        sentenceLayerNodesNum          = 2,
        sentenceLayerNodesSize         = (2, 2),
        docLayerNodesNum               = 2,
        docLayerNodesSize              = (2, 3),
        datatype                       = theano.config.floatX,
        pooling_mode                   = "average_exc_pad"
    ):
        self.__wordEmbeddingDim = wordEmbeddingDim
        self.__sentenceLayerNodesNum = sentenceLayerNodesNum
        self.__sentenceLayerNodesSize = sentenceLayerNodesSize
        self.__docLayerNodesNum = docLayerNodesNum
        self.__docLayerNodesSize = docLayerNodesSize
        self.__WBound = 0.2
        self.__MAXDIM = 10000
        self.__datatype = datatype
        self.sentenceW = None
        self.sentenceB = None
        self.docW = None
        self.docB = None
        self.__pooling_mode = pooling_mode
        
        # For  DomEmbeddingNN optimizer.
        # self.shareRandge = T.arange(maxRandge)
        
        # Get sentence layer W
        self.sentenceW = theano.shared(
            numpy.asarray(
                rng.uniform(low = -self.__WBound, high = self.__WBound, size = (self.__sentenceLayerNodesNum, self.__sentenceLayerNodesSize[0], self.__sentenceLayerNodesSize[1])),
                dtype = datatype
            ),
            borrow=True
        )
        # Get sentence layer b
        sentenceB0     = numpy.zeros((sentenceLayerNodesNum,), dtype = datatype)
        self.sentenceB = theano.shared(value = sentenceB0, borrow = True)
        
        # Get doc layer W
        self.docW = theano.shared(
            numpy.asarray(
                rng.uniform(low = -self.__WBound, high = self.__WBound, size = (self.__docLayerNodesNum, self.__docLayerNodesSize[0], self.__docLayerNodesSize[1])),
                dtype = datatype
            ),
            borrow = True
        )
        # Get doc layer b
        docB0 = numpy.zeros((docLayerNodesNum,), dtype = datatype)
        self.docB = theano.shared(value = docB0, borrow=True)
        
        self.sentenceResults, _ = theano.scan(
            fn            = self.__dealWithSentence,
            non_sequences = [corpus, self.sentenceW, self.sentenceB],
            sequences     = [dict(input=sentenceWordCount, taps=[-1, -0])],
            strict        = True
        )
        

        doc_out = conv.conv2d(input=self.sentenceResults, filters=self.docW)
        docPool = downsample.max_pool_2d(
            doc_out, 
            (self.__MAXDIM, 1), 
            mode = self.__pooling_mode, 
            ignore_border = False
        )
        docOutput = T.tanh(docPool + self.docB.dimshuffle([0, 'x', 'x']))
        self.output = docOutput.flatten(1)
        
        self.params = [self.sentenceW, self.sentenceB, self.docW, self.docB]
        self.outputDimension = self.__docLayerNodesNum * \
        (self.__sentenceLayerNodesNum * (self.__wordEmbeddingDim - self.__sentenceLayerNodesSize[1] + 1) - \
         self.__docLayerNodesSize[1] + 1)
   
    
    def __dealWithSentence(self, sentenceWordCount0, sentenceWordCount1, docs, sentenceW, sentenceB):
        # t = T.and_((shareRandge < sentenceWordCount1), (shareRandge >= sentenceWordCount0)).nonzero()
        sentence = docs[sentenceWordCount0:sentenceWordCount1]
        
        sentence_out = conv.conv2d(input=sentence, filters=sentenceW)
        sentence_pool = downsample.max_pool_2d(sentence_out, (self.__MAXDIM, 1), mode=self.__pooling_mode, ignore_border=False)
        
        sentence_output = T.tanh(sentence_pool + sentenceB.dimshuffle([0, 'x', 'x']))
        sentence_embedding = sentence_output.flatten(1)
        return sentence_embedding
