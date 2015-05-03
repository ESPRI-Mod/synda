# Select which ESGF index to use

Synda index settings are stored in sdt.conf in [index] section.

* *default_index* parameter is used for interactive search operations.
* *indexes* parameter is used for parallel searches (to improve response time by distributing queries on several indexes simultaneously).

Note: host set in *default_index* parameter can also be set in *indexes* parameter (i.e. used at both places).

## Usage

    default_index=<index>
    indexes=<idx1,idx2,etc..>

## ESGF main indexes

* esg-datanode.jpl.nasa.gov
* esgf-node.ipsl.fr
* esgf-data.dkrz.de
* esgf-index1.ceda.ac.uk
* esg.ccs.ornl.gov

