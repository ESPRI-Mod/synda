#!/bin/bash
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# This script retrieves a file from ESGF using GRID-FTP protocol

# Note
#  This script displays checksum on stdout.
#  (so don't print anything except the checksum on stdout)
#
# Return values
#   0  success
#   1  error
#   3  incorrect arguments
#   4  incorrect environment (fatal error, make the daemon to stop)
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
    echo "  $0 -d 2 gsiftp://bmbf-ipcc-ar5.dkrz.de:2811//cmip5/output1/MPI-M/MPI-ESM-LR/1pctCO2/mon/ocean/Omon/r1i1p1/v20120308/soga/soga_Omon_MPI-ESM-LR_1pctCO2_r1i1p1_199001-199912.nc /tmp/sdt_test_file.nc"
}

curdate ()
{
    date '+%F %T'
}

msg ()
{
    local msg="$1"

    echo "$msg" 1>&2 # stderr
    #echo $buf
}

cleanup_on_error ()
{
    rm -f "$local_file"
}

abort ()
{
    cleanup_on_error
    exit 7
}

# path

export PATH=/sbin:/bin:/usr/sbin:/usr/bin

# signal

trap "abort" SIGINT SIGTERM

# mask

umask u=rw,g=rw,o=r # set 'cmip5' group writable

# retrieve options

debug_level=0
checksum_type=md5
while getopts 'c:d:h' OPTION
do
  case $OPTION in
  c)    checksum_type=$OPTARG
        ;;
  d)    debug_level=$OPTARG
        ;;
  h)    usage
        exit 0
        ;;
  esac
done
shift $(($OPTIND - 1)) # remove options

############################################
# set checksum command depending on checksum type
checksum_cmd=
if [ "$checksum_type" = "sha256" ]; then
    checksum_cmd="openssl dgst -sha256 | awk '{if (NF==2) print \$2 ; else print \$1}' "
elif [ "$checksum_type" = "md5" ]; then
    checksum_cmd="md5sum  | awk '{print \$1}' "
elif [ "$checksum_type" = "MD5" ]; then # HACK: some checksum types are uppercase
    checksum_cmd="md5sum  | awk '{print \$1}' "
else
    :

    # do not raise error here anymore, as some ESGF files do not have checksum (but we still want to retrieve them)
    #
    #err "incorrect checksum type ($checksum_type)"
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
    err "incorrect format (local_file=$local_file)"
    exit 3
fi

# check if file is already present
if [ -e "$local_file" ]; then # use '-e' instead of '-f' to also prevent /dev/null to be used
    err "local file already exists ($local_file)"
    exit 3
fi

# check if we have right to create local file
if touch "$local_file"; then # not that touch error msg is lost here (sent to stderr)
    rm "$local_file"
else
    err "local file creation error ($local_file)"
    exit 30
fi

############################################
# init
#

multiuser="0"

if [ "$multiuser" = "0" ]; then
    certdirprefix=$HOME
else
    certdirprefix=/var/tmp/synda/sdt
fi

export LANG=C
export LC_ALL=C

export ESGF_SECURITY_ROOT=$certdirprefix/.esg
export ESGF_CREDENTIAL=$ESGF_SECURITY_ROOT/credentials.pem 

export X509_USER_CERT=$ESGF_CREDENTIAL
export X509_USER_KEY=$ESGF_CREDENTIAL
export X509_USER_PROXY=$ESGF_CREDENTIAL
export X509_CERT_DIR=$ESGF_SECURITY_ROOT/certificates

GRIDFTP_CMD=globus-url-copy

local_folder=`dirname $local_file` # retrieve destination folder

############################################
# gridftp debug parameters
#
# debug mode
if [ $debug_level -eq 4 ]; then
    set -x # bash debug mode (warning, this make globus-url-copy output to be duplicated 3 times)

    export GLOBUS_ERROR_OUTPUT=1
    export GLOBUS_ERROR_VERBOSE=1
    export GLOBUS_GSI_AUTHZ_DEBUG_LEVEL=2
    export GLOBUS_GSI_AUTHZ_DEBUG_FILE=/tmp/gridftp_debug.log

    GRIDFTP_DEBUG_OPT=" -v -vb -dbg "
elif [ $debug_level -eq 3 ]; then
    GRIDFTP_DEBUG_OPT=" -v -vb -dbg "
elif [ $debug_level -eq 2 ]; then
    GRIDFTP_DEBUG_OPT=" -v -vb "
elif [ $debug_level -eq 1 ]; then
    GRIDFTP_DEBUG_OPT=" -v "
elif [ $debug_level -eq 0 ]; then
    GRIDFTP_DEBUG_OPT=
fi

############################################
# create folder

mkdir -p ${local_folder}

############################################
# start transfer

CMD="$GRIDFTP_CMD $GRIDFTP_DEBUG_OPT $url $local_file"

if [[ $debug_level > 0 ]]; then
    echo $CMD
    $CMD 1>&2
else
    $CMD 1>&2
fi

child_status=$?

############################################
# post-processing
#
if [ $child_status -ne 0 ]; then
    # error

    if [ $child_status -eq 143 ]; then # 143 means 'wget' gets killed
        status=29
    else
        status=$child_status
    fi

    cleanup_on_error # remove local file (this is to not have thousand of empty files)

    err "Transfer failed with error $status - $* - $child_status"

    exit $status
else
    # success

    cs=$(eval "cat $local_file | $checksum_cmd") # compute checksum (eval is needed as checksum_cmd contains pipe)
    echo $cs                                     # return checksum on stdout

    #err "Transfer done - $* - $cs"

    exit 0
fi
