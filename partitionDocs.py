from os import path, listdir, mkdir
from sys import argv 
import re

p = "<(.*?)>"
reg = re.compile(p)

buf = []
outcount = 0

taglist = ["rm", "rate", "techindustry", "investment", "expansion",
            "purchsales", "rd", "image", "shares", "merge",
            "manage", "rule", "lawsuit", "else", "crisis", "other"]

def outputResult2(state, filename, outputdir, content):
    global outcount
    prefix = filename.split(".")[0]
    outfilename = path.join(outputdir, "%s_%s.txt" %(prefix, state))
    #print "output file name: " + outfilename
    with open(outfilename, "w") as fdout:
        fdout.write(content)
        fdout.close()
        outcount += 1

def outputResult(state, filename, outputdir): # filename: XXX.txt
    
    global outcount
    prefix = filename.split(".")[0]
    outfilename = path.join(outputdir, "%s_%s.txt" %(prefix, state))
    #print "output file name: " + outfilename
    with open(outfilename, "w") as fdout:
        for line in buf:
            fdout.write(line)
        fdout.close()
        outcount += 1
    del buf[:]
        

def partitionFile(filename, localname, outputdir): # filename: [input path]/XXX.txt , localname: XXX.txt
    state = ""
    newstate = ""

    with open(filename, "r") as fd:

        content = fd.read()
        for tag in taglist:
            tokens = content.split('<%s>' % tag)
            print "tag: %s, len: %d" % (tag, len(tokens))
            if len(tokens) > 1: 
                #print tokens[1]
                outputResult2(tag, localname, outputdir, tokens[1])
'''
        for line in fd.readlines():
            print line
            m = reg.match(line.strip())
            if m != None:
                newstate = m.group(1)
                print "newstate: "+newstate
                tokens = line.split("<"+state+">")
                if tokens:
                    buf.append(tokens[-1])
                if state == newstate:
                    print "------ output: "+state
                    outputResult(state, localname, outputdir)
                    
                state = newstate
                
            else:
                buf.append(line)
        if len(buf) > 0: outputResult(state, localname, outputdir)
'''
if __name__ == "__main__":
    if len(argv) < 2:
        print "usage: python partitionDocs.py [input dir] [output dir]"
        exit(0)
     
    if path.exists(argv[1]) == False:
        print "Input file not exist."
        exit(0)
    outcount = 0
    count = 0
    for f in listdir(argv[1]):
        if ".txt" not in f: continue

        obsname = path.join(argv[1], f)
        
        if path.exists(argv[2]) == False: mkdir(argv[2])
        
        if( path.isfile(obsname) ):
            print "process file " + obsname
            partitionFile(obsname, f, argv[2])
            count += 1
        else:
            print "ERROR: skip " + obsname

    print "finish. number of files processed: %d/%d" %(count, outcount)
