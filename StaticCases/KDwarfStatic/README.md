#Static Case (K Dwarf Star)

This is where the source files for the K Dwarf Static Case are stored.

To generate the data, you **MUST** have VPLanet installed and vspace, multi-planet, and bigplanet setup completed.
To get started, run `vspace vspace.in` in the command line. This creates all the simulation folders to run.
Now you are ready to run VPLanet! Since there are 10,000 simulations per case, it is *recommended* to use multi-planet. In this particular case, multi-planet will be ran first, then bigplanet will be ran in the makeplot.py script. Type the following in the command line:

```
multi-planet vspace.in
```

This creates the HDF5 file in conjunction with running the simulations. After the data is generated, run `python makeplot.py` to generate the plot.
