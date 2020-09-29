import subprocess as sp
import numpy as np
import os
import sys
import vplot as vpl


def get_data(case,data):

    full_path = os.getcwd() + '/' + case
    sims = sorted([f.path for f in os.scandir(full_path) if f.is_dir()])

    if os.path.exists(data):
        return data,sims

    else:

        tGlobal = np.zeros(len(sims))
        snowballL = np.zeros(len(sims))
        snowballS = np.zeros(len(sims))
        northCapL = np.zeros(len(sims))
        northCapS = np.zeros(len(sims))
        southCapL = np.zeros(len(sims))
        southCapS = np.zeros(len(sims))
        icebeltL = np.zeros(len(sims))
        icebeltS = np.zeros(len(sims))
        iceFree = np.zeros(len(sims))

        with open(data,'w+') as data_write:
            for i in np.arange(len(sims)):
                f = sims[i]
                print(f)
                out = vpl.GetOutput(f)

                tGlobal[i] = getattr(out.log.final, 'earth').TGlobal

                snowballL[i] = getattr(out.log.final, 'earth').SnowballLand
                snowballS[i] = getattr(out.log.final, 'earth').SnowballSea

                northCapL[i] = getattr(out.log.final, 'earth').IceCapNorthLand
                northCapS[i] = getattr(out.log.final, 'earth').IceCapNorthSea

                southCapL[i] = getattr(out.log.final, 'earth').IceCapSouthLand
                southCapS[i] = getattr(out.log.final, 'earth').IceCapSouthSea

                icebeltL[i] = getattr(out.log.final, 'earth').IceBeltLand
                icebeltS[i] = getattr(out.log.final, 'earth').IceBeltSea

                iceFree[i] = getattr(out.log.final, 'earth').IceFree

                data_write.write("%s %s %s %s %s %s %s %s %s %s \n" % (tGlobal[i], snowballL[i], snowballS[i], northCapL[i], northCapS[i], southCapL[i], southCapS[i], icebeltL[i],icebeltS[i], iceFree[i]))
        return data,sims

