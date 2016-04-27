#!/usr/bin/env python
from ctypes import *
import ConfigParser

dll = cdll.LoadLibrary("./cnntext/cnn_predictor.so")
dll.load_model.restype = c_void_p
dll.predict.restype = POINTER(c_float)

config = ConfigParser.ConfigParser()
config.read("./conf/cnntext.conf")

model_path = config.get('path','model_path')
setting_path = config.get('path','setting_path')
hyfile_path = config.get('path','hyfile_path')

num_of_class = config.get('para','num_of_class')
top = config.get('para','top')


class cnn:
    " CNN Predictor "
    def __init__(self):
        self.Loadmodel(model_path,setting_path,hyfile_path,num_of_class,top)
    
    def Loadmodel(self, model_filename, setting_filename,hyfile ,num_of_class,top):
        self.__model = dll.load_model(c_char_p(model_filename), c_char_p(setting_filename))
        self.__dim = int(num_of_class)
        self.__top = int(top)
        self.__hy = []
        file = open(hyfile)
        for line in file:
            self.__hy.append(line.strip().split(' ')[1])    

    def Predict(self, text):
        res = dll.predict(c_void_p(self.__model), c_char_p(text))
        # max_prob = 0
        # imax = -1
        index = sorted(range(0,self.__dim), key=lambda i: res[i],reverse=True)
        top_index = index[0:self.__top]
        prob = [str(res[i]) for i in top_index]
        label = [self.__hy[i] for i in top_index]
        result = [0] * 2 * self.__top
        result[0::2] = label
        result[1::2] = prob
        return ' '.join(result)

#if __name__ == '__main__':
    #from cnn import CNNPredictor
    #model,line = cnn(),open("/home/work/tonghan/LR_Model/test_data/test","r").readline()
    #print model.Predict(line)

