# Gridftp Howto

## Installation

*globus-url-copy* additional program is needed to transfer files with GridFtp.

It is part of the 'globus-gass-copy-progs' package and can be installed using
instructions below.

### Debian and derivative

Install the package with

    sudo apt-get install globus-gass-copy-progs

### RHEL and derivative

You need to install EPEL repository

    sudo yum install epel-release -y

then install the package with

    sudo yum install globus-gass-copy-progs

## Configuration

To use gridftp as default protocol, add 'protocol=gridftp' parameter in default.txt file.

Note that default.txt file location differs depending on which synda installation method has been used.

For source installation, location is:

    $ST_HOME/conf/default/default.txt

For system package installation, location is:

    /etc/synda/sdt/default/default.txt

## Usage

Download a file using gridftp protocol

    synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 pastureFrac protocol=gridftp

## Miscellaneous Information

Print gridftp url for a given file

    synda dump cmip5.output1.MPI-M.MPI-ESM-LR.1pctCO2.day.atmos.cfDay.r1i1p1.v20120314.albisccp_cfDay_MPI-ESM-LR_1pctCO2_r1i1p1_19700101-19891231.nc limit=1 protocol=gridftp replica=false -nf -C url

Print a random gridftp url

    synda dump data_node=bmbf-ipcc-ar5.dkrz.de limit=1 protocol=gridftp -nf -C url

Print a list of gridftp urls

    synda dump protocol=gridftp variable=tas limit=1000 -f -C url

(in this last example, the command returns a mix of gridftp url and http
url. This is because when gridftp protocol is not available, http protocol is
used instead)
