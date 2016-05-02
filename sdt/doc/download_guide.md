# Download Guide

## Synopsis

This document describes how to download files using Synda.

## Introduction

There are two way of downloading data with Synda: using *synda get* command, and
using *synda install* command.

*synda get* is similar to *wget* command while *synda install* is similar
to *apt-get* command (but asynchronous).

*synda get* is handy to quickly download a few files, while synda install is
intended to manage a large number of files.

The differences between *synda get* and *synda install* are listed below:

*synda get*:

* no tracking
* no parallel download
* no daemon involved
* synchronous

*synda install*:

* tracking
* parallel download
* asynchronous
* use daemon to manage download

The next sections will detail both commands.

## Download files using 'synda get' command

### Usage

    synda get DATASET

#### Example of use

Install a dataset

    synda install cmip5.output1.CCCma.CanESM2.historicalMisc.day.atmos.day.r2i1p4.v2

Install a variable

    synda install cmip5.output1.CCCma.CanESM2.historicalMisc.day.atmos.day.r2i1p4.v2

Install a file

    synda install cmip5.output1.CNRM-CERFACS.CNRM-CM5.rcp85.fx.atmos.fx.r0i0p0.v20130826.sftlf_fx_CNRM-CM5_rcp85_r0i0p0.nc

Install files using facets stored in an file. This example use
'sample_selection_01.txt' file which is available in the selection sample folder
($HOME/sdt/selection/sample).

    <-- 'sample_selection_01.txt'
    project="CMIP5"
    model="CNRM-CM5 CSIRO-Mk3-6-0"
    experiment="historical amip"
    ensemble="r1i1p1"
    variable[atmos][mon]="tasmin tas psl"
    variable[ocean][fx]="areacello sftof"
    variable[land][mon]="mrsos,nppRoot,nep"
    variable[seaIce][mon]="sic evap"
    variable[ocnBgchem][mon]="dissic fbddtalk"
    -->

    synda install -s sample_selection_01.txt

### Error management

#### Changing replica for all file in errors

If download fails you can try another replica.

To change the replica for all files in error, use command below

    synda replica next

#### Getting more details about errors

Log files below contain useful informations about errors

* 'transfer.log' contains download status for each file.
* 'debug.log' contains 'wget' command log.
* 'discovery.log' contains search-api log.

Note: log files are stored in '$HOME/sdt/log' folder (single-user installation)
and '/var/log/synda/sdt' folder (multi-user installation).

## Download files using 'synda install' command

### Usage

To install a dataset

    synda install DATASET

    synda install [args] [options]

This command installs file(s) matching given search criteria. 

Note that two versions of the same dataset can be installed side by side (i.e.
versions are not mutualy exclusive).


### Example

Install a dataset

    synda get cmip5.output1.CCCma.CanESM2.historicalMisc.day.atmos.day.r2i1p4.v2

Install a variable

    synda get cmip5.output1.CCCma.CanESM2.historicalMisc.day.atmos.day.r2i1p4.v2

Install a file

    synda get cmip5.output1.CNRM-CERFACS.CNRM-CM5.rcp85.fx.atmos.fx.r0i0p0.v20130826.sftlf_fx_CNRM-CM5_rcp85_r0i0p0.nc

Install files using facets stored in an file. This example use
'sample_selection_01.txt' file which is available in the selection sample folder
($HOME/sdt/selection/sample).

    <-- 'sample_selection_01.txt'
    project="CMIP5"
    model="CNRM-CM5 CSIRO-Mk3-6-0"
    experiment="historical amip"
    ensemble="r1i1p1"
    variable[atmos][mon]="tasmin tas psl"
    variable[ocean][fx]="areacello sftof"
    variable[land][mon]="mrsos,nppRoot,nep"
    variable[seaIce][mon]="sic evap"
    variable[ocnBgchem][mon]="dissic fbddtalk"
    -->

    synda install -s sample_selection_01.txt

### Start/Stop files download

In single-user installation, run command below

    synda daemon [ start | stop ]

In multi-user installation, run command below

    service synda [ start | stop ]

### Error management

#### Changing replica for all file in errors

If download fails you can try another replica.

To change the replica for all files in error, use command below

    synda replica next

#### Getting more details about errors

Log files below contain useful informations about errors

* 'transfer.log' contains download status for each file.
* 'debug.log' contains 'wget' command log.
* 'discovery.log' contains search-api log.

Note: log files are stored in '$HOME/sdt/log' folder (single-user installation)
and '/var/log/synda/sdt' folder (multi-user installation).
