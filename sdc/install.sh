#!/bin/bash -e

##################################
#  @program        synda
#  @description    climate models data transfert program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# Notes regarding synda versions
#  - This installer can upgrade synda 2.9+ and install synda 3.0+
#  - To upgrade synda 2.8, use sd28to29.py script
#  - To install synda 2.9, see synda/old/29 on orion svn.
#  - To install/upgrade synda 2.8-, see synda/old/28_and_older on orion svn.

# func

stop_spinner ()
{
    # Note that this func do not really stop the spinner.
    # It only take care of the spinner cleanup.
    # The spinner stops when this process exit
    # (in fact, because of the redirection, the spinner output also stops when
    # stop_redir_stdxxx() is called (to be confirmed)).

    # spinning cleanup
    printf "\r \r" >&3
}

start_redir_stdxxx ()
{
    # first save current stdxxx
    # (i.e. 3 become same as 1)
    #
    exec 3>&1
    exec 4>&2

    # then redirect stdxxx to log file
    #
    exec 1>$log_file 2>&1
}

stop_redir_stdxxx ()
{
    # restore stdxxx and close file descriptor 3 before we exit
    exec 1>&3 3>&- 2>&4 4>&-
}

err ()
{
    local code="$1"
    local msg="$2"

    stop_spinner
    stop_redir_stdxxx

    echo "$code - $msg"
    exit 1
}

fatal_err ()
{
    # this func is used by the trap mecanism

    err "INSTALL-ERR011" "error occurs during installation: see $log_file for details"
}

check_python_version ()
{
    # return values
    #  0 => python version ok
    #  1 => python version too old

    $PYTHON_CMD <<__PYTHONSCRIPT__ 2>&1
import sys
if sys.hexversion < 0x02060000:
    sys.exit(1)
else:
    sys.exit(0)
__PYTHONSCRIPT__
}

usage ()
{
    cat >&2 << EOF

USAGE: $(basename $0): [ -u ] [ -e archive ] [-h] [ -t prefix ] [ -d ] [ MODULE ]

POSITIONAL ARGS:
   MODULE       Specify which module(s) to install.
                Available modules are: 'transfer','postprocessing'.
                If no module specified, install 'transfer' module.

OPTIONS:
   -d <vernum>   Specify version to install
   -e <file>     Use specified archive instead of downloading archive from synda website
   -t <path>     Specify directory where to install the application
   -u            Upgrade
   -h            Show this message

EOF
}

check_dependency ()
{
    local cmd="$1"

    if ! which $cmd >/dev/null 2>&1; then
        # we come here if <cmd> is not found

        err "INSTALL-ERR006" "missing dependency: $cmd"
    fi
}

check_dependencies ()
{
    check_dependency mktemp
    check_dependency bc
    check_dependency md5sum
    check_dependency awk
    check_dependency sqlite3
}

# from http://stackoverflow.com/questions/4023830/how-compare-two-strings-in-dot-separated-version-format-in-bash
vercomp () {
    # Returns
    #  0 => '='
    #  1 => '>'
    #  2 => '<'

    if [[ $1 == $2 ]]
    then
        return 0
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++))
    do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++))
    do
        if [[ -z ${ver2[i]} ]]
        then
            # fill empty fields in ver2 with zeros
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]}))
        then
            return 1
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]}))
        then
            return 2
        fi
    done
    return 0
}

st_is_running ()
{
    # check if daemon is running
    if [ -f "$st_root/tmp/daemon.pid" ]; then
        err "INSTALL-ERR004" "The synda daemon must be stopped during installation"
    fi
    # check if IHM is running
    if [ -f "$st_root/tmp/ihm.pid" ]; then
        err "INSTALL-ERR018" "synda must be stopped during installation"
    fi
}

sp_is_running ()
{
    # check if daemon is running
    if [ -f "$sp_root/tmp/daemon.pid" ]; then
        err "INSTALL-ERR044" "The synda post-processing daemon must be stopped during installation"
    fi
}

install_python ()
{
    # Python installation from source 
    cd $tmpdir
    $WGET_CMD $python_url
    tar xzf $python_archive_name
    cd $python_package_name
    ./configure --prefix $python_dir
    make
    make install
    export PATH=$python_dir/bin:$PATH
    post_install_msg="$post_install_msg\nPython has been installed in $python_dir"
}

