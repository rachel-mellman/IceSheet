#Evolving Cases (Monte Carlo simulations)

This is where the raw data for the Monte Carlo Simulations are stored. In each folder is the source files as well as the `vspace.in` file which is needed for running VPLanet.

To generate the data, you **MUST** have VPLanet installed and both vspace and multi-planet setup completed.
To get started, run `vspace vspace.in` in the command line. This creates all the simulation folders to run.
Then, run the rand_dist.py file with `python rand_dist.py vspace.in`. This script changes the values of the eccentricity amplitude to be the proper values.
Now you are ready to run VPLanet! Since there are 10,000 simulations per case, it is *recommended* to use mult-planet, which can be done by typing the following:

```
multi-planet vspace.in <number of cores>
```

Because of the seed in the vspace.in file, you should generate identical data to that in Wilhelm et al. 2020.
