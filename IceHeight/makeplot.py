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

dest = ['/media/caitlyn/Data_Drive1/Projects/IceBelt/F_Cases/F_Monte_Carlo/','/media/caitlyn/Data_Drive1/Projects/IceBelt/G_Cases/G_Monte_Carlo/','/media/caitlyn/Data_Drive1/Projects/IceBelt/K_Cases/K_Monte_Carlo/']
star = ['F Star','G Star','K Star']
num = 1000

fig, axs = plt.subplots(3,1,figsize=(9,7))
fig.subplots_adjust(hspace=0.5)

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

            data += ((ice_last.T)/1000)
            indi = axs[x].plot(lats,((ice_last.T)/1000), color = 'gray', alpha = 0.25)

    for z in range(data.size):
        avg_count[z] = data[z]/icecount

    #avg_plot = axs[x].plot(lats,avg_count, color = 'black', linewidth = 4)

    indi_leg = mlines.Line2D([],[],color = 'gray',linewidth = 3 ,label = 'Indivdual Cases', alpha = 0.5)
    avg_leg = mlines.Line2D([],[],color = 'black',linewidth = 4,label = 'Average')

    axs[x].set_xlim(-90,90)

    # axs[0].text(-33,2400,star[0],verticalalignment='top',horizontalalignment='right', fontsize = 11)
    # axs[1].text(-58,3400,star[1],verticalalignment='top',horizontalalignment='right', fontsize = 11)
    # axs[2].text(-65.75,4000,star[2],verticalalignment='top',horizontalalignment='right', fontsize = 11)

    axs[0].set_title("K Star", fontsize = 16)
    axs[1].set_title("G Star", fontsize = 16)
    axs[2].set_title("F Star", fontsize = 16)

    axs[x].set_xlabel(r'Latitude [$^\circ$]', fontsize = 12)
    axs[x].set_ylabel("Ice Height [km]", fontsize = 12)

    axs[0].legend(handles = [indi_leg,avg_leg], fontsize=14, loc = 'upper left', bbox_to_anchor=(0, 1.75, 1, 0.102),ncol=2, mode="expand", borderaxespad=0)


plt.tight_layout()
os.chdir('IceBelt/IceHeight')
if (sys.argv[1] == 'pdf'):
    plt.savefig('IceHeight' + '.pdf')
if (sys.argv[1] == 'png'):
    plt.savefig('IceHeight' + '.png')

plt.show()
plt.close()
