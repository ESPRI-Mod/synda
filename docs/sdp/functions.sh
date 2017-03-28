#!/bin/bash -e

# Description
#   This script gathers useful functions used by post-processing scripts.

curdate ()
{
    date +'%Y/%m/%d %I:%M:%S %p'
}

msg ()
{
    LEVEL="${1}"
    MSG="${2}"
    if [ ! -z ${LOGFILE} ] && [ -f ${LOGFILE} ]; then
        echo "$(curdate) ${LEVEL} ${MSG}" 1>> ${LOGFILE}
    else
        echo "$(curdate) ${LEVEL} ${MSG}" 2>&1
    fi
}

send_mail ()
{
    DEST="${1}"
    TEXT="${2}"
    OBJ="${3}"
    # Send email to data provider in argument
    if [ -n "${DEST}" ]; then
        echo "${TEXT}" | mail -s "${OBJ}" "${DEST}"
    fi
}

get_facet_from_path ()
{
    key="${1}"  # The facet key to get the value
    path="${2}" # The input path to match
    drs="${3}"  # The corresponding DRS template

	l__path=$(echo ${path} | awk -F "/" '{print NF}')
	l__drs=$(echo ${drs} | awk -F "/" '{print NF}')

	offset=$(echo "${l__path} - ${l__drs}" | bc)
	key_rank=$(echo ${drs} |  awk -F "/" '{for (i=1;i<=NF;i++){if ($i == "'${key}'"){print i}}}')
    if [ -z ${key_rank} ]; then
	    exit 1
    else
	    value_rank=$(echo "${key_rank} + ${offset}" | bc)
        value=$(echo ${path} | awk -F "/" '{print $'${value_rank}'}')
        echo ${value}
    fi
}
