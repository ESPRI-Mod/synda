#!/bin/bash
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# This script retrieve a file from ESGF using HTTP protocol
#
# Notes
#  - on success, the script displays checksum on stdout.
#    (thus be carefull not to print anything except checksum on stdout)
#  - short error message must be printed on stderr (one line max terminated by EOL).
#    More detailed error message (e.g. multilines) can be printed in the log file.
#
# Return values
#  0 => success
#  1 => Wget error
#  2 => File already exist on the local filesystem
#  3 => Incorrect arguments
#  4 => Incorrect environment
#       (fatal error, make the daemon to stop)
#  5 => Incorrect checksum type
#  6 => Error occurs while retrieving the X509 certificate 
#  7 => This script has been killed (SIGINT or SIGTERM)
# 12 => Permission error (e.g. CMIP5-RESEARCH role missing)
# 20 => 403 Forbidden
#       (permission denied after the redirect to ORP, means user do not have permission to access data)
# 21 => Read error (Connection timed out) in headers
#       (after the redirect)
# 22 => 403 Forbidden
#       (permission denied before the redirect to ORP, means something is wrong in the security stack)
# 23 => Unknown error
# 24 => Unknown error
# 25 => Read error (Connection timed out) in headers
#       (before the redirect)
# 26 => Unknown error
# 27 => Unknown error
# 28 => Unknown error
# 29 => wget process has been killed (most likely caused by a "shutdown immediate")
# 30 => file creation error (likely caused by missing access right)

usage ()
{
    echo ""
    echo "Usage"
    echo "  $0 [ -d [1|2|3] ] <src> <dest>"
    echo ""
    echo "Options:"
    echo "  -c      checksum type used to compute file checksum (default md5)"
    echo "  -d      debug level"
    echo ""
    echo "Example"
    echo "  $0 http://esg01.nersc.gov/thredds/fileServer/esg_dataroot/c20c/UCT-CSAG/HadAM3P-N96/NonGHG-Hist/HadCM3-p50-est1/v1-0/mon/atmos/pr/run060/pr_Amon_HadAM3P-N96_NonGHG-Hist_HadCM3-p50-est1_v1-0_run060_200807-201110.nc /tmp/foobar.nc"
}

curdate ()
{
    date '+%F %T'
}

err ()
{
    # display message on stderr

    buf="$1"

    echo "$buf" 1>&2  # stderr
    #echo $buf
}

log ()
{
    # display message with timestamp in logfile

    local code="$1"
    local msg="$2"

    local buf="$(curdate) - $code - $msg"

    echo "$buf" >> $debug_file
}

log_wget_output_debug ()
{
    # same as log_wget_output, but only log if debug mode is enabled

    if [ $debug_level -gt 0 ]; then
        log_wget_output @*
    fi
}

log_wget_output ()
{
    local code="$1"
    local buf="$2"
    local script_args="$3"

    log "$code" "WGET OUTPUT BEGIN ($wget_error_status_from_parsing,$script_args)"
    echo "$buf" >> $debug_file
    log "$code" "WGET OUTPUT END"
}

cleanup ()
{
    kill -TERM "$wget_pid" 1>/dev/null 2>/dev/null # kill child if still running
    rm -f "$local_file"
}

abort ()
{
    cleanup
    exit 7
}

# set path

export PATH=/sbin:/bin:/usr/sbin:/usr/bin

# set flag

set -o pipefail

# signal

trap "abort" SIGINT SIGTERM

# options

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

# args

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


# init

multiuser="0"

if [ "$multiuser" = "0" ]; then
    certdirprefix=$HOME
else
    certdirprefix=/var/tmp/synda/sdt
fi

export LANG=C
export LC_ALL=C
USE_CERTIFICATE="yes" # yes | no
export ESGF_CREDENTIAL=$certdirprefix/.esg/credentials.pem
export ESGF_CERT_DIR=$certdirprefix/.esg/certificates
wget_pid=

wgetoutputparser="${0%/*}/sdparsewgetoutput.sh"

# set log & tmp dir.
if [ "$multiuser" = "0" ]; then

    # check root folder
    if [ -z "$ST_HOME" ]; then
        err "Root directory not found ($ST_HOME)"
        exit 4
    fi

    tmpdir="${ST_HOME}/tmp"
    logdir="${ST_HOME}/log"
else
    tmpdir=/var/tmp/synda/sdt
    logdir=/var/log/synda/sdt
fi

debug_file=$logdir/debug.log

# wget parameters
WGET_TRIES=1
WGET_TIMEOUT=360

sha256_cmd ()
{
    echo "openssl dgst -sha256 | awk '{if (NF==2) print \$2 ; else print \$1}' "
}

md5_cmd ()
{
    echo "md5sum  | awk '{print \$1}' "
}


# manage checksum type
checksum_cmd=
if [ "$checksum_type" = "sha256" ]; then
    checksum_cmd=$(sha256_cmd)
elif [ "$checksum_type" = "SHA256" ]; then
    checksum_cmd=$(sha256_cmd)
elif [ "$checksum_type" = "md5" ]; then
    checksum_cmd=$(md5_cmd)
elif [ "$checksum_type" = "MD5" ]; then # HACK: some checksum types are uppercase
    checksum_cmd=$(md5_cmd)
else
    # we may come file for ESGF files that do not have checksum
    
    # fall back to sha256 in this case (arbitrary)
    checksum_cmd=$(sha256_cmd)
fi

