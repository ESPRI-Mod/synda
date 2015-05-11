# Synda Transfer - administration guide

## Introduction

This document describes how to use synda software to create an ESGF archives
partial mirror on a local cluster and keep it up to date.

## Installation

See https://github.com/Prodiguer/synda

## Selection file

To select which data to download, you need to set filters. Filters are stored
in selection files (aka template). Those selection files are stored in
'$HOME/sdt/selection' folder.

Example of a selection file

    <--
    project=CMIP5
    model=CNRM-CM5 CSIRO-Mk3-6-0
    experiment=historical amip
    ensemble=r1i1p1
    variable[atmos][mon]=tasmin tas psl
    variable[ocean][fx]=areacello sftof
    variable[land][mon]=mrsos,nppRoot,nep
    variable[seaIce][mon]=sic evap
    variable[ocnBgchem][mon]=dissic fbddtalk
    -->

### Adding a selection file

Create a new file in '$HOME/sdt/selection' folder and set the filters.

Stop the daemon

    synda daemon stop

Run commands below to start the discovery

    synda install -s <selection-file>

Then start the daemon to begin the download

    synda daemon start

### Modifying a selection file

Edit the file and change filters accordingly.

Then run commands below

    synda daemon stop
    synda install -s <selection-file>
    synda daemon start

### Removing a selection file

Run commands below

    synda daemon stop
    synda remove -s <selection-file>

Then remove the file from the '$HOME/sdt/selection' folder.

## Retrieving new dataset versions for all selection files

Run commands below

    synda daemon stop
    synda upgrade

## Removing old dataset versions for all selection files

Run commands below

    synda daemon stop
    synda autoremove

## Watching download progress

Commands below give informations about download queue state

    synda queue
    synda watch

## Error management

Errors can occur during download for different reasons: remove server is down,
incorrect files access right, authorization issue, authentication issue..
Sections below are intended to help diagnose and solve those issues.

### Displaying errors

Command below can be used to print how many error occured

    synda queue

### Retrying download in errors

Command below can be used to retry transfer(s) in error.

    synda retry

Note: crontab can be used to retry errors every day

### Changing replica for all files in errors

Sometime, current file replica always fails as the remote server is down. One
way to solve the problem is to change the file replica. 

To change the replica for all files in error, use command below

    synda replica next

### Getting more details about errors

Log files below contain useful informations about errors (log files are stored
in '$HOME/sdt/log' folder)

* 'transfer.log' contains a download status for each file.
* 'get_data.log' contains 'sdget.sh' script log.
* 'get_data__debug.log' contains 'wget' command log.
* 'discovery.log' contains search-api log.
