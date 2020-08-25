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
dest = [["/media/caitlyn/Data_Drive1/Projects/IceBelt/K_Cases/K_obl_stat/","/media/caitlyn/Data_Drive1/Projects/IceBelt/K_Cases/K_ecc01_stat/","/media/caitlyn/Data_Drive1/Projects/IceBelt/K_Cases/K_ecc02_stat/","/media/caitlyn/Data_Drive1/Projects/IceBelt/K_Cases/K_ecc03_stat/"],["/media/caitlyn/Data_Drive1/Projects/IceBelt/G_Cases/G_obl_stat/","/media/caitlyn/Data_Drive1/Projects/IceBelt/G_Cases/G_ecc01_stat/","/media/caitlyn/Data_Drive1/Projects/IceBelt/G_Cases/G_ecc02_stat/"],["/media/caitlyn/Data_Drive1/Projects/IceBelt/F_Cases/F_obl_stat/","/media/caitlyn/Data_Drive1/Projects/IceBelt/F_Cases/F_ecc01_stat/"]]
style = ["solid","dashed", "dotted", "dashdot"]
labels = ["e=0","e=0.1","e=0.2","e=0.3"]
star = ["K Star", "G Star", "F Star"]

fig, axs = plt.subplots(3,1,figsize=(9,7))
#fig.subplots_adjust(hspace=0.1)

for i in range(len(dest)):
    for ii in range(len(dest[i])):

        try:
            case = next(os.walk(os.path.join(dest[i][ii],'.')))[1][0]
        except StopIteration:
            pass
        print(dest[i][ii])
        os.chdir(dest[i][ii])
        num = int(num)
        folders = sp.check_output("echo " + dest[i][ii] + case + "/semi_obl*", shell=True).split()
        listf = dest[i][ii] + "/list_" + case

        # if the list file exists, extract data for plotting
        if os.path.exists(listf):
            lum0, obliq0, semi0, albedo_f, snowball, northCapL, northCapS, southCapL, southCapS, icebeltL, icebeltS, iceFree = np.loadtxt(
                listf, unpack=True)

        else:

            lum0 = np.zeros(len(folders))
            obliq0 = np.zeros(len(folders))
            semi0 = np.zeros(len(folders))
            albedo_f = np.zeros(len(folders))
            snowball = np.zeros(len(folders))
            northCapL = np.zeros(len(folders))
            northCapS = np.zeros(len(folders))
            southCapL = np.zeros(len(folders))
            southCapS = np.zeros(len(folders))
            icebeltL = np.zeros(len(folders))
            icebeltS = np.zeros(len(folders))
            iceFree = np.zeros(len(folders))

            crap = open(listf, "w")
            for i in np.arange(len(folders)):
                f = folders[i].decode('UTF-8')
                out = vpl.GetOutput(f)
                lum0[i] = getattr(out.log.initial, 'sun').Luminosity
                obliq0[i] = getattr(out.log.initial, 'earth').Obliquity
                semi0[i] = getattr(out.log.initial, 'earth').SemiMajorAxis
                albedo_f[i] = out.earth.AlbedoGlobal[-1]

                snowball[i] = getattr(out.log.final, 'earth').Snowball

                northCapL[i] = getattr(out.log.final, 'earth').IceCapNorthLand
                northCapS[i] = getattr(out.log.final, 'earth').IceCapNorthSea

                southCapL[i] = getattr(out.log.final, 'earth').IceCapSouthLand
                southCapS[i] = getattr(out.log.final, 'earth').IceCapSouthSea

                icebeltL[i] = getattr(out.log.final, 'earth').IceBeltLand
                icebeltS[i] = getattr(out.log.final, 'earth').IceBeltSea

                iceFree[i] = getattr(out.log.final, 'earth').IceFree

                if snowball[i] == 1:
                    icebeltL[i] = 0
                    icebeltS[i] = 0
                    northCapL[i] = 0
                    northCapS[i] = 0
                    southCapL[i] = 0
                    southCapS[i] = 0
                    iceFree[i] = 0

                crap.write("%s %s %s %s %s %s %s %s %s %s %s %s \n" % (
                    lum0[i], obliq0[i], semi0[i], albedo_f[i], snowball[i], northCapL[i], northCapS[i], southCapL[i], southCapS[i], icebeltL[i], icebeltS[i], iceFree[i]))

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

        icF = axs[i].contour(obliq0,S,icebeltL, [0.5, 1], colors = 'black', linestyles = style[ii])


    e0 = mlines.Line2D([],[],color = 'black',linewidth=3,label = labels[0],linestyle = style[0])
    e1 = mlines.Line2D([],[],color = 'black',linewidth=3,label = labels[1],linestyle = style[1])
    e2 = mlines.Line2D([],[],color = 'black',linewidth=3,label = labels[2],linestyle = style[2])
    e3 = mlines.Line2D([],[],color = 'black',linewidth=3,label = labels[3],linestyle = style[3])

    axs[0].text(43.75,0.9875,star[0],verticalalignment='top',horizontalalignment='right', fontsize = 11)
    axs[1].text(48.5,0.99,star[1],verticalalignment='top',horizontalalignment='right', fontsize = 11)
    axs[2].text(53,0.995,star[2],verticalalignment='top',horizontalalignment='right', fontsize = 11)


    axs[2].legend(handles = [e0,e1,e2,e3], loc = 'upper left',fontsize=12, bbox_to_anchor=(0., -0.45, 1., .102),ncol=4, mode="expand", borderaxespad=0.)
    axs[i].set_ylabel("Instellation", fontsize=12)
    axs[2].set_xlabel("Obliquity [$^\circ$]", fontsize=12)

    axs[0].set_xlim(40,90)
    axs[1].set_xlim(45,90)
    axs[2].set_xlim(50,90)

    axs[0].set_ylim(0.82,1)
    axs[1].set_ylim(0.88,1)
    axs[2].set_ylim(0.92,1)

    plt.tight_layout()

plt.savefig("/media/caitlyn/Data_Drive1/Projects/IceBelt/EccCompare.pdf")
plt.show()
plt.close()
