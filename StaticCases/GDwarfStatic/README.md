#Static Case (G Dwarf Star)

This is where the source files for the G Dwarf Static Case are stored.

To generate the data, you **MUST** have VPLanet installed and vspace, multi-planet, and bigplanet setup completed.
To get started, run `vspace vspace.in` in the command line. This creates all the simulation folders to run.
Now you are ready to run VPLanet! Since there are 10,000 simulations per case, it is *recommended* to use multi-planet. In this particular case, multi-planet will be run then bigplanet will be run separately afterwards. Type the following in the command line:

```
multi-planet vspace.in
```

This generates the data that will be stored in the HDF5 files. Once multi-planet is completed, type the next command in the command line:

```
bigplanet vspace.in
```

This creates the HDF5 files that is used to create the the plot. After the data is generated, run `python makeplot.py` to generate the plot.
