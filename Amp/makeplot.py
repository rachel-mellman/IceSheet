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
num = 1000

fig, axs = plt.subplots(3,1,figsize=(9,6.5))
fig.subplots_adjust(hspace=0.3)

for x in range(len(dest)):
    try:
        case = next(os.walk(os.path.join(dest[x],'.')))[1][0]
    except StopIteration:
            pass

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
    eccAmp = np.zeros(len(folders))
    obliqAmp = np.zeros(len(folders))

    for i in np.arange(len(folders)):
        f = folders[i].decode('UTF-8')
        out = vpl.GetOutput(f)
        snowball[i] = getattr(out.log.final, 'earth').Snowball
        northCapL[i] = getattr(out.log.final, 'earth').IceCapNorthLand
        northCapS[i] = getattr(out.log.final, 'earth').IceCapNorthSea
        southCapL[i] = getattr(out.log.final, 'earth').IceCapSouthLand
        southCapS[i] = getattr(out.log.final, 'earth').IceCapSouthSea
        icebeltL[i] = getattr(out.log.final, 'earth').IceBeltLand
        icebeltS[i] = getattr(out.log.final, 'earth').IceBeltSea
        iceFree[i] = getattr(out.log.final, 'earth').IceFree

        earth = open((f + '/earth.in'),"r+")
        for line in earth:
            line.strip().split('/n')
            if line.startswith('dEccAmp'):
                eccaline = line.split()
                eccAmp[i] = eccaline[1]
            if line.startswith('dObliqAmp'):
                obliqaline = line.split()
                obliqAmp[i] = obliqaline[1]
        earth.close()

        if (
             icebeltS[i] == 1 and icebeltL[i] == 1 and southCapS[i] == 0 and southCapL[i] == 0 and northCapS[i] == 0 and northCapL[i] == 0 or
             icebeltS[i] == 1 and icebeltL[i] == 0 and southCapS[i] == 0 and southCapL[i] == 0 and northCapS[i] == 0 and northCapL[i] == 0 or
             icebeltL[i] == 1 and icebeltS[i] == 0 and southCapS[i] == 0 and southCapL[i] == 0 and northCapS[i] == 0 and northCapL[i] == 0
             ):

            ib = axs[x].scatter(eccAmp[i],obliqAmp[i], color = vpl.colors.pale_blue, label = 'Ice Belt')

    axs[x].set_xlabel('Eccentricity Amplitute', fontsize = 12)
    axs[x].set_ylabel(r'Oblquity Amplitute [$^\circ$]', fontsize = 12)

plt.tight_layout()

if (sys.argv[1] == 'pdf'):
    plt.savefig('Amplitute' + '.pdf')
if (sys.argv[1] == 'png'):
    plt.savefig('Amplitute' + '.png')

plt.show()
plt.close()
