from sys import argv
from os import listdir, path
import chardet
import io

def decodeFile(raw, coding, outputdir, filename):
    decoded = raw.decode(coding)
    outfile = path.join(outputdir, filename)
    with io.open(outfile, mode="w", encoding='big5', errors='ignore') as fdout:
        print type(decoded)
        fdout.write(decoded)
        #fdout.write(decoded.encode('big5', errors="ignore"))
        fdout.close()

if len(argv) < 3:
    print "usage: python detectChar.py [input dir] [output dir]"
    exit(0)

for f in listdir(argv[1]):
    if ".txt" not in f: continue
    
    filename = path.join(argv[1], f)
    with open(filename, "r") as fd:
        raw = fd.read()
        charset = chardet.detect(raw)

        if charset['encoding'] != None:
            coding = charset['encoding']
            print "%s, %s" % (f, coding)
            if coding != "Big5" and coding != "big5":
                decodeFile(raw, coding, argv[2], f)
        else:
            print "%s, %s" % (f, "None")

