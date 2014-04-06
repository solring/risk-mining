import json

fd = open("CampbellKeywordChinese.csv", "r")
fdout = open("CampbellKeywordChinese.json", "w")
lines = fd.readlines()
fd.close()

cate = ""
#fdout.write("{\n")
flag = True

types = {}

for line in lines:
    line = line.decode('big5', 'strict')
    line = line.strip().strip(",")
    if flag:
        flag = False
        cate = line
        continue
    if line == "": # next line is the start of a catagory
        flag = True
        continue

    tokens = line.split(",")
    for t in tokens:
        if t == "": continue
        t = t.strip()
        #types[t] = cate
        outstr = "%s, %s\n" %(t, cate)
        fdout.write(outstr.encode('utf-8', 'strict'))

#fdout.write("}")
#json.dump(types, fdout, encoding='utf-8')
fdout.close()

