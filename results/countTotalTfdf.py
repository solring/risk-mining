from sys import argv
from os import listdir, path

tflist = {}
dflist = {}

if __name__=='__main__':
    for f in listdir('.'):
        if 'tf.csv' not in f: continue
        with open(f, "r") as fd:
            start = True
            for line in fd.readlines():
                if start:
                    start = False
                    continue
                tokens = line.split(',')
                word = tokens[0]
                tf = int(tokens[1])
                df = int(tokens[2])

                if word not in tflist:
                    tflist[word] = 0
                    dflist[word] = 0
                tflist[word] += tf
                dflist[word] += df
    dflist_sorted = sorted(dflist.items(), key=lambda x:x[1], reverse=True)
    tflist_sorted = sorted(tflist.items(), key=lambda x:x[1], reverse=True)

    with open("total-tf.csv", "w") as fdout:
        fdout.write("word, tf, df\n")
        for x in tflist_sorted:
            fdout.write("%s, %d, %d\n" % (x[0], x[1], dflist[x[0]]))


