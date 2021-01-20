#!/usr/bin/env python

import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import vplot as vpl
import os
import sys
import matplotlib.patches as mpatches
#bigplanet imports
from bigplanet import ExtractColumn
from bigplanet import ExtractUniqueValues
from bigplanet import CreateMatrix
from bigplanet import CreateHDF5file
import h5py

#changes cwd to where the file is
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Variable list
dest = "KDwarfStatic"
CreateHDF5file('vspace.in')
HDF5_File = h5py.File('KDwarfStatic.hdf5', 'r')

#grabs columns needed for calulations and data
earth_Obliq = ExtractColumn(HDF5_File,'earth_Obliquity_final')
earth_instel = ExtractColumn(HDF5_File,'earth_Instellation_final')

earth_icebelt_L = ExtractColumn(HDF5_File,'earth_IceBeltLand_final')
earth_icebelt_S = ExtractColumn(HDF5_File,'earth_IceBeltSea_final')
earth_northcap_L = ExtractColumn(HDF5_File,'earth_IceCapNorthLand_final')
earth_northcap_S = ExtractColumn(HDF5_File,'earth_IceCapNorthSea_final')
earth_southcap_L = ExtractColumn(HDF5_File,'earth_IceCapSouthLand_final')
earth_southcap_S = ExtractColumn(HDF5_File,'earth_IceCapSouthSea_final')

earth_icefree = ExtractColumn(HDF5_File,'earth_IceFree_final')
earth_snowball = ExtractColumn(HDF5_File,'earth_Snowball_final')


#gets the x and y axis data
earth_Obliq_uniq = ExtractUniqueValues(HDF5_File,'earth_Obliquity_forward')
earth_intstel_uniq = ExtractUniqueValues(HDF5_File,'earth_Instellation_final')

#changing units of y axis
earth_intstel_uniq =  np.reshape(earth_intstel_uniq,(earth_intstel_uniq.shape)) / 1350

# Fixing bug in vplanet where if snowball == 1 that sometimes other variables
# can also equal 1
for i in range(len(earth_snowball)):
    if earth_snowball[i] == 1.0:
        earth_icebelt_L[i] = 0
        earth_northcap_L[i] = 0
        earth_northcap_S[i] = 0
        earth_southcap_L[i] = 0
        earth_southcap_S[i] = 0

#creates a new numpy array that is for Polar Caps
PolarCaps = np.zeros(len(earth_northcap_L))
for i in range(len(PolarCaps)):

    if (
    earth_northcap_L[i] == 1 and earth_southcap_L[i] == 1 and
    earth_icebelt_S[i] == 0 and earth_icebelt_L[i] == 0 or
    earth_northcap_S[i] == 1 and earth_northcap_L[i] == 1 and
    earth_southcap_S[i] == 1 and earth_southcap_L[i] == 1 and
    earth_icebelt_S[i] == 0 and earth_icebelt_L[i] == 0 or
    earth_northcap_S[i] == 1 and earth_southcap_S[i] == 1 and
    earth_icebelt_S[i] == 0 and earth_icebelt_L[i] == 0 or
    earth_northcap_L[i] == 1 and earth_southcap_S[i] == 1 and
    earth_icebelt_S[i] == 0 and earth_icebelt_L[i] == 0 or
    earth_northcap_S[i] == 1 and earth_southcap_L[i] == 1 and
    earth_icebelt_S[i] == 0 and earth_icebelt_L[i] == 0
    ):
        PolarCaps[i] = 1

#creates the zaxis for plotting
icebeltmatrix = CreateMatrix(earth_Obliq_uniq, earth_intstel_uniq, earth_icebelt_L)
icefreematrix = CreateMatrix(earth_Obliq_uniq, earth_intstel_uniq, earth_icefree)
snowballmatrix = CreateMatrix(earth_Obliq_uniq, earth_intstel_uniq, earth_snowball)
Capsmatrix = CreateMatrix(earth_Obliq_uniq, earth_intstel_uniq, PolarCaps)

plt.figure(figsize=(9,6.5))
plt.ylabel("Instellation [Earth]", fontsize=16)
plt.xlabel("Obliquity [$^\circ$]", fontsize=16)
plt.ylim(0.867,1.211)
plt.xlim(0,90)

iFF = plt.contourf(earth_Obliq_uniq,earth_intstel_uniq,icefreematrix,[0,1],colors = vpl.colors.dark_blue)
sNF = plt.contourf(earth_Obliq_uniq,earth_intstel_uniq,snowballmatrix,[0.5,1],colors = '#efefef')
PcF = plt.contourf(earth_Obliq_uniq,earth_intstel_uniq,Capsmatrix,[0.5,1],colors = vpl.colors.purple)
icF = plt.contourf(earth_Obliq_uniq,earth_intstel_uniq,icebeltmatrix,[0.5,1],colors = vpl.colors.pale_blue)

h1, _ = iFF.legend_elements()
h2, _ = icF.legend_elements()
h3, _ = sNF.legend_elements()
h4, _ = PcF.legend_elements()

plt.legend([h1[0], h2[0], h3[0], h4[0]], [ 'Ice Free', 'Ice Belt', 'Snowball','Polar Ice Caps'],loc = 'upper left', bbox_to_anchor=(0, 1.02, 1, 0.102),ncol=4, mode="expand", borderaxespad=0)

if (sys.argv[1] == 'pdf'):
    plt.savefig(dest + '.pdf', dpi=300)
if (sys.argv[1] == 'png'):
    plt.savefig(dest + '.png', dpi=300)

plt.show()
plt.close()
