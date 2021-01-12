# ESGF replication howto

## Introduction

This document describes how to create an ESGF archives partial mirror on a
local cluster and keep it up to date.

## Synda installation

See [Installation guide](https://github.com/Prodiguer/synda#installation)

## Create a selection file to describe which data to replicate

See [Selection file](selection_file.md)

Notes: 

* You can create many selection files (e.g. one per project)
* Selection file(s) must be stored in the 'selection' folder

## File discovery

To start file discovery, run command below

    synda upgrade

At this point, files metadata are stored in local database and data download can begin.

## Files download

### Start

To start the download, Synda service (aka Synda daemon) must be started.

In single-user installation, run command below

    synda daemon start

In multi-user installation, run command below

    service synda start

### Stop

To stop the download, Synda service must be stopped.

In single-user installation, run command below

    synda daemon stop

In multi-user installation, run command below

    service synda stop

## Watching download progress

Commands below give download status and progress

    synda queue
    synda watch

## Version management

In ESGF, a dataset can change over time and thus have several versions.

### Update datasets to the last version

Re-run the discovery to search for new versions

    synda upgrade

Then start the Synda service to start the download of new versions if any.

### Remove old datasets version

Run command below

    synda autoremove

## Error management

Errors can occur during download for different reasons: remote server is down,
incorrect files access right, authorization issue, authentication issue..

Sections below are intended to help diagnose and solve those issues.

### Displaying errors

Command below can be used to print how many error occured

    synda queue

### Retrying download in errors

Command below can be used to retry transfer(s) in error.

    synda retry

Note: crontab can be used to retry errors (e.g. every day)

### Changing replica for all files in errors

Sometime, current file replica always fails as the remote server is down. One
way to solve the problem is to change the file replica. 

To change the replica for all files in error, use command below

    synda replica next

### Getting more details about errors

Log files below contain useful informations about errors

* 'transfer.log' contains download status for each file.
* 'debug.log' contains 'wget' command log.
* 'discovery.log' contains search-api log.

Note: log files are stored in '$HOME/sdt/log' folder (single-user installation)
and '/var/log/synda/sdt' folder (multi-user installation).
