#!/bin/bash
##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

# This script retrieve a file from ESGF using GRID-FTP protocol

# Note
#  this script displays checksum on stdout.
#  (so don't print anything except the checksum on stdout)
#
# Return values
#   0  success
#   1  error
#   3  incorrect arguments
#   7  this script has been killed (SIGINT or SIGTERM)
#  29  child process has been killed (most likely caused by a "shutdown immediate")
#  30  file creation error (likely caused by missing access right)

usage ()
{
    echo ""
    echo "Usage"
    echo "  $0 [ -d <1|2|3|4> ] [ -c <sha256|md5> ] <src> <dest>"
    echo ""
    echo "Options:"
    echo "  -c      checksum type (default md5)"
    echo "  -d      debug level"
    echo ""
    echo "Example"
    echo "  $0 -d 2 gsiftp://albedo2.dkrz.de:2811//cmip5/output1/BNU/BNU-ESM/1pctCO2/mon/seaIce/OImon/r1i1p1/v20120503/grCongel/grCongel_OImon_BNU-ESM_1pctCO2_r1i1p1_185001-198912.nc /dev/null"
    echo "  $0 gsiftp://carbon.dkrz.de:2811/cmip5/output1/MPI-M/MPI-ESM-LR/amip/mon/atmos/Amon/r1i1p1/v20111005/cl/cl_Amon_MPI-ESM-LR_amip_r1i1p1_197901-198912.nc /tmp/sdt_test_file.nc"
}

curdate ()
{
    date '+%F %T'
}

msg ()
{
    l__code="$1"
    l__msg="$2"

    echo "$(curdate) - $l__code - $l__msg"
}

cleanup_on_error ()
{
    kill -TERM "$child_pid" 1>/dev/null 2>/dev/null # kill child if still running
    rm -f "$local_file"
}

abort ()
{
    cleanup_on_error
    exit 7
}

# signal

trap "abort" SIGINT SIGTERM

# mask

umask u=rw,g=rw,o=r # set 'cmip5' group writable

# retrieve options

g__debug_level=
g__checksum_type=md5
while getopts 'c:d:h' OPTION
do
  case $OPTION in
  c)    g__checksum_type=$OPTARG
        ;;
  d)    g__debug_level=$OPTARG
        ;;
  h)    usage
        exit 0
        ;;
  esac
done
shift $(($OPTIND - 1)) # remove options

############################################
# manage checksum type
g__checksum_cmd=
if [ "$g__checksum_type" = "sha256" ]; then
    g__checksum_cmd="openssl dgst -sha256 | awk '{if (NF==2) print \$2 ; else print \$1}' "
elif [ "$g__checksum_type" = "md5" ]; then
    g__checksum_cmd="md5sum  | awk '{print \$1}' "
elif [ "$g__checksum_type" = "MD5" ]; then # HACK: some checksum types are uppercase
    g__checksum_cmd="md5sum  | awk '{print \$1}' "
else
    :

    # do not raise error here anymore, as some ESGF files do not have checksum (but we still want to retrieve them)
    #
    #msg "ERR005" "incorrect checksum type ($g__checksum_type)" | tee -a $g__log_file
    #exit 5
fi

############################################
# retrieve positional arguments

url="$1"
local_file="$2"

############################################
# check arguments

if [ -z "$local_file" ]; then
    usage
    exit 3
fi

if [ -z "$url" ]; then
    usage
    exit 3
fi

# prevent download if path not starting with '/'
if [[ "${local_file:0:1}" = "/" ]]; then # check for starting slash
    :
else
    msg "ERR004" " incorrect format (local_file=$local_file)"
    exit 3
fi

# check if file is already present
if [ -f "$local_file" ]; then
    msg "ERR011" "local file already exists ($local_file)" | tee -a $g__log_file
    exit 3
fi

# check if we have right to create local file
if touch "$local_file"; then # not that touch error msg is lost here (sent to stderr)
    rm "$local_file"
else
    msg "ERR111" "local file creation error ($local_file)" | tee -a $g__log_file
    exit 30
fi

############################################
# init
#

# set root folder
if [ -z "$ST_HOME" ]; then
    msg "ERR008" "root directory not found ($ST_HOME)"
    exit 4
else
    SYNCDA_ROOT=${ST_HOME}
fi

export LANG=C
export LC_ALL=C

export ESGF_SECURITY_ROOT=$HOME/.esg
export ESGF_CREDENTIAL=$ESGF_SECURITY_ROOT/credentials.pem 

export X509_USER_CERT=$ESGF_CREDENTIAL
export X509_USER_KEY=$ESGF_CREDENTIAL
export X509_USER_PROXY=$ESGF_CREDENTIAL
export X509_CERT_DIR=$ESGF_SECURITY_ROOT/certificates

GRIDFTP_CMD=globus-url-copy

child_pid=

g__log_dir=$SYNCDA_ROOT/log
g__log_file=${g__log_dir}/get_data.log

############################################
# gridftp debug parameters
#
# debug mode
if [ -n "$g__debug_level" ]; then
    if [ $g__debug_level -eq 4 ]; then
        set -x # bash debug mode (warning, this make globus-url-copy output to be duplicated 3 times)

        export GLOBUS_ERROR_OUTPUT=1
        export GLOBUS_ERROR_VERBOSE=1
        export GLOBUS_GSI_AUTHZ_DEBUG_LEVEL=2
        export GLOBUS_GSI_AUTHZ_DEBUG_FILE=/tmp/AUTHMODULELOG

        GRIDFTP_DEBUG_OPT=" -v -vb -dbg "
    elif [ $g__debug_level -eq 3 ]; then
        GRIDFTP_DEBUG_OPT=" -v -vb -dbg "
    elif [ $g__debug_level -eq 2 ]; then
        GRIDFTP_DEBUG_OPT=" -v -vb "
    elif [ $g__debug_level -eq 1 ]; then
        GRIDFTP_DEBUG_OPT=" -v "
    fi
else
    GRIDFTP_DEBUG_OPT=
fi

############################################
# set environment

mkdir -p ${g__log_dir}

# create local folder if not exists
local_folder=`dirname $local_file` # retrieve destination folder
mkdir -p ${local_folder}

CMD="$GRIDFTP_CMD $GRIDFTP_DEBUG_OPT $url $local_file"

############################################
# start transfer
#
child_status=0
if [ -n "$g__debug_level" ]; then
    echo $WGET_CMD
    eval $WGET_CMD 2>&1
    child_status=$?
    child_pid=$!
else
    wget_stdxxx=`eval $WGET_CMD 2>&1`
    child_status=$?
fi

############################################
# post-processing
#
if [ $child_status -ne 0 ]; then
    if [ $child_status -eq 143 ]; then # 143 means 'wget' gets killed
        status=29
    else
        status=$child_status
    fi

    cleanup_on_error # remove local file (this is to not have thousand of empty files)

    msg "ERR001" "Transfer failed with error $status - $* - $child_status" | tee -a $g__log_file

    exit $status
else
    # success

    # retrieve checksum
    l__checksum=$(cat $local_file | $g__checksum_cmd)

    # return checksum
    echo $l__checksum

    msg "INF003" "transfer done - $* - $l__checksum" >> $g__log_file

    exit 0
fi
