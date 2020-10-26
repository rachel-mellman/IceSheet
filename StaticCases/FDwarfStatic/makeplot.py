#!/usr/bin/env python

import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import vplot as vpl
import os
import sys
import matplotlib.patches as mpatches


#Variable List
dest = "FDwarfStatic"
num = 100
L_sun = 3.846e26
a_earth = 1
listf = "list_FDwarfStatic"


# if the list file exists, extract data for plotting

lum0, obliq0, semi0, inst, snowball, northCapL, northCapS, southCapL, southCapS, icebeltL, icebeltS, iceFree, tGlobal = np.loadtxt(
    listf, unpack=True)

PolarCaps = np.zeros(num*num)
MoistGreen = np.zeros(num*num)
for i in np.arange(num*num):

    if (
    northCapL[i] == 1 and southCapL[i] == 1 and icebeltS[i] == 0 and icebeltL[i] == 0 or
    northCapS[i] == 1 and northCapL[i] == 1 and southCapS[i] == 1 and southCapL[i] == 1 and icebeltS[i] == 0 and icebeltL[i] == 0 or
    northCapS[i] == 1 and southCapS[i] == 1 and icebeltS[i] == 0 and icebeltL[i] == 0 or
    northCapL[i] == 1 and southCapS[i] == 1 and icebeltS[i] == 0 and icebeltL[i] == 0 or
    northCapS[i] == 1 and southCapL[i] == 1 and icebeltS[i] == 0 and icebeltL[i] == 0
    ):
        PolarCaps[i] = 1

    if tGlobal[i] >= 70 and iceFree[i] == 1:
        MoistGreen[i] = 1


lum0 = np.reshape(lum0, (num, num))
obliq0 = np.reshape(obliq0, (num, num)) * 180 / np.pi
semi0 = np.reshape(semi0, (num, num)) / 1.49598e11
inst = np.reshape(inst, (num, num)) / 1350
snowball = np.reshape(snowball, (num, num))
northCapL = np.reshape(northCapL, (num, num))
northCapS = np.reshape(northCapS, (num, num))
southCapL = np.reshape(southCapL, (num, num))
southCapS = np.reshape(southCapS, (num, num))
icebeltL = np.reshape(icebeltL, (num, num))
icebeltS = np.reshape(icebeltS, (num, num))
iceFree = np.reshape(iceFree, (num, num))
tGlobal = np.reshape(tGlobal, (num, num))

PolarCaps = np.reshape(PolarCaps, (num, num))
MoistGreen = np.reshape(MoistGreen, (num, num))

plt.figure(figsize=(9,6.5))
plt.ylabel("Instellation [Earth]", fontsize=16)
plt.xlabel("Obliquity [$^\circ$]", fontsize=16)
plt.ylim(0.932,1.208)
plt.xlim(0,90)

iFF = plt.contourf(obliq0, inst, iceFree, [0, 1], colors = vpl.colors.dark_blue)
sNF = plt.contourf(obliq0, inst, snowball, [0.5, 1], colors = '#efefef')
PcF = plt.contourf(obliq0,inst,PolarCaps, [0.5, 1], colors = vpl.colors.purple)
icF = plt.contourf(obliq0,inst,icebeltL, [0.5, 1], colors = vpl.colors.pale_blue)

h1, _ = iFF.legend_elements()
h2, _ = icF.legend_elements()
h3, _ = sNF.legend_elements()
h4, _ = PcF.legend_elements()

plt.legend([h1[0], h2[0], h3[0], h4[0]], [ 'Ice Free', 'Ice Belt', 'Snowball','Polar Ice Caps'],loc = 'upper left', bbox_to_anchor=(0, 1.02, 1, 0.102),ncol=4, mode="expand", borderaxespad=0)

if (sys.argv[1] == 'pdf'):
    plt.savefig(dest + '.pdf')
if (sys.argv[1] == 'png'):
    plt.savefig(dest + '.png')

plt.show()
plt.close()
