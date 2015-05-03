# Select which ESGF index to use

Synda index settings are stored in sdt.conf in [index] section.

*default_index* parameter is used for interactive search operations.

*indexes* parameter is used for parallel search (to improve response time by distributing queries on several indexes simultaneously).

Most of the time, the default index is set at both place (i.e. in *default_index* and in *indexes*)

## Usage

    default_index=<index>
    indexes=<idx1,idx2,etc..>

## ESGF main indexes

* esg-datanode.jpl.nasa.gov
* esgf-node.ipsl.fr
* esgf-data.dkrz.de
* esgf-index1.ceda.ac.uk
* esg.ccs.ornl.gov

