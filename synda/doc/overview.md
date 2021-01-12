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

To list facets

    synda param

To list facet values

    synda param FACET

To search datasets

    synda search FACET..

To download a dataset

    synda get DATASET

To download a dataset with tracking info

    synda install DATASET

## See also

* [User Guide](user_guide.md)
* [Download Tutorial](download_tutorial.md)
