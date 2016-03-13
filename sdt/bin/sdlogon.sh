#!/bin/bash

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# This script logon into ESGF using X509 certificate.

# Notes
#  - Certificate is retrieved from a MyProxy server.
#  - Myproxy command used in this script is myproxyclient, Python based, from NDG stack
#    (for info about myproxyclient, see http://ndg-security.ceda.ac.uk/wiki/MyProxyClient)

usage ()
{
	echo ""
	echo "Usage"
	echo "  $0  [ -h <host> ]  [ -p <port> ] [ -u <username> ] [ -v ]"
	echo ""
	echo "Options:"
	echo "  -h      myproxy host"
	echo "  -p      myproxy port"
	echo "  -u      username"
	echo "  -r      force renew certificate even if valid"
	echo "  -v      verbose"
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

export PATH=/sbin:/bin:/usr/sbin:/usr/bin

if [ $# -eq 0 ]; then
	usage
	exit 0
fi

verbose="no"
force_renew=0
force_renew_ca_certficates=0
port=7512
host=pcmdi9.llnl.gov
while getopts 'h:p:ru:vx' OPTION
do
  case $OPTION in
  h)	host=$OPTARG
		;;
  p)	port=$OPTARG
		;;
  r)	force_renew=1
		;;
  u)	username=$OPTARG
		;;
  v)	verbose="yes"
		;;
  x)	force_renew_ca_certficates=1
		;;
  esac
done
shift $(($OPTIND - 1)) # remove options

MYPROXY_CMD="${0%/*}/myproxyclient"
MYPROXY_VERBOSE=""
#MYPROXY_VERBOSE="--verbose"
FORCE_RENEW_CERTIFICATE="no"
multiuser="0"

# set root folder
if [ "$multiuser" = "0" ]; then
    if [ -z "$ST_HOME" ]; then
        msg "ERR008" "root directory not found"
        exit 9
    else
        conf_dir=${ST_HOME}/conf
    fi
else
    conf_dir="/etc/synda/sdt"
fi

if [ "$multiuser" = "0" ]; then
    certdirprefix=$HOME
else
    certdirprefix=/var/tmp/synda/sdt
fi

export ESGF_CREDENTIAL=$certdirprefix/.esg/credentials.pem
export ESGF_CERT_DIR=$certdirprefix/.esg/certificates

# we unset X509_USER_PROXY to prevent error below (i.e. to ignore X509_USER_PROXY if already set by user)
#
#  Error: [('system library', 'fopen', 'No such file or directory'),
#  ('BIO routines', 'FILE_CTRL', 'system lib'), ('SSL routines',
#  'SSL_CTX_use_certificate_chain_file', 'system lib')]
#
unset X509_USER_PROXY
#export X509_USER_PROXY=$ESGF_CREDENTIAL # old stuff


conf_filename="credentials.conf"
conf_file="$conf_dir/$conf_filename"
passwd_filename=".sdpass"
passwd_file="$conf_dir/$passwd_filename"

# retrieve password
if [ -f "$passwd_file" ]; then
    # if dedicated passwd file exist, we use it first

    g__pass=`cat $passwd_file`
else
    # if dedicated passwd file doesn't exist, we read the passwd in conf file

    # check
    if [ ! -f "$conf_file" ]; then
        msg "ERR006" "missing conf file ($conf_file)"
        exit 4
    fi

    esgf_credential_section=$(cat $conf_file | awk 'BEGIN{esgf_credential=0}{if ($0 ~ /^\[esgf_credential\]/) {esgf_credential=1;next}; if ((esgf_credential==1) && ($0 ~ /^\[/)) {esgf_credential=0;next}; if (esgf_credential==1) print $0}') # extract 'esgf_credential' section content
    g__pass=$(echo "$esgf_credential_section" | awk -F '=' '{ if (! ($0 ~ /^;/) && ! ($0 ~ /^#/) && $0 ~ /password/) print $2}' ) # what we do here is read 'password' and ignore comment if any (i.e. line starting with ';' or '#').
fi

