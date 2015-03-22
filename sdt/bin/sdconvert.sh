#!/bin/bash

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sd28to29.sh 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
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
