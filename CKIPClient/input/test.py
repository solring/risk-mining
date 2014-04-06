from os import listdir, path
import codecs

for f in listdir("."):
    print f
    if f[0] == '.': continue
    with codecs.open(f, mode="r", encoding='big5') as fd:
        for line in fd.readlines():
            print line
            # print line.decode('big5', 'strict')
        print "------------"
