# coding = utf8
# ========================================================
#   Copyright (C) 2016 All rights reserved.
#   
#   filename : structureTest_Training.py
#   author   : okcd00 / chendian@baidu.com
#   feat     : Ganbin Zhou & Ping Luo @ ICS_ICT
#   date     : 2016-02-12
#   desc     : python structureTest_Training.py train cfh_all cfh_all average_exc_pad
# ======================================================== 

# Default Packages
import os
import sys
import string
import logMod
import cPickle

# Theano-Related Packages
import numpy
import theano
from theano import tensor as T, printing
from sklearn.metrics import roc_curve, auc

# Machine-Learning Packages
from mlp import HiddenLayer
from logistic_sgd import LogisticRegression
from DocEmbeddingNN import DocEmbeddingNN
from knowledgableClassifyFlattenedLazy import CorpusReader

l = logMod.logMod()


def work(mode, data_name, test_dataname, pooling_mode="average_exc_pad"):
    print "mode_select : ", mode
    print "data_select : ", data_name
    print "pooling_mode: ", pooling_mode
    print
    l.Notice("Using Mode[%s], Data[%s], PoolingModel[%s]" % (mode, data_name, pooling_mode) )
    l.Notice("Function Work Starts.")
    rng = numpy.random.RandomState(23455)
    docSentenceCount  = T.ivector("docSentenceCount")
    sentenceWordCount = T.ivector("sentenceWordCount")
    corpus, docLabel  = T.matrix("corpus"), T.ivector('docLabel') 
    
    
    # for list-type data
    l.Notice("Start Constructing Layers.")
    layer0 = DocEmbeddingNN(
        corpus,                            
        docSentenceCount,                  
        sentenceWordCount,                 
        rng,                               
        wordEmbeddingDim       = 200,      
        sentenceLayerNodesNum  = 50,       
        sentenceLayerNodesSize = [5, 200], 
        docLayerNodesNum       = 10,       
        docLayerNodesSize      = [3, 50],  
        pooling_mode           = pooling_mode
    )

    layer1 = HiddenLayer(
        rng,                             
        input = layer0.output,           
        n_in  = layer0.outputDimension,  
        n_out = 10,                      
        activation = T.tanh
    )
    
    layer2 = LogisticRegression(
        input = layer1.output,  
        n_in  = 10,             
        n_out = 2               
    )

    # construct the parameter array.
    params = layer2.params + layer1.params + layer0.params
    
    # Load the parameters last time, optionally.
    para_path  = "data/" + data_name     + "/model/" + pooling_mode + ".model"
    traintext  = "data/" + data_name     + "/train/text"
    trainlabel = "data/" + data_name     + "/train/label"
    testtext   = "data/" + test_dataname + "/test/text"
    testlabel  = "data/" + test_dataname + "/test/label"
    
    loadParamsVal(para_path, params)

    if( mode == "train" or mode == "test" ):
        learning_rate = 0.1
        error = layer2.errors(docLabel)
        cost  = layer2.negative_log_likelihood(docLabel)
        
        grads = T.grad(cost, params)
        updates = [(param_i, param_i - learning_rate * grad_i) for param_i, grad_i in zip(params, grads)]
        
        l.Notice("Start Loading Data")
        cr_test = CorpusReader(
            minDocSentenceNum  = 5,        
            minSentenceWordNum = 5,        
            dataset            = testtext, 
            labelset           = testlabel
        )
        
        validDocMatrixes, validDocSentenceNums, validSentenceWordNums, validIds, validLabels, _, _ = cr_test.getCorpus([0, 1000])
        
        # if mode == "test" :
        #     print "Right answer: "
        #     print zip(validIds, validLabels)
        
        validDocMatrixes      = transToTensor(validDocMatrixes, theano.config.floatX)
        validLabels           = transToTensor(validLabels,           numpy.int32)
        validDocSentenceNums  = transToTensor(validDocSentenceNums,  numpy.int32)
        validSentenceWordNums = transToTensor(validSentenceWordNums, numpy.int32)
        l.Notice("Data has been loaded already")
        
        valid_model = theano.function(
            [],
            [cost, error, layer2.y_pred, docLabel, T.transpose(layer2.p_y_given_x)[1]],
            givens = {
                corpus:            validDocMatrixes,
                docSentenceCount:  validDocSentenceNums,
                sentenceWordCount: validSentenceWordNums,
                docLabel:          validLabels
            }
        )
        
        # Validate the model 
        costNum, errorNum, pred_label, real_label, pred_prob = valid_model()
        print "Valid current model:"
        print "Cost:  ", costNum
        print "Error: ", errorNum
        if mode == "test" :
            print "Valid Pred: \n", pred_label
            print "pred_prob : \n", pred_prob
        
        fpr, tpr, _ = roc_curve(real_label, pred_prob)
        if mode == "test" :
            print "tpRate_all: \n", tpr
            print "fpRate_all: \n", fpr
        roc_auc = auc(fpr, tpr)
        print "data_name:     ", data_name
        print "test_dataname: ", test_dataname
        print "ROC: ", roc_auc
        
        fpr, tpr, threshold = roc_curve(real_label, pred_label)
        
        index_of_one = list(threshold).index(1)
        ar = (tpr[index_of_one] + 1 - fpr[index_of_one]) / 2
        print "TPR: ", tpr[index_of_one]
        print "FPR: ", fpr[index_of_one]
        print "AR:  ", ar
        print "threshold: ", threshold[index_of_one]
        if mode == "test" :
            valid_model.free()
            return errorNum, roc_auc, tpr[index_of_one], fpr[index_of_one], ar
        
        l.Notice("Start Loading Training Data")
        cr_train = CorpusReader(
            minDocSentenceNum  = 5,         
            minSentenceWordNum = 5,         
            dataset            = traintext, 
            labelset           = trainlabel
        )
        
        docMatrixes, docSentenceNums, sentenceWordNums, ids, labels, _, _  = cr_train.getCorpus([0, 100000])
        
        # print "Right answer: "
        # print zip(ids, labels)
        
        docMatrixes      = transToTensor(docMatrixes, theano.config.floatX)
        labels           = transToTensor(labels,           numpy.int32)
        docSentenceNums  = transToTensor(docSentenceNums,  numpy.int32)
        sentenceWordNums = transToTensor(sentenceWordNums, numpy.int32)
        
        index, batchSize = T.lscalar("index"), 10
        n_batches = (len(docSentenceNums.get_value())  - 1 - 1) / batchSize + 1
        print
        print "Batch size         : ", batchSize
        print "Train set size     : ", len(docMatrixes.get_value())
        print "Valid set size     : ", len(validDocMatrixes.get_value())
        print "training batches   : ", n_batches
        
        l.Notice("Compiling computing graph.")
        # for list-type data
        train_model = theano.function(
            [index],
            [cost, error, layer2.y_pred, docLabel],
            updates = updates,
            givens  = {
                corpus: docMatrixes,
                docSentenceCount : docSentenceNums[index * batchSize: (index + 1) * batchSize + 1],
                sentenceWordCount: sentenceWordNums,
                docLabel: labels[index * batchSize: (index + 1) * batchSize]
            }
        )
        l.Notice("Computing Graph Compiled")
        
        l.Notice("Start Training")
        ite, epoch, n_epochs = 0, 0, 10
        while (epoch < n_epochs):
            epoch = epoch + 1
            l.Notice("Now batches at %d-th epoch." % epoch )
            for i in range(n_batches):
                # for list-type data
                costNum, errorNum, pred_label, real_label = train_model(i)
                
                # for padding data
                ite += 1
                if(ite % 10 == 0):
                    print
                    print "@iter -> %d " % ite
                    print "Cost : ", costNum
                    print "Error: ", errorNum
                    
            # Validate the model
            costNum, errorNum, pred_label, real_label, pred_prob = valid_model()
            print
            print "Current validate Model %d" % epoch
            print "Cost       : ", costNum
            print "Error      : ", errorNum
            # print "pred_prob  : \n", pred_prob
            # print "Valid Pred : \n", pred_label
            
            # False positive rate = FP/N, True positive rate = TP/P
            fpr, tpr, _ = roc_curve(real_label, pred_prob)
            
            # Receiver Operating Characteristic - Be used to rank a binary classifier
            roc_auc = auc(fpr, tpr)
            print "data_name: ", data_name
            print "test_data: ", test_dataname
            print "ROC: ", roc_auc
            print
            
            fpr, tpr, threshold = roc_curve(real_label, pred_label)
            index_of_one = list(threshold).index(1)
            print "TPR: ", tpr[index_of_one]
            print "FPR: ", fpr[index_of_one]
            print "AR = [TPR + (1-FPR)] / 2"
            print "AR:  ", (tpr[index_of_one] + 1 - fpr[index_of_one]) / 2
            print "threshold: ", threshold[index_of_one]
            
            # Save model
            l.Notice("Now Saving parameters.")
            saveParamsVal(para_path, params)
            l.Notice("Parameters Saved.")
        
        l.Notice("End Training.")        
        valid_model.free()
        train_model.free()
        
    
def saveParamsVal(path, params):
    with open(path, 'wb') as f: # open file with write-mode
        for para in params:     # serialize and save object
            cPickle.dump(para.get_value(), f, protocol = cPickle.HIGHEST_PROTOCOL)

            
def loadParamsVal(path, params):
    if(not os.path.exists(path)): return None
    try:
        with open(path, 'rb') as f:  # open file with read-mode
            for para in params:
                para.set_value(cPickle.load(f), borrow=True)
    except Exception,e: 
        l.Warning("Load ParamsVal Failed for %s" % str(e))
        pass
    
    
def transToTensor(data, t):
    return theano.shared(
        numpy.array(
            data,
            dtype = t
        ),
        borrow = True
    )
    
    
if __name__ == '__main__':
    mode = sys.argv[1]
    if len(sys.argv) > 1 : # 0/*.py  1/mode  2/data  3/test  4/pooling
        work(
            mode          = sys.argv[1].lower(), 
            data_name     = sys.argv[2], 
            test_dataname = sys.argv[3], 
            pooling_mode  = sys.argv[4]
        )
        print "All finished!"
    else : # Mode in [test, train]
        print "Need Arguments. For Example: \"mode [Data] [testData] [poolingMode]\""
