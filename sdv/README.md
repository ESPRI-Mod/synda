# Synda validation module

This module contains UAT tests.

## Test environment setup

To set up a test environment, you will need to install:

* Synda
* Test scripts dependencies
* Test scripts

### Synda installation

Log on the test machine.

Install Synda (from source or system package) using [this link](https://github.com/Prodiguer/synda#installation)

Note: depending on which tests to run, SDT module, SDP module or both must be installed.

### Test scripts dependencies installation

Test scripts need the *fabric* python package

To install it, run

    aptitude install fabric

### Test scripts installation

Run commands below

    mkdir synda_UAT
    cd synda_UAT
    git clone git://github.com/Prodiguer/synda.git
    cd synda/sdv

## Test execution procedure

To execute a test, run commands below

    cd <testname>
    /usr/bin/python <testname>.py

Example

    cd svincrdiscover
    /usr/bin/python svincrdiscover.py
