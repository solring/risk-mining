from os import path, listdir 
from sys import argv, getfilesystemencoding 
import chardet
import re
import json
import io

DEBUG = False

typemapping = { "Financial":"Fin", 
                "Idiosyncratic":"Idio", 
                "Systematic":"Sys", 
                "Legal & Regulatory":"Legal", 
                "Tax":"Tax"}
taglist = ["rm", "rate", "techindustry", "investment", "expansion",
            "purchsales", "rd", "image", "shares", "merge",
            "manage", "rule", "lawsuit", "else", "crisis", "other"]

class TagProfile:   # information tuple for tags
    def __init__(self):
        self.total = 0
        self.totalkwd = 0
        self.typecounts = {}
        for c in typemapping.itervalues():
            self.typecounts[c] = 0

class FileProfile:
    def __init__(self, name):
        self.name = name
        self.total = 0
        self.totalkwd = 0
        self.typecounts = {}
        for c in typemapping.itervalues():
            self.typecounts[c] = 0
        self.tags = {}
        

filelist = {}
#wordlist = {}
typedict = {}
tf = {}
df = {}

def outputResult(dirname):

    with io.open( dirname+".csv", mode="w", encoding="big5") as fd:

        # headers
        fd.write(u'filename, totalwords, totalkwds, ')
        for c in typemapping.itervalues():
            fd.write(c+u', ')
        
        for tag in taglist:
            fd.write(tag+u"_totalwords, "+tag+u"_totalkwds, ")
            for c in typemapping.itervalues():
                fd.write(u"%s_%s, " % (tag, c))
            
        fd.write(u"\n")

        # for every files
        for f, profile in filelist.iteritems():
            fd.write(u"%s, %d, %d, " % (f.decode(getfilesystemencoding()), profile.total, profile.totalkwd) )
            for c in typemapping.itervalues():
                fd.write(u"%s, " % profile.typecounts[c])
            
            for tag in taglist:
                if tag in profile.tags:
                    prof = profile.tags[tag]
                    fd.write(u"%d, %d, " % (prof.total, prof.totalkwd))
                    for c in typemapping.itervalues():
                        fd.write(u"%s, " % prof.typecounts[c])
                else:
                    fd.write(u"0, 0, 0, 0, 0, 0, 0, ")
                
            fd.write(u"\n")

        fd.close()

    with io.open( dirname+"-tf.csv", mode="w", encoding="utf8") as fd:
        tf_sorted = sorted(tf.items(), key=lambda x:x[1], reverse=True)
        for t in tf_sorted:
            fd.write("%s, %d, %d\n" %(t[0], t[1], df[t[0]]))

def parsetexts(filename, mainfile, tag):

    if mainfile not in filelist: 
        filelist[mainfile] = FileProfile(mainfile)
    if tag not in filelist[mainfile].tags: 
        filelist[mainfile].tags[tag] = TagProfile()
    
    tp = filelist[mainfile].tags[tag]
    fp = filelist[mainfile]

    fd = open(filename, "r")
    raw = fd.read()  # read entire file
    if raw == None or len(raw) == 0: return

    # detect encoging
    charset = chardet.detect(raw)
    if DEBUG : print "encoding = %s" % charset['encoding']
    if charset['encoding'] == None:
        print "ERROR: cannot decode"
        return

    content = raw.decode(charset['encoding'], errors='ignore')
    tp.total = len(content)
    fp.total += tp.total

    for keyword, category in typedict.iteritems():

        #print "content type: %s" % type(content)
        #print "kwd type: %s" % type(keyword)
        if keyword in content: 
            if DEBUG: print "------------------------- HIT!!"
            count = content.count(keyword)
            
            # count words
            if count > 0:
                df[keyword] += 1
                tf[keyword] += count
                fp.totalkwd += count
                tp.totalkwd += count

            abbr = typemapping[category]    # abbreviation of category
            if DEBUG: print "keyword: %s, cate: %s, count: %d" %(keyword, abbr, count)

            if abbr not in fp.typecounts: fp.typecounts[abbr] = 0
            fp.typecounts[abbr] += count
        
            if abbr not in tp.typecounts: tp.typecounts[abbr] = 0
            tp.typecounts[abbr] += count


if __name__ == "__main__":
    
    if len(argv) < 1:
        print "usage: python countwords.py [input dir]"
        exit(0)
    
    # Load CampbellKeyworkChinese as a dictionary
    with open("CampbellKeyworkChinese.json", "r") as typefd:
        types = json.load(typefd, encoding='utf8')
        for t in types:
            typedict[t["word"]] = t["category"]
            tf[t["word"]] = 0
            df[t["word"]] = 0
    if DEBUG:
        for k, v in typedict.iteritems(): print "%s, %s" % (k, v)

    for f in listdir(argv[1]):

        if ".txt" not in f: continue

        filename = path.join(argv[1], f)
        if( path.isfile(filename) ):
            mainfile = f.split("_")[0]
            tag = f.split("_")[1][:-4]
            print "main: %s, tag: %s" %(mainfile, tag)
            parsetexts(filename, mainfile, tag)
    
    outputResult(path.dirname(argv[1]))
