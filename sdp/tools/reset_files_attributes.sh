#!/bin/bash -e
#
# Description
#  File attributes reset
#
# Usage
#  Run the script without argument as root

cmip5_path=/data/esg/CMIP5
owner=
group=

echo "Reset files attributes script started at $(date)"

for d in output1 output2 process merge; do
    cd $cmip5_path/$d

    echo "Processing '$(pwd)' folder"

    # store files list in tmp file
    echo "Building files list"
    tmpfile=$(mktemp /tmp/reset_files_attributes_$$_XXXXXXX)
    find $(ls | grep -v IPSL) ! -type l -print0 > $tmpfile

    # set owner & group
    echo "Setting files ownership"
    cat $tmpfile | xargs -0 chown $owner:$group

    # set write accesses right
    echo "Setting files access permissions"
    cat $tmpfile | xargs -0 chmod g+w

    # flag du gid sur le groupe pour tous les dossiers CMIP5 (hors IPSL)
    find $(ls | grep -v IPSL) -type d -print0 | xargs -0 chmod g+s
done

echo "Script completed at $(date)"