def data_eval(raw_data,sims):

    ifCount = 0
    mgCount = 0
    snSCount = 0
    snLCount = 0
    snTCount = 0
    ibSCount = 0
    ibLCount = 0
    ibTCount = 0
    ncCount = 0
    scCount = 0
    pcCount = 0
    wwCount = 0
    unCount = 0
    sclsCount = 0
    lcssCount = 0

    with open('climateType.log','w+') as type_log:
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

                if tGlobal >= 70 and iceFree == 1:
                    mgCount += 1
                    type_log.write(sims[number] + " Moist Greenhouse \n")
                elif iceFree == 1 and tGlobal <= 70:
                    ifCount += 1
                    type_log.write(sims[number] + " Ice Free \n")

                elif (
                    snowballL == 0 and snowballS == 1 and northCapS == 0 and
                    northCapL == 0 and southCapS == 0 and southCapL == 0
                ):
                    snSCount += 1
                    type_log.write(sims[number] + " Sea Snowball \n")
                elif (
                    snowballL == 1 and snowballS == 0 and northCapS == 0 and
                    northCapL == 0 and southCapS == 0 and southCapL == 0
                ):
                    snLCount += 1
                    type_log.write(sims[number] + " Land Snowball \n")
                elif (
                    snowballL == 1 and snowballS == 1 and northCapS == 0 and
                    northCapL == 0 and southCapS == 0 and southCapL == 0
                ):
                    snTCount += 1
                    type_log.write(sims[number] + " Total Snowball \n")

                elif (
                    northCapL == 0 and southCapL == 0 and icebeltS == 1 and icebeltL == 0 or
                    northCapS == 0 and northCapL == 0 and southCapS == 0 and southCapL == 0 and
                    icebeltS == 1 and icebeltL == 0 or northCapS == 0 and southCapS == 0 and
                    icebeltS == 1 and icebeltL == 0 or northCapL == 0 and southCapS == 0 and
                    icebeltS == 1 and icebeltL == 0 or northCapS == 0 and southCapL == 0 and
                    icebeltS == 1 and icebeltL == 0
                ):
                    ibSCount += 1
                    type_log.write(sims[number] + " Sea IceBelt \n")
                elif (
                    northCapL == 0 and southCapL == 0 and icebeltS == 0 and icebeltL == 1 or
                    northCapS == 0 and northCapL == 0 and southCapS == 0 and southCapL == 0 and
                    icebeltS == 0 and icebeltL == 1 or northCapS == 0 and southCapS == 0 and
                    icebeltS == 0 and icebeltL == 1 or northCapL == 0 and southCapS == 0 and
                    icebeltS == 0 and icebeltL == 1 or northCapS == 0 and southCapL == 0 and
                    icebeltS == 0 and icebeltL == 1
                ):
                    ibLCount += 1
                    type_log.write(sims[number] + " Land IceBelt \n")
                elif (
                    northCapL == 0 and southCapL == 0 and icebeltS == 1 and icebeltL == 1 or
                    northCapS == 0 and northCapL == 0 and southCapS == 0 and southCapL == 0 and
                    icebeltS == 1 and icebeltL == 1 or northCapS == 0 and southCapS == 0 and
                    icebeltS == 1 and icebeltL == 1 or northCapL == 0 and southCapS == 0 and
                    icebeltS == 1 and icebeltL == 1 or northCapS == 0 and southCapL == 0 and
                    icebeltS == 1 and icebeltL == 1
                ):
                    ibTCount += 1
                    type_log.write(sims[number] + ' Land/Sea IceBelt \n')

                elif (
                    northCapL == 1 and southCapL == 0 and icebeltS == 0 and icebeltL == 0 and
                    snowballL == 0 and snowballS == 0 or northCapS == 1 and northCapL == 1 and
                    southCapS == 0 and southCapL == 0 and icebeltS == 0 and icebeltL == 0 and
                    snowballL == 0 and snowballS == 0 or northCapS == 1 and southCapS == 0 and
                    icebeltS == 0 and icebeltL == 0 and snowballL == 0 and snowballS == 0
                ):
                    ncCount += 1
                    type_log.write(sims[number] + " Northern Polar Cap \n")
                elif (
                    northCapL == 0 and southCapL == 1 and icebeltS == 0 and icebeltL == 0 and
                    snowballL == 0 and snowballS == 0 or northCapS == 0 and northCapL == 0 and
                    southCapS == 1 and southCapL == 1 and icebeltS == 0 and icebeltL == 0 and
                    snowballL == 0 and snowballS == 0 or northCapS == 0 and southCapS == 1 and
                    icebeltS == 0 and icebeltL == 0 and snowballL == 0 and snowballS == 0
                ):
                    scCount += 1
                    type_log.write(sims[number] + " Southern Polar Cap \n")

                elif (
                    northCapL == 1 and southCapL == 1 and icebeltS == 0 and icebeltL == 0 and
                    snowballL == 0 and snowballS == 0 or northCapS == 1 and northCapL == 1 and
                    southCapS == 1 and southCapL == 1 and icebeltS == 0 and icebeltL == 0 and
                    snowballL == 0 and snowballS == 0 or northCapS == 1 and southCapS == 1 and
                    icebeltS == 0 and icebeltL == 0 and snowballL == 0 and snowballS == 0 or
                    northCapL == 1 and southCapS == 1 and icebeltS == 0 and icebeltL == 0 and
                    snowballL == 0 and snowballS == 0 or northCapS == 1 and southCapL == 1 and
                    icebeltS == 0 and icebeltL == 0 and snowballL == 0 and snowballS == 0
                ):
                    pcCount+= 1
                    type_log.write(sims[number] + " Polar Caps \n")
                elif (
                    northCapL == 1 and southCapL == 1 and icebeltS == 1 and icebeltL == 1 or
                    northCapS == 1 and northCapL == 1 and southCapS == 1 and southCapL == 1 and
                    icebeltS == 1 and icebeltL == 1 or northCapS == 1 and southCapS == 1 and
                    icebeltS == 1 and icebeltL == 1 or northCapL == 1 and southCapS == 1 and
                    icebeltS == 1 and icebeltL == 1 or northCapS == 1 and southCapL == 1 and
                    icebeltS == 1 and icebeltL == 1
                 ):
                     wwCount+= 1
                     type_log.write(sims[number] + " Wilhem World \n")

                elif(northCapS == 1 and snowballL == 1 or southCapS == 1  and snowballL == 1):
                    sclsCount += 1
                    type_log.write(sims[number] + " Sea Cap and Land Snowball \n")
                elif(northCapL == 1 and snowballS == 1 or southCapL == 1  and snowballS == 1):
                    lcssCount += 1
                    type_log.write(sims[number] + " Land Cap and Sea Snowball \n")

                else:
                    unCount += 1
                    type_log.write(sims[number] + " Unknown Type \n")

        type_log.write("Total Number of Moist Greenhouse: " + str(mgCount) + " out of " + str(len(sims)) + "\n")
        type_log.write("Total Number of Ice Free: " + str(ifCount) + " out of " + str(len(sims)) + "\n")

        type_log.write("Total Number of Sea Snowball: " + str(snSCount) + " out of " + str(len(sims)) + "\n")
        type_log.write("Total Number of Land Snowball: " + str(snLCount) + " out of " + str(len(sims)) + "\n")
        type_log.write("Total Number of Land/Sea Snowball: " + str(snTCount) + " out of " + str(len(sims)) + "\n")

        type_log.write("Total Number of Sea IceBelt: " + str(ibSCount) + " out of " + str(len(sims)) + "\n")
        type_log.write("Total Number of Land IceBelt: " + str(ibLCount) + " out of " + str(len(sims)) + "\n")
        type_log.write("Total Number of Land/Sea IceBelt: " + str(ibTCount) + " out of " + str(len(sims)) + "\n")

        type_log.write("Total Number of Northern Caps: " + str(ncCount) + " out of " + str(len(sims)) + "\n")
        type_log.write("Total Number of Southern Caps: "  + str(scCount) + " out of " + str(len(sims)) + "\n")
        type_log.write("Total Number of Polar Caps: " + str(pcCount) + " out of " + str(len(sims)) + "\n")

        type_log.write("Total Number of Wilhelm Worlds: " + str(wwCount) + " out of " + str(len(sims)) + "\n")

        type_log.write("Total Number of Sea Caps + Land Snowball: " + str(sclsCount) + " out of " + str(len(sims)) + "\n")
        type_log.write("Total Number of Land Caps + Sea Snowball: " + str(lcssCount) + " out of " + str(len(sims)) + "\n")

        type_log.write("Total Number of Unknown Cases: " + str(unCount) + " out of " + str(len(sims)) + "\n")

def type_check(folder_name):

    data = folder_name + "_data_raw"

    raw_data = get_data(folder_name,data)
    raw_data_file = raw_data[0]
    sims = raw_data[1]
    data_eval(raw_data_file,sims)

type_check(sys.argv[1])
