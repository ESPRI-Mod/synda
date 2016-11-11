#!/bin/bash -e

# Description
#   Creates hardlinks in "<ROOT>/esgf/process" tree for every "<ROOT>/esgf/mirror" files.
#   Processes by variable.
#
# Notes
#   - the process is incremental ("process" tree is not removed every night)
#   - rsync '--delete' can't be used, as we merge TWO directory into one
#    (i.e. '--delete' only work with one directory mirroring one directory)
#   - trailing slash is mandatory in input
#
# Usage
#   ./coalesce.sh <PROJECT> <SCR_PATH> <DEST_PATH>
#
# Input
#   The project ID
#   <PROJECT>
#   An atomic dataset full path as the directory that contains NetCDF files
#   <SRC_PATH>  : /prodigfs/esgf/mirror/<PROJECT>/<downstream_DRS>/
#
# Output
#   An atomic dataset full path as the directory that contains hardlinks
#   <DEST_PATH> : /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>/

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

send_mail()
{
    DEST=${1}
    TEXT=${2}
    # Send email to data provider in argument
    if [ -n "${DEST}" ]; then
        echo "$TEXT" | mail -s "SYNDA: Duplicated CMIP5 files in output1 and output2" "${DEST}"
    fi
}


# --------- arguments & initialization --------- #

while [ "${1}" != "" ]; do
    case "${1}" in
        # Project ID/Facet
        "--project")            shift; project="${1}"        ;;

        # /prodigfs/esgf/mirror/<PROJECT>/<downstream_DRS>
        "--src_variable_path")  shift; mirror_path="${1}"    ;;

        # /prodigfs/esgf/process/<PROJECT>/<downstream_DRS>
        "--dest_variable_path") shift; process_path="${1}"   ;;
    esac
    shift
done

if [ ${project} == "CMIP5" ]; then
    output1_path=$( echo "${mirror_path}" | sed 's|/\*/|/output1/|' )  # /prodigfs/esgf/mirror/CMIP5/output1/<downstream_DRS>
    output2_path=$( echo "${mirror_path}" | sed 's|/\*/|/output2/|' )  # /prodigfs/esgf/mirror/CMIP5/output2/<downstream_DRS>
fi


# --------- main --------- #

msg "INFO" "coalesce.sh started (variable = ${mirror_path})"

# This is needed, because rsync expects destination path to exist (or at least parent folders in destination path).
# More info: http://www.schwertly.com/2013/07/forcing-rsync-to-create-a-remote-path-using-rsync-path/
umask g+w
mkdir -p ${process_path}
umask g-w

if [ ${project} == "CMIP5" ]; then

    if [ -d ${output1_path} -a -d ${output2_path} ]; then

        nbr=$( comm -12  <(ls ${output1_path} | sort ) <(ls ${output2_path} | sort ) | wc -l ) # List files that intersect both outputs

        if [ ${nbr} -gt 0 ]; then
            # Duplicate(s) found
            msg "INFO" "${nbr} duplicate(s) found b/w output1 and output2 (${mirror_path})"
            # Notification to administrator -> To forward to modeling center/data provider/manager?
            send_mail "glipsl@ipsl.jussieu.fr" "${nbr} duplicate(s) found b/w output1 and output2.\n$( comm -12  <(ls ${output1_path} | sort ) <(ls ${output2_path} | sort ))"

            # Merge using ln as this case is difficult to solve with rsync (rsync copy file instead of linking when file exists in destination (maybe lustre specific)). It was decided to merge duplicated from output1.
            cd ${process_path}
            for f in $( ls ${output1_path} ); do
                ln ${output1_path}${f} ${f}
            done
            for f in $( comm -13  <(ls ${output1_path} | sort ) <(ls ${output2_path} | sort ) ); do # List files that exist in output2 only
                ln ${output2_path}${f} ${f}
            done
        else
            if [ -d ${output1_path} ]; then
                /usr/bin/rsync -viax --link-dest=${output1_path} ${output1_path} ${process_path}
            fi

            if [ -d ${output2_path} ]; then
                /usr/bin/rsync -viax --link-dest=${output2_path} ${output2_path} ${process_path}
            fi
        fi
    else
        if [ -d ${output1_path} ]; then
            /usr/bin/rsync -viax --link-dest=${output1_path} ${output1_path} ${process_path}
        fi

        if [ -d ${output2_path} ]; then
            /usr/bin/rsync -viax --link-dest=${output2_path} ${output2_path} ${process_path}
        fi
    fi

else

    if [ -d ${mirror_path} ]; then
        /usr/bin/rsync -viax --link-dest=${mirror_path} ${mirror_path} ${process_path}
    fi

fi

msg "INFO" "coalesce.sh complete"
