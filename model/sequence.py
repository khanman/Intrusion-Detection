#! /usr/bin/env python
# coding=utf8
import json
import re
import os.path
import sys

d = []
out = []
out_list = []
lines = open(sys.argv[1],"r")
values = []
for line in lines:
    if(line.strip() != ""):
        tokens = line.split()
        cmd = tokens[1].split("(")[0]
        if ( not re.match(r'[\w|\d]+',cmd)):
            #print "Ignoring : ",line
            continue
        values.append(cmd)
for i in range(len(values) - 2):
    outputTuple = (values[i],values[i+1])
    out.append(outputTuple)
for i in out:
    if i not in out_list:
        out_list.append(i)
for a in out_list:
    tdict = {}
    tdict["syscall_1"] = a[0]
    tdict["syscall_2"] = a[1]
    d.append(tdict)
print(json.dumps({'model': d},indent=3,sort_keys=True))                
