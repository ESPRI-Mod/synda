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
# Note
#  - on success, the script displays checksum on stdout.
#    (thus be carefull not to print anything except checksum on stdout)
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

# TAG43242 error
#
# When not using eval, checksum_cmd doesn't get interpreted correctly
#
# md5sum: |: No such file or directory
# md5sum: awk: No such file or directory
# md5sum: '{print: No such file or directory
# md5sum: $1}': No such file or directory

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

msg ()
{
    # display msg on stderr and logfile

	l__code="$1"
	l__msg="$2"

    buf="$(curdate) - $l__code - $l__msg"

    echo $buf 1>&2             # stderr
	#echo $buf >> $log_file    # deprecated ('transfer.log' duplicate)
}

cleanup ()
{
    kill -TERM "$wget_pid" 1>/dev/null 2>/dev/null # kill child if still running
	rm -f "$local_file"
	rm -f "$g__tmpfile__checksum"
}

abort ()
{
    cleanup
    exit 7
}

# set flag

set -o pipefail

# signal

trap "abort" SIGINT SIGTERM

# options

DEBUG="no"
debug_level=1
g__checksum_type=md5
while getopts 'c:d:h' OPTION
do
  case $OPTION in
  c)	checksum_type=$OPTARG
		;;
  d)	DEBUG="yes"
		debug_level=$OPTARG
		;;
  h)	usage
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
export LANG=C
export LC_ALL=C
USE_CERTIFICATE="yes" # yes | no
export ESGF_CREDENTIAL=$HOME/.esg/credentials.pem
export ESGF_CERT_DIR=$HOME/.esg/certificates
wget_pid=

# set root folder
if [ -z "$ST_HOME" ]; then
    msg "ERR008" "root directory not found ($ST_HOME)"
    exit 4
else
    SYNCDA_ROOT=${ST_HOME}
fi

log_dir=$SYNCDA_ROOT/log
#log_file=${log_dir}/get_data.log # deprecated ('transfer.log' duplicate)
debug_file=${log_dir}/debug.log


# set tmp dir.
g__tmpdir=$SYNCDA_ROOT/tmp
mkdir -p $g__tmpdir # create tmp dir. (if missing)

# wget parameters
WGET_TRIES=1
WGET_TIMEOUT=360

# manage checksum type
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
	#msg "ERR005" "incorrect checksum type ($checksum_type)"
	#exit 5
fi

# set checksum tmp file
g__tmpfile__checksum_template=$g__tmpdir/checksum_$$_XXXXXXX # set checksum tmp file template
g__tmpfile__checksum=$(mktemp $g__tmpfile__checksum_template) # create checksum tmp file

# wget configuration
#
# without checksum
# WGETOPT=" --timeout=$WGET_TIMEOUT --tries=$WGET_TRIES -O $local_file "
#
# with checksum
WGETOPT="-D $local_file" # hack: (this is to help CFrozenDownloadCheckerThread class to do its work (this class need to know the local file associated with the process, but because of the FIFO, this dest file do not show in "ps fax" output, so we put the dest file in unused " -D domain-list" option (this option is used only in recursive mode, which we do not use))
WGETOPT="$WGETOPT --timeout=$WGET_TIMEOUT --tries=$WGET_TRIES -O - "

# debug mode
if [ "x$DEBUG" = "xyes" ]; then

	if [ $debug_level -eq 4 ]; then
		set -x # bash debug mode (warning, this make wget output to be duplicated 3 times)

		WGETOPT=" $WGETOPT -v -d "

	elif [ $debug_level -eq 3 ]; then

		WGETOPT=" $WGETOPT -v -d "

	elif [ $debug_level -eq 2 ]; then

		WGETOPT=" $WGETOPT -v "
	fi

else
	# set verbose mode for wget (this is not related to debug mode and need to be set all the time)
	WGETOPT=" $WGETOPT -v " # note that progress are displayed in verbose mode

	# this is not used anymore, because it hide HTTP errors
	#WGETOPT=" $WGETOPT --quiet "
	#WGETOPT=" $WGETOPT --no-verbose "

	# so we must deal with the transfer progress.
	# it is not a big deal as it is automatically removed from wget stdxxx during parsing
fi

# Don't check the server certificate against the available certificate authorities.  Also don't require the URL host name to match the common name presented by the certificate.
NO_CHECK_SERVER_CERTIFICATE=" --no-check-certificate "
#NO_CHECK_SERVER_CERTIFICATE=" "
TLS_ONLY=" --secure-protocol=TLSv1 "
#TLS_ONLY=" "
g__lifetime=168

mkdir -p ${log_dir}

# prevent download if path not starting with '/'
if [[ "${local_file:0:1}" = "/" ]]; then # check for starting slash
	:
else
	msg "ERR004" " incorrect format (local_file=$local_file)"
	exit 3
fi

# check if file is already present
if [ -e "$local_file" ]; then # use '-e' instead of '-f' to also prevent /dev/null to be used
	msg "ERR011" "local file already exists ($local_file)"
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

	msg "ERR111" "local file creation error ($local_file)"

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

# file redirection n checksum management
WGET_CMD="$WGET_CMD | tee $local_file | $checksum_cmd > $g__tmpfile__checksum"

# set 'cmip5' group writable
umask u=rw,g=rw,o=r

############################################
# start wget
#
wget_error_status_from_parsing=0
wget_status=0
if [ "x$DEBUG" = "xyes" ]; then
	# in debug mode, we don't parse wget output

	echo $WGET_CMD 1>&2

    # we need eval to prevent TAG43242 error
	eval $WGET_CMD

	wget_status=$?
    wget_pid=$!
else

    # - we need eval to prevent TAG43242 error
    # - we save stderr and forget about stdout (stdout is empty anyway)
	wget_stderr=$(`eval $WGET_CMD` 2>&1 >/dev/null)

	wget_status=$?

	# if wget "--tries" option is set to 1, we parse wget output to get informations on the cause of the error
	# (currently, wget output parsing work only if "--tries" is set to 1)
	#
	if [ "$WGET_TRIES" = "1" ]; then
        source $SYNCDA_ROOT/bin/sdparsewgetoutput.sh
	fi
fi

############################################
# post-processing
#
if [ $wget_status -ne 0 ]; then
	if [ $wget_status -eq 143 ]; then # 143 means 'wget' gets killed
		getdata_status=29
	else
		# wget wrap many different errors with -1 code
		# so we better use the code resulting from the parsing
		#
		#
		# if we found some error during the parsing, we use it, else we use 1
		#
		if [ $wget_error_status_from_parsing -ne 0 ]; then
			getdata_status=$wget_error_status_from_parsing
		else
			getdata_status=1
		fi
	fi

    cleanup # remove local file (this is to not have thousand of empty files)

	msg "ERR001" "Transfer failed with error $getdata_status - $* - $wget_status"

	exit $getdata_status
else
	# success

	# retrieve checksum
	l__checksum=$(<$g__tmpfile__checksum) # bash trick
	rm -f "$g__tmpfile__checksum"

	# return checksum on stdout
	echo $l__checksum

	msg "INF003" "transfer done - $* - $l__checksum"

	exit 0
fi
