#!/bin/bash
#
# Description
#  This script install 'globustransfer' module over a system package based Synda
#  installation (.rpm or .deb).
#
# Requirement
#  Synda 3.3+ must be installed from system package (rpm or deb) before running
#  this script.
#
# Usage
#  Run this script as root to install 'globustransfer' module.
#
# Status
#  Developement
#
# Note
#  This script is a slave copy of part of 'install.sh' script.
#  If any modification must be made to this code, edit the
#  master copy first (i.e. 'install.sh'), then sync the slave.


# func

set_default_python_version ()
{
    # This func set PYTHON_CMD variable to given python version if found.

    local python_version=$1

    if which $python_version >/dev/null 2>&1; then
        # we come here if <python_version> is found

        PYTHON_CMD=$python_version
    fi
}


# init

# alias 'python' to the Python 2 highest version
set_default_python_version python2.6
set_default_python_version python2.7

client_dir=/usr/share/python/synda/sdt/lib/$PYTHON_CMD/site-packages/globusonline/transfer/api_client/x509_proxy/

# use ve-python
source /usr/share/python/synda/sdt/bin/activate


# main

# install go transfer API
pip instal globusonline-transfer-api-client

# install mkproxy
mkdir /var/tmp/synda/sdt/mkproxy
pushd /var/tmp/synda/sdt/mkproxy
wget https://raw.githubusercontent.com/globusonline/transfer-api-client-python/master/mkproxy/mkproxy.c
wget https://raw.githubusercontent.com/globusonline/transfer-api-client-python/master/mkproxy/Makefile
make
cp mkproxy $client_dir
popd

# install python-nexus-client
easy_install https://github.com/globusonline/python-nexus-client/archive/integration.zip
