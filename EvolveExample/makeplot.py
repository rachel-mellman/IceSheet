import numpy as np
import matplotlib.pyplot as plt
import vplot as vpl
from matplotlib import ticker
import os
import subprocess
import re
import sys

def clim_evol(plname,dir='.',xrange=False,orbit=False,show=True):
  """
  Creates plots of insolation, temperature, albedo, ice mass,
  and bed rock height over the length of the simulation

  Parameters
  ----------
  plname : string
    The name of the planet with .Climate data

  Keyword Arguments
  -----------------
  dir : string
    Directory of vplanet simulation (default = '.')
  xrange : float tuple, list, or numpy array
    Range of x-values (time) to restrict plot
    (default = False (no restriction))
  orbit : bool
    Plot orbital data (obliquity, eccentricity, COPP)
    (default = False)
  show : bool
    Show plot in Python (default = True)

  Output
  ------
  PDF format plot with name 'evol_<dir>.pdf'

  """
  if not isinstance(dir,(list,tuple)):
    dir = [dir]

  nfiles = len(dir)

  if nfiles > 1 and orbit == True:
    raise Exception("Error: cannot plot multiple files when orbit = True")


  fig = plt.figure(figsize=(9,8))
  fig.subplots_adjust(wspace=0.5,hspace = 0.5)

  for ii in np.arange(nfiles):
    out = vpl.GetOutput(dir[ii])

    ctmp = 0
    for p in range(len(out.bodies)):
      if out.bodies[p].name == plname:
        body = out.bodies[p]
        ctmp = 1
      else:
        if p == len(out.bodies)-1 and ctmp == 0:
          raise Exception("Planet %s not found in folder %s"%(plname,dir[ii]))

    try:
      ecc = body.Eccentricity
    except:
      ecc = np.zeros_like(body.Time)+getattr(out.log.initial,plname).Eccentricity

    try:
      inc = body.Inc
    except:
      inc = np.zeros_like(body.Time)

    try:
      obl = body.Obliquity
    except:
      obltmp = getattr(out.log.initial,plname).Obliquity
      if obltmp.unit == 'rad':
        obltmp *= 180/np.pi
      obl = np.zeros_like(body.Time)+obltmp

    f = open(dir[ii]+'/'+plname+'.in','r')
    lines = f.readlines()
    f.close()
    pco2 = 0
    #pdb.set_trace()
    for i in range(len(lines)):
      if lines[i].split() != []:
        if lines[i].split()[0] == 'dRotPeriod':
          P = -1*np.float(lines[i].split()[1])
        if lines[i].split()[0] == 'dSemi':
          semi = np.float(lines[i].split()[1])
          if semi < 0:
            semi *= -1
        if lines[i].split()[0] == 'dpCO2':
          pco2 = np.float(lines[i].split()[1])

    try:
      longp = (body.ArgP + body.LongA + body.PrecA)*np.pi/180.0
    except:
      longp = body.PrecA*np.pi/180.0

    esinv = ecc*np.sin(longp)*np.sin(obl*np.pi/180.)

    lats = np.unique(body.Latitude)
    nlats = len(lats)
    ntimes = len(body.Time)

    # plot temperature
    temp = np.reshape(body.TempLat,(ntimes,nlats))
    ax1 = plt.subplot(4,2,1)
    pos = ax1.figbox.get_points()
    c = plt.contourf(body.Time,lats,temp.T,cmap='plasma')
    plt.ylabel(r'Latitude [$^\circ$]', fontsize = 10)
    plt.title(r'Surface Temp [$^{\circ}$C]', fontsize = 12)
    plt.ylim(-85,85)
    plt.yticks([-60,-30,0,30,60], fontsize = 9)
    plt.xticks(fontsize = 9)
    if xrange:
      plt.xlim(xrange)
    cbar = plt.colorbar(c,cax=plt.axes([pos[1,0]+0.01,pos[0,1],0.01,pos[1,1]-pos[0,1]]))
    plt.setp(cbar.ax.yaxis.get_ticklabels(), fontsize = 9)

    # plot albedo
    alb = np.reshape(body.AlbedoLat,(ntimes,nlats))
    ax2 = plt.subplot(4,2,3)
    pos = ax2.figbox.get_points()
    c = plt.contourf(body.Time,lats,alb.T,cmap = 'Blues_r')
    plt.ylabel(r'Latitude [$^\circ$]', fontsize = 10)
    plt.title('Albedo [TOA]', fontsize = 12)
    plt.ylim(-85,85)
    plt.yticks([-60,-30,0,30,60], fontsize = 9)
    plt.xticks(fontsize = 9)
    if xrange:
      plt.xlim(xrange)
    cbar = plt.colorbar(c,cax=plt.axes([pos[1,0]+0.01,pos[0,1],0.01,pos[1,1]-pos[0,1]]))
    plt.setp(cbar.ax.yaxis.get_ticklabels(), fontsize = 9)


    # plot ice height
    ice = np.reshape(body.IceHeight,(ntimes,nlats))
    ax3 = plt.subplot(4,2,5)
    pos = ax3.figbox.get_points()
    c = plt.contourf(body.Time,lats,ice.T,cmap='Blues_r')
    plt.ylabel(r'Latitude [$^\circ$]', fontsize = 10)
    plt.title('Ice sheet height [m]', fontsize = 12)
    plt.ylim(-85,85)
    plt.yticks([-60,-30,0,30,60], fontsize = 9)
    plt.xticks(fontsize = 9)
    if xrange:
      plt.xlim(xrange)
    cbar = plt.colorbar(c,cax=plt.axes([pos[1,0]+0.01,pos[0,1],0.01,pos[1,1]-pos[0,1]]))
    plt.setp(cbar.ax.yaxis.get_ticklabels(), fontsize = 9)


    # plot bedrock
    brock = np.reshape(body.BedrockH,(ntimes,nlats))
    ax4 = plt.subplot(4,2,7)
    pos = ax4.figbox.get_points()
    c = plt.contourf(body.Time,lats,brock.T,cmap='Reds_r')
    plt.ylabel(r'Latitude [$^\circ$]', fontsize = 10)
    plt.title('Bedrock height [m]', fontsize = 12)
    plt.ylim(-85,85)
    plt.yticks([-60,-30,0,30,60], fontsize = 9)
    plt.xlabel('Time [years]',fontsize = 10)
    plt.xticks(fontsize = 9)
    if xrange:
      plt.xlim(xrange)
    cbar = plt.colorbar(c,cax=plt.axes([pos[1,0]+0.01,pos[0,1],0.01,pos[1,1]-pos[0,1]]))
    plt.setp(cbar.ax.yaxis.get_ticklabels(), fontsize = 9)

    # plot insolation
    insol = np.reshape(body.AnnInsol,(ntimes,nlats))
    ax5 = plt.subplot(4,2,2)
    pos = ax5.figbox.get_points()
    c = plt.contourf(body.Time,lats,insol.T,cmap='plasma')
    plt.ylabel(r'Latitude [$^\circ$]', fontsize = 10)
    plt.title(r'Annual average insolation [W/m$^2$]', fontsize = 12)
    plt.ylim(-85,85)
    plt.yticks([-60,-30,0,30,60], fontsize = 9)
    plt.xticks(fontsize = 9)
    if xrange:
      plt.xlim(xrange)
    cbar = plt.colorbar(c,cax=plt.axes([pos[1,0]+0.01,pos[0,1],0.01,pos[1,1]-pos[0,1]]))
    plt.setp(cbar.ax.yaxis.get_ticklabels(), fontsize = 9)

    #obliquity
    plt.subplot(4,2,4)
    plt.plot(body.Time,obl,linestyle = 'solid',marker='None',color='darkblue',linewidth =2)
    plt.ylabel(r'Obliquity [$^\circ$]', fontsize = 10)
    plt.yticks(fontsize = 9)
    plt.xticks(fontsize = 9)

    if xrange:
        plt.xlim(xrange)

    #eccentricity
    plt.subplot(4,2,6)
    plt.plot(body.Time,ecc,linestyle = 'solid',marker='None',color='darkorchid',linewidth =2)
    plt.ylabel('Eccentricity', fontsize = 10)
    plt.xticks(fontsize = 9)
    plt.yticks(fontsize = 9)
    if xrange:
        plt.xlim(xrange)

    #e sin(obl) sin varpi
    plt.subplot(4,2,8)
    plt.plot(body.Time,esinv,linestyle = 'solid',marker='None',color='salmon',linewidth=2)
    plt.ylabel('COPP', fontsize = 10)
    plt.xlabel('Time [years]', fontsize = 10)
    plt.xticks(fontsize = 9)
    plt.yticks(fontsize = 9)
    if xrange:
        plt.xlim(xrange)

    if dir[ii] == '.':
      dir[ii] = 'cwd'

    if (sys.argv[1] == 'pdf'):
        plt.savefig('Evolve_Example.pdf')
    if (sys.argv[1] == 'png'):
        plt.savefig('Evolve_Example.png')
    if show:
        plt.show()
    else:
        plt.close()

#makes the plots
print("Making evolution plot.")
clim_evol('earth', orbit=True,xrange = (0,250000))