set_X509_CERT_DIR ()
{
	# if you have the error "self signed certificate in certificate chain"
	# it may be related with X509_CERT_DIR
	# you can try to set it to the values below:
	# - ""
	# - $certdirprefix/.esg/certificates
	# - /etc/grid-security/certificates


	# also if you have error below, try without setting "X509_CERT_DIR" env. var.
	#
	# Error authenticating: GSS Major Status: Authentication Failed
	# GSS Minor Status Error Chain:
	# globus_gss_assist: Error during context initialization
	# OpenSSL Error: a_verify.c:168: in library: asn1 encoding routines, function ASN1_item_verify: EVP lib
	# OpenSSL Error: fips_rsa_eay.c:748: in library: rsa routines, function RSA_EAY_PUBLIC_DECRYPT: padding check failed
	# OpenSSL Error: rsa_pk1.c:100: in library: rsa routines, function RSA_padding_check_PKCS1_type_1: block type is not 01


	#export X509_CERT_DIR=/etc/grid-security/certificates
	export X509_CERT_DIR=$certdirprefix/.esg/certificates
}

set_X509_CERT_DIR

# check passwd
if [ $g__pass = "pwd" ]; then
	msg "ERR019" "ESGF passwd not set"
	exit 4
fi

# check username 
if [ -z "$username" ]; then
	msg "ERR019" "ESGF username not set"
	exit 4
fi



# myproxyclient options

# from myproxyclient documentation
#
#  - http://ndg-security.ceda.ac.uk/wiki/MyProxyClient
#  - lib/python2.7/site-packages/myproxy/client.py
#
# -b, --bootstrap       Download trusted CA certificates
# -T, --trustroots      Update trustroots
#
# notes
#     - If bootstrap is set, connect to MyProxy server without verification of
#       the server's SSL certificate against any CA certificates
#     - If bootstrap is set, updateTrustRoots will be forced to True also

#  myproxyclient failed with this option, so disabled for now
# -t $g__lifetime 

# currently, we set trustroots option everytime

g__myproxy_opts="logon -T $MYPROXY_VERBOSE -s $host -p $port -l $username -o $ESGF_CREDENTIAL"

# currently, we set bootstrap option everytime # TODO: change this to set only the first time (i.e. if .esg/certificates is empty)

bootstrap=1

if [ $bootstrap -eq 1 ]; then
    g__myproxy_opts="$g__myproxy_opts -b "
fi



# return code
#   0 => certificate doesn't exists
#   1 => certificate exists
certificate_exists () 
{
	if [ -f $ESGF_CREDENTIAL ]; then
		return 1
	else
		return 0
	fi
}
# return code
#   0 => certificate isn't valid
#   1 => certificate is valid
certificate_is_valid () 
{
	openssl x509 -checkend 500 -noout -in $ESGF_CREDENTIAL # checks whether the cert expires in the next 500 seconds
	if [ $? = 0 ]; then
		return 1
	else
		return 0
	fi
}
# return code
#   0 => success
#  >0 => error
renew_certificate () 
{
    BUF="$MYPROXY_CMD $g__myproxy_opts"
    BUF_PASSWD_STDIN="echo '$g__pass' | $BUF -S " # "-S" is to read pwd from stdin

	if [ "x$verbose" = "xyes" ]; then
		echo $BUF # this is to prevent displaying the password on stdxxx (i.e. BUF and BUF_PASSWD_STDIN are the same except for the password)
		eval $BUF_PASSWD_STDIN
	else
		eval $BUF_PASSWD_STDIN >& /dev/null
	fi
}

# when testing certificate, remove current certificate
if [ "x$force_renew"  = "x1" ]; then
	rm -f $ESGF_CREDENTIAL
fi

if [ $force_renew_ca_certficates -eq 1 ]; then
	rm -rf $ESGF_CERT_DIR
fi

if [ $FORCE_RENEW_CERTIFICATE = "yes" ]; then
	renew_certificate
fi

certificate_exists
if [ $? -eq 1 ]; then
	certificate_is_valid
	if [ $? -eq 1 ]; then
        :
        #msg "INF006" "Certificate is valid, nothing to do"
	else
		renew_certificate
	fi
else
	renew_certificate
fi


# check (second pass => if it fails again, then fatal error)
certificate_exists
if [ $? -eq 0 ]; then
	msg "ERR009" "Error occured while retrieving certificate"
	exit 4
else
    chmod 600 $ESGF_CREDENTIAL # needed by globus-url-copy

	certificate_is_valid
	if [ $? -eq 0 ]; then
		msg "ERR010" "Error occurs while retrieving certificate"
		exit 4
	fi
fi

exit 0
