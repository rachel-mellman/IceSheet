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
dest = "K_exp1024_obl_stat"
num = 32

L_sun = 3.846e26
a_earth = 1

plt.ylabel("Stellar Flux relative to Earth",fontsize = 16)
plt.xlabel("Starting Obliquity",fontsize = 16)
# ALWAYS KEEP Y-LIM TO BE A DISTANCE OF 0.175
plt.ylim(0.835,1.01)
plt.xlim(45,90)

#Configures list file for ploting
listf = "list_" + dest
lum,obliq,semi,albedo_f,totice_m,snowball = np.loadtxt(listf, unpack = True)

#reshapes data for plotting
lum = np.reshape(lum, (num,num))
obliq = np.reshape( obliq,(num,num)) * 180/np.pi
semi = np.reshape( semi,(num,num)) /1.49598e11
albedo_f = np.reshape( albedo_f,(num,num))
totice_m = np.reshape( totice_m,(num,num))
snowball = np.reshape( snowball,(num,num))

#calulates Stellar FLux
S = (lum/(semi**2))/(L_sun/(a_earth**2))

ct = plt.pcolormesh(obliq, S, albedo_f,cmap='Blues_r')
ct.set_edgecolor('face')
c1 = plt.contour(obliq, S,totice_m, [0], colors = 'k',linewidths = 2)
c1f = plt.contourf(obliq, S, totice_m,[1, float("inf")], colors = 'none',  hatches=['//'], extend='lower')


#Does hatching in the IceBelt formation region
class AnyObject(object):
    pass

class AnyObjectHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = mpatches.Rectangle([x0, y0], width, height,facecolor='None',
                                   edgecolor='black', hatch='//', lw=2,
                                   transform=handlebox.get_transform())
        handlebox.add_artist(patch)
        return patch

plt.legend([AnyObject()], ['Ice Belt Formation'],
           handler_map={AnyObject: AnyObjectHandler()}, loc = "upper left")

#adds the colorbar
pl = plt.colorbar(ct, ax = None)
pl.set_label("Global Albedo")

if (sys.argv[1] == 'pdf'):
    plt.savefig(dest + '.pdf', dpi=300)
if (sys.argv[1] == 'png'):
    plt.savefig(dest + '.png', dpi=300)

plt.show()
plt.close()
