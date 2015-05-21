# Gridftp howto

## Usage examples

Print gridftp url for a given file

    synda dump cmip5.output1.MPI-M.MPI-ESM-LR.1pctCO2.day.atmos.cfDay.r1i1p1.v20120314.albisccp_cfDay_MPI-ESM-LR_1pctCO2_r1i1p1_19700101-19891231.nc limit=1 protocol=gridftp replica=false -nf -C url

Print a random gridftp url

    synda dump data_node=bmbf-ipcc-ar5.dkrz.de limit=1 protocol=gridftp -nf -C url

Add files in download queue using gridftp protocol

    synda install data_node=bmbf-ipcc-ar5.dkrz.de limit=1 protocol=gridftp

Note that files not available gridftp protocol is not available, http protocol is used

## Set 

To use gridftp as default protocol, edit $ST_HOME/conf/default/default.txt file 
and set 'protocol' parameter to 'gridftp'.
