# -*- coding: utf-8  -*-

import requests
import re
from os import listdir, path
from sys import argv
from StringIO import StringIO

root = "http://sunlight.iis.sinica.edu.tw"
url = "http://sunlight.iis.sinica.edu.tw/cgi-bin/text.cgi"

pattern = "URL=\'(.*?)\'"
reg = re.compile(pattern)

if __name__ == "__main__":
    
    if len(argv) < 2:
        print "usage: python CPIKcrawler.py [inputdir] [outputdir]"
        exit(0)
    
    query = "中文輸入".decode('utf8')
    payload = {'query': query.encode('big5'), 'Submit': "送出".decode('utf8').encode('big5')}
    res = requests.post(url, data=payload)
    print "status code: %d" % res.status_code
    
    m = reg.match(res.content)
    if m != None:
        newurl = root + m.group(1)
        print "new url: " + newurl

    
'''
    for f in listdir(argv[1]):
        filename = path.join(argv[1], f)
        print "file: " + f
        with open(filename, "r") as fd:
            query = fd.read()
            payload = {'query': query, 'Submit': "送出".decode('utf8').encode('big5')}
            res = requests.post(url, data=payload)
            print "status code: " + res.status_code
'''
            #with open(StringIO(res.contents))


