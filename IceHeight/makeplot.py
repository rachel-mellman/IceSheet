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

dest = ['/media/caitlyn/Data_Drive1/Projects/IceBelt/F_Cases/F_Monte_Carlo/','/media/caitlyn/Data_Drive1/Projects/IceBelt/G_Cases/G_Monte_Carlo/','/media/caitlyn/Data_Drive1/Projects/IceBelt/K_Cases/K_Monte_Carlo/']
star = ['F Star','G Star','K Star']
num = 1000

fig, axs = plt.subplots(3,1,figsize=(9,6.5))
fig.subplots_adjust(hspace=0.4)

for x in range(len(dest)):
    try:
        case = next(os.walk(os.path.join(dest[x],'.')))[1][0]
    except StopIteration:
            pass

    os.chdir(dest[x])
    num = int(num)
    data = np.zeros(151)
    avg_count = np.zeros(151)
    icecount = 0
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

            icecount += 1
            ice = np.reshape(body.IceHeight,(ntimes,nlats))
            ice_last = ice[-1]

            data += ice_last.T
            indi = axs[x].plot(lats,ice_last.T, color = 'gray', alpha = 0.5)

    for z in range(data.size):
        avg_count[z] = data[z]/icecount

    avg_plot = axs[x].plot(lats,avg_count, color = 'black', linewidth = 4)

    indi_leg = mlines.Line2D([],[],color = 'gray',linewidth = 3 ,label = 'Indivdual Cases', alpha = 0.5)
    avg_leg = mlines.Line2D([],[],color = 'black',linewidth = 4,label = 'Average')

    axs[0].set_xlim(-40,40)
    axs[1].set_xlim(-70,70)
    axs[2].set_xlim(-80,80)

    axs[0].text(-33,2400,star[0],verticalalignment='top',horizontalalignment='right', fontsize = 11)
    axs[1].text(-58,3400,star[1],verticalalignment='top',horizontalalignment='right', fontsize = 11)
    axs[2].text(-65.75,4000,star[2],verticalalignment='top',horizontalalignment='right', fontsize = 11)


    axs[x].set_xlabel("Latitude", fontsize = 12)
    axs[x].set_ylabel("Ice Height [m]", fontsize = 12)

    axs[2].legend(handles = [indi_leg,avg_leg], loc = 'upper left',fontsize=12, bbox_to_anchor=(0., -0.5, 1., .102),ncol=4, mode="expand", borderaxespad=0.)


plt.tight_layout()
#plt.savefig("/media/caitlyn/Data_Drive1/Projects/IceBelt/IceHeight.png")
plt.show()
plt.close()