install_python_if_needed ()
{

    l__needpythoninstall=0

    # check for python requirements
    if which $PYTHON_CMD >/dev/null 2>&1; then
        # we come here if python is found

        # check for python minimal version
        
        if ! check_python_version; then
            # python is too old

            l__needpythoninstall=1
        fi
    else
        # python not found

        l__needpythoninstall=1
    fi


    # TODO also check for sqlite dev header
    #       - sqlite dev header installation
    #           - example with centos
    #               - do as root
    #                   - yum install sqlite-devel.i386
    #                   - yum install sqlite-devel.x86_64

    
    # install python if needed
    if [ $l__needpythoninstall = "1" ]; then
        install_python
    fi
}

check_python_installation ()
{
    # check if python is found and if python version is not too old

    if ! which $PYTHON_CMD >/dev/null 2>&1; then # true if "which" exit code is not 0
        err "INSTALL-ERR001" "python not found"
    else
        # check for python minimal version
        
        if ! check_python_version; then
            # python is too old

            err "INSTALL-ERR010" "python version is too old"
        fi
    fi
}

update_transfer_environment_pre_install ()
{
    current_version=${1}
    new_version=${2}

    # check
    if [ -z "$current_version" ]; then
        err "INSTALL-ERR402" "Incorrect current version"
    fi
    if [ -z "$new_version" ]; then
        err "INSTALL-ERR404" "Incorrect new version"
    fi
    if [[ "$new_version" < "3.0" ]]; then
        err "INSTALL-ERR406" "Incorrect new version"
    fi
    if [[ "$new_version" < "$current_version" ]]; then
        err "INSTALL-ERR408" "Incorrect new version"
    fi

    # payload goes here
    # ..
}

update_transfer_environment_post_install ()
{
    current_version=${1}
    new_version=${2}

    if [ "$new_version" = "3.0" ]; then # in 3.1+, update mecanism is embedded in the binary
        sqlite3 $st_root/db/sdt.db "update version set version='$new_version'"
    fi
}

init_ve ()
{
    ve_dir=${1}

    if [ ! -f $ve_dir/bin/activate ]; then
        err "INSTALL-ERR002" "$ve_dir doesn't look like a Synda installation folder (activate not found)"
    fi

    source $ve_dir/bin/activate # set PATH to the ve python

    check_python_installation
}

check_ve ()
{
    ve_dir=${1}

    if [ -f $ve_dir/bin/activate ]; then
        # previous installation already exists


        # If we are here, it can be because:
        #     - Previous installation failed.
        #       In this case we really want to overwrite previous installation. So user should answer 'yes' to the question below.
        #     - User wants only to update synda application (i.e. not virtualenv and related stuff), but forgot to pass '-u' option.
        #       In this case we want to restart the installation with the '-u' option. So user should answer 'no' to the question below.


        # MEMO
        #
        # Basically, INSTALL-ERR008 was made so 
        #  - to inform user that no need to re-install ve and pypi package everytime
        #    synda application must be updated. 
        #    And so to inform user about the existency of '-u' install script option.
        #  - to PREVENT overwriting synda configuration file (yes, when synda
        #    is installed without '-u' option, configuration file is overwrited without 
        #    confirmation nor backup !)
        #
        # But if first installation failed, user has to reinstall everything.
        # Which mean that INSTALL-ERR008 (error code and message) was not explicite at all and even more not correct.


        # old action (obsolete)
        #err "INSTALL-ERR008" "'activate' script should not exist at this step (try removing virtualenv from your PATH before running install.sh script)"

        # new action 1
        #
        # We continue the installation no matter what.
        #
        # The good point is if previous installation failed, the user did the right thing by reinstalling everything.
        #
        # But the drawback is that if it's just an synda application upgrade, it's overkill to reinstall everything
        # (this is especially annoying when doing fast cycle debugging or development).
        #
        # But there should be no harm, so until we have more interactivity in this script, we go for that solution.
        #
        :

        # new action 2
        #
        # Doesn't work because the spinner cannot be stopped without stopping also this script,
        # and we need the spinner to be stopped while displaying the confirmation message !
        # To fix this problem, maybe use another way to stop the spinner (using lockfile existency
        # check for example), and maybe rewrite this script in Python (to be confirmed, not sure this will help).
        #
        #read -p "Existing synda installation detected ($ve_dir). Do you want to continue the installation ? (y/n)" -n 1 -r
        #echo # move to a new line (needed because of the '-n' option)
        #if [ "$REPLY" = "y" ]; then
        #    :
        #else
        #    stop_spinner
        #    stop_redir_stdxxx
        #    echo "Abort."
        #    exit 1
        #fi
    fi
}

