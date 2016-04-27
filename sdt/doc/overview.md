# Synda overview

## Synopsis

This document describes how to search and download files from ESGF archives with Synda.

## General

Synda downloads files using HTTP or GridFtp protocol.

Search criteria called facets are used to select which files to download.

Search criteria can be set on command line

    synda search atmos fx CMIP5

or stored in a file

    synda search -s FILE

## Usage

To search datasets

    synda search FACETS

To download a dataset in direct mode (synchronous)

    synda get DATASET

To download a dataset in daemon mode (asynchronous)

    synda install DATASET

## Notes

For more information about direct mode download, see link below

* [Direct Mode Download Guide](sync_download_guide.md)

For more information about async mode download, see links below

* [Async Download Guide](async_download_guide.md)
* [Async Download Tutorial](async_download_tutorial.md)
