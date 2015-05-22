# Gridftp Howto

# Installation

globus-url-copy additional program is needed to transfer files over GridFtp.

On Debian, it is part of the 'globus-gass-copy-progs' package and can be installed with:

    apt-get install globus-gass-copy-progs

## Configuration

To use gridftp as default protocol, edit $ST_HOME/conf/default/default.txt file 
and set 'protocol' parameter to 'gridftp'.

## Usage examples

Print gridftp url for a given file

    synda dump cmip5.output1.MPI-M.MPI-ESM-LR.1pctCO2.day.atmos.cfDay.r1i1p1.v20120314.albisccp_cfDay_MPI-ESM-LR_1pctCO2_r1i1p1_19700101-19891231.nc limit=1 protocol=gridftp replica=false -nf -C url

Print a random gridftp url

    synda dump data_node=bmbf-ipcc-ar5.dkrz.de limit=1 protocol=gridftp -nf -C url

Add files in download queue using gridftp protocol

    synda install cmip5.output1.MPI-M.MPI-ESM-LR.decadal1995.mon.land.Lmon.r2i1p1.v20120529 protocol=gridftp

## Note

When gridftp protocol is not available, http protocol is used instead. 

This is why the command below returns a mix of gridftp url and http url

    synda dump protocol=gridftp variable=tas limit=1000  -f -C url