install_ve ()
{
    ve_dest_dir=${1}

    # install python virtualenv
    cd $tmpdir
    $WGET_CMD ${virtual_env_url}
    tar xzvf ${virtual_env_archive_name}
    cd ${virtual_env_package_name}
    $PYTHON_CMD virtualenv.py --distribute --unzip-setuptools $ve_dest_dir
    source $ve_dest_dir/bin/activate # set PATH to the ve python
    pip install --upgrade setuptools==44.0
}

fix_myproxyclient ()
{
    # Fix error below:
    # <---
    # AttributeError: 'MyProxyServerSSLCertVerification' object has no attribute '__name__'
    # --->

    if [ "$python_pkg_install_cmd" = "easy_install" ]; then
        client_file=$st_root/lib/$PYTHON_CMD/site-packages/MyProxyClient*.egg/myproxy/client.py
    elif [ "$python_pkg_install_cmd" = "pip install" ]; then
        client_file=$st_root/lib/$PYTHON_CMD/site-packages/myproxy/client.py
    else
        err "INSTALL-ERR108" "Unknown Python package installer ($python_pkg_install_cmd)"
    fi
    sed -i "s|SERVER_CN_PREFIX = 'host/'|SERVER_CN_PREFIX = 'host/'\n\n    __name__='MyProxyServerSSLCertVerification'|" $client_file
    rm -f ${client_file/.py/.pyc} # remove pre-compiled file
}

fix_pyopenssl ()
{
    # this is to prevent "AttributeError: 'FFILibrary' object has no attribute 'SSL_OP_NO_TICKET'" error

    easy_install https://github.com/pyca/pyopenssl/tarball/master # note: pip cannot be used here ('easy_install' only)
}

install_sg_application ()
{
    # install go transfer API
    $python_pkg_install_cmd globusonline-transfer-api-client

    # install mkproxy
    #
    # (program written in C to create a proxy certificate from a public key)
    #
    client_dir=$st_root/lib/$PYTHON_CMD/site-packages/globusonline/transfer/api_client/x509_proxy/
    rm -rf $tmpdir/mkproxy
    mkdir $tmpdir/mkproxy
    pushd $tmpdir/mkproxy
    wget --no-check-certificate https://raw.githubusercontent.com/globusonline/transfer-api-client-python/master/mkproxy/mkproxy.c
    wget --no-check-certificate https://raw.githubusercontent.com/globusonline/transfer-api-client-python/master/mkproxy/Makefile
    make
    cp mkproxy $client_dir
    popd

    # install python-nexus-client
    $python_pkg_install_cmd https://github.com/globusonline/python-nexus-client/archive/integration.zip
}

install_st_additional_packages ()
{
    # install pypi python modules in virtualenv
    $python_pkg_install_cmd pyOpenSSL psutil humanize tabulate progress pycountry python-jsonrpc python-daemon==1.6.1 retrying requests beautifulsoup4 texttable pillow==3.4.2 reportlab

    # install lxml pypi python modules in virtualenv (old versions only)
    (
    set +e 
    vercomp $st_version 3.6
    if [ $? -eq 2 ]; then
         $python_pkg_install_cmd lxml==3.3.5
    fi
    exit 0
    ) # subshell is used here to prevent setting "+e" option globally (i.e. for the all script)

    if [ "$PYTHON_CMD" = "python2.6" ]; then
        $python_pkg_install_cmd argparse
    fi

    $python_pkg_install_cmd myproxyclient

    # disabled as this fix is not needed anymore (see TAG5453H5J34HJ4J4H5HJ32HJ)
    #fix_myproxyclient

    # disabled as this fix is not needed anymore (relates to pyopenssl 0.14, now latest version of pyopenssl is 0.16)
    #fix_pyopenssl
}

install_sp_additional_packages ()
{
    # install pypi python modules in virtualenv
    # maybe freeze those version: cryptography==0.6 cffi==0.8.6 python-jsonrpc==0.5.1
    $python_pkg_install_cmd pyOpenSSL humanize tabulate progress python-jsonrpc python-daemon==1.6.1 retrying bunch simplejson
    # pygraphviz

    if [ "$PYTHON_CMD" = "python2.6" ]; then
        $python_pkg_install_cmd argparse
    fi
}

