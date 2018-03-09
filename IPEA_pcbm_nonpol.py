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

results = open("/work/akohn/projects/ptb7/qm/PTB7nonpol_IPEA.txt", "w")
layer1 = [1,9,17,8,16,24]
layer2 = [2,10,18,7,15,23]
layer3 = [3,11,19,6,14,22]
layer4 = [4,12,20,5,13,21]


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

for i in os.listdir('/work/akohn/projects/ptb7/qm/nonpol-ptb'):
    if "gr" not in i:
         continue

    groundTarget = "/work/akohn/projects/ptb7/qm/nonpol-ptb/" + i + "/qchem.out"
    catTarget = groundTarget.replace("gr", "ca")
    anTarget = groundTarget.replace("gr", "an")

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
    molNum = int(i.split(".")[1])
    print molNum

    if molNum in layer1:
        print "Assigning to layer 1"
        layer1IP += IP
        layer1EA += EA
        layer1num += 1
    if molNum in layer2:
        print "Assigning to layer 2"
        layer2IP += IP
        layer2EA += EA
        layer2num += 1
    if molNum in layer3:
        print "Assigning to layer 3"
        layer3IP += IP
        layer3EA += EA
        layer3num += 1
    if molNum in layer4:
        print "Assigning to layer 4"
        layer4IP += IP
        layer4EA += EA
        layer4num += 1



    results.write(i + "\t\t" + str(EA) + "\t\t\t" + str(IP) + "\n")

results.write("L1avgIP\t" + str(layer1IP/layer1num) + "\n")
results.write("L1avgEA\t" + str(layer1EA/layer1num) + "\n")
results.write("L2avgIP\t" + str(layer2IP/layer2num) + "\n")
results.write("L2avgEA\t" + str(layer2EA/layer2num) + "\n")
results.write("L3avgIP\t" + str(layer3IP/layer3num) + "\n")
results.write("L3avgEA\t" + str(layer3EA/layer3num) + "\n")
results.write("L4avgIP\t" + str(layer4IP/layer4num) + "\n")
results.write("L4avgEA\t" + str(layer4EA/layer4num) + "\n")
results.close()
