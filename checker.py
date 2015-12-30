#! /usr/bin/env python
# coding=utf8

import json
import re
import sys

d = []
out = []
out_list = []
lines = open(sys.argv[2],"r")
values = []
for line in lines:
    if(line.strip() != ""):
        tokens = line.split()
        cmd = tokens[1].split("(")[0]
        if ( not re.match(r'[\w|\d]+',cmd)):
            continue
        values.append(cmd)

cmdPairList = []
for i in range(len(values)-1):
    cmdPairList.append((values[i],values[i+1]))
with open(sys.argv[1]) as jsonFile:
        data = json.load(jsonFile)

cmdListFromJson = []
element = {}
pair = ()
isBreak = False
models = data['model']
models.extend(data['model_augmented'])
for index,value in enumerate(models):
    if (index < len(cmdPairList)):
        if not (value['syscall_1'] == cmdPairList[index][0] and value['syscall_2'] == cmdPairList[index][1]):
            element = value
            pair = cmdPairList[index]
            isBreak = True
            break
        else:
            isBreak = True
            element = value
            break
tdict = {}
tdict["malicious"] = isBreak
tdict["syscall"] = element['syscall_1']
if element.has_key('syscall_1_arg'):
    tdict["syscall_arg"] = element['syscall_1_arg']
else:
    tdict["syscall_arg"] = None
print(json.dumps(tdict,indent=3,sort_keys=True))     
    
