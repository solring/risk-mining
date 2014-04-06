#!/bin/python
# -*- coding: utf-8  -*-

from os import path, listdir
from sys import argv
import json
import codecs

class FileProfile:
    def __init__(self, name):
        self.name = name
        self.scores = {}
        

filelist = {}
wordlist = {}
typedict = {}
stopwords = []

DEBUG = False

def initStopword():
    stopfd = codecs.open("stopword.txt", mode="r", encoding='utf-8')
    for w in stopfd.readlines():
        stopwords.append(w.strip())
        if DEBUG == True: print w
    stopfd.close()

def initTypedict():
    typefd = codecs.open("CampbellKeywordChinese.csv", mode="r", encoding='utf-8')
    for line in typefd.readlines():
        token = line.strip().split(",")
        typedict[token[0].strip()] = token[1].strip()
        if DEBUG == True: print token[0]
    typefd.close

def parsetexts(f):
    print "in parsetexts: %s" % f
    filelist[f] = FileProfile(f)

    fd = codecs.open(f, encoding='big5', mode='r')
    content = fd.read()
    # content = content.decode('big5', 'ignore')
    tokens = content.strip().split("　".decode('utf-8', 'strict'))
    
    for t in tokens:
        k = t.split("(")[0] # get the word

        if k in stopwords: 
            print 'stopword: %s' % k
            continue # filter out stopwords

        if k not in wordlist:   # count words
            wordlist[k] = 0
        wordlist[k] += 1
        
        if k in typedict:   # check if the word is in the target list
            tp = typedict[k]
            print "get word: %s - type: %s" % (k, tp)
            if tp not in filelist[f].scores:
                filelist[f].scores[tp] = 0
            filelist[f].scores[tp] += 1
        else:
            print "get word: "+k

    print "---------- scores of file %s ---------" % f 
    for key, item in filelist[f].scores.items():
        print "type %s: %d" %(key, item)


if __name__ == "__main__":
    
    if len(argv) < 2:
        print "usage: python countwords.py [input dir] [output file]"
        exit(0)
    
    initStopword()

    initTypedict()
        
    for f in listdir(argv[1]):
        if f[0] == '.': continue
        print "to parse: %s" % f
        parsetexts(path.join(argv[1], f))
    
    print "=============== word rank ============="
    print " total # of unique words: %d" % len(wordlist)
    print "======================================="
    count = 0
    for key, value in sorted(wordlist.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        # if count > 20: break
        print "%s : %d" %(key, value)
        count += 1
