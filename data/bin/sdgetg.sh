#!/bin/bash
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# This script retrieves a file from ESGF using GRID-FTP protocol

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
    echo "  $0 [ -v ] [ -p parseoutput ] [ -t timeout ] <src> <dest>"
    echo ""
    echo "Options:"
    echo "  -d      debug"
    echo "  -p      parseoutput"
    echo "  -t      timeout"
    echo "  -v      verbose"
    echo ""
    echo "Example"
    echo "  $0 -vvv gsiftp://esgf1.dkrz.de:2811//cmip5/cmip5/output1/MPI-M/MPI-ESM-LR/decadal1995/mon/land/Lmon/r2i1p1/v20120529/pastureFrac/pastureFrac_Lmon_MPI-ESM-LR_decadal1995_r2i1p1_199601-200512.nc /tmp/sdt_test_file.nc"
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

# set locales

export LANG=C
export LC_ALL=C

# path

export PATH=/sbin:/bin:/usr/sbin:/usr/bin

# signal

trap "abort" SIGINT SIGTERM

# pre-option init.

max_verbosity=4

# retrieve options

debug=0
parseoutput=0 # not used for now (but needed to keep the same public interface as sdget.sh)
verbosity=0
timeout=360 # not used for now (but needed to keep the same public interface as sdget.sh)
certdirprefix=
tmpdir=/tmp # not used for now (but needed to keep the same public interface as sdget.sh)
logdir=/tmp # not used for now (but needed to keep the same public interface as sdget.sh)
while getopts 'c:dhl:p:t:T:v' OPTION
do
  case $OPTION in
  c)    certdirprefix=$OPTARG
        ;;
  d)    debug=1
        ;;
  h)    usage
        exit 0
        ;;
  l)    logdir=$OPTARG
        ;;
  p)    parseoutput=$OPTARG
        ;;
  t)    timeout=$OPTARG
        ;;
  T)    tmpdir=$OPTARG
        ;;
  v)    (( verbosity=verbosity+1 ))
        ;;
  esac
done
shift $(($OPTIND - 1)) # remove options

if [ $verbosity -gt 3 ]; then
    verbosity=$max_verbosity
fi

# retrieve positional arguments

url="$1"
local_file="$2"

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
    msg "incorrect format (local_file=$local_file)"
    exit 3
fi

# check if file is already present
if [ -e "$local_file" ]; then # use '-e' instead of '-f' to also prevent /dev/null to be used
    msg "local file already exists ($local_file)"
    exit 3
fi

# retrieve destination folder
local_folder=`dirname $local_file`

# set group writable
umask "u=rwx,g=rwx,o=rx"

# create folder if not exists
mkdir -p ${local_folder}

# check if we have right to create local file
if touch "$local_file" >/dev/null 2>&1; then # note that touch error msg is removed here to prevent having the same message twice
    rm "$local_file"
else
    msg "local file creation error ($local_file)"
    exit 30
fi

# init

if [ $debug -eq 1 ]; then
    # currently, debug option is not used in this script (we keep it here to stay sync between sdget.sh and sdgetg.sh scripts)

    :
fi

export ESGF_SECURITY_ROOT=$certdirprefix
export ESGF_CREDENTIAL=$ESGF_SECURITY_ROOT/credentials.pem 

export X509_USER_CERT=$ESGF_CREDENTIAL
export X509_USER_KEY=$ESGF_CREDENTIAL
export X509_USER_PROXY=$ESGF_CREDENTIAL
export X509_CERT_DIR=$ESGF_SECURITY_ROOT/certificates

export GLOBUS_TCP_PORT_RANGE=50000,51000
#export GLOBUS_TCP_SOURCE_RANGE=50000,51000

GRIDFTP_CMD=globus-url-copy

# note: GRIDFTP_OPT can be set directly in sdt.conf
if [ -z "$GRIDFTP_OPT" ]; then
    GRIDFTP_OPT=""
fi

# verbosity parameter
if [ $verbosity -eq 3 ]; then
    set -x # bash verbose mode (warning, this make globus-url-copy output to be duplicated 3 times)

    export GLOBUS_ERROR_OUTPUT=1
    export GLOBUS_ERROR_VERBOSE=1
    export GLOBUS_GSI_AUTHZ_DEBUG_LEVEL=2
    export GLOBUS_GSI_AUTHZ_DEBUG_FILE=/tmp/gridftp_debug.log

    GRIDFTP_DEBUG_OPT=" -v -vb -dbg "
elif [ $verbosity -eq 2 ]; then
    GRIDFTP_DEBUG_OPT=" -v -vb -dbg "
elif [ $verbosity -eq 1 ]; then
    GRIDFTP_DEBUG_OPT=" -v -vb "
elif [ $verbosity -eq 0 ]; then
    GRIDFTP_DEBUG_OPT=
fi

# set group writable
umask u=rw,g=rw,o=r

# start transfer

CMD="$GRIDFTP_CMD $GRIDFTP_OPT $GRIDFTP_DEBUG_OPT $url $local_file"

if [[ $verbosity > 0 ]]; then
    echo $CMD
    $CMD 1>&2
else
    $CMD 1>&2
fi

child_status=$?

# post-processing

if [ $child_status -ne 0 ]; then
    # error

    if [ $child_status -eq 143 ]; then # 143 means 'wget' gets killed
        status=29
    else
        status=$child_status
    fi

    cleanup_on_error # remove local file (this is to not have thousand of empty files)

    msg "Transfer failed with error $status - $* - $child_status"

    exit $status
else
    # success

    #msg "Transfer done - $* - $cs"

    exit 0
fi
