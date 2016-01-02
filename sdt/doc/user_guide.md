# *synda* command user guide

synda - a file discovery and installation tool for Earth Science Grid Federation (ESGF) archive

## Synopsis

    synda COMMAND [args] [options]

## General

Synda downloads files from ESGF using HTTP or GridFtp protocol.

Search criteria called facets are used to select which files to download.

Search criteria can be set on command line

    synda search atmos fx CMIP5

or stored in a file

    synda search -s FILE

## Usage

To list datasets

    synda search FACETS

To install a dataset

    synda install DATASET

To remove a dataset

    synda remove DATASET

Note that 'install' command is asynchronous, which mean that the transfer is
handled by a background process. To check when the download is complete, you 
can display the download queue status with 'queue' command (see below).

## Command summary

### *daemon*

This command is for single-user installation only

(in multi-user installation, Synda daemon is installed as a service and is managed using 'service' command)

#### Example of use

Start the download daemon

    synda daemon start

Stop the download daemon

    synda daemon stop

### *install*

    synda install [args] [options]

This command installs file(s) matching given search criteria. 

Note that two versions of the same dataset can be installed side by side (i.e.
versions are not mutualy exclusive).

#### Example of use

Install a dataset

    synda install cmip5.output1.CCCma.CanESM2.historicalMisc.day.atmos.day.r2i1p4.v2

Install a variable

    synda install cmip5.output1.CCCma.CanESM2.historicalMisc.day.atmos.day.r2i1p4.v2

Install a file

    synda install cmip5.output1.CNRM-CERFACS.CNRM-CM5.rcp85.fx.atmos.fx.r0i0p0.v20130826.sftlf_fx_CNRM-CM5_rcp85_r0i0p0.nc

Install files using facets stored in an file. This example use
'sample_selection_1.txt' file which is available in the selection sample folder
($HOME/sdt/selection/sample).

    <-- 'sample_selection_1.txt'
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

    synda install -s sample_selection_1.txt

### *param*

Print ESGF parameters (aka facets aka search criteria)

To list all facets name

    synda param

To list all values of one facet

    synda param FACET

#### Example of use

    synda param project

### *queue*

Print the download queue

### *retry*

Retry transfer(s) in error.

### *search*

    synda search [args] [options]

#### Options 

    -r, --replica         show replica
    -z, --dry_run         display the query sent to the ESGF Search-API web service

Listing type can be specified using options below

    -a, --aggregation     same as --variable
    -d, --dataset         display dataset based listing
    -f, --file            display file based listing
    -v, --variable        display variable based listing

#### Example of use

List datasets (default)

    synda search CMIP5 frequency=day atmos tas -d

List variables

    synda search CMIP5 frequency=day atmos tas -v

List files

    synda search CMIP5 frequency=day atmos tas -f

### *show*

#### Example of use

Show dataset details

    synda show cmip5.output1.IPSL.IPSL-CM5A-LR.abrupt4xCO2.mon.atmos.Amon.r8i1p1.v20110726

Show file details

    synda show cmip5.output1.IPSL.IPSL-CM5A-LR.abrupt4xCO2.fx.land.fx.r0i0p0.v20110726.sftgif_fx_IPSL-CM5A-LR_abrupt4xCO2_r0i0p0.nc

### *stat*

#### Example of use

    synda stat ECMWF-ERAINT ALADIN52 frequency=day

### *version*

Print the different available versions for a dataset

#### Example of use

List all dataset versions

    synda version cmip5.output1.IPSL.IPSL-CM5A-LR.abrupt4xCO2.mon.atmos.Amon.r8i1p1.v20110726

### *watch*

List running transfer(s)

## More examples

    synda search project=CMIP5 realm=atmos
    synda search project=ISI-MIP%20Fasttrack searchapi_host=esg.pik-potsdam.de
    synda search realm=atmos project=CMIP5
    synda search atmos 5
    synda search MIROC rcp45 2
    synda search CCSM4 rcp45 atmos mon r1i1p1
    synda search c20c.UCT-CSAG.HadAM3P-N96.NonGHG-Hist.HadCM3-p50-est1.v1-0.mon.atmos.run060.v20140528
    synda search title=rlds_bced_1960_1999_gfdl-esm2m_rcp8p5_2051-2060.nc searchapi_host=esg.pik-potsdam.de
    synda search tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
    synda search tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613
    synda search dataset_id=tamip.output1.NCAR.CCSM4.tamip200904.3hr.atmos.3hrSlev.r9i1p1.v20120613|tds.ucar.edu
    synda search title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc project=EUCLIPSE
    synda search title=rlds_Amon_MPI-ESM-LR_amip_r1i1p1_1979-2008.nc
    synda search clt_day_CanESM2_esmControl_r1i1p1_19010101-22501231.nc
    synda search pr_day_MPI-ESM-LR_abrupt4xCO2_r1i1p1_18500101-18591231.nc
    synda search cmip5.output1.IPSL.IPSL-CM5A-LR.abrupt4xCO2.fx.land.fx.r0i0p0.v20110726.sftgif_fx_IPSL-CM5A-LR_abrupt4xCO2_r0i0p0.nc
    synda search variable=tas institute!=MPI-M
