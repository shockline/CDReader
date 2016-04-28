# coding = utf8
# ========================================================
#   Copyright (C) 2016 All rights reserved.
#   
#   filename : structureTest_OneDocTesting.py
#   author   : okcd00 / chendian@baidu.com
#   feat     : Ganbin Zhou @ ICS_ICT
#   date     : 2016-02-12
#   desc     : python structureTest_OneDocTesting.py statistic cfh_all cfh_all average_exc_pad
# ======================================================== 


# Theano-Related Packages
import numpy
import theano
from theano import tensor as T, printing

# Machine-Learning Packages
from mlp import HiddenLayer
from logistic_sgd import LogisticRegression
from DocEmbeddingNNOneDoc import DocEmbeddingNNOneDoc
from knowledgableClassifyFlattenedLazy import CorpusReader

# Default Packages
import os
import sys
import codecs
import string
import logMod
import cPickle

l = logMod.logMod()

def work(model_name, dataset_name, pooling_mode):
    print "model_name:   ", model_name
    print "dataset_name: ", dataset_name
    print "pooling_mode: ", pooling_mode
    print "Started!"
    rng = numpy.random.RandomState(23455)
    sentenceWordCount = T.ivector("sentenceWordCount")
    corpus = T.matrix("corpus")
    docLabel = T.ivector('docLabel') 
    
    # for list-type data
    layer0 = DocEmbeddingNNOneDoc(
        corpus, 
        sentenceWordCount, 
        rng, 
        wordEmbeddingDim       = 200, 
        sentenceLayerNodesNum  = 100, 
        sentenceLayerNodesSize = [5, 200], 
        docLayerNodesNum       = 100, 
        docLayerNodesSize      = [3, 100],
        pooling_mode           = pooling_mode
    )

    layer1_output_num = 100
    layer1 = HiddenLayer(
        rng,
        input      = layer0.output,
        n_in       = layer0.outputDimension,
        n_out      = layer1_output_num,
        activation = T.tanh
    )
    
    layer2 = LogisticRegression(input = layer1.output, n_in = 100, n_out = 2)

    cost = layer2.negative_log_likelihood(1 - layer2.y_pred)
        
    # calculate sentence sentence_score
    sentence_grads = T.grad(cost, layer0.sentenceResults)
    sentence_score = T.diag(T.dot(sentence_grads, T.transpose(layer0.sentenceResults)))
    
    # calculate word sentence_score against the whole network
    word_grad  = T.grad(cost, corpus)
    word_score = T.diag(T.dot(word_grad, T.transpose(corpus)))
    
    # calculate word
    cell_scores = T.grad(cost, layer1.output)
    
    # calculate word score against cells
    word_score_against_cell = [T.diag(T.dot(T.grad(layer1.output[i], corpus), T.transpose(corpus))) for i in xrange(layer1_output_num)]

    
    # construct the parameter array.
    params = layer2.params + layer1.params + layer0.params
    
    # Load the parameters last time, optionally.
    model_path = "data/" + dataset_name + "/model_100,100,100,100,parameters/" + pooling_mode + ".model"
    loadParamsVal(model_path, params)
    
    l.Notice("Compiling computing graph. (This might be a long time, needs about 25 Mins) ")
    output_model = theano.function(
        [corpus, sentenceWordCount],
        [layer2.y_pred, sentence_score, word_score, layer1.output, cell_scores] + word_score_against_cell
    )
    l.Notice("Computing Graph Compiled")
    
    input_path = "data/" + dataset_name + "/input/"
    input_filename = input_path + "small_text"
    cr = CorpusReader(
        minDocSentenceNum  = 5, 
        minSentenceWordNum = 5, 
        dataset = input_filename
    )
    count = 0
    while(count < cr.getDocNum()):
        info = cr.getCorpus([count, count + 1])
        count += 1
        if info is None:
            l.Warning("Info is None, Pass")
            continue
        docMatrixes, _, sentenceWordNums, ids, sentences, _ = info
        docMatrixes = numpy.matrix(
            docMatrixes,
            dtype=theano.config.floatX
        )
        sentenceWordNums = numpy.array(
            sentenceWordNums,
            dtype=numpy.int32
        )
        l.Notice("start to predict: %s." % ids[0])
        info = output_model(docMatrixes, sentenceWordNums)
        pred_y, g    = info[0], info[1]
        word_scores  = info[2]
        cell_outputs = info[3]
        cell_scores  = info[4]
        word_scores_against_cell = info[5:]
        
        if len(word_scores_against_cell) != len(cell_outputs):
            l.Warning("The dimension of word_score and word are different.")
            raise Exception("The dimension of word_socre and word are different.")
        
        l.Notice("End predicting.")
        
        l.Notice("Writing resfile.")
        
        score_sentence_list = zip(g, sentences)
        score_sentence_list.sort(key = lambda x:-x[0])
        
        current_doc_dir = "data/output/" + dataset_name + "/" + str(pred_y[0]) + "/" + ids[0]
        if not os.path.exists(current_doc_dir): 
            os.makedirs(current_doc_dir)
        
        # sentence sentence_score
        with codecs.open(current_doc_dir + "/sentence_score", "w", 'utf-8', "ignore") as f:
            f .write("pred_y: %i\n" % pred_y[0])
            for g0, s in score_sentence_list:
                f.write("%f\t%s\n" % (g0, string.join(s, " ")))
    
        wordList = list()
        for s in sentences: wordList.extend(s)
        print "length of word_scores", len(word_scores)
        print "length of wordList"   , len(wordList)
        score_word_list = zip(wordList , word_scores)
        with codecs.open(current_doc_dir + "/nn_word", "w", 'utf-8', "ignore") as f:
            for word, word_score in score_word_list:
                f.write("%s\t%f\n" % (word, word_score))
        
        with codecs.open(current_doc_dir + "/nn_word_merged", "w", 'utf-8', "ignore") as f:
            merged_score_word_list = merge_kv(score_word_list)
            for word, word_score in merged_score_word_list:
                f.write("%s\t%f\n" % (word, word_score))
        
        if not os.path.exists(current_doc_dir + "/nc_word"):
            os.makedirs(current_doc_dir + "/nc_word")
        neu_num = 0
        
        for w, c_output, c_score in zip(word_scores_against_cell, cell_outputs, cell_scores):
            with codecs.open(current_doc_dir + "/nc_word/" + str(neu_num), "w", 'utf-8', "ignore") as f:
                f.write("cell sentence_score: %lf\n" % c_output)
                for word, word_score in zip(wordList, w):
                    f.write("%s\t%f\n" % (word, word_score))
            merged_score_word_list = merge_kv(zip(wordList, w))
            with codecs.open(current_doc_dir + "/nc_word/" + str(neu_num) + "_merged", "w", 'utf-8', "ignore") as f:
                f.write("cell_scores: %lf\n" % c_score)
                f.write("cell_output: %lf\n" % c_output)
                for word, word_score in merged_score_word_list:
                    f.write("%s\t%f\n" % (word, word_score))
            neu_num += 1
        l.Notice("%s Written." % str(count))
        
    print "All finished!"
    
def loadParamsVal(path, params):
    try:
        with open(path, 'rb') as f:  # open file with write-mode
            for para in params:
                para.set_value(cPickle.load(f), borrow=True)
    except:
        l.Warning("Load ParamsVal Failed.")
        pass
    
def transToTensor(data, t):
    return theano.shared(
        numpy.array(
            data,
            dtype=t
        ),
        borrow=True
    )

def merge_kv(list_to_merge):
    score_map = {}
    for item in list_to_merge:
        score_map.setdefault(item[0],0)
        score_map[item[0]] += item[1]
    merged_list = list(score_map.items())
    merged_list.sort(key=lambda x:x[1], reverse=True)
    return merged_list

if __name__ == '__main__':
    if sys.argv[1] == "statistic" :
        work(model_name=sys.argv[2], dataset_name=sys.argv[3], pooling_mode=sys.argv[4])
    elif sys.argv[1].lower() == "analyze" :
        from analyseLogFolder import analyseLogFolder
        analyseLogFolder("data/output/cfh_all")
    else :
        print "Need Arguments. For Example: \"statistic [Data] [testData] [poolingMode]\""
