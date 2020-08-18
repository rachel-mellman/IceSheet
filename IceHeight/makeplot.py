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
# check if case has ice belt land
# if it does then it needs to get the ice sheet height
# gets the Latitude distance and finds the middle
# once all the cases have been looked at, find the avg ice sheet height
# plot lat (x axis) vs ice sheet height (y axis)
# each inidivdual case is plotted in grey
# avg is plotted in black
#do this for FGK

dest = ['/media/caitlyn/Data_Drive/Projects/IceBelt/F_Cases/F_Monte_Carlo/','/media/caitlyn/Data_Drive/Projects/IceBelt/G_Cases/G_Monte_Carlo/','/media/caitlyn/Data_Drive/Projects/IceBelt/K_Cases/K_Monte_Carlo/']
num = 1000
# case = next(os.walk(os.path.join(dest,'.')))[1][0]
# os.chdir(dest)
# num = int(num)
# folders = sp.check_output("echo " + dest + case + "/semi_obl*", shell=True).split()

fig, axs = plt.subplots(3,1,figsize=(9,6.5))
fig.subplots_adjust(wspace=0.5)

for x in range(len(dest)):

    case = next(os.walk(os.path.join(dest[x],'.')))[1][0]
    os.chdir(dest[x])
    num = int(num)
    folders = sp.check_output("echo " + dest[x] + case + "/semi_obl*", shell=True).split()

    snowball = np.zeros(len(folders))
    northCapL = np.zeros(len(folders))
    northCapS = np.zeros(len(folders))
    southCapL = np.zeros(len(folders))
    southCapS = np.zeros(len(folders))
    icebeltL = np.zeros(len(folders))
    icebeltS = np.zeros(len(folders))
    iceFree = np.zeros(len(folders))

    for i in np.arange(len(folders)):
        f = folders[i].decode('UTF-8')
        out = vpl.GetOutput(f)
        body = out.bodies[1]
        snowball[i] = getattr(out.log.final, 'earth').Snowball
        northCapL[i] = getattr(out.log.final, 'earth').IceCapNorthLand
        northCapS[i] = getattr(out.log.final, 'earth').IceCapNorthSea
        southCapL[i] = getattr(out.log.final, 'earth').IceCapSouthLand
        southCapS[i] = getattr(out.log.final, 'earth').IceCapSouthSea
        icebeltL[i] = getattr(out.log.final, 'earth').IceBeltLand
        icebeltS[i] = getattr(out.log.final, 'earth').IceBeltSea
        iceFree[i] = getattr(out.log.final, 'earth').IceFree

        if snowball[i] == 1:
            northCapL[i] = 0
            northCapS[i] = 0
            southCapL[i] = 0
            southCapS[i] = 0
            icebeltL[i] = 0
            icebeltS[i] = 0
            iceFree[i] = 0

        elif iceFree[i] == 1:
            northCapL[i] = 0
            northCapS[i] = 0
            southCapL[i] = 0
            southCapS[i] = 0
            icebeltL[i] = 0
            icebeltS[i] = 0

        elif (
            icebeltL[i] == 1 and icebeltS[i] == 0 and southCapS[i] == 0 and southCapL[i] == 0 and northCapS[i] == 0 and northCapL[i] == 0
        ):
            lats = np.unique(body.Latitude)
            nlats = len(lats)
            ntimes = len(body.Time)

            ice = np.reshape(body.IceHeight,(ntimes,nlats))
            ice_last = ice[-1]
            indi = axs[x].plot(lats,ice_last.T, color = 'gray', alpha = 0.75)

    avg_ice = (sum(ice_last.T)/len(ice_last.T))
    avg_lats = (sum(lats)/len(lats))

    avg = axs[x].plot(avg_lats,avg_ice.T, color = 'black', linewidth = 5)

    indi_leg = mlines.Line2D([],[],color = 'gray',linewidth=3 ,label = 'Inidivdual Cases', alpha = 0.75)
    avg_leg = mlines.Line2D([],[],color = 'black',linewidth=5,label = 'Average')

    axs[0].set_xlim(-20,20)
    axs[1].set_xlim(-40,40)
    axs[2].set_xlim(-60,60)
    axs[x].set_xlabel("Latitude")
    axs[x].set_ylabel("Ice Height [m]")
    axs[x].legend(handles = [indi_leg,avg_leg], loc = 'upper right')

plt.show()
plt.close()
