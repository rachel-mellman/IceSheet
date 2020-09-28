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

dest = ['/media/caitlyn/Data_Drive2/Projects/IceBelt/K_Cases/K_Monte_Carlo_large/',
        '/media/caitlyn/Data_Drive2/Projects/IceBelt/G_Cases/G_Monte_Carlo_Large_2/',
        '/media/caitlyn/Data_Drive2/Projects/IceBelt/F_Cases/F_Monte_Carlo_large/']

star = ['K Star','G Star','F Star']
num = 10000

fig, axs = plt.subplots(3,1,figsize=(9,7))
fig.subplots_adjust(top=0.851,bottom=0.098,left=0.085,right=0.98,hspace=0.839,wspace=0.2)

for x in range(len(dest)):


    case = [f.path for f in os.scandir(dest[x]) if f.is_dir()][0]
    case_name = [f.name for f in os.scandir(dest[x]) if f.is_dir()][0]

    os.chdir(dest[x])
    num = int(num)
    data = np.zeros(151)
    avg_count = np.zeros(151)
    icecount = 0
    folders = sorted([f.path for f in os.scandir(case) if f.is_dir()])
    raw_data = case_name + "_data_raw"

    with open(raw_data,'r') as data_read:
        content = [line.strip().split() for line in data_read.readlines()]
        for number,line in enumerate(content):

            tGlobal = float(line[0])
            snowballL = float(line[1])
            snowballS = float(line[2])
            northCapL = float(line[3])
            northCapS = float(line[4])
            southCapL = float(line[5])
            southCapS = float(line[6])
            icebeltL = float(line[7])
            icebeltS = float(line[8])
            iceFree = float(line[9])

            if (
                northCapL == 1 and southCapL == 1 and icebeltS == 0 and
                icebeltL == 0 and snowballL == 0 and snowballS == 0 or
                northCapS == 1 and northCapL == 1 and southCapS == 1 and
                southCapL == 1 and icebeltS == 0 and icebeltL == 0 and
                snowballL == 0 and snowballS == 0 or
                northCapS == 1 and southCapS == 1 and icebeltS == 0 and
                icebeltL == 0 and snowballL == 0 and snowballS == 0 or
                northCapL == 1 and southCapS == 1 and icebeltS == 0 and
                icebeltL == 0 and snowballL == 0 and snowballS == 0 or
                northCapS == 1 and southCapL == 1 and icebeltS == 0 and
                icebeltL == 0 and snowballL == 0 and snowballS == 0
            ):
                if icecount <= 100:
                    out = vpl.GetOutput(folders[number])
                    body = out.bodies[1]

                    lats = np.unique(body.Latitude)
                    nlats = len(lats)
                    ntimes = len(body.Time)

                    ice = np.reshape(body.IceHeight,(ntimes,nlats))
                    ice_last = ice[-1]

                    data += ((ice_last.T)/1000)
                    indi = axs[x].plot(lats,((ice_last.T)/1000), color = 'gray', alpha = 0.25)
                    icecount += 1

    for z in range(data.size):
        avg_count[z] = data[z]/icecount

    avg_plot = axs[x].plot(lats,avg_count, color = 'black', linewidth = 4)


    indi_leg_pc = mlines.Line2D([],[],color = 'gray',linewidth = 3 ,label = 'Indivdual Cases', alpha = 0.25)
    avg_leg = mlines.Line2D([],[],color = 'black',linewidth = 4,label = 'Average')

    axs[x].set_xlim(-83,83)
    axs[2].set_ylim(0.0,5.0)
    axs[1].set_ylim(0.0,5.0)
    axs[0].set_ylim(0.0,5.5)

    axs[2].set_yticks([0.0,2.5,5.0])
    axs[1].set_yticks([0.0,2.5,5.0])
    axs[0].set_yticks([0.0,2.5,5.0])

    axs[0].set_title("K Star", fontsize = 16)
    axs[1].set_title("G Star", fontsize = 16)
    axs[2].set_title("F Star", fontsize = 16)

    axs[x].set_xlabel(r'Latitude [$^\circ$]', fontsize = 12)
    axs[x].set_ylabel("Ice Height [km]", fontsize = 12)

    axs[0].legend(handles = [indi_leg_pc,avg_leg], fontsize=14, loc = 'upper left', bbox_to_anchor=(0, 1.75, 1, 0.102),ncol=2, mode="expand", borderaxespad=0)


plt.tight_layout()
os.chdir('/home/caitlyn/IceBelt/CapHeight')
if (sys.argv[1] == 'pdf'):
    plt.savefig('CapHeight' + '.pdf')
if (sys.argv[1] == 'png'):
    plt.savefig('CapHeight' + '.png')

plt.show()
plt.close()
