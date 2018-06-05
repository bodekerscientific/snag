SNAG
====

The Single column model Namelist Auto Generator

This package is designed to enable users of the UM Single Column Model (SCM) to be able to create and modify the namelist file required by the SCM in a Pythonic way.

It is currently only set up for observational forcing cases only.

Installation
============

Install the latest version of the package using pip:

    pip install snag


Getting Started
===============

How to use the package

Requirements:
- netCDF files containing the gridded input data covering the height and time required by the model
- a YAML configuration file specifying model options to be set in the namelist

We would suggest you start by taking the example YAML file and modifying for your case.

Required input data:
temperature
pressure
specific humidity
u + v winds
w winds + vertical movement due to horizontal advection
ozone

Overview of SNAG process:
SNAG reads the YAML configuration file and input data, calculates the tendencies required for the specified forcing/relaxation options, checks the consistency of the namelist options,
then writes the namelist to a Fortran namelist file. Users can optionally perturb the tendencies before they are written to the namelist.

The values specified in the YAML file will override any parameters calculated from the input data i.e nfor. BUT SNAG will create any required parameters from the input
data if they are not specified in the YAML file.

Note that tendencies (_inc) are given in units per day, so look quite large.

For land points:

Specifiy initial temperatures (in &INPROF) as well as soil moisture through either smcli or sth (&INJULES). the number of (deep) soil layers is set in ROSES using variable st_levels.


take care with scientific notation for numbers: 1.0e-4 will be interpreted as a number, but 1e-4 will incorrectly display as a string in the resulting namelist.
This will break the build and show up as an "input conversion error" in the Rose error log

List arrays [1.5, 1.3, 1.2]