# wget configuration
#
# without checksum
# WGETOPT=" --timeout=$WGET_TIMEOUT --tries=$WGET_TRIES -O $local_file "
#
# with checksum
WGETOPT="-D $local_file" # hack: (this is to help CFrozenDownloadCheckerThread class to do its work (this class need to know the local file associated with the process, but because of the FIFO, this dest file do not show in "ps fax" output, so we put the dest file in unused " -D domain-list" option (this option is used only in recursive mode, which we do not use))
WGETOPT="$WGETOPT --timeout=$WGET_TIMEOUT --tries=$WGET_TRIES -O $local_file "

# limit redirect retry to ease output parsing
#
# notes
#  - the message "2 redirections exceeded." is printed in debug.log file, this is normal
#  - we need 2 redirects (to go the the IDP to verify user identity and come back)
#
WGETOPT="$WGETOPT --max-redirect=2 "


# set verbose mode
if [ $debug_level -eq 3 ]; then
    set -x # bash debug mode (warning, this makes wget output to be duplicated 3 times)
    WGETOPT=" $WGETOPT -v -d "
elif [ $debug_level -eq 2 ]; then
    WGETOPT=" $WGETOPT -v -d "
elif [ $debug_level -eq 1 ]; then
    WGETOPT=" $WGETOPT -v " # note that progress are displayed in verbose mode
elif [ $debug_level -eq 0 ]; then
    # level used in normal operation (no debug info displayed)

    # we need this even in non-debug mode, else it hide HTTP errors
    WGETOPT=" $WGETOPT -v " # note that progress are displayed in verbose mode

    #WGETOPT=" $WGETOPT --quiet "
    #WGETOPT=" $WGETOPT --no-verbose "

    # so we must deal with the transfer progress.
    # it is not a big deal as it is automatically removed from wget stdxxx during parsing

    :
fi

# Don't check the server certificate against the available certificate authorities.  Also don't require the URL host name to match the common name presented by the certificate.
NO_CHECK_SERVER_CERTIFICATE=" --no-check-certificate "
#NO_CHECK_SERVER_CERTIFICATE=" "
TLS_ONLY=" --secure-protocol=TLSv1 "
#TLS_ONLY=" "
g__lifetime=168

# prevent download if local file path not starting with '/'
if [[ "${local_file:0:1}" = "/" ]]; then # check for starting slash
    :
else
    err "Incorrect format: local file path must start with a slash ($local_file)"
    exit 3
fi

# check if file is already present
if [ -e "$local_file" ]; then # use '-e' instead of '-f' to also prevent /dev/null to be used
    err "Local file already exists ($local_file)"
    exit 2
fi

# retrieve destination folder
local_folder=`dirname $local_file`

# create folder if not exists
mkdir -p ${local_folder}

# check if we have right to create local file

if touch "$local_file"; then
    rm "$local_file"
else
    err "Local file creation error ($local_file)"
    exit 30
fi

#
if [ $USE_CERTIFICATE = "yes" ]; then
    WGET_CMD="wget $WGETOPT \
        --certificate=$ESGF_CREDENTIAL --private-key=$ESGF_CREDENTIAL --ca-directory=$ESGF_CERT_DIR --ca-certificate=$ESGF_CREDENTIAL \
        $NO_CHECK_SERVER_CERTIFICATE \
        $TLS_ONLY \
        $url"
else
    WGET_CMD="wget $WGETOPT \
        $NO_CHECK_SERVER_CERTIFICATE \
        $TLS_ONLY \
        $url"
fi

wget_stderr2stdout()
{
    # this func gives the possibility to filter wget errmsg in downstream steps (e.g. to exclude download progress)

    # we send stderr on stdout and forget about stdout (stdout is empty anyway)
    $WGET_CMD 2>&1 >/dev/null # note that bash redirection order if important (i.e. '>/dev/null 2>&1' wouldn't work)
}

# set 'cmip5' group writable
umask u=rw,g=rw,o=r

############################################
# start wget
#
wget_error_status_from_parsing=0
wget_status=0
if [ $debug_level -gt 0 ]; then
    # - in this mode, wget info are displayed in realtime
    # - we don't parse wget output here because we want as much info as possible and also because this is not compatible with realtime

    # display debug info on stderr
    echo $WGET_CMD 1>&2
    wget_stderr2stdout 1>&2

    wget_status=$?
    wget_pid=$!
else
    # in this mode, wget info are displayed in differed time

    wget_errmsg=$(wget_stderr2stdout)
    wget_status=$?
    # | grep -v 'K .....') # hide progress

    # we parse wget output to keep only HTTP response code from wget messages
    if [ "$WGET_TRIES" = "1" ]; then # (currently, wget output parsing work only if "--tries" is set to 1)
        source "$wgetoutputparser"
    fi
fi

############################################
# post-processing
#
if [ $wget_status -ne 0 ]; then
    if [ $wget_status -eq 143 ]; then # 143 means 'wget' gets killed
        status=29
    else
        # wget wrap many different errors with -1 code
        # so we better use the code resulting from the parsing
        #
        #
        # if we found some error during the parsing, we use it, else we use 1
        #
        if [ $wget_error_status_from_parsing -ne 0 ]; then
            status=$wget_error_status_from_parsing
        else
            status=1
        fi
    fi

    cleanup # remove local file (this is to not have thousand of empty files)

    log "DEB010" "Transfer failed with error $status - $* - $wget_status"

    if [ $status -eq 12 ]; then
        err "Permission error (you need to susbscribe to the required role/group to access the data (e.g. cmip5-research))."
    else
        err "Transfer failed with error $status (see sdget.sh script for details about the error)"
    fi

    exit $status
else
    # success

    # checksum
    cs=$(eval "cat $local_file | $checksum_cmd") # compute checksum (eval is needed as checksum_cmd contains pipe)
    echo $cs                                     # return checksum on stdout

    #log "DEB020" "Transfer done - $*"
    exit 0
fi
