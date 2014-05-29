# -*- coding: utf-8 -*-

from os import listdir, path, rename
from sys import argv

for f in listdir(argv[1]):
    tokens = path.splitext(f)
    new = tokens[0].strip()+tokens[1]
    new = new.replace(' ', '')
    new = new.replace(' ', '')
    new = new.replace('_', '')

    print "old: %s, new: %s" % (f, new)
    rename(path.join(argv[1], f), path.join(argv[1], new))
    
