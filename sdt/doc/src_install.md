# Synda installation from source

## Synopsis

This documents contains instructions to install Synda from source.

## Requirements

Linux distribution with Python 2.6+.

## Installation

As root, install the following system packages:

RHEL and derivative (Centos, Scientific Linux, Fedora..)

```
yum install gcc python python-pip python-devel openssl-devel sqlite sqlite-devel libxslt-devel libxml2-devel zlib-devel libffi-devel
```

Debian and derivative (Ubuntu, Mint, LXLE..)

```
apt-get install gcc python python-pip python-dev libssl-dev sqlite3 libsqlite-dev libxslt-dev libxml2-dev libz-dev libffi-dev
```

Then install the application (as simple user or root):

```
wget --no-check-certificate https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh
chmod +x ./install.sh
./install.sh
```

## Configuration

Add lines below in your shell configuration file (e.g. '.bashrc')

```
export ST_HOME=$HOME/sdt
export PATH=$ST_HOME/bin:$PATH
```

Then edit credentials file to set openid and password (ESGF credential).

```
vi $ST_HOME/conf/credentials.conf
```

Note: to download file from ESGF, you need to create an openID account on one
ESGF identity provider website (e.g. PCMDI, BADC or DKRZ) and subscribe to
CMIP5-RESEARCH role.

## Files location

* $HOME/sdt/doc
* $HOME/sdt/bin
* $HOME/sdt/conf
* $HOME/sdt/data
* $HOME/sdt/db
* $HOME/sdt/log
* $HOME/sdt/tmp
* $HOME/.esg/certificates

## Note

Installation mode is single-user when installing Synda from source (for
multi-user installation, see 'installation from RPM package' method)
