#!/bin/bash

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

# This script transform 2.8 selection file into 2.9 selection file.

if [ $# -eq 0 ]; then
    echo "Usage: $0 FILE"
    exit 2
fi

file=$1

# rename fields
sed -i 's/^tablename/cmor_table/;s/^group/sgroup/;s/^ensembles/ensemble/;s/^2D_variables/variable/;s/^3D_variables/variable/;s/^variables/variable/;s/^experiments/experiment/g;s/^models/model/g' $file

# remove obsolete 'fullscan' line
sed -i '/^fullscan/d' $file

echo "$file modified."

exit 0
