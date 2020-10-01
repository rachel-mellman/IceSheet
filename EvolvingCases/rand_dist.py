#!/usr/bin/env python

import subprocess as sub
import numpy as np
import math
import os
import sys
import fileinput

def rand_dist(space_file):
    with open(input_file, 'r') as vsf:
        for newline in f:
            datalist.append(newline.strip().split())
            for l in datalist:
                if l[0] == 'destfolder':
                    folder_name = l[1]
                if l[0] == 'seed':
                    seed = l[1]
            print("The seed is " +  seed)
            np.random.seed(int(seed))

    try:
        sims = sorted(next(os.walk(os.path.join(folder_name,'.')))[1])
    except StopIteration:
        pass

    print(sims)
    for f in sims:
        os.chdir(folder_name + "/" + f)
        earth = open('earth.in',"r+")

        for line in earth:
            line.strip().split('/n')

            if line.startswith('dEcc '):
                EccAmp = 2.0
                eccline = line.split()
                ecc = np.float(eccline[1])
                limit = ((0.5*EccAmp) + ecc)
                while limit >= 1:
                    EccAmp = np.random.uniform(low=np.float(0),high=np.float(2*ecc))
                    limit = ((0.5*EccAmp) + ecc)
                texteamp = "dEccAmp      " + str(EccAmp) +  "\n"

            if line.startswith('dObliquity'):
                oblline = line.split()
                obliq = np.float(oblline[1])
                #find when obliq is <= 90
                if obliq <= 90:
                    ObliqAmp = np.random.uniform(low=np.float(0),high=np.float(obliq))
                else:
                    ObliqAmp = np.random.uniform(low=np.float(0),high=np.float(180 - obliq))
                textoblamp = "dObliqAmp   " + str(ObliqAmp) + "\n"

        earth.write(textoblamp)
        earth.write(texteamp)
        earth.close()
        print("dObliqAmp: " + str(ObliqAmp))
        print("dEccAmp: " + str(EccAmp))
        os.chdir("../../")

rand_dist(sys.argv[1],sys.argv[2])
