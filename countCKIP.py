# -*- coding:utf-8 -*-

from sys import argv
from os import listdir, path
import chardet
import re

pattern = " (.*?)\(.*?\) "
reg = re.compile(pattern)

if len(argv) < 2:
    exit(0)

preserve = [u'稅', u'鋼', u'金', u'銀', u'銅', u'鈷', u'鎳', u'煤', u'鋰', u'鋅']
wordlist = {}
stopwords = []
out_encoding = argv[2]

# stop word list
with open("stopword.txt", "r") as fdstop:
    content = fdstop.read()
    charset = chardet.detect(content)
    print "stopword charset: %s" % charset['encoding']    
    for line in content.decode(charset['encoding']).split(u'\n'):
        w = line.strip()
        stopwords.append(w)

for f in listdir(argv[1]):
    if ".txt" not in f: continue
    print "----- file %s -----" % f
    filename = path.join(argv[1], f)
    with open(filename, "r") as fd:
        content = fd.read()
        for m in re.finditer(pattern, content):
            word = m.group(0)
            if word in stopwords: continue
            if len(word) <= 1:
                if word not in preserve: continue

            print "get: %s" % word.encode('utf8')
            if word not in wordlist:
                wordlist[word] = 0
            wordlist[word] += 1
'''
        for line in fd.readlines(): 
            tokens = line.decode('big5').strip().split(u' ')

            for t in tokens:
                word = ""
            
                tokens2 = t.split(u'(')
                if len(tokens2) > 1: word = tokens2[0]

                if word in stopwords: continue
                if len(word) <= 1:
                    if word not in preserve: continue

                print "get: %s" % word.encode('utf8')
                if word not in wordlist:
                    wordlist[word] = 0
                wordlist[word] += 1

'''                

outfile = path.join(argv[1], "ckipwordcount-%s.csv" % out_encoding)
with open(outfile, "w") as fdout:
    
    fdout.write("word, count\n")
    list_sorted = sorted(wordlist.items(), key=lambda x:x[1], reverse=True)
    for w in list_sorted:
        fdout.write("%s, %d\n" % (w[0].encode(out_encoding), w[1]))

       

