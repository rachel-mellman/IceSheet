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
dest = "F_exp10000"
num = 100

L_sun = 3.846e26
a_earth = 1

plt.ylabel("Stellar Flux relative to Earth",fontsize = 16)
plt.xlabel("Starting Obliquity",fontsize = 16)
plt.ylim(0.835,1.01)
plt.xlim(45,90)

if os.path.exists(listf):
    lum0, obliq0, semi0, albedo_f, snowball, northCapL, northCapS, southCapL, southCapS, icebeltL, icebeltS, iceFree = np.loadtxt(
        listf, unpack=True)

lum0 = np.reshape(lum0, (num, num))
obliq0 = np.reshape(obliq0, (num, num)) * 180 / np.pi
semi0 = np.reshape(semi0, (num, num)) / 1.49598e11
albedo_f = np.reshape(albedo_f, (num, num))
snowball = np.reshape(snowball, (num, num))
northCapL = np.reshape(northCapL, (num, num))
northCapS = np.reshape(northCapS, (num, num))
southCapL = np.reshape(southCapL, (num, num))
southCapS = np.reshape(southCapS, (num, num))
icebeltL = np.reshape(icebeltL, (num, num))
icebeltS = np.reshape(icebeltS, (num, num))
iceFree = np.reshape(iceFree, (num, num))

#calulates Stellar FLux
S = (lum0 / (semi0**2)) / (L_sun / (a_earth**2))

plt.figure(figsize=(9,6.5))
plt.ylabel("Stellar Flux relative to Earth", fontsize=16)
plt.xlabel("Obliquity", fontsize=16)
plt.ylim(0.92,1)
plt.xlim(50, 90)

iFF = plt.contourf(obliq0, S, iceFree, [0, 1], colors = '#1321d8')
sNF = plt.contourf(obliq0, S, snowball, [0.5, 1], colors = '#efefef')
icF = plt.contourf(obliq0,S,icebeltL, [0.5, 1], colors = '#13aed5')

h1, _ = iFF.legend_elements()
h2, _ = icF.legend_elements()
h3, _ = sNF.legend_elements()
#h4, _ = aZF.legend_elements()
plt.legend([h1[0], h2[0], h3[0]], [ 'Ice Free', 'Ice Belt', 'Snowball'], loc = "upper left")

plt.tight_layout()

if (sys.argv[1] == 'pdf'):
    plt.savefig(dest + '.pdf', dpi=300)
if (sys.argv[1] == 'png'):
    plt.savefig(dest + '.png', dpi=300)

plt.show()
plt.close()
