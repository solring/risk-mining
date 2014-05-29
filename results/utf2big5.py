from os import listdir, path
import io
import chardet

if __name__=="__main__":
    for f in listdir("."):
        if ".csv" not in f: continue
        print "file: "+f
        with open(f, "r") as fd:
            content = fd.read()
            charset = chardet.detect(content)
            print "charset: %s" % charset['encoding']

            content = content.decode(charset['encoding'], errors='ignore')
            print "type of content: %s" % type(content)

            with open(f+".big5", "w") as fdout:
                fdout.write(content.encode('big5', errors='ignore'))
                fdout.close()
            
            fd.close()


