# Synda validation module

This module contains UAT tests.

## Test execution procedure

To run a test, follow the steps below

### Synda installation

Log on the test machine.

Install Synda (from source or system package).

Note: depending on which tests to run, SDT module, SDP module or both must be installed.

### Test scripts dependency

Test scripts need the *fabric* python package

To install it, run

    aptitude install fabric

### Test scripts installation

Run commands below

    mkdir UAT_test
    cd UAT_test
    git clone git://github.com/Prodiguer/synda.git
    cd synda/sdv

### Test execution

Run command below

    /usr/bin/python <testname>.py

Example

    /usr/bin/python svincrdiscover.py
