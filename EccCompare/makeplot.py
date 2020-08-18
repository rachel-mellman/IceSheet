import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import vplot as vpl
import os
import matplotlib.patches as mpatches
import sys
import scipy.ndimage
from matplotlib.pyplot import figure
import matplotlib.lines as mlines


num = 100
#data = [["list_K_exp10000","list_K_exp10000_ecc01","list_K_exp10000_ecc02","list_K_exp10000_ecc03"],
#    ["list_G_exp10000","list_G_exp10000_ecc01","list_K_exp10000_ecc02"],
#    ["list_F_exp10000","list_F_exp10000_ecc01"]]
data = [["list_K_exp10000"],["list_G_exp10000"],["list_F_exp10000"]]
style = ["solid","dashed", "dotted", "dash dotted"]
labels = [["e=0","e=0.1","e=0.2","e=0.3"],["e=0","e=0.1","e=0.2"],["e=0","e=0.1"]]

fig, axs = plt.subplots(1,3,figsize=(9,6.5))
fig.subplots_adjust(wspace=0.5)

for i in range(len(data)):
    for ii in i:

        lum0, obliq0, semi0, albedo_f, snowball, northCapL, northCapS, southCapL, southCapS, icebeltL, icebeltS, iceFree = np.loadtxt(data[ii], unpack=True)

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

        L_sun = 3.846e26
        a_earth = 1
        S = (lum0 / (semi0**2)) / (L_sun / (a_earth**2))

        icF = axs[i].contour(obliq0,S,icebeltL, [0.5, 1], colors = "k", linewidths=3, linestyle = style[ii])


    line = mlines.Line2D([],[],color = k,linewidth=3,label = labels[ii],linestyle=style[ii])

    axs[i].legend(handles = [line], loc='upper left')

    axs[i].ylabel("Stellar Flux relative to Earth", fontsize=16)
    axs[i].xlabel("Obliquity", fontsize=16)
    axs[i].xlim(40,90)
    axs[i].ylim(0.85,1)

#plt.savefig("EccCompare.png")
plt.show()
plt.close()
