# Gridftp howto

## Configuration

To use gridftp as default protocol, edit $ST_HOME/conf/default/default.txt file 
and set 'protocol' parameter to 'gridftp'.

## Usage examples

Print a random gridftp url

    synda dump data_node=bmbf-ipcc-ar5.dkrz.de limit=1 protocol=gridftp -nf -C url

Add files using gridftp protocol

    synda install limit=1 protocol=gridftp -nf -C url

Note that files not available gridftp protocol is not available, http protocol is used
