#! /usr/bin/env python
# coding=utf8

import json
import re
import os.path
import sys

if __name__ == "__main__":
    d = []
    out = []
    lines = open(sys.argv[1],"r")
    values = []
    #lines = lines.readlines()[:-1]
    for line in lines:
        #if(line.strip() != ""):
        if(line.strip() != ""):
            #print "Processing line : ",line
            tokens = line.split()
            cmdTokens = re.split(r'[(,)]',tokens[1])
            cmd = cmdTokens[0]
            if ( not re.match(r'[\w|\d]+',cmd)):
                #print "Ignoring : ",line
                continue

            argTokens = cmdTokens[1].split(',')
            arg0 = argTokens[0].replace('"','')
            arg = arg0
            #if re.match(r'^0x*', arg0):
            if not (re.match(r'.*\/.*',arg0)):
                arg = "NULL"
            #print "Line  Command : ",cmd," arg : ",arg
            values.append((cmd,arg))
    out_list = []
    resultDict = {}
    for i in range(len(values) - 1):
        if(len(resultDict) == 0):
            resultDict[values[i][0]+values[i][1]] = (values[i],values[i+1])
        else:
            key = values[i][0]+values[i+1][0]
            arg1 = values[i][1]
            arg2 = values[i+1][1]
            if(resultDict.has_key(key)):
                exPair = resultDict[key]
                newArg1 = os.path.commonprefix([exPair[0][1],arg1])
                newArg2 = os.path.commonprefix([exPair[1][1],arg2])
                resultDict[key] = ((values[i][0],newArg1),(values[i+1][0],newArg2))
            else:
                resultDict[key] = ((values[i][0],arg1),(values[i+1][0],arg2))
    for a in resultDict.itervalues():
        #print "Tuple : ",a
        tdict = {}
        tdict["syscall_1"] = a[0][0]
        tdict["syscall_2"] = a[1][0]
        arg0 = a[0][1]
        arg1 = a[1][1]
        if arg0 == "NULL":
            arg0 = None
        if arg1 == "NULL":
            arg1 = None
        tdict["syscall_1_arg"] = arg0
        tdict["syscall_2_arg"] = arg1
        d.append(tdict)
    print "TOtal : ",len(resultDict)
    print(json.dumps({'model': d},indent=3,sort_keys=True))