pre_install ()
{
    conf_file=${1}

    # check
    if [ ! -f "$conf_file" ]; then
        err "INSTALL-ERR032" "config file not found ($conf_file)"
    fi

    # backup conf files
    cp $conf_file /tmp

    # store checksum of conf files (to inform user if it is modified during upgrade)
    g__before_md5_conffile=$(md5sum $conf_file | awk '{print $1}')
}

post_install ()
{
    conf_file=${1}

    # check if conf files were modified
    g__after_md5_conffile=$(md5sum $conf_file | awk '{print $1}')
    if [ "$g__before_md5_conffile" != "$g__after_md5_conffile" ]; then
        post_install_msg="$post_install_msg\n\nWARNING: $conf_file has been reinitialized to default values\nA copy of the original file has been saved in /tmp"
    fi
}

retrieve_archive ()
{
    # retrieve application archive

    url=${1}

    if [ -n "$g__archive" ]; then
        # This case is used to prevent having to send the package to the web server
        # (useful when no internet access and want to do some local deployment for test)

        # check
        if [ ! -f "$g__archive" ]; then
            err "INSTALL-ERR400" "Archive file is missing ($g__archive)"
        fi

        # copy archive in tmp dir
        cp -f $g__archive $tmpdir

        cd $tmpdir

    elif [ -z "$g__archive" ]; then
        # "-e" option not used, so we retrieve archive from the web server

        cd $tmpdir
        $WGET_CMD $url
    fi
}

install_st_application ()
{
    retrieve_archive $st_url

    # install
    tar xzvf $st_archive
    cd $st_package

    # debug
    #$PYTHON_CMD -c "import sys; print 'prefix:%s'%sys.prefix"

    $PYTHON_CMD setup.py install --install-scripts=$st_lib

    chmod go+r "$st_conf_file"
    chmod go-r "$st_cred_file"

    # create symlink in 'bin'
    cd $st_root/bin
    #create_st_symlink

    ln -fs $st_lib/sdcleanup_tree.sh sdcleanup_tree.sh
    ln -fs $st_lib/sdget.sh sdget.sh
    ln -fs $st_lib/sdgetg.sh sdgetg.sh
    ln -fs $st_lib/sdlogon.sh sdlogon.sh
    ln -fs $st_lib/sdparsewgetoutput.sh sdparsewgetoutput.sh
    ln -fs $st_lib/synda.py synda
    ln -fs $st_lib/sdtc.py sdtc
    ln -fs $st_lib/sdconfig.py sdconfig
    ln -fs $st_lib/sdget.py sdget
    ln -fs $st_lib/sdmerge.py sdmerge
    ln -fs $st_lib/sddownloadtest.py sddownloadtest

    cd -

    post_install_msg="$post_install_msg\nsynda application has been installed in $st_root"
}

install_sp_application ()
{
    retrieve_archive $pp_url

    tar xzvf $pp_archive
    cd $sp_package

    $PYTHON_CMD setup.py install --install-scripts=$pp_lib

    chmod go-r "$pp_cred_file"

    # create symlink in 'bin'
    # TODO: no need to symlink every files as only 'spdaemon' is needed
    cd $sp_root/bin
    create_sp_symlink
    cd -

    # download then store 'worker' script in 'bin' folder
    #
    # WARNING: SDW is always the HEAD version (ie each new run of the
    # "install.sh" script may install a different version of SDW (if someone commited
    # in github in the meantime, of course))
    #
    wget -O $sp_root/bin/synda_wo https://raw.githubusercontent.com/Prodiguer/synda/master/sdw/bin/worker
    chmod +x $sp_root/bin/synda_wo

    post_install_msg="$post_install_msg\nsynda-pp application has been installed in $sp_root"
}

set_default_python_version ()
{
    # This func set PYTHON_CMD variable to given python version if found.

    local python_version=$1

    if which $python_version >/dev/null 2>&1; then
        # we come here if <cmd> is found

        PYTHON_CMD=$python_version
    fi
}

