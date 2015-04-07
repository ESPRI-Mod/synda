#!/bin/bash -e
##################################
#  @program        synchro-data
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

# Description
#   This script set 'latest' for xml file
#
# Usage
#   ./latest_xml.sh <path> 
#
# Input
#   dataset full path (e.g. <PREFIX>/esg/CMIP5/process/MIROC/MIROC-ESM/historicalNat/mon/atmos/Amon/r1i1p1/v20120710/)
#
# Output
#   None

# ------ functions ------ #

curdate ()
{
    date +'%Y/%m/%d %I:%M:%S %p'
}

msg ()
{
    l__code="${1}"
    l__msg="${2}"

    echo "$(curdate) ${l__code} ${l__msg}" 1>&2
}


# --------- arguments & initialization --------- #

dataset_path="${1}"
dataset_dir=$( dirname $dataset_path)
dataset_version=$( basename $dataset_path )


# --------- main --------- #

msg "INFO" "latest_xml.sh started (dataset_path = ${dataset_path}"

for variable_path in $( find ${dataset_path}*/ -type d ) ; do
	cd $( echo ${variable_path} | awk -F '/' '{print "/prodigfs/esg/xml/"$4"/"$8"/"$10"/"$9"/"$14}' )
    
	xml=$( echo ${variable_path} | awk -F '/' '{print tolower($4)"."$7"."$8"."$12"."$9"."$10"."$11"."$14"."$13".xml"}' )
	xml_latest=$( echo ${variable_path} | awk -F '/' '{print tolower($4)"."$7"."$8"."$12"."$9"."$10"."$11"."$14".latest.xml"}' )
    
    # Unlink existing xml latest symlink
    if [ -h "${xml_latest}" ] ; then
        unlink ${xml_latest}
    fi

    # xml latest symlink
	ln -s ${xml} ${xml_latest}		
	
    cd - >/dev/null 2>&1
done

msg "INFO" "latest_xml.sh complete"
