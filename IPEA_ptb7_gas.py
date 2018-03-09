#!/usr/bin/env python

import numpy
import sys
import os.path


def parse(fname):
    f = open(fname)
    line = f.readline()
    while len(line) != 0:
            
        line = f.readline()

        if "Total energy" in line:
            #print line
            return float(line.split()[-1])
    return 0

results = open("/work/akohn/projects/ptb7/qm/gas_IPEA.txt", "w")

results.write("ID\t\t\tEA\tIP\n")
layer1IP = 0.0
layer1EA = 0.0
layer1num = 0.0
layer2IP = 0.0
layer2EA = 0.0
layer2num = 0.0
layer3IP = 0.0
layer3EA = 0.0
layer3num = 0.0
layer4IP = 0.0
layer4EA = 0.0
layer4num = 0.0


for i in os.listdir('/work/akohn/projects/ptb7/qm/gas/ptb7/neutral'):
    #print i
    groundTarget = "/work/akohn/projects/ptb7/qm/gas/ptb7/neutral/" + i + "/" + i + ".out"
    catTarget = groundTarget.replace("neutral", "cation")
    anTarget = groundTarget.replace("neutral", "anion")
    if not os.path.isfile(groundTarget) or not os.path.isfile(catTarget) or not os.path.isfile(anTarget):
        continue
   
    if "Total energy in the final basis set" not in open(groundTarget).read() or "Total energy in the final basis set" not in open(catTarget).read() or "Total energy in the final basis set" not in open(anTarget).read():
        continue
    #print "My target is" + groundTarget
    neutE = parse(groundTarget)
    catE = parse(catTarget)
    anE = parse(anTarget)

    IP = 27.2114 * (catE - neutE)
    EA = 27.2114 * (neutE - anE)
    molStr = i[5:7]
    if molStr[1] == ".":
        molNum = int(molStr[0])
    else:
        molNum = int(molStr)

    if molNum == 1 or molNum == 9 or molNum == 17 or molNum == 8 or molNum == 16 or molNum == 24:
        layer1IP += IP
        layer1EA += EA
        layer1num += 1
    if molNum == 2 or molNum == 10 or molNum == 18 or molNum == 7 or molNum == 15 or molNum == 23:
        layer2IP += IP
        layer2EA += EA
        layer2num += 1
    if molNum == 3 or molNum == 11 or molNum == 19 or molNum == 6 or molNum == 14 or molNum == 22:
        layer3IP += IP
        layer3EA += EA
        layer3num += 1
    if molNum == 4 or molNum == 12 or molNum == 20 or molNum == 5 or molNum == 13 or molNum == 21:
        layer4IP += IP
        layer4EA += EA
        layer4num += 1



    results.write(str(molNum) + "\t\t" + str(EA) + "\t\t\t" + str(IP) + "\n")

results.write("L1avgIP\t" + str(layer1IP/layer1num) + "\n")
results.write("L1avgEA\t" + str(layer1EA/layer1num) + "\n")
results.write("L2avgIP\t" + str(layer2IP/layer2num) + "\n")
results.write("L2avgEA\t" + str(layer2EA/layer2num) + "\n")
results.write("L3avgIP\t" + str(layer3IP/layer3num) + "\n")
results.write("L3avgEA\t" + str(layer3EA/layer3num) + "\n")
results.write("L4avgIP\t" + str(layer4IP/layer4num) + "\n")
results.write("L4avgEA\t" + str(layer4EA/layer4num) + "\n")
results.close()
