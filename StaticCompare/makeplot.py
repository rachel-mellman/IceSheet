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
data = ['../StaticCases/KDwarfStatic/list_KDwarfStatic','../StaticCases/GDwarfStatic/list_GDwarfStatic','../StaticCases/FDwarfStatic/list_FDwarfStatic']
colorz = [vpl.colors.red,vpl.colors.orange,vpl.colors.pale_blue]
labels = ['K Dwarf','G Dwarf','F Dwarf']

plt.figure(figsize=(9,6.5))

for i in range(len(data)):

    lum0, obliq0, semi0, inst, snowball, northCapL, northCapS, southCapL, southCapS, icebeltL, icebeltS, iceFree, tGlobal = np.loadtxt(
        data[i], unpack=True)

    lum0 = np.reshape(lum0, (num, num)) / 3.846e26
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


    icF = plt.contour(obliq0,inst,icebeltL, [0.5, 1], colors = colorz[i], linewidths=3)


line0 = mlines.Line2D([],[],color = colorz[0],linewidth=3,label = labels[0])
line1 = mlines.Line2D([],[],color = colorz[1],linewidth=3,label = labels[1])
line2 = mlines.Line2D([],[],color = colorz[2],linewidth=3,label = labels[2])

plt.legend(handles = [line0,line1,line2], loc='upper left')
plt.ylabel('Instellation [Earth]', fontsize=16)
plt.xlabel(r'Obliquity [$^\circ$]', fontsize=16)
plt.xlim(40,90)
plt.ylim(0.865,1.01)

plt.tight_layout()

if (sys.argv[1] == 'pdf'):
    plt.savefig('StaticCompare' + '.pdf')
if (sys.argv[1] == 'png'):
    plt.savefig('StaticCompare' + '.png')

plt.show()
plt.close()
