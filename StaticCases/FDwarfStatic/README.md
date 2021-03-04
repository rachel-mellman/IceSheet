#Static Case (F Dwarf Star)

This is where the source files for the F Dwarf Static Case are stored.

To generate the data, you **MUST** have VPLanet installed and vspace, multi-planet, and bigplanet setup completed.
To get started, run `vspace vspace.in` in the command line. This creates all the simulation folders to run.
Now you are ready to run VPLanet! Since there are 10,000 simulations per case, it is *recommended* to use multi-planet. In this particular case, the bigplanet argument in multi-planet will be set to true. Type the following in the command line:

```
multi-planet -bp True vspace.in
```

This generates the data that will be stored in the HDF5 files. Once multi-planet is completed, type the next command in the command line:

```
python makeplot.py
```

This creates the HDF5 files, and then plots the data in a contour plot. 
