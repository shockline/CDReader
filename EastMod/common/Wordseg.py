import os
import sys
import jieba

def Path_make_corpus(dirname):
    corpus = ""
    if os.path.isdir(dirname):
        filenames = os.listdir(dirname)
        for filename in filenames:
            f = open(dirname + '/' + filename, 'r')
            f_content = f.read()
            f_content = ' '.join(f_content.split())
            if f_content != ' ' or f_content != '\n' or f_content != '':
                 words_seg = jieba.lcut(f_content)
                 for i in range(len(words_seg)):
                     words_seg[i] = words_seg[i].encode('utf-8')
                 corpus = ' '.join(words_seg)
            f.close()
    return corpus


def File_make_corpus(filename):
    corpus = ""
    if os.path.isfile(filename):
        f = open(filename,'r')
        contents = f.readlines()
        for i in range(len(contents)):
            f_content = contents[i]
            if f_content != ' ' or f_content != '\n' or f_content != '':
                words_seg = jieba.lcut(f_content)
                for j in range(len(words_seg)):
                    words_seg[j] = words_seg[j].encode('utf-8')
                corpus = ' '.join(words_seg)
        f.close()
    return corpus


def String_make_corpus(text):
    corpus = ""
    if isinstance(text, basestring):
        words_seg = jieba.lcut(text)
        for i in range(len(words_seg)):
            words_seg[i] = words_seg[i].encode('utf-8')
        corpus = ' '.join(words_seg)
    return corpus


def dealWithContent(content, posDict, negDict):
    pos, neg = [], []
    for Word in content:
        if Word in posDict and Word not in pos: 
            pos.append(Word)
            continue
        if Word in negDict and Word not in neg:
            neg.append(Word)
    return " ".join(pos) + '\t' + " ".join(neg)