#!/bin/bash -e

# Description
#   This script publishes mapfiles.
#   Processes by dataset.

# --------- arguments & initialization --------- #

while [ "${1}" != "" ]; do
    case "${1}" in
        "--project")         shift; project="${1}"       ;;
        "--dataset_pattern") shift; input_dataset="${1}" ;;
        "--script-dir")      shift; scripts_path="${1}"  ;;
        "--worker-log")      shift; LOGFILE="${1}"       ;;
    esac
    shift
done

source ${scripts_path}/functions.sh

# INI files directory
ESGCET_PATH="/esg/config/esgcet/"
# Indexnode hostname
MYPROXY_HOST="esgf-node.fr"
# myproxy-logon port
MYPROXY_PORT="7512"
# Publisher's openID login registered
MYPROXY_LOGIN="xxxxxxxx"
# Publisher's openID password
MYPROXY_PASSWD="xxxxxxxx"
# Root path
ROOT_PATH="/your/data/path"
# Mapfile directory
MAP_DIR="/your/mapfiles/path"

# --------- main --------- #

msg "INFO" "publication.sh started"

# Loads ESGF environment
source /etc/esg.env

# Checkup directories and temporary files
if [ ! -d ${ESGCET_PATH} ]; then
    msg "ERROR" "${ESGCET_PATH} does not exist. STOP." >&2
    exit 1
fi
if [ ! -d ${HOME}/.globus ]; then
    msg "ERROR" "${HOME}/.globus does not exist. STOP." >&2
    exit 1
fi
if [ -f ${HOME}/.globus/certificate-file ]; then
    msg "WARNING" "${HOME}/.globus/certificate-file already exists. Deleted." >&2
    rm -f ${HOME}/.globus/certificate-file
fi

# Retrieve mapfile name with an esgprep dry run
uuid=$(uuidgen)
esgprep mapfile -i ${ESGCET_PATH} -v \
                --project ${project,,} \
                --outdir /tmp/map \
                --no-checksum\
                --mapfile "{dataset_id}.{version}.${uuid}" \
                ${ROOT_PATH}${input_dataset} 1>&2 2> /dev/null
mapfile_orig=$(ls /tmp/map | grep "${uuid}")
mapfile=$(echo ${mapfile_orig} | sed "s|\.${uuid}||g")
rm -fr /tmp/map/${mapfile_orig}

# Gets proxy certificates for publication
msg "INFO"  "Get ESGF certificates..."
echo ${MYPROXY_PASSWD} | myproxy-logon -b -T -s ${MYPROXY_HOST} -p ${MYPROXY_PORT} -l ${MYPROXY_LOGIN} -o ${HOME}/.globus/certificate-file -S

# Initialize node and controlled vocabulary
esginitialize -c -i ${ESGCET_PATH}

msg "INFO"  "Unpublishing ${mapfile} if exists..."
# Unpublication
esgunpublish -i ${ESGCET_PATH} \
             --database-delete \
             --no-republish \
             --map ${MAP_DIR}${mapfile}
msg "INFO"  "Publishing ${mapfile} on datanode..."
# Datanode publication
esgpublish -i ${ESGCET_PATH} \
           --project ${project,,} \
           --thredds \
           --service fileservice \
           --set-replica \
           --map ${MAP_DIR}${mapfile}
msg "INFO"  "Publishing ${mapfile} on indexnode..."
#Indexnode publication
esgpublish -i ${ESGCET_PATH} \
           --project ${project,,} \
           --publish \
           --noscan \
           --service fileservice \
           --set-replica \
           --map ${MAP_DIR}${mapfile}

msg "INFO" "publication.sh complete"