install_transfer_module ()
{
    # disabled, as if it failed during the first install (e.g. for a dependency problem), we still need to be able to redo the virtualenv install !
    #check_ve $st_root

    install_ve $st_root # beware: this call switch the current context to the new virtualenv python
    install_st_additional_packages
    install_st_application
}

update_transfer_module ()
{
    init_ve $st_root

    # TODO: replace using 'synda -V' asap
    #update_transfer_environment_pre_install $(synda -V) $st_version
    currver=$(cat $st_root/lib/sd/sdapp.py | grep "version=" | sed "s/[[:alpha:]=']*//g" )
    update_transfer_environment_pre_install $currver $st_version

    pre_install $st_conf_file
    install_st_application
    post_install $st_conf_file

    update_transfer_environment_post_install $currver $st_version
}

install_postprocessing_module ()
{
    # disabled, as if it failed during the first install (e.g. for a dependency problem), we still need to be able to redo the virtualenv install !
    #check_ve $sp_root

    install_ve $sp_root # beware: this call switch the current context to the new virtualenv python
    install_sp_additional_packages
    install_sp_application
}

update_postprocessing_module ()
{
    init_ve $sp_root
    pre_install $pp_conf_file
    install_sp_application
    post_install $pp_conf_file
}

install_globustransfer_module ()
{
    init_ve $st_root
    install_sg_application # sg stands for 'Synda Globus'
}

create_st_symlink ()
{
    for f in $st_lib/*; do

        file_extension=${f##*.} # dot is excluded
        if [[ $file_extension != "pyc" ]]; then

            symlink_name=$( echo ${f##*/} | sed s/.py$// ) # note that shell script with .sh extension keep their extension
            ln -fs $f $symlink_name
        fi
    done
}

create_sp_symlink ()
{
    for f in $pp_lib/*; do

        file_extension=${f##*.} # dot is excluded
        if [[ $file_extension != "pyc" ]]; then

            symlink_name=$( echo ${f##*/} | sed s/.py$// ) # note that shell script with .sh extension keep their extension
            ln -fs $f $symlink_name
        fi
    done
}

start_spinner ()
{
    pid=$$
    (
        spin='-\|/'
        i=0
        while kill -0 $pid 2>/dev/null; do
          i=$(( (i+1) %4 ))
          printf "\r${spin:$i:1}" >&3
          sleep .1
        done
    ) &
}

# bash trigger

trap 'fatal_err' ERR # bash trick related to the "-e" option above, see manpage

# remove 'sdx/bin' from PATH (needed as install.sh must use a real python install, not a virtualenv python)

export PATH=$(echo $PATH | tr ':' '\n' | awk '!/\/sd.\/bin/' | paste -sd:)

# init.

g__prefix=$HOME
g__verbose=
g__upgrade=0
g__transfer=0
g__postprocessing=0
g__globustransfer=0
g__archive=
g__version=

# retrieve options

while getopts 'd:e:ht:uv' OPTION
do
    case $OPTION in
    d) g__version="$OPTARG"
       ;;
    e) g__archive="$OPTARG"
       ;;
    h) usage
       exit 2
       ;;
    t) g__prefix="$OPTARG"
       ;;
    u) g__upgrade=1
       ;;
    v) g__verbose="-v"
       ;;
    ?) exit 1 # we come here when a required option argument is missing (bash getopts mecanism)
       ;;
    esac
done

# remove options so to only keep positional arguments
shift $((OPTIND-1))

