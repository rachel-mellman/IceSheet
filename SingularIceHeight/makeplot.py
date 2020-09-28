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

dest = [
    '/media/caitlyn/Data_Drive1/Projects/IceBelt/K_Cases/K_Monte_Carlo/',
    '/media/caitlyn/Data_Drive1/Projects/IceBelt/G_Cases/G_Monte_Carlo/',
    '/media/caitlyn/Data_Drive1/Projects/IceBelt/F_Cases/F_Monte_Carlo/'
        ]
star = ['K Star','G Star','F Star']
num = 10000

fig, axs = plt.subplots(3,1,figsize=(9,7))
fig.subplots_adjust(top=0.851,bottom=0.098,left=0.085,right=0.98,hspace=0.839,wspace=0.2)

for x in range(len(dest)):


    case = [f.path for f in os.scandir(dest[x]) if f.is_dir()][0]

    os.chdir(dest[x])
    num = int(num)
    data = np.zeros(151)
    avg_count = np.zeros(151)
    icecount = 0
    folders = sorted([f.path for f in os.scandir(case) if f.is_dir()])

    snowballL = np.zeros(len(folders))
    snowballS = np.zeros(len(folders))
    northCapL = np.zeros(len(folders))
    northCapS = np.zeros(len(folders))
    southCapL = np.zeros(len(folders))
    southCapS = np.zeros(len(folders))
    icebeltL = np.zeros(len(folders))
    icebeltS = np.zeros(len(folders))
    iceFree = np.zeros(len(folders))

    for i in np.arange(len(folders)):
        f = folders[i]
        print(f)
        out = vpl.GetOutput(f)
        body = out.bodies[1]

        snowballL[i] = getattr(out.log.final, 'earth').SnowballLand
        snowballS[i] = getattr(out.log.final, 'earth').SnowballSea
        northCapL[i] = getattr(out.log.final, 'earth').IceCapNorthLand
        northCapS[i] = getattr(out.log.final, 'earth').IceCapNorthSea
        southCapL[i] = getattr(out.log.final, 'earth').IceCapSouthLand
        southCapS[i] = getattr(out.log.final, 'earth').IceCapSouthSea
        icebeltL[i] = getattr(out.log.final, 'earth').IceBeltLand
        icebeltS[i] = getattr(out.log.final, 'earth').IceBeltSea
        iceFree[i] = getattr(out.log.final, 'earth').IceFree

        #checks if a northern ice cap
        if (
            northCapL == 1 and southCapL == 0 and icebeltS == 0 and icebeltL == 0 and
            snowballL == 0 and snowballS == 0 or northCapS == 1 and northCapL == 1 and
            southCapS == 0 and southCapL == 0 and icebeltS == 0 and icebeltL == 0 and
            snowballL == 0 and snowballS == 0 or northCapS == 1 and southCapS == 0 and
            icebeltS == 0 and icebeltL == 0 and snowballL == 0 and snowballS == 0
        ):
            lats = np.unique(body.Latitude)
            nlats = len(lats)
            ntimes = len(body.Time)

            icecount += 1
            ice = np.reshape(body.IceHeight,(ntimes,nlats))
            ice_last = ice[-1]

            data += ((ice_last.T)/1000)
            indi = axs[x].plot(lats,((ice_last.T)/1000), color = 'blue', alpha = 0.25)
        #checks if a southern ice cap
        elif (
            northCapL == 0 and southCapL == 1 and icebeltS == 0 and icebeltL == 0 and
            snowballL == 0 and snowballS == 0 or northCapS == 0 and northCapL == 0 and
            southCapS == 1 and southCapL == 1 and icebeltS == 0 and icebeltL == 0 and
            snowballL == 0 and snowballS == 0 or northCapS == 0 and southCapS == 1 and
            icebeltS == 0 and icebeltL == 0 and snowballL == 0 and snowballS == 0
        ):
            lats = np.unique(body.Latitude)
            nlats = len(lats)
            ntimes = len(body.Time)

            icecount += 1
            ice = np.reshape(body.IceHeight,(ntimes,nlats))
            ice_last = ice[-1]

            data += ((ice_last.T)/1000)
            indi = axs[x].plot(lats,((ice_last.T)/1000), color = 'red', alpha = 0.25)


    for z in range(data.size):
        avg_count[z] = data[z]/icecount

    avg_plot = axs[x].plot(lats,avg_count, color = 'black', linewidth = 4)


    indi_leg_nc = mlines.Line2D([],[],color = 'blue',linewidth = 3 ,label = 'Indivdual Cases (Northern Cap)', alpha = 0.25)
    indi_leg_sc = mlines.Line2D([],[],color = 'red',linewidth = 3 ,label = 'Indivdual Cases (Southern Caps)', alpha = 0.25)

    avg_leg = mlines.Line2D([],[],color = 'black',linewidth = 4,label = 'Average')

    axs[x].set_xlim(-83,83)
    axs[2].set_ylim(0.0,5.0)
    axs[1].set_ylim(0.0,5.0)
    axs[0].set_ylim(0.0,5.5)

    axs[2].set_yticks([0.0,2.5])
    axs[1].set_yticks([0.0,2.5,5.0])
    axs[0].set_yticks([0.0,2.5,5.0])

    axs[0].set_title("K Star", fontsize = 16)
    axs[1].set_title("G Star", fontsize = 16)
    axs[2].set_title("F Star", fontsize = 16)

    axs[x].set_xlabel(r'Latitude [$^\circ$]', fontsize = 12)
    axs[x].set_ylabel("Ice Height [km]", fontsize = 12)

    axs[0].legend(handles = [indi_leg_nc,indi_leg_sc,avg_leg], fontsize=14, loc = 'upper left', bbox_to_anchor=(0, 1.75, 1, 0.102),ncol=2, mode="expand", borderaxespad=0)


plt.tight_layout()
os.chdir('/home/caitlyn/IceBelt/SingularIceHeight')
if (sys.argv[1] == 'pdf'):
    plt.savefig('IceHeight' + '.pdf')
if (sys.argv[1] == 'png'):
    plt.savefig('IceHeight' + '.png')

plt.show()
plt.close()