# retrieve positional args
if [ $# -ge 1 ]; then
    for module in "$@"; do
        if [ $module = "transfer" ]; then
            g__transfer=1
        elif [ $module = "postprocessing" ]; then
            g__postprocessing=1
        elif [ $module = "globustransfer" ]; then
            g__globustransfer=1
        fi
    done
else
    # default if no args

    g__transfer=1
fi

# init
log_file="$PWD/install.log"

# info
echo "Installation in progress..."
echo "To see installation details, open a new terminal and run the command 'tail -f $log_file'"

# from here, send script output to log file
start_redir_stdxxx
start_spinner

# check
if [[ "$g__version" == *-* ]]; then
    err "INSTALL-ERR119" "Incorrect version number"
fi

# check
# (having more than one package specified with '-e' option is a bit tricky to handle, so this check prevent it for now)
if [ -n "$g__archive" ]; then
    # archive has been specified

    if [ $# -gt 1 ]; then
        # means more than one module are to be installed

        err "INSTALL-ERR118" "'-e' option cannot be used for more than one module"
    fi
fi

# check
# (having more than one package specified with '-d' option is a bit tricky to handle, so this check prevent it for now)
if [ -n "$g__version" ]; then
    # version has been specified

    if [ $# -gt 1 ]; then
        # means more than one module has been asked to be installed

        err "INSTALL-ERR218" "'-d' option cannot be used for more than one module"
    fi
fi

# init.
export LC_ALL=C
export LANG=C
#
# variables used to check for configuration files modification
g__after_md5_conffile=
g__before_md5_conffile=
#
post_install_msg= # used to display some info to the user after installation
tmpdir=$( mktemp -d -p /tmp tmp.sdt.XXXXXXXXXX ) # use mktemp instead of hardcoded path in case different user install synda from source on a multi-user machine
#
st_url_prefix=http://sd-104052.dedibox.fr/synda/sdt/src
st_version=${g__version:-3.8} # default version if not specified by the user
st_package=sdt-${st_version}
st_archive=${st_package}.tar.gz
st_url="$st_url_prefix/${st_archive}"
st_root="$g__prefix/sdt"
st_lib="$st_root/lib/sd"
st_conf_file="$st_root/conf/sdt.conf"
st_cred_file="$st_root/conf/credentials.conf"
#
sp_url_prefix=http://sd-104052.dedibox.fr/synda/sdp/src
sp_version=${g__version:-1.3} # set HEAD version unless vernum is specified by the user
sp_package=sdp-${sp_version}
pp_archive=${sp_package}.tar.gz
pp_url="$sp_url_prefix/${pp_archive}"
sp_root="$g__prefix/sdp"
pp_lib="$sp_root/lib/sp"
pp_conf_file="$sp_root/conf/sdp.conf"
pp_cred_file="$sp_root/conf/credentials.conf"
#
python_pkg_install_cmd="pip install" # "pip install" or easy_install
WGET_CMD="wget --no-check-certificate"
#
virtual_env_package_name="virtualenv-14.0.6"
virtual_env_archive_name=${virtual_env_package_name}.tar.gz
virtual_env_url="https://pypi.python.org/packages/source/v/virtualenv/${virtual_env_archive_name}#md5=1a475df2219457b6b4febb9fe595d915"
#
python_package_name=Python-2.6.6
python_archive_name=Python-2.6.6.tgz
python_url=http://www.python.org/ftp/python/2.6.6/Python-2.6.6.tgz
python_dir=$HOME/python2.6

# additional check
if [ $g__transfer -eq 1 ]; then

    # check transfer minimal version supported by this installer
    # (this is because the installer depends of the environment and the environment changed in 3.0 (sdt.conf file moved to conf folder))
    firstchar="$(echo $st_version | head -c 1)"
    if [ "$firstchar" -lt "3" ]; then
        err "INSTALL-ERR100" "This installer can only be used to install synda-transfer 3.0+ version."
    fi

fi

# clean temp files

mkdir -p $tmpdir
rm -rf $tmpdir/sdt-*
rm -rf $tmpdir/sdp-*

check_dependencies

# alias 'python' to the Python 2 highest version
set_default_python_version python2.6
set_default_python_version python2.7

# main

if [ $g__upgrade -eq 0 ]; then
    # install

    install_python_if_needed

    if [ $g__transfer -eq 1 ]; then
        st_is_running
        install_transfer_module

        # Retrieve parameters from ESGF
        export ST_HOME=$g__prefix/sdt
        if ! $st_root/bin/synda update 2>/dev/null; then # this 'if' block is used as an an alternative to "set +o errexit" to prevent fatal error
            echo "Warning: cannot retrieve parameters from ESGF"
        fi
    fi

    if [ $g__postprocessing -eq 1 ]; then
        sp_is_running
        install_postprocessing_module
    fi

    if [ $g__globustransfer -eq 1 ]; then
        st_is_running
        install_globustransfer_module
    fi
else
    # upgrade

    if [ $g__transfer -eq 1 ]; then
        st_is_running
        update_transfer_module
    fi

    if [ $g__postprocessing -eq 1 ]; then
        sp_is_running
        update_postprocessing_module
    fi
fi

stop_spinner
stop_redir_stdxxx

# display some info about what has been done
echo "Installation complete."
echo -e "$post_install_msg" # "-e" option interpret char like '\n'
echo ""

exit 0